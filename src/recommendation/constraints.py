"""Day 8: explicit hard constraints over frozen Day 5-7 representations.

The old engines/API are unchanged. SearchConstraints deliberately is NOT a
SearchFilters subtype: use AdvancedRecommender so new constraints cannot be
silently ignored by an older engine. No fitting occurs during a search.
"""

from collections.abc import Mapping
from copy import copy, deepcopy
from dataclasses import asdict, dataclass, fields
from numbers import Integral

import numpy as np
import pandas as pd

from src.recommendation.baseline import CosineRecommender, SearchFilters, _finite_number, _plain
from src.recommendation.knn import KNNRecommender


@dataclass(frozen=True)
class SearchConstraints:
    filters: SearchFilters
    sub_positions: tuple[str, ...] = ()
    min_goals_per90: float | None = None
    min_assists_per90: float | None = None
    preferred_foot: str | None = None
    foot_mode: str = "hard"
    excluded_club_ids: tuple[int, ...] = ()

    def __post_init__(self):
        if type(self.filters) is not SearchFilters:
            raise ValueError("filters must be a Day 5 SearchFilters object")
        # Revalidate even if a caller has constructed an invalid frozen object.
        SearchFilters(**asdict(self.filters))
        for name in ("min_goals_per90", "min_assists_per90"):
            value = getattr(self, name)
            if value is not None:
                _finite_number(value, name)
                if value < 0:
                    raise ValueError(f"{name} must be nonnegative per 90 minutes")
        if self.filters.position == "Goalkeeper" and (
                self.min_goals_per90 is not None or self.min_assists_per90 is not None):
            raise ValueError("Goalkeeper search does not use goals/assists thresholds")
        if self.preferred_foot is not None and (
                not isinstance(self.preferred_foot, str) or
                self.preferred_foot not in ("left", "right", "both")):
            raise ValueError("preferred_foot must be left, right, both or None (exact match)")
        if self.foot_mode not in ("hard", "soft"):
            raise ValueError("foot_mode must be hard or soft")
        if self.foot_mode == "soft" and self.preferred_foot is None:
            raise ValueError("soft foot mode requires preferred_foot")
        for name in ("sub_positions", "excluded_club_ids"):
            value = getattr(self, name)
            if not isinstance(value, (tuple, list)):
                raise ValueError(f"{name} must be a list or tuple, not a string/set")
            if name == "sub_positions":
                valid = all(isinstance(x, str) and x.strip() == x and bool(x) for x in value)
            else:
                valid = all(not isinstance(x, (bool, np.bool_)) and
                            isinstance(x, Integral) and x > 0 for x in value)
            if not valid or len(set(value)) != len(value):
                raise ValueError(f"{name} has invalid or duplicate entries")
            object.__setattr__(self, name, tuple(sorted(value)))

    @classmethod
    def from_request(cls, request):
        """Strict flat request; budget is EUR or explicitly converted EUR_million.

        Accept max_budget_eur OR the pair budget_value/budget_unit, never both.
        Bare max_budget_eur=5 means five EUR: magnitude cannot reveal intent.
        """
        if not isinstance(request, Mapping):
            raise ValueError("Request must be a mapping")
        basic = {f.name for f in fields(SearchFilters)}
        extra = {f.name for f in fields(cls)} - {"filters"}
        if set(request) - basic - extra - {"budget_value", "budget_unit"}:
            raise ValueError("Unknown constraint fields")
        values = dict(request)
        if "budget_value" in values or "budget_unit" in values:
            if not {"budget_value", "budget_unit"} <= values.keys() or "max_budget_eur" in values:
                raise ValueError("Supply one budget representation with explicit unit")
            budget, unit = values.pop("budget_value"), values.pop("budget_unit")
            _finite_number(budget, "budget_value")
            if unit not in ("EUR", "EUR_million") or budget < 0:
                raise ValueError("Budget unit must be EUR or EUR_million; value >= 0")
            amount = float(budget) * (1_000_000 if unit == "EUR_million" else 1)
            _finite_number(amount, "converted EUR budget")
            values["max_budget_eur"] = amount
        try:
            base = SearchFilters(**{k: v for k, v in values.items() if k in basic})
            return cls(base, **{k: v for k, v in values.items() if k in extra})
        except (TypeError, KeyError) as exc:
            raise ValueError("Invalid or missing search constraint") from exc

    def describe(self):
        base = {k: (v if k == "position" or v is None else float(v))
                for k, v in asdict(self.filters).items()}
        extra = {"sub_positions": list(self.sub_positions),
                 "min_goals_per90": None if self.min_goals_per90 is None else float(self.min_goals_per90),
                 "min_assists_per90": None if self.min_assists_per90 is None else float(self.min_assists_per90),
                 "preferred_foot": self.preferred_foot, "foot_mode": self.foot_mode,
                 "excluded_club_ids": [int(x) for x in self.excluded_club_ids]}
        return {**base, **extra,
                "budget_unit": "EUR", "boundaries": "inclusive",
                "soft_preference_policy": "equal rounded cosine score only, then player_id",
                "missing_policy": "active hard constraint: unknown fails; soft foot: no bonus"}


