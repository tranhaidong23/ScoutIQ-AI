"""Exact cosine-neighbor retrieval on the unchanged Day 5/6 representation.

Filter before retrieval; enumerate all valid neighbors before deterministic
tie-breaking. Fitting NearestNeighbors here stores filtered, already-transformed
vectors. It does NOT fit a scaler or change the reference population.
"""

from copy import deepcopy
from numbers import Integral
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from src.features.build_features import CUTOFF, validate_features
from src.recommendation.baseline import (
    CosineRecommender, FEATURE_FILE, POLICIES, SearchFilters, _category_values, _plain,
)
from src.recommendation.weighted import WeightedCosineRecommender


def cosine_neighbors(matrix, query):
    """Return exact sklearn distances and indices for ALL nonzero candidates."""
    matrix = np.asarray(matrix, dtype=float)
    query = np.asarray(query, dtype=float)
    if (matrix.ndim != 2 or query.ndim != 1 or matrix.shape[1] != len(query)
            or matrix.shape[1] == 0 or not np.isfinite(matrix).all()
            or not np.isfinite(query).all()):
        raise ValueError("Cosine vectors must be finite, dimensionally compatible arrays")
    if np.linalg.norm(query) <= 1e-12 or (
            len(matrix) and (np.linalg.norm(matrix, axis=1) <= 1e-12).any()):
        raise ValueError("Cosine distance is undefined for zero vectors")
    if not len(matrix):
        return np.array([], dtype=float), np.array([], dtype=int)
    neighbors = NearestNeighbors(metric="cosine", algorithm="brute", n_jobs=1)
    neighbors.fit(matrix)
    distances, indices = neighbors.kneighbors(query.reshape(1, -1), n_neighbors=len(matrix))
    distances = distances[0]
    if (not np.isfinite(distances).all() or (distances < -1e-12).any()
            or (distances > 2 + 1e-12).any()):
        raise ValueError("Invalid cosine distance returned by NearestNeighbors")
    return np.clip(distances, 0, 2), indices[0]


