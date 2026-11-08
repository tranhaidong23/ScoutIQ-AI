"""Position-specific cosine retrieval over a fixed historical player catalogue.

No skill labels, market-value ranking, future prediction or invented statistics.
Preprocessing is fitted once on explicit reference IDs, never on search results.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from numbers import Integral, Real
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.features.build_features import CUTOFF, validate_candidates, validate_features

ROOT = Path(__file__).resolve().parents[2]
FEATURE_FILE = ROOT / "data/processed/scoutiq_features_2025_26.csv"


@dataclass(frozen=True)
class FeaturePolicy:
    numeric: tuple[str, ...]
    categorical: tuple[str, ...]
    scope: str
    limitation: str


POLICIES = {
    "Attack": FeaturePolicy(
        ("goals_per90", "assists_per90"), ("sub_position",), "attacking_output_and_role",
        "Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu."),
    "Midfield": FeaturePolicy(
        ("goals_per90", "assists_per90"), ("sub_position",), "attacking_output_and_role",
        "Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự."),
    "Defender": FeaturePolicy(
        ("age", "minutes_played"), ("sub_position", "foot"), "context_profile_only",
        "Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự."),
    "Goalkeeper": FeaturePolicy(
        ("age", "minutes_played"), ("foot",), "context_profile_only",
        "Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng."),
}


def _finite_number(value, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, Real) or not np.isfinite(value):
        raise ValueError(f"{label} must be a finite number")


@dataclass(frozen=True)
class SearchFilters:
    position: str
    min_age: float = 0
    max_age: float = 100
    max_budget_eur: float | None = None
    min_minutes: float = 900

    def __post_init__(self):
        if self.position not in POLICIES:
            raise ValueError("Unknown position")
        for name in ("min_age", "max_age", "min_minutes"):
            _finite_number(getattr(self, name), name)
        if not 0 <= self.min_age <= self.max_age <= 100 or self.min_minutes < 0:
            raise ValueError("Invalid age range or minimum minutes")
        if self.max_budget_eur is not None:
            _finite_number(self.max_budget_eur, "max_budget_eur")
            if self.max_budget_eur < 0:
                raise ValueError("Budget must be nonnegative EUR")


def _category_values(series: pd.Series) -> pd.Series:
    # Empty/missing is not a fabricated foot/role or a shared similarity feature.
    return series.astype("string").fillna("").str.strip()


def _unit_vectors(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norms = np.linalg.norm(matrix, axis=1)
    nonzero = norms > 1e-12
    unit = np.zeros_like(matrix, dtype=float)
    np.divide(matrix, norms[:, None], out=unit, where=nonzero[:, None])
    return unit, nonzero


def _plain(value):
    if pd.isna(value):
        return None
    return value.item() if isinstance(value, np.generic) else value


class CosineRecommender:
    """Retrieve similar players by ID within the same broad position.

    Attack/Midfield: limited attacking output. Defender/GK: context profiles only.
    Default fit scope is a descriptive catalogue snapshot, not an evaluation split.
    Pass fit_player_ids to keep held-out players out of scaler/category fitting.
    """

    def __init__(self, catalogue: pd.DataFrame, *, fit_player_ids=None):
        validate_candidates(catalogue)
        required = {"sub_position", "foot", "current_club_name", "club_name_verified"}
        if not required.issubset(catalogue):
            raise ValueError(f"Missing metadata columns: {sorted(required - set(catalogue))}")
        self._catalogue = catalogue.sort_values("player_id").reset_index(drop=True).copy(deep=True)
        known_ids = set(self._catalogue.player_id)
        ids = list(known_ids) if fit_player_ids is None else list(fit_player_ids)
        if (not ids or any(isinstance(i, bool) or not isinstance(i, Integral) for i in ids)
                or len(ids) != len(set(ids)) or not set(ids).issubset(known_ids)):
            raise ValueError("Fit IDs must be nonempty, unique, known integer player IDs")
        self._fit_ids = frozenset(int(i) for i in ids)
        self._fit_mode = "catalogue_snapshot" if fit_player_ids is None else "explicit_reference_ids"
        self._models = {}
        for position, group in self._catalogue.groupby("position", sort=True):
            policy = POLICIES[position]
            group = group.reset_index(drop=True)
            reference = group.loc[group.player_id.isin(self._fit_ids)]
            if reference.empty:
                raise ValueError(f"No fitting reference for position {position}")
            scaler = StandardScaler().fit(reference[list(policy.numeric)].to_numpy(dtype=float))
            categories = {
                col: tuple(sorted(set(_category_values(reference[col])) - {""}))
                for col in policy.categorical
            }
            numeric = scaler.transform(group[list(policy.numeric)].to_numpy(dtype=float))
            names = list(policy.numeric)
            blocks = [numeric]
            for col, values in categories.items():
                observed = _category_values(group[col])
                for value in values:
                    blocks.append(observed.eq(value).to_numpy(dtype=float).reshape(-1, 1))
                    names.append(f"{col}={value}")
            matrix = np.column_stack(blocks)
            if not np.isfinite(matrix).all():
                raise ValueError("Nonfinite model vector")
            unit, nonzero = _unit_vectors(matrix)
            self._models[position] = {
                "data": group, "scaler": scaler, "categories": categories,
                "feature_names": names, "matrix": matrix, "unit": unit, "nonzero": nonzero,
                "fit_ids": tuple(int(i) for i in reference.player_id),
            }

    @classmethod
    def from_csv(cls, path: Path = FEATURE_FILE, *, fit_player_ids=None):
        data = pd.read_csv(path)
        # Validate the complete Day 4 artefact, including stored percentiles.
        # Percentiles are NOT selected by this recommender.
        validate_features(data)
        return cls(data, fit_player_ids=fit_player_ids)

    def describe(self) -> dict:
        audit = {"cutoff": str(CUTOFF.date()), "fit_mode": self._fit_mode, "positions": {}}
        for position, model in self._models.items():
            policy = POLICIES[position]
            audit["positions"][position] = {
                "numeric": list(policy.numeric), "categorical": list(policy.categorical),
                "scope": policy.scope, "limitation": policy.limitation,
                "encoded_features": list(model["feature_names"]),
                "fit_count": len(model["fit_ids"]),
                "fit_ids_sha256": hashlib.sha256(
                    ",".join(map(str, model["fit_ids"])).encode()).hexdigest(),
                "scaler_mean": model["scaler"].mean_.tolist(),
                "scaler_scale": model["scaler"].scale_.tolist(),
                "categories": {col: list(values) for col, values in model["categories"].items()},
                "zero_vector_count": int((~model["nonzero"]).sum()),
                "missing_or_unseen_categories": {
                    col: int((~_category_values(model["data"][col]).isin(values)).sum())
                    for col, values in model["categories"].items()
                },
            }
        return audit

    def recommend(self, reference_player_id: int, filters: SearchFilters, *, top_k: int = 5) -> dict:
        if isinstance(top_k, bool) or not isinstance(top_k, Integral) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")
        if isinstance(reference_player_id, bool) or not isinstance(reference_player_id, Integral):
            raise ValueError("Reference player ID must be an integer")
        reference = self._catalogue.loc[self._catalogue.player_id == reference_player_id]
        if reference.empty:
            raise ValueError("Unknown reference player ID")
        query = reference.iloc[0]
        if query.position != filters.position:
            raise ValueError("Reference and filter position must match; cross-position scores are not comparable")
        policy = POLICIES[filters.position]
        model = self._models[filters.position]
        data = model["data"]
        query_index = int(np.flatnonzero(data.player_id.to_numpy() == reference_player_id)[0])
        eligible = (
            data.age.between(filters.min_age, filters.max_age)
            & data.minutes_played.ge(filters.min_minutes)
            & data.player_id.ne(reference_player_id)
        )
        if filters.max_budget_eur is not None:
            eligible &= data.market_value_in_eur.le(filters.max_budget_eur)
        warnings = [policy.limitation,
                    "Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.",
                    "Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff."]
        if filters.min_minutes < 900:
            warnings.append("Catalogue đã lọc >=900 phút; giảm bộ lọc không khôi phục cầu thủ ngoài catalogue.")
        for col, vocabulary in model["categories"].items():
            if _category_values(pd.Series([query[col]])).iloc[0] not in vocabulary:
                warnings.append(f"Tham chiếu thiếu/chưa có {col} trong tập fit; mã hóa bằng block 0, không suy đoán.")
        response = {
            "reference": {col: _plain(query[col]) for col in ("player_id", "name", "position")},
            "filters": {"position": filters.position, "min_age": float(filters.min_age),
                        "max_age": float(filters.max_age), "max_budget_eur": (
                            None if filters.max_budget_eur is None else float(filters.max_budget_eur)),
                        "min_minutes": float(filters.min_minutes)},
            "top_k_requested": int(top_k), "eligible_count": int(eligible.sum()),
            "excluded_zero_vectors": int((eligible & ~model["nonzero"]).sum()),
            "cutoff": str(CUTOFF.date()), "similarity_scope": policy.scope,
            "warnings": warnings, "results": [], "status": "ok",
        }
        if not model["nonzero"][query_index]:
            response["status"] = "zero_reference_vector"
            warnings.append("Không tính cosine cho vector tham chiếu bằng 0; không trả thứ hạng tùy ý.")
            return response
        indices = np.flatnonzero(eligible.to_numpy() & model["nonzero"])
        if not len(indices):
            response["status"] = "no_candidates"
            return response
        scores = model["unit"][indices] @ model["unit"][query_index]
        ranked = pd.DataFrame({"row_index": indices, "player_id": data.iloc[indices].player_id.to_numpy(),
                               "similarity_score": np.round(np.clip(scores, -1, 1), 12)})
        # Quantize only machine noise; no price/age/playing-time tie breaker.
        ranked = ranked.sort_values(["similarity_score", "player_id"], ascending=[False, True]).head(top_k)
        for rank, row in enumerate(ranked.itertuples(index=False), start=1):
            candidate = data.iloc[int(row.row_index)]
            terms = model["unit"][int(row.row_index)] * model["unit"][query_index]
            evidence = {
                col: {"reference": _plain(query[col]), "candidate": _plain(candidate[col])}
                for col in (*policy.numeric, *policy.categorical)
            }
            components = {name: float(value) for name, value in zip(model["feature_names"], terms)}
            fragments = [f"{col}: {evidence[col]['candidate']} (tham chiếu {evidence[col]['reference']})"
                         for col in (*policy.numeric, *policy.categorical)]
            club = _plain(candidate.club_name_verified) or _plain(candidate.current_club_name)
            result = {col: _plain(candidate[col]) for col in
                      ("player_id", "name", "position", "sub_position", "age", "minutes_played",
                       "market_value_in_eur", "valuation_date")}
            result.update({"rank": rank, "club": club, "similarity_score": float(row.similarity_score),
                           "similarity_scope": policy.scope, "evidence": evidence,
                           "cosine_components": components,
                           "explanation": "; ".join(fragments) + ". " + policy.limitation})
            response["results"].append(result)
        if len(response["results"]) < top_k:
            warnings.append("Không đủ ứng viên hợp lệ để trả đủ K; không tự nới điều kiện.")
        return response
