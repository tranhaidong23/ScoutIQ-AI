"""Unified local service: validation -> hard filters -> ranking -> evidence.

Owns fitted engines for a single immutable snapshot/configuration. There is no
endpoint, database, credential loading, networking or model tuning here.
"""

from copy import deepcopy
from dataclasses import asdict
import hashlib
from io import BytesIO
import json

import pandas as pd

from src.features.build_features import validate_features, CUTOFF
from src.recommendation.baseline import CosineRecommender
from src.recommendation.comparison import PlayerComparison
from src.recommendation.config import ProjectPaths, ServiceConfig
from src.recommendation.constraints import AdvancedRecommender
from src.recommendation.explainability import RecommendationExplainer
from src.recommendation.knn import KNNRecommender
from src.recommendation.schemas import loads_request, parse_request, validate_response
from src.recommendation.weighted import WeightedCosineRecommender


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False, separators=(",", ":")).encode()).hexdigest()


class RecommendationService:
    def __init__(self, catalogue, *, fit_player_ids=None, config=None):
        if config is not None and type(config) is not ServiceConfig:
            raise ValueError("config must be ServiceConfig")
        self._config = ServiceConfig(**asdict(config or ServiceConfig()))
        self._comparison = PlayerComparison(catalogue)
        data = catalogue.sort_values("player_id").reset_index(drop=True).copy(deep=True)
        # Order-independent fingerprint of the full loaded table, including unused columns.
        content = data.to_csv(index=False, lineterminator="\n").encode("utf-8")
        sha = hashlib.sha256(content).hexdigest()
        self._dataset = {"version": "scoutiq-2025_26:" + sha, "content_sha256": sha,
                         "csv_sha256": None, "rows": len(data), "columns": len(data.columns),
                         "season": "2025/26", "cutoff": str(CUTOFF.date()), "source": "Transfermarkt"}
        fit_ids = None if fit_player_ids is None else tuple(fit_player_ids)
        common = {"fit_player_ids": fit_ids}
        self._engines = {
            "cosine": CosineRecommender(data, **common),
            "weighted_cosine": WeightedCosineRecommender(data, weights=self._config.weights, **common),
            "knn_cosine": KNNRecommender(data, **common),
            "knn_weighted_cosine": KNNRecommender(data, weights=self._config.weights, **common),
        }
        self._presenters = {method: RecommendationExplainer(AdvancedRecommender(engine))
                            for method, engine in self._engines.items()}
        self._configuration_id = fingerprint({"config": asdict(self._config),
                                             "engines": self._audits(), "dataset_content": sha})

    @classmethod
    def from_csv(cls, path=None, *, fit_player_ids=None, config=None):
        from pathlib import Path
        blob = Path(ProjectPaths().features if path is None else path).read_bytes()
        data = pd.read_csv(BytesIO(blob))
        validate_features(data)
        service = cls(data, fit_player_ids=fit_player_ids, config=config)
        service._dataset["csv_sha256"] = hashlib.sha256(blob).hexdigest()
        return service

    def _audits(self):
        return {method: engine.describe() for method, engine in self._engines.items()}

    def describe(self):
        return deepcopy({"dataset": self._dataset, "configuration_id": self._configuration_id,
                         "config": asdict(self._config), "engines": self._audits()})

    def recommend(self, payload):
        request, constraints = parse_request(payload, self._config)
        exp = self._presenters[request["method"]].recommend(
            request["reference_player_id"], constraints, top_k=request["top_k"])
        legacy = exp["recommendation"]
        ids = [r["player_id"] for r in legacy["results"]]
        comparisons = []
        if request["include_comparison"]:
            for start in range(0, len(ids), 4):
                comparisons.append(self._comparison.compare(
                    [request["reference_player_id"]] + ids[start:start+4],
                    reference_player_id=request["reference_player_id"]))
        response = {"schema_version": "scoutiq.service.v1", "status": exp["status"], "request": request,
                    "metadata": {"method": request["method"], "filters": constraints.describe(),
                        "candidate_count": legacy["eligible_count"],
                        "rankable_count": legacy["eligible_count"] - legacy["excluded_zero_vectors"],
                        "returned_count": len(ids), "top_k": request["top_k"],
                        "dataset": deepcopy(self._dataset), "configuration_id": self._configuration_id,
                        "limitations": deepcopy(exp["limitations"])},
                    "explanation": exp, "comparisons": comparisons}
        return validate_response(response)

    def recommend_json(self, text):
        return json.dumps(self.recommend(loads_request(text)), ensure_ascii=False, allow_nan=False, sort_keys=True)
