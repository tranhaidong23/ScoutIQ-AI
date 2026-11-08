"""Day 9: descriptive, unit-explicit comparisons; no overall winner or scoring."""

from numbers import Integral, Real
import json

import numpy as np
import pandas as pd

from src.features.build_features import CUTOFF, validate_candidates
from src.recommendation.baseline import POLICIES, _plain

UNITS = {"age": "years", "minutes_played": "minutes", "market_value_in_eur": "EUR",
         "goals_per90": "goals/90 minutes", "assists_per90": "assists/90 minutes",
         "sub_position": "category", "position": "category", "foot": "category"}
CONTEXT_METRICS = ("age", "minutes_played", "market_value_in_eur")
ATTACK_METRICS = ("goals_per90", "assists_per90")
LIMITS = ["Market value là ước tính tại snapshot, không phải phí chuyển nhượng hoặc kỹ năng.",
          "Phút/tuổi là bối cảnh; per90 chưa điều chỉnh giải đấu, chiến thuật hoặc bất định mẫu.",
          "Metadata CLB chưa được xác minh đúng tại cutoff; missing không được suy đoán.",
          "Không có kết luận cầu thủ tốt hơn tổng thể hoặc xác suất chuyển nhượng."]


def numeric_difference(candidate, reference):
    """Signed/absolute difference and relative percent, with explicit null reason."""
    for value in (candidate, reference):
        if value is not None and (isinstance(value, (bool, np.bool_)) or
                                  not isinstance(value, Real) or not np.isfinite(value)):
            raise ValueError("Differences require finite numeric values or explicit None")
    if candidate is None or reference is None:
        return {"signed_difference": None, "absolute_difference": None,
                "relative_difference_pct": None, "relative_reason": "missing_value",
                "direction": "unknown"}
    difference = float(candidate) - float(reference)
    relative = None if reference == 0 else 100 * (difference / abs(float(reference)))
    if not np.isfinite(difference) or (relative is not None and not np.isfinite(relative)):
        raise ValueError("Difference arithmetic overflow")
    return {"signed_difference": difference, "absolute_difference": abs(difference),
            "relative_difference_pct": relative,
            "relative_reason": "zero_reference" if reference == 0 else None,
            "direction": "equal" if difference == 0 else "higher" if difference > 0 else "lower"}


class PlayerComparison:
    def __init__(self, catalogue):
        if not isinstance(catalogue, pd.DataFrame):
            raise ValueError("Catalogue must be a DataFrame")
        validate_candidates(catalogue)
        required = {"sub_position", "foot", "current_club_id", "current_club_name", "club_name_verified"}
        if not required <= set(catalogue):
            raise ValueError("Missing comparison metadata columns")
        if "market_value_m" in catalogue and not np.allclose(
                catalogue.market_value_m, catalogue.market_value_in_eur / 1_000_000,
                rtol=1e-9, atol=1e-12):
            raise ValueError("Inconsistent EUR/million EUR units")
        self._data = catalogue.copy(deep=True).set_index("player_id", drop=False)

    def player(self, player_id):
        if (isinstance(player_id, (bool, np.bool_)) or not isinstance(player_id, Integral)
                or player_id <= 0 or player_id not in self._data.index):
            raise ValueError("Unknown or invalid player ID")
        return self._data.loc[player_id].copy()

    def identity(self, player_id):
        row = self.player(player_id)
        names = ("player_id", "name", "position", "sub_position", "age", "minutes_played",
                 "market_value_in_eur", "valuation_date", "foot", "current_club_id",
                 "current_club_name", "club_name_verified")
        values = {key: _plain(row[key]) for key in names}
        # Empty category strings also denote missing, not a shared category.
        values = {k: None if isinstance(v, str) and not v.strip() else v for k, v in values.items()}
        return {"values": values, "missing_fields": [k for k, v in values.items() if v is None],
                "units": {k: v for k, v in UNITS.items() if k in values}}

    def compare(self, player_ids, *, reference_player_id=None):
        if not isinstance(player_ids, (list, tuple)) or not 2 <= len(player_ids) <= 5:
            raise ValueError("Comparison requires 2-5 distinct player IDs in an ordered list")
        players = [self.player(i) for i in player_ids]
        if len(set(player_ids)) != len(player_ids):
            raise ValueError("Duplicate comparison IDs")
        reference_id = player_ids[0] if reference_player_id is None else reference_player_id
        reference = self.player(reference_id)
        if reference_id not in player_ids:
            raise ValueError("Reference must be one of the 2-5 compared players")
        positions = {p.position for p in players}
        homogeneous_attack = len(positions) == 1 and reference.position in ("Attack", "Midfield")
        metrics = CONTEXT_METRICS + (ATTACK_METRICS if homogeneous_attack else ())
        rows = []
        for player in players:
            for metric in metrics:
                value, baseline = _plain(player[metric]), _plain(reference[metric])
                rows.append({"player_id": int(player.player_id), "reference_player_id": int(reference_id),
                             "metric": metric, "source_column": metric, "unit": UNITS[metric],
                             "value": value, "reference_value": baseline,
                             **numeric_difference(value, baseline)})
        categories = []
        for player in players:
            for metric in ("position", "sub_position", "foot"):
                a, b = self.identity(int(player.player_id))["values"][metric], self.identity(reference_id)["values"][metric]
                categories.append({"player_id": int(player.player_id), "metric": metric,
                                   "value": a, "reference_value": b,
                                   "match": None if a is None or b is None else a == b,
                                   "reason": "missing_value" if a is None or b is None else None})
        result = {"schema_version": "scoutiq.comparison.v1", "cutoff": str(CUTOFF.date()),
                  "season": "2025/26", "reference_player_id": int(reference_id),
                  "players": [self.identity(i) for i in player_ids],
                  "scope": "attacking_output_and_context" if homogeneous_attack else "context_only",
                  "numeric_differences": rows, "categorical_comparisons": categories,
                  "difference_definition": "signed=candidate-reference; absolute=abs(signed); relative_pct=100*signed/abs(reference), null if zero/missing",
                  "limitations": LIMITS + (["Khác vị trí hoặc Defender/GK: chỉ so bối cảnh, không so goals/assists như kỹ năng."]
                                            if not homogeneous_attack else [POLICIES[reference.position].limitation])}
        json.dumps(result, allow_nan=False)
        return result