class KNNRecommender:
    """None weights reproduces Day 5; explicit weights use Day 6 geometry.

    Response construction mirrors baseline semantics while leaving baseline.py
    and weighted.py untouched. Regression tests protect this adapter boundary.
    """

    def __init__(self, catalogue: pd.DataFrame, *, fit_player_ids=None, weights=None):
        if not isinstance(catalogue, pd.DataFrame):
            raise ValueError("Catalogue must be a pandas DataFrame")
        self._representation = (
            CosineRecommender(catalogue, fit_player_ids=fit_player_ids) if weights is None
            else WeightedCosineRecommender(catalogue, fit_player_ids=fit_player_ids, weights=weights))
        self._weights = None if weights is None else self._representation.describe()["weights"]

    @classmethod
    def from_csv(cls, path: Path = FEATURE_FILE, *, fit_player_ids=None, weights=None):
        data = pd.read_csv(path)
        validate_features(data)
        return cls(data, fit_player_ids=fit_player_ids, weights=weights)

    def describe(self):
        return {
            "retrieval": "sklearn.NearestNeighbors", "metric": "cosine",
            "algorithm": "brute", "n_jobs": 1,
            "index_scope": "filtered_nonzero_candidates_per_request",
            "tie_break": "round(1-distance,12) descending, player_id ascending; all candidates before K",
            "representation": self._representation.describe(),
        }

    def recommend(self, reference_player_id, filters: SearchFilters, *, top_k=5):
        if not isinstance(filters, SearchFilters):
            raise ValueError("filters must be SearchFilters")
        if isinstance(top_k, bool) or not isinstance(top_k, Integral) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")
        if isinstance(reference_player_id, bool) or not isinstance(reference_player_id, Integral):
            raise ValueError("Reference player ID must be an integer")
        reference = self._representation._catalogue.loc[
            self._representation._catalogue.player_id == reference_player_id]
        if reference.empty:
            raise ValueError("Unknown reference player ID")
        query = reference.iloc[0]
        if query.position != filters.position:
            raise ValueError("Reference and filter position must match")
        policy = POLICIES[filters.position]
        model = self._representation._models[filters.position]
        data = model["data"]
        query_index = int(np.flatnonzero(data.player_id.to_numpy() == reference_player_id)[0])
        eligible = (data.age.between(filters.min_age, filters.max_age)
                    & data.minutes_played.ge(filters.min_minutes)
                    & data.player_id.ne(reference_player_id))
        if filters.max_budget_eur is not None:
            eligible &= data.market_value_in_eur.le(filters.max_budget_eur)
        warnings = [
            policy.limitation,
            "Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.",
            "Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff.",
            "KNN cosine là phương án truy xuất; không mặc định tốt hơn hoặc đo chất lượng tuyển trạch.",
        ]
        if filters.min_minutes < 900:
            warnings.append("Catalogue đã lọc >=900 phút; giảm bộ lọc không khôi phục cầu thủ ngoài catalogue.")
        for col, vocabulary in model["categories"].items():
            if _category_values(pd.Series([query[col]])).iloc[0] not in vocabulary:
                warnings.append(f"Tham chiếu thiếu/chưa có {col} trong tập fit; mã hóa bằng block 0, không suy đoán.")
        weights = None if self._weights is None else self._weights[filters.position]
        if weights is not None:
            warnings.append("Trọng số là giả thuyết thử nghiệm, chưa tối ưu bằng relevance labels.")
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
            "algorithm": "sklearn_nearest_neighbors_cosine",
            "weights": deepcopy(weights),
        }
        if not model["nonzero"][query_index]:
            response["status"] = "zero_reference_vector"
            warnings.append("Không tính cosine cho vector tham chiếu bằng 0; không trả thứ hạng tùy ý.")
            return response
        indices = np.flatnonzero(eligible.to_numpy() & model["nonzero"])
        if not len(indices):
            response["status"] = "no_candidates"
            return response
        distances, neighbors = cosine_neighbors(model["unit"][indices], model["unit"][query_index])
        selected = indices[neighbors]
        ranked = pd.DataFrame({
            "row_index": selected, "player_id": data.iloc[selected].player_id.to_numpy(),
            "cosine_distance": distances, "similarity_score": np.round(1 - distances, 12),
        })
        # Ask sklearn for all neighbors, so ties at K are not truncated arbitrarily.
        ranked = ranked.sort_values(["similarity_score", "player_id"], ascending=[False, True]).head(top_k)
        for rank, row in enumerate(ranked.itertuples(index=False), 1):
            candidate = data.iloc[int(row.row_index)]
            terms = model["unit"][int(row.row_index)] * model["unit"][query_index]
            active = [col for col in (*policy.numeric, *policy.categorical)
                      if weights is None or weights[col] > 0]
            evidence = {col: {"reference": _plain(query[col]), "candidate": _plain(candidate[col])}
                        for col in active}
            fragments = [
                f"{col}: {evidence[col]['candidate']} (tham chiếu {evidence[col]['reference']}"
                + ("" if weights is None else f"; w={weights[col]:g}") + ")"
                for col in active
            ]
            result = {col: _plain(candidate[col]) for col in (
                "player_id", "name", "position", "sub_position", "age", "minutes_played",
                "market_value_in_eur", "valuation_date")}
            result.update({
                "rank": rank, "club": _plain(candidate.club_name_verified) or _plain(candidate.current_club_name),
                "similarity_score": float(row.similarity_score),
                "cosine_distance": float(row.cosine_distance), "similarity_scope": policy.scope,
                "evidence": evidence,
                "cosine_components": {name: float(value) for name, value in zip(model["feature_names"], terms)},
                "explanation": "; ".join(fragments) + ". " + policy.limitation,
            })
            response["results"].append(result)
        if len(response["results"]) < top_k:
            warnings.append("Không đủ ứng viên hợp lệ để trả đủ K; không tự nới điều kiện.")
        return response

