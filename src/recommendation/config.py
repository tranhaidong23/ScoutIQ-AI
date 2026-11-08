"""Portable paths and explicit server-owned configuration; no learned defaults."""

from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

from src.recommendation.weighted import default_weights, validate_weights

METHODS = ("cosine", "weighted_cosine", "knn_cosine", "knn_weighted_cosine")


@dataclass(frozen=True)
class ProjectPaths:
    root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])

    def __post_init__(self):
        object.__setattr__(self, "root", Path(self.root).resolve())

    @property
    def features(self):
        return self.root / "data/processed/scoutiq_features_2025_26.csv"

    @property
    def reports(self):
        return self.root / "reports"


@dataclass(frozen=True)
class ServiceConfig:
    default_method: str = "cosine"
    default_top_k: int = 5
    weights: dict = field(default_factory=default_weights)

    def __post_init__(self):
        if self.default_method not in METHODS:
            raise ValueError("Unsupported default method")
        if type(self.default_top_k) is not int or self.default_top_k <= 0:
            raise ValueError("default_top_k must be a positive integer")
        object.__setattr__(self, "weights", deepcopy(validate_weights(self.weights)))