def filter_candidates(catalogue, query_id, constraints):
    """Return a Boolean mask and ordered, disjoint-removal audit (no ranking).

    Numbers in each stage depend on the documented order, not causal importance.
    Club exclusion uses current_club_id; unknown club fails a requested exclusion.
    """
    if not isinstance(constraints, SearchConstraints):
        raise ValueError("constraints must be SearchConstraints")
    f = constraints.filters
    required = {"player_id", "position", "age", "minutes_played", "market_value_in_eur"}
    required |= ({"sub_position"} if constraints.sub_positions else set())
    required |= ({"foot"} if constraints.preferred_foot else set())
    required |= ({"current_club_id"} if constraints.excluded_club_ids else set())
    required |= {col for col, value in (("goals_per90", constraints.min_goals_per90),
                                      ("assists_per90", constraints.min_assists_per90)) if value is not None}
    if not isinstance(catalogue, pd.DataFrame) or not required <= set(catalogue.columns):
        raise ValueError("Catalogue lacks columns required by active constraints")
    if isinstance(query_id, (bool, np.bool_)) or not isinstance(query_id, Integral) or query_id <= 0:
        raise ValueError("Query ID must be a positive integer")
    query = catalogue.loc[catalogue.player_id.eq(query_id)]
    if len(query) != 1 or query.iloc[0].position != f.position:
        raise ValueError("Query ID must be unique, present and match position")
    if constraints.sub_positions:
        known = set(catalogue.loc[catalogue.position.eq(f.position), "sub_position"].dropna())
        if not set(constraints.sub_positions) <= known:
            raise ValueError("Unknown sub_position or sub_position incompatible with position")
    if constraints.excluded_club_ids:
        known = set(catalogue.current_club_id.dropna())
        if not set(constraints.excluded_club_ids) <= known:
            raise ValueError("Unknown excluded club ID in this snapshot")
    mask = pd.Series(True, index=catalogue.index)
    audit = []

    def apply(name, condition):
        nonlocal mask
        before = int(mask.sum())
        mask &= condition.fillna(False)
        after = int(mask.sum())
        audit.append({"constraint": name, "before": before, "after": after, "removed": before - after})

    def finite(col):
        numeric = pd.to_numeric(catalogue[col], errors="coerce")
        return numeric, numeric.notna() & np.isfinite(numeric)

    apply("position", catalogue.position.eq(f.position))
    apply("exclude_query", catalogue.player_id.ne(query_id))
    age, valid = finite("age")
    apply("age_range", valid & age.between(f.min_age, f.max_age))
    if f.max_budget_eur is not None:
        value, valid = finite("market_value_in_eur")
        apply("max_budget_eur", valid & value.ge(0) & value.le(f.max_budget_eur))
    minutes, valid = finite("minutes_played")
    apply("min_minutes", valid & minutes.ge(f.min_minutes))
    if constraints.sub_positions:
        apply("sub_positions", catalogue.sub_position.isin(constraints.sub_positions))
    for col, minimum in (("goals_per90", constraints.min_goals_per90),
                         ("assists_per90", constraints.min_assists_per90)):
        if minimum is not None:
            value, valid = finite(col)
            apply("min_" + col, valid & value.ge(minimum))
    if constraints.preferred_foot and constraints.foot_mode == "hard":
        apply("preferred_foot", catalogue.foot.eq(constraints.preferred_foot))
    if constraints.excluded_club_ids:
        clubs, valid = finite("current_club_id")
        apply("excluded_club_ids", valid & clubs.gt(0) & clubs.mod(1).eq(0) &
              ~clubs.isin(constraints.excluded_club_ids))
    return mask, audit


