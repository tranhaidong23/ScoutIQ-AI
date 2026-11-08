"""Versioned JSON Schema plus cross-field checks; independent of any web server.

Legacy evidence objects remain extensible; their required core is typed here.
Strict finite JSON and semantic checks supplement JSON Schema (including integer
lexical types: 5.0 is not accepted as an ID even though JSON Schema allows it).
"""

from copy import deepcopy
import json
import math

from jsonschema import Draft202012Validator, validators

from src.recommendation.baseline import POLICIES
from src.recommendation.comparison import UNITS, numeric_difference
from src.recommendation.config import METHODS, ServiceConfig
from src.recommendation.constraints import SearchConstraints
from src.recommendation.explainability import constraint_evidence, render_explanation


def obj(properties, required=None, *, extra=False):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": extra}


def array(items, **kwargs):
    return {"type": "array", "items": items, **kwargs}


NUMBER = {"type": "number"}
NONNEGATIVE = {"type": "number", "minimum": 0}
ID = {"type": "integer", "minimum": 1}
COUNT = {"type": "integer", "minimum": 0}
STRING = {"type": "string"}
NULL_STRING = {"type": ["string", "null"]}
NULL_NUMBER = {"type": ["number", "null"]}
STRINGS = array(STRING)
STATUS = {"enum": ["ok", "no_candidates", "zero_reference_vector"]}
HASH = {"type": "string", "pattern": "^[a-f0-9]{64}$"}

FILTER_SCHEMA = obj({
    "position": {"enum": list(POLICIES)}, "min_age": NONNEGATIVE, "max_age": NONNEGATIVE,
    "max_budget_eur": {"type": ["number", "null"], "minimum": 0}, "min_minutes": NONNEGATIVE,
    "budget_value": NONNEGATIVE, "budget_unit": {"enum": ["EUR", "EUR_million"]},
    "sub_positions": array({"type": "string", "minLength": 1}, uniqueItems=True),
    "min_goals_per90": {"type": ["number", "null"], "minimum": 0},
    "min_assists_per90": {"type": ["number", "null"], "minimum": 0},
    "preferred_foot": {"enum": ["left", "right", "both", None]},
    "foot_mode": {"enum": ["hard", "soft"]}, "excluded_club_ids": array(ID, uniqueItems=True),
}, ["position"])
REQUEST_SCHEMA = {"$schema": "https://json-schema.org/draft/2020-12/schema", **obj({
    "reference_player_id": ID, "filters": FILTER_SCHEMA,
    "method": {"enum": list(METHODS)}, "top_k": ID, "include_comparison": {"type": "boolean"},
}, ["reference_player_id", "filters"])}

IDENTITY = obj({"values": obj({
    "player_id": ID, "name": STRING, "position": {"enum": list(POLICIES)},
    "age": NONNEGATIVE, "minutes_played": NONNEGATIVE, "market_value_in_eur": NONNEGATIVE,
    "foot": NULL_STRING, "sub_position": NULL_STRING, "valuation_date": STRING,
    "current_club_id": NULL_NUMBER, "current_club_name": NULL_STRING, "club_name_verified": NULL_STRING,
}), "missing_fields": STRINGS, "units": {"type": "object"}})
SIMILARITY = obj({"score": {"type": "number", "minimum": -1, "maximum": 1},
    "method": {"enum": ["cosine", "weighted_cosine"]}, "retrieval": {"enum": ["direct", "sklearn_knn_cosine"]},
    "unit": {"const": "dimensionless"}, "range": {"const": [-1, 1]},
    "component_sum": NUMBER, "is_probability": {"const": False}})
FEATURE = obj({"feature": STRING, "source_column": STRING, "unit": STRING,
    "kind": {"enum": ["numeric", "categorical"]}, "candidate_value": {}, "reference_value": {},
    "weight": NONNEGATIVE, "cosine_component_sum": NUMBER,
    "encoded_components": {"type": "object", "additionalProperties": NUMBER}}, extra=True)
EVIDENCE = obj({"rank": ID, "candidate": IDENTITY, "reference": IDENTITY,
    "similarity": SIMILARITY, "selected_features": array(FEATURE, minItems=1),
    "hard_constraints": array(obj({"field": STRING, "operation": STRING, "required": {},
        "observed": {}, "passed": {"const": True}, "unit": STRING}), minItems=1),
    "soft_preference": {"type": ["object", "null"]}, "scope": STRING,
    "position_limitation": STRING, "limitations": STRINGS})
RESULT_ROW = obj({"player_id": ID, "name": STRING, "position": {"enum": list(POLICIES)},
    "rank": ID, "similarity_score": {"type": "number", "minimum": -1, "maximum": 1},
    "age": NONNEGATIVE, "minutes_played": NONNEGATIVE, "market_value_in_eur": NONNEGATIVE,
    "cosine_components": {"type": "object", "additionalProperties": NUMBER},
    "evidence": {"type": "object", "additionalProperties": obj({"candidate": {}, "reference": {}})},
    "constraint_evidence": {"type": "object"}, "soft_preference_match": {"type": "boolean"}}, extra=True)
