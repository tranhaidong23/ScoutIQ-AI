"""Read-only structured evidence over Day 5-8 engines; deterministic text rendering."""

from copy import deepcopy
from dataclasses import asdict
import json

import numpy as np

from src.recommendation.baseline import CosineRecommender, POLICIES, SearchFilters, _plain
from src.recommendation.comparison import PlayerComparison, UNITS, LIMITS, numeric_difference
from src.recommendation.constraints import AdvancedRecommender, SearchConstraints
from src.recommendation.knn import KNNRecommender


def constraint_evidence(candidate, reference_id, request):
    base = request.filters if isinstance(request, SearchConstraints) else request
    checks = []

    def add(field, operation, required, observed, passed, unit):
        checks.append({"field": field, "operation": operation, "required": required,
                       "observed": observed, "passed": bool(passed), "unit": unit})

    c = candidate
    add("position", "equals", base.position, c["position"], c["position"] == base.position, "category")
    add("player_id", "not_equals", reference_id, c["player_id"], c["player_id"] != reference_id, "ID")
    add("age", "between_inclusive", [base.min_age, base.max_age], c["age"],
        base.min_age <= c["age"] <= base.max_age, "years")
    add("minutes_played", "minimum", base.min_minutes, c["minutes_played"],
        c["minutes_played"] >= base.min_minutes, "minutes")
    if base.max_budget_eur is not None:
        add("market_value_in_eur", "maximum", base.max_budget_eur, c["market_value_in_eur"],
            c["market_value_in_eur"] <= base.max_budget_eur, "EUR")
    if isinstance(request, SearchConstraints):
        if request.sub_positions:
            add("sub_position", "in", list(request.sub_positions), c["sub_position"],
                c["sub_position"] in request.sub_positions, "category")
        for metric, threshold in (("goals_per90", request.min_goals_per90),
                                  ("assists_per90", request.min_assists_per90)):
            if threshold is not None:
                add(metric, "minimum", threshold, c[metric], c[metric] >= threshold, UNITS[metric])
        if request.preferred_foot and request.foot_mode == "hard":
            add("foot", "equals", request.preferred_foot, c["foot"], c["foot"] == request.preferred_foot, "category")
        if request.excluded_club_ids:
            club = c["current_club_id"]
            add("current_club_id", "not_in", list(request.excluded_club_ids), club,
                club is not None and club not in request.excluded_club_ids, "ID")
    if not all(check["passed"] for check in checks):
        raise ValueError("Cannot explain a candidate that violates a hard constraint")
    return checks


def render_explanation(evidence):
    """Render solely from structured evidence, never from engine free-form text."""
    c, ref = evidence["candidate"]["values"], evidence["reference"]["values"]
    sim = evidence["similarity"]
    fragments = [f"{c['name']} (ID {c['player_id']}) so với {ref['name']}: "
                 f"{sim['method']}={sim['score']:.6f}; không phải xác suất hoặc điểm kỹ năng."]
    for feature in evidence["selected_features"]:
        key = feature["feature"]
        a, b = feature["candidate_value"], feature["reference_value"]
        if feature["kind"] == "numeric":
            d = feature["difference"]
            fragments.append(f"{key}: {a} so với {b} {feature['unit']}; "
                             f"chênh lệch có dấu {d['signed_difference']:+.6g} {feature['unit']}.")
        else:
            fragments.append(f"{key}: {a if a is not None else 'thiếu dữ liệu'} / "
                             f"{b if b is not None else 'thiếu dữ liệu'}; raw match={feature['raw_match']}.")
    fragments.append(f"Market value={c['market_value_in_eur']} EUR; tuổi={c['age']}; phút={c['minutes_played']}. "
                     f"Đạt {len(evidence['hard_constraints'])} điều kiện cứng; định giá không là phí mua.")
    missing = evidence["candidate"]["missing_fields"]
    if missing:
        fragments.append("Thiếu metadata ứng viên: " + ", ".join(missing) + "; không suy đoán.")
    if evidence["soft_preference"] is not None:
        fragments.append("Ưu tiên chân thuận chỉ phá hòa khi cosine bằng nhau, không thay score.")
    fragments.append(evidence["position_limitation"])
    return " ".join(fragments)


