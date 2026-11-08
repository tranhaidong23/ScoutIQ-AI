"""Day 6: diagonal weighted cosine using unchanged Day 5 preprocessing.

Weights belong to semantic numeric features / categorical one-hot blocks.
A categorical block weight applies to each indicator (one active per row);
it is not divided by vocabulary size. No relevance labels are assumed.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from numbers import Real
from pathlib import Path

import numpy as np
import pandas as pd

from src.features.build_features import validate_features
from src.recommendation.baseline import (
    CosineRecommender, FEATURE_FILE, POLICIES, SearchFilters, _unit_vectors,
)


def default_weights() -> dict:
    """Hypotheses, not learned weights or a validated scouting optimum."""
    return {
        "Attack": {"goals_per90": .4, "assists_per90": .4, "sub_position": .2},
        "Midfield": {"goals_per90": .3, "assists_per90": .5, "sub_position": .2},
        "Defender": {"age": .2, "minutes_played": .2, "sub_position": .4, "foot": .2},
        "Goalkeeper": {"age": .25, "minutes_played": .25, "foot": .5},
    }


def unit_weights() -> dict:
    return {position: {name: 1.0 for name in (*policy.numeric, *policy.categorical)}
            for position, policy in POLICIES.items()}


def experiment_weights() -> dict:
    default = default_weights()
    numeric = {
        "Attack": {"goals_per90": .6, "assists_per90": .3, "sub_position": .1},
        "Midfield": {"goals_per90": .2, "assists_per90": .7, "sub_position": .1},
        "Defender": {"age": .4, "minutes_played": .4, "sub_position": .1, "foot": .1},
        "Goalkeeper": {"age": .45, "minutes_played": .45, "foot": .1},
    }
    categorical = {
        "Attack": {"goals_per90": .2, "assists_per90": .2, "sub_position": .6},
        "Midfield": {"goals_per90": .15, "assists_per90": .25, "sub_position": .6},
        "Defender": {"age": .1, "minutes_played": .1, "sub_position": .6, "foot": .2},
        "Goalkeeper": {"age": .1, "minutes_played": .1, "foot": .8},
    }
    no_categories, no_first_numeric = deepcopy(default), deepcopy(default)
    for position, policy in POLICIES.items():
        for name in policy.categorical:
            no_categories[position][name] = 0.0
        # Controlled removal: goals/90 for Attack/Midfield, age for context groups.
        no_first_numeric[position][policy.numeric[0]] = 0.0
    return {
        "weighted_default": default,
        "numeric_emphasis": numeric,
        "categorical_emphasis": categorical,
        "ablate_categories": no_categories,
        "ablate_first_numeric": no_first_numeric,
    }


def validate_weights(weights) -> dict:
    if not isinstance(weights, Mapping) or set(weights) != set(POLICIES):
        raise ValueError("Weights must specify exactly all four positions")
    clean = {}
    for position, policy in POLICIES.items():
        current = weights[position]
        expected = set((*policy.numeric, *policy.categorical))
        if not isinstance(current, Mapping) or set(current) != expected:
            raise ValueError(f"Weights for {position} must specify exactly {sorted(expected)}")
        clean[position] = {}
        for name, weight in current.items():
            if (isinstance(weight, (bool, np.bool_)) or not isinstance(weight, Real)
                    or not np.isfinite(weight) or weight < 0):
                raise ValueError(f"Weight {position}.{name} must be finite and nonnegative")
            clean[position][name] = float(weight)
        maximum = max(clean[position].values())
        if maximum == 0:
            raise ValueError(f"At least one positive weight is required for {position}")
        if any(w > 0 and w / maximum == 0 for w in clean[position].values()):
            raise ValueError(f"Weight dynamic range underflows for {position}")
    return clean


class WeightedCosineRecommender(CosineRecommender):
    """sum(w*x*y) / sqrt(sum(w*x*x)*sum(w*y*y)); zero weights ablate.

    Reuses Day 5's validation, reference-only fit, filters and ranking.
    This subclass intentionally depends on the baseline's internal matrix;
    parity and regression tests guard that boundary.
    """

    def __init__(self, catalogue: pd.DataFrame, *, fit_player_ids=None, weights=None):
        self._weights = validate_weights(default_weights() if weights is None else weights)
        if not isinstance(catalogue, pd.DataFrame):
            raise ValueError("Catalogue must be a pandas DataFrame")
        super().__init__(catalogue, fit_player_ids=fit_player_ids)
        for position, model in self._models.items():
            semantic = self._weights[position]
            encoded = np.array([semantic[name.split("=", 1)[0]]
                                for name in model["feature_names"]], dtype=float)
            # A common positive rescaling cancels in cosine. Avoid huge w*x*x.
            encoded /= max(semantic.values())
            matrix = model["matrix"] * np.sqrt(encoded)
            if not np.isfinite(matrix).all():
                raise ValueError("Nonfinite weighted model vector")
            model["unit"], model["nonzero"] = _unit_vectors(matrix)
            model["effective_weights"] = encoded
            model["weighted_matrix"] = matrix

    @classmethod
    def from_csv(cls, path: Path = FEATURE_FILE, *, fit_player_ids=None, weights=None):
        data = pd.read_csv(path)
        validate_features(data)
        return cls(data, fit_player_ids=fit_player_ids, weights=weights)

    def describe(self) -> dict:
        audit = super().describe()
        audit["algorithm"] = "diagonal_weighted_cosine"
        audit["weights"] = deepcopy(self._weights)
        audit["weight_interpretation"] = (
            "semantic feature/block weights; each one-hot indicator gets its block weight; "
            "sqrt(w/max_w) applied before L2; no per-player reliability multiplier")
        for position, model in self._models.items():
            audit["positions"][position]["effective_encoded_weights"] = dict(
                zip(model["feature_names"], model["effective_weights"].tolist()))
        return audit

    def recommend(self, reference_player_id: int, filters: SearchFilters, *, top_k=5) -> dict:
        if not isinstance(filters, SearchFilters):
            raise ValueError("filters must be SearchFilters")
        result = super().recommend(reference_player_id, filters, top_k=top_k)
        weights = self._weights[filters.position]
        result["algorithm"] = "diagonal_weighted_cosine"
        result["weights"] = deepcopy(weights)
        result["warnings"].append(
            "Trọng số là giả thuyết thử nghiệm, chưa tối ưu bằng relevance labels; "
            "độ ổn định không phải chất lượng tuyển trạch.")
        for row in result["results"]:
            # Do not cite an ablated feature as a reason for a recommendation.
            row["evidence"] = {key: value for key, value in row["evidence"].items()
                               if weights[key] > 0}
            fragments = [
                f"{key}: {value['candidate']} (tham chiếu {value['reference']}; w={weights[key]:g})"
                for key, value in row["evidence"].items()
            ]
            row["explanation"] = "; ".join(fragments) + ". " + POLICIES[filters.position].limitation
        return result