LEGACY_RESPONSE = obj({"reference": obj({"player_id": ID, "name": STRING, "position": STRING}),
    "results": array(RESULT_ROW), "status": STATUS, "eligible_count": COUNT,
    "excluded_zero_vectors": COUNT, "top_k_requested": ID, "cutoff": STRING,
    "search_constraints": {"type": "object"}, "filter_audit": obj({
        "after_hard_constraints": COUNT, "catalogue_before": COUNT, "stages": array({"type": "object"})})}, extra=True)
EXPLANATION = obj({"schema_version": {"const": "scoutiq.explanation.v1"},
    "cutoff": STRING, "season": {"const": "2025/26"}, "recommendation": LEGACY_RESPONSE,
    "reference": IDENTITY, "explanations": array(obj({"evidence": EVIDENCE, "text": STRING})),
    "status": STATUS, "empty_reason": NULL_STRING, "fit_audit": {"type": "object"},
    "request": {"type": "object"}, "limitations": STRINGS})
DIFFERENCE = obj({"player_id": ID, "reference_player_id": ID, "metric": STRING,
    "source_column": STRING, "unit": STRING, "value": NULL_NUMBER, "reference_value": NULL_NUMBER,
    "signed_difference": NULL_NUMBER, "absolute_difference": NULL_NUMBER,
    "relative_difference_pct": NULL_NUMBER, "relative_reason": NULL_STRING, "direction": STRING})
COMPARISON = obj({"schema_version": {"const": "scoutiq.comparison.v1"}, "cutoff": STRING,
    "season": {"const": "2025/26"}, "reference_player_id": ID,
    "players": array(IDENTITY, minItems=2, maxItems=5), "scope": STRING,
    "numeric_differences": array(DIFFERENCE), "categorical_comparisons": array({"type": "object"}),
    "difference_definition": STRING, "limitations": STRINGS})
DATASET = obj({"version": STRING, "content_sha256": HASH,
    "csv_sha256": {"anyOf": [HASH, {"type": "null"}]}, "rows": ID, "columns": ID,
    "season": {"const": "2025/26"}, "cutoff": {"const": "2026-06-12"}, "source": {"const": "Transfermarkt"}})
RESPONSE_SCHEMA = {"$schema": "https://json-schema.org/draft/2020-12/schema", **obj({
    "schema_version": {"const": "scoutiq.service.v1"}, "status": STATUS,
    "request": {**REQUEST_SCHEMA, "required": list(REQUEST_SCHEMA["properties"])},
    "metadata": obj({"method": {"enum": list(METHODS)}, "filters": {"type": "object"},
        "candidate_count": COUNT, "rankable_count": COUNT, "returned_count": COUNT, "top_k": ID,
        "dataset": DATASET, "configuration_id": HASH, "limitations": STRINGS}),
    "explanation": EXPLANATION, "comparisons": array(COMPARISON),
})}

_checker = Draft202012Validator.TYPE_CHECKER.redefine("integer", lambda _, value: type(value) is int)
_Validator = validators.extend(Draft202012Validator, type_checker=_checker)
_REQUEST = _Validator(REQUEST_SCHEMA)
_RESPONSE = _Validator(RESPONSE_SCHEMA)


def finite_json(value):
    """Reject non-JSON Python types, non-string keys and non-finite numbers."""
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            raise ValueError("JSON object keys must be strings")
        for item in value.values(): finite_json(item)
    elif type(value) is list:
        for item in value: finite_json(item)
    elif type(value) is float:
        if not math.isfinite(value): raise ValueError("JSON numbers must be finite")
    elif value is not None and type(value) not in (str, int, bool):
        raise ValueError("Only native JSON values are accepted")


def validate_schema(value, validator):
    finite_json(value)
    error = next(validator.iter_errors(value), None)
    if error is not None:
        # Do not echo payload values (a future client may send private content).
        raise ValueError(f"Schema validation failed at {list(error.absolute_path)} ({error.validator})")


def parse_request(payload, config=None):
    validate_schema(payload, _REQUEST)
    config = config or ServiceConfig()
    clean = deepcopy(payload)
    clean.setdefault("method", config.default_method)
    clean.setdefault("top_k", config.default_top_k)
    clean.setdefault("include_comparison", False)
    constraints = SearchConstraints.from_request(clean["filters"])
    return clean, constraints


def loads_request(text):
    if type(text) is not str: raise ValueError("JSON request must be text")
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result: raise ValueError("Duplicate JSON object key")
            result[k] = v
        return result
    def constant(_): raise ValueError("Nonfinite JSON number")
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON request") from exc