class RecommendationExplainer:
    def __init__(self, engine):
        if not isinstance(engine, (CosineRecommender, KNNRecommender, AdvancedRecommender)):
            raise ValueError("Unsupported recommendation engine")
        self._engine = engine
        underlying = engine._engine if isinstance(engine, AdvancedRecommender) else engine
        self._knn = isinstance(underlying, KNNRecommender)
        self._representation = underlying._representation if self._knn else underlying
        self._comparison = PlayerComparison(self._representation._catalogue)

    def recommend(self, reference_player_id, filters, *, top_k=5):
        self._validate_request(filters)
        response = self._engine.recommend(reference_player_id, filters, top_k=top_k)
        return self._build(response, reference_player_id, filters)

    def _validate_request(self, filters):
        expected = SearchConstraints if isinstance(self._engine, AdvancedRecommender) else SearchFilters
        if type(filters) is not expected:
            raise ValueError("Invalid search request")

    def explain_response(self, response, reference_player_id, filters, *, top_k=5):
        """Validate a response against the same fitted engine/request before explaining.

        Reject stale/tampered IDs, rank, score, units, evidence, status or counts.
        This validation path recomputes a read-only request, not fitting or training.
        """
        if not isinstance(response, dict):
            raise ValueError("Response must be an engine response mapping")
        self._validate_request(filters)
        try:
            encoded = json.dumps(response, allow_nan=False, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise ValueError("Response must be finite JSON data") from exc
        canonical = self._engine.recommend(reference_player_id, filters, top_k=top_k)
        if encoded != json.dumps(canonical, allow_nan=False, sort_keys=True):
            raise ValueError("Response differs from engine/query/constraints; explanation refused")
        return self._build(response, reference_player_id, filters)

    def _build(self, response, reference_id, request):
        audit = self._representation.describe()
        reference = self._comparison.identity(reference_id)
        position = reference["values"]["position"]
        policy = POLICIES[position]
        weights = audit.get("weights", {}).get(position)
        method = "weighted_cosine" if weights is not None else "cosine"
        selected = [key for key in (*policy.numeric, *policy.categorical)
                    if weights is None or weights[key] > 0]
        explanations = []
        for result in response["results"]:
            candidate_id = result["player_id"]
            candidate = self._comparison.identity(candidate_id)
            row, refrow = self._comparison.player(candidate_id), self._comparison.player(reference_id)
            features = []
            for key in selected:
                a, b = _plain(row[key]), _plain(refrow[key])
                if key in policy.categorical:
                    a = None if a is None or not str(a).strip() else a
                    b = None if b is None or not str(b).strip() else b
                components = {name: value for name, value in result["cosine_components"].items()
                              if name == key or name.startswith(key + "=")}
                feature = {"feature": key, "source_column": key, "unit": UNITS[key],
                           "kind": "numeric" if key in policy.numeric else "categorical",
                           "candidate_value": a, "reference_value": b,
                           "weight": 1.0 if weights is None else float(weights[key]),
                           "cosine_component_sum": float(sum(components.values())),
                           "encoded_components": components}
                if key in policy.numeric:
                    feature["difference"] = numeric_difference(a, b)
                else:
                    vocab = audit["positions"][position]["categories"][key]
                    feature.update({"raw_match": None if a is None or b is None else a == b,
                                    "candidate_known_in_reference_vocabulary": a in vocab,
                                    "reference_known_in_reference_vocabulary": b in vocab})
                features.append(feature)
            component_sum = float(sum(f["cosine_component_sum"] for f in features))
            if not np.isfinite(component_sum) or abs(component_sum - result["similarity_score"]) > 1e-10:
                raise ValueError("Active feature components do not explain cosine score")
            raw = {k: _plain(v) for k, v in row.items()}
            raw.update(candidate["values"])
            checks = constraint_evidence(raw, reference_id, request)
            soft = None
            if isinstance(request, SearchConstraints) and request.foot_mode == "soft":
                soft = {"field": "foot", "preferred": request.preferred_foot,
                        "observed": candidate["values"]["foot"],
                        "matched": result["soft_preference_match"], "effect": "equal_score_tie_only"}
            evidence = {"rank": result["rank"], "candidate": candidate, "reference": reference,
                        "similarity": {"score": result["similarity_score"], "method": method,
                                       "retrieval": "sklearn_knn_cosine" if self._knn else "direct",
                                       "unit": "dimensionless", "range": [-1, 1],
                                       "component_sum": component_sum, "is_probability": False},
                        "selected_features": features, "hard_constraints": checks,
                        "soft_preference": soft, "scope": policy.scope,
                        "position_limitation": policy.limitation,
                        "limitations": LIMITS + ["Cosine components là phân rã hình học, không phải tác động nhân quả hoặc phần trăm kỹ năng."]}
            explanations.append({"evidence": evidence, "text": render_explanation(evidence)})
        output = {"schema_version": "scoutiq.explanation.v1", "cutoff": response["cutoff"],
                  "season": "2025/26", "recommendation": deepcopy(response),
                  "reference": reference, "explanations": explanations,
                  "status": response["status"],
                  "empty_reason": response["status"] if not response["results"] else None,
                  "fit_audit": audit["positions"][position],
                  "request": request.describe() if isinstance(request, SearchConstraints) else
                  {key: _plain(value) for key, value in asdict(request).items()},
                  "limitations": LIMITS + [policy.limitation]}
        json.dumps(output, allow_nan=False)
        return output