class AdvancedRecommender:
    """Request-local filtered view; no mutation or refit of wrapped engine.

    Private Day 5-7 representation access is isolated here and guarded by
    regression, score, pool-before-ranking and immutability tests.
    """

    def __init__(self, engine):
        if not isinstance(engine, (CosineRecommender, KNNRecommender)):
            raise ValueError("Use a fitted cosine, weighted cosine or KNN engine")
        self._engine = engine

    def describe(self):
        return {"search": "advanced_constraints_v1", "engine": deepcopy(self._engine.describe())}

    def recommend(self, reference_player_id, constraints, *, top_k=5):
        if not isinstance(constraints, SearchConstraints):
            raise ValueError("Use SearchConstraints; legacy requests go to the original engine")
        for value, name in ((reference_player_id, "query ID"), (top_k, "top_k")):
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        representation = (self._engine._representation if isinstance(self._engine, KNNRecommender)
                          else self._engine)
        catalogue = representation._catalogue
        query = catalogue.loc[catalogue.player_id.eq(reference_player_id)]
        if query.empty or query.iloc[0].position != constraints.filters.position:
            raise ValueError("Query ID must exist and match search position")
        mask, stages = filter_candidates(catalogue, reference_player_id, constraints)
        ids = set(catalogue.loc[mask, "player_id"])
        position = constraints.filters.position
        model = representation._models[position]
        # Keep query for its encoded vector even when it fails candidate constraints.
        selected = model["data"].player_id.isin(ids | {reference_player_id}).to_numpy()
        view = copy(representation)
        view._models = dict(representation._models)
        subset = dict(model)
        subset["data"] = model["data"].loc[selected].reset_index(drop=True)
        for key in ("matrix", "unit", "nonzero", "weighted_matrix"):
            if key in model:
                subset[key] = model[key][selected].copy()
        view._models[position] = subset
        if isinstance(self._engine, KNNRecommender):
            engine = copy(self._engine)
            engine._representation = view
        else:
            engine = view
        # Full eligible ranking supports a soft tie preference across the K boundary.
        rankable_count = int((subset["nonzero"] &
                              subset["data"].player_id.ne(reference_player_id).to_numpy()).sum())
        response = engine.recommend(reference_player_id, constraints.filters, top_k=max(1, rankable_count))
        lookup = catalogue.set_index("player_id")
        soft = constraints.foot_mode == "soft"
        for row in response["results"]:
            data = lookup.loc[row["player_id"]]
            evidence = {key: _plain(data[key]) for key in (
                "sub_position", "age", "market_value_in_eur", "minutes_played",
                "goals_per90", "assists_per90", "foot", "current_club_id")}
            row["constraint_evidence"] = evidence
            row["soft_preference_match"] = bool(
                soft and pd.notna(data.foot) and data.foot == constraints.preferred_foot)
            row["explanation"] += (
                f" Ràng buộc: tuổi={evidence['age']}; market value EUR={evidence['market_value_in_eur']};"
                f" phút={evidence['minutes_played']}; vai trò={evidence['sub_position']};"
                f" chân={evidence['foot']}; club_id={evidence['current_club_id']}.")
            if constraints.min_goals_per90 is not None or constraints.min_assists_per90 is not None:
                row["explanation"] += (f" Hiệu suất tấn công: goals/90={evidence['goals_per90']};"
                                       f" assists/90={evidence['assists_per90']}.")
        response["results"].sort(key=lambda r: (-r["similarity_score"],
                                               -int(r["soft_preference_match"]), r["player_id"]))
        response["results"] = response["results"][:top_k]
        for rank, row in enumerate(response["results"], 1):
            row["rank"] = rank
        response["top_k_requested"] = int(top_k)
        response["search_constraints"] = constraints.describe()
        response["filter_audit"] = {"catalogue_before": len(catalogue),
                                    "after_hard_constraints": len(ids), "stages": stages}
        response["warnings"].append(
            "Hard constraints áp dụng trước ranking; dữ liệu thiếu không thỏa điều kiện cứng; "
            "club exclusions dùng metadata CLB chưa kiểm chứng tại cutoff.")
        if soft:
            response["warnings"].append(
                "Ưu tiên chân thuận chỉ phá hòa khi cosine làm tròn 12 chữ số bằng nhau, "
                "sau đó player_id; không đổi similarity hoặc nới hard constraints.")
        if len(response["results"]) < top_k:
            message = "Không đủ ứng viên hợp lệ để trả đủ K; không tự nới điều kiện."
            if message not in response["warnings"]:
                response["warnings"].append(message)
        return response