def validate_response(response):
    """Shape + cross-field consistency, without a second engine retrieval."""
    validate_schema(response, _RESPONSE)
    request, constraints = parse_request(response["request"])
    meta, exp = response["metadata"], response["explanation"]
    legacy, ref = exp["recommendation"], exp["reference"]["values"]
    rows, items = legacy["results"], exp["explanations"]
    def require(condition):
        if not condition: raise ValueError("Inconsistent service response")
    require(meta["method"] == request["method"])
    require(meta["filters"] == constraints.describe() == exp["request"] == legacy["search_constraints"])
    require(meta["top_k"] == request["top_k"] == legacy["top_k_requested"])
    require(meta["candidate_count"] == legacy["eligible_count"] == legacy["filter_audit"]["after_hard_constraints"])
    require(meta["rankable_count"] == meta["candidate_count"] - legacy["excluded_zero_vectors"])
    require(meta["returned_count"] == len(rows) == len(items) <= min(meta["rankable_count"], meta["top_k"]))
    require(response["status"] == exp["status"] == legacy["status"])
    require(bool(rows) == (response["status"] == "ok"))
    require(exp["empty_reason"] == (None if rows else response["status"]))
    require(ref["player_id"] == request["reference_player_id"] == legacy["reference"]["player_id"])
    require(ref["position"] == constraints.filters.position)
    require(exp["cutoff"] == legacy["cutoff"] == meta["dataset"]["cutoff"])
    require(meta["dataset"]["version"] == "scoutiq-2025_26:" + meta["dataset"]["content_sha256"])
    require(meta["limitations"] == exp["limitations"])
    require(legacy["reference"]["name"] == ref["name"] and legacy["reference"]["position"] == ref["position"])
    ids = [r["player_id"] for r in rows]
    require(len(set(ids)) == len(ids) and ref["player_id"] not in ids)
    require(rows == sorted(rows, key=lambda r: (-r["similarity_score"], -int(r["soft_preference_match"]), r["player_id"])))
    for rank, (row, item) in enumerate(zip(rows, items), 1):
        ev = item["evidence"]; player = ev["candidate"]["values"]; sim = ev["similarity"]
        require(row["rank"] == ev["rank"] == rank and ev["reference"] == exp["reference"])
        require(all(player[k] == row[k] for k in ("player_id", "name", "position", "age", "minutes_played", "market_value_in_eur")))
        require(sim["score"] == row["similarity_score"])
        require(sim["method"] == ("weighted_cosine" if "weighted" in request["method"] else "cosine"))
        require(sim["retrieval"] == ("sklearn_knn_cosine" if request["method"].startswith("knn") else "direct"))
        require(ev["hard_constraints"] == constraint_evidence({**row["constraint_evidence"], **player}, ref["player_id"], constraints))
        require(item["text"] == render_explanation(ev))
        total = 0.0
        require(len({f["feature"] for f in ev["selected_features"]}) == len(ev["selected_features"]))
        for f in ev["selected_features"]:
            key = f["feature"]
            require(key in (*POLICIES[player["position"]].numeric, *POLICIES[player["position"]].categorical))
            require(f["unit"] == UNITS[key] and f["source_column"] == key and f["weight"] > 0)
            require(key in row["evidence"])
            require(f["candidate_value"] == row["evidence"][key]["candidate"] and f["reference_value"] == row["evidence"][key]["reference"])
            require(f["encoded_components"] == {k:v for k,v in row["cosine_components"].items() if k == key or k.startswith(key + "=")})
            require(math.isclose(f["cosine_component_sum"], sum(f["encoded_components"].values()), abs_tol=1e-10))
            if f["kind"] == "numeric": require(f["difference"] == numeric_difference(f["candidate_value"], f["reference_value"]))
            total += f["cosine_component_sum"]
        require(math.isclose(total, sim["score"], abs_tol=1e-10) and math.isclose(total, sim["component_sum"], abs_tol=1e-10))
    expected_groups = [[ref["player_id"]] + ids[i:i+4] for i in range(0, len(ids), 4)] if request["include_comparison"] else []
    require(len(response["comparisons"]) == len(expected_groups))
    for group, expected_ids in zip(response["comparisons"], expected_groups):
        require([p["values"]["player_id"] for p in group["players"]] == expected_ids)
        require(group["reference_player_id"] == ref["player_id"] and group["cutoff"] == exp["cutoff"])
        identity_by_id = {ref["player_id"]: exp["reference"], **{
            item["evidence"]["candidate"]["values"]["player_id"]: item["evidence"]["candidate"] for item in items}}
        require(group["players"] == [identity_by_id[i] for i in expected_ids])
        attacking = ref["position"] in ("Attack", "Midfield")
        metrics = ["age", "minutes_played", "market_value_in_eur"] + (["goals_per90", "assists_per90"] if attacking else [])
        require(group["scope"] == ("attacking_output_and_context" if attacking else "context_only"))
        require([(r["player_id"], r["metric"]) for r in group["numeric_differences"]] == [(i,m) for i in expected_ids for m in metrics])
        require([(r.get("player_id"), r.get("metric")) for r in group["categorical_comparisons"]] ==
                [(i,m) for i in expected_ids for m in ("position", "sub_position", "foot")])
        for r in group["numeric_differences"]:
            require(r["player_id"] in expected_ids and r["reference_player_id"] == ref["player_id"])
            require(r["metric"] in UNITS and r["unit"] == UNITS[r["metric"]] and r["source_column"] == r["metric"])
            require(all(r[k] == v for k,v in numeric_difference(r["value"], r["reference_value"]).items()))
    return response
