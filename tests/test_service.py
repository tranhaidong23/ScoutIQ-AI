"""Service contract and integration over real snapshot, no synthetic players."""

from copy import deepcopy
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from jsonschema import Draft202012Validator

from src.recommendation.config import METHODS, ProjectPaths, ServiceConfig
from src.recommendation.run_day8 import SCENARIOS
from src.recommendation.run_day10 import LEGACY_METHOD, latency_summary, run, scenario_request
from src.recommendation.schemas import REQUEST_SCHEMA, RESPONSE_SCHEMA, loads_request, parse_request, validate_response
from src.recommendation.service import RecommendationService


@pytest.fixture(scope="module")
def prior():
    return json.loads((ProjectPaths().reports / "day9/evaluation.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def service(prior):
    return RecommendationService.from_csv(fit_player_ids=prior["reference"]["fit_ids"])


@pytest.fixture
def payload():
    _, query, constraints = SCENARIOS[0]
    return scenario_request(query, constraints, "cosine")


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("name,query,constraints", SCENARIOS)
def test_exact_day9_and_json_reproducibility(service, prior, name, query, constraints, method):
    payload = scenario_request(query, constraints, method)
    original = deepcopy(payload)
    result = service.recommend(payload)
    old = next(c for c in prior["examples"] if (c["scenario"], c["engine"]) == (name, LEGACY_METHOD[method]))
    assert result["explanation"] == {k:v for k,v in old.items() if k not in ("scenario", "engine")}
    expected_groups = [{k:v for k,v in c.items() if k not in ("scenario", "engine", "group")}
                       for c in prior["comparisons"] if (c["scenario"],c["engine"]) == (name,LEGACY_METHOD[method])]
    assert result["comparisons"] == expected_groups
    encoded = service.recommend_json(json.dumps(payload))
    assert json.loads(encoded) == result and encoded == service.recommend_json(json.dumps(payload))
    assert payload == original
    if name == "no_results":
        assert result["metadata"]["returned_count"] == 0 and result["comparisons"] == []


@pytest.mark.parametrize("change", [
    {"method":"knn"}, {"method":None}, {"method":["cosine"]}, {"unknown":True}, {"weights":{}},
    {"reference_player_id":True}, {"reference_player_id":132098.0}, {"reference_player_id":"132098"},
    {"reference_player_id":0}, {"reference_player_id":999999999},
    {"top_k":0}, {"top_k":-2}, {"top_k":True}, {"top_k":5.0}, {"top_k":np.nan},
    {"include_comparison":"yes"}, {"include_comparison":1}, {"filters":None},
    {"filters":{"position":"Attack", "max_budget_eur":float("inf")}},
    {"filters":{"position":"Attack", "min_age":30,"max_age":20}},
    {"filters":{"position":"Attack", "max_budget_eur":-1}},
    {"filters":{"position":"Attack", "budget_value":5}},
    {"filters":{"position":"Attack", "budget_unit":"USD", "budget_value":5}},
    {"filters":{"position":"Attack", "budget_value":5,"budget_unit":"EUR", "max_budget_eur":5}},
    {"filters":{"position":"Goalkeeper", "min_goals_per90":0}},
    {"filters":{"position":"Defender"}},
    {"filters":{"position":"Attack", "sub_positions":["Unknown role"],"max_budget_eur":0}},
    {"filters":{"position":"Attack", "excluded_club_ids":[999999999],"max_budget_eur":0}},
    {"filters":{"position":"Attack", "sub_positions":("Centre-Forward",)}},
    {"filters":{"position":"Attack", "min_goals_per900":1}},
])
def test_invalid_service_inputs(service, payload, change):
    payload.update(change)
    with pytest.raises(ValueError): service.recommend(payload)


@pytest.mark.parametrize("text", ["null", "[]", "{}", "not json", '{"top_k":NaN}',
    '{"filters":{"position":"Attack","position":"Midfield"}}',
    '{"reference_player_id":132098,"reference_player_id":137576}',
    '{"reference_player_id":132098,"filters":{"position":"Attack","max_budget_eur":1e999}}'])
def test_json_invalid_inputs(service, text):
    with pytest.raises(ValueError): service.recommend_json(text)


def test_defaults_budget_and_optional_comparison(service, payload):
    payload.pop("method"); payload.pop("top_k"); payload.pop("include_comparison")
    result = service.recommend(payload)
    assert result["metadata"]["method"] == "cosine" and result["metadata"]["top_k"] == 5
    assert result["comparisons"] == []
    payload["filters"].pop("max_budget_eur")
    payload["filters"].update(budget_value=5, budget_unit="EUR_million")
    equivalent = service.recommend(payload)
    assert result["explanation"] == equivalent["explanation"]
    assert equivalent["metadata"]["filters"]["max_budget_eur"] == 5_000_000


@pytest.mark.parametrize("k", [1, 3, 5, 10000])
def test_k_and_comparison_group_boundaries(service, payload, k):
    payload["top_k"] = k
    result = service.recommend(payload)
    rows = result["explanation"]["recommendation"]["results"]
    assert len(rows) == min(k,22)
    groups = result["comparisons"]
    assert [p["values"]["player_id"] for g in groups for p in g["players"][1:]] == [r["player_id"] for r in rows]
    assert all(2 <= len(g["players"]) <= 5 for g in groups)


@pytest.mark.parametrize("kind", ["method","count","rankable","returned","k","status","reference","score",
    "rank","bool_id","float_id","unit","text","nan","inf","dataset","filter","components","group","difference","missing_rows"])
def test_corrupt_response_rejected(service, payload, kind):
    r = service.recommend(payload); meta = r["metadata"]; exp = r["explanation"]
    ev = exp["explanations"][0]["evidence"]
    if kind == "method": meta["method"] = "weighted_cosine"
    elif kind == "count": meta["candidate_count"] += 1
    elif kind == "rankable": meta["rankable_count"] += 1
    elif kind == "returned": meta["returned_count"] -= 1
    elif kind == "k": meta["top_k"] += 1
    elif kind == "status": r["status"] = "no_candidates"
    elif kind == "reference": exp["reference"]["values"]["player_id"] = 137576
    elif kind == "score": ev["similarity"]["score"] -= .1
    elif kind == "rank": ev["rank"] = 2
    elif kind == "bool_id": ev["candidate"]["values"]["player_id"] = True
    elif kind == "float_id": ev["candidate"]["values"]["player_id"] = float(ev["candidate"]["values"]["player_id"])
    elif kind == "unit": ev["selected_features"][0]["unit"] = "EUR_million"
    elif kind == "text": exp["explanations"][0]["text"] = "unsupported claim"
    elif kind == "nan": ev["similarity"]["score"] = np.nan
    elif kind == "inf": r["comparisons"][0]["numeric_differences"][0]["value"] = np.inf
    elif kind == "dataset": meta["dataset"]["version"] = "fake"
    elif kind == "filter": meta["filters"]["max_budget_eur"] = 1
    elif kind == "components": ev["selected_features"][0]["cosine_component_sum"] += .1
    elif kind == "group": r["comparisons"][0]["players"].reverse()
    elif kind == "difference": r["comparisons"][0]["numeric_differences"][0]["absolute_difference"] = 99
    elif kind == "missing_rows": r["comparisons"][0]["numeric_differences"].pop()
    with pytest.raises(ValueError): validate_response(r)


def test_no_refit_alias_or_mutation(service, payload, monkeypatch):
    from sklearn.preprocessing import StandardScaler
    def forbidden(*args, **kwargs): raise AssertionError("No scaler fitting during requests")
    before = service.describe()
    monkeypatch.setattr(StandardScaler, "fit", forbidden)
    a = service.recommend(payload); a["metadata"]["dataset"]["rows"] = 0
    a["explanation"]["reference"]["values"]["name"] = "mutated response"
    broken = {**payload, "top_k":True}
    with pytest.raises(ValueError): service.recommend(broken)
    assert service.describe() == before
    assert service.recommend(payload)["metadata"]["dataset"]["rows"] == 4112


def test_permutation_and_configuration_isolation(service, prior, payload):
    data = pd.read_csv(ProjectPaths().features)
    config = ServiceConfig()
    second = RecommendationService(data.iloc[::-1], fit_player_ids=prior["reference"]["fit_ids"][::-1], config=config)
    config.weights["Attack"]["goals_per90"] = 999
    a = service.recommend(payload); b = second.recommend(payload)
    assert a["explanation"] == b["explanation"] and a["comparisons"] == b["comparisons"]
    assert a["metadata"]["configuration_id"] == b["metadata"]["configuration_id"]
    assert b["metadata"]["dataset"]["csv_sha256"] is None
    assert a["metadata"]["dataset"]["content_sha256"] == b["metadata"]["dataset"]["content_sha256"]


@pytest.mark.parametrize("method", METHODS)
def test_zero_vector_and_nonzero_pool(method):
    data = pd.read_csv(ProjectPaths().features)
    small = data.loc[data.position.eq("Attack")].head(3).copy()
    small["sub_position"] = pd.NA
    ids = small.player_id.tolist()
    service = RecommendationService(small, fit_player_ids=[ids[0]])
    payload = {"reference_player_id":ids[0], "filters":{"position":"Attack"}, "method":method, "include_comparison":True}
    result = service.recommend(payload)
    assert result["status"] == "zero_reference_vector" and result["comparisons"] == []
    payload["reference_player_id"] = ids[1]
    result = service.recommend(payload)
    assert result["metadata"]["rankable_count"] < result["metadata"]["candidate_count"]


@pytest.mark.parametrize("kwargs", [{"default_method":"other"},{"default_top_k":True},{"default_top_k":0},{"weights":{}}])
def test_invalid_config(kwargs):
    with pytest.raises(ValueError): ServiceConfig(**kwargs)


def test_schemas_paths_latency_and_runner_guard(tmp_path, monkeypatch):
    Draft202012Validator.check_schema(REQUEST_SCHEMA)
    Draft202012Validator.check_schema(RESPONSE_SCHEMA)
    default = ProjectPaths().features
    monkeypatch.chdir(tmp_path)
    assert ProjectPaths().features == default and default.is_file()
    assert ProjectPaths(tmp_path).features == tmp_path / "data/processed/scoutiq_features_2025_26.csv"
    assert latency_summary([1,2,3,4,5])["median_ms"] == 3
    assert latency_summary([1,2,3,4,5])["p95_ms"] == pytest.approx(4.8)
    for bad in ([], [-1], [np.inf]):
        with pytest.raises(ValueError): latency_summary(bad)
    with pytest.raises(FileExistsError): run(tmp_path)
    with pytest.raises(ValueError): run(tmp_path / "not_created", repeats=0)
    assert not (tmp_path / "not_created").exists()


def test_dataset_validation_and_defaults_config(payload):
    data = pd.read_csv(ProjectPaths().features)
    data.loc[0,"goals_per90"] = np.nan
    with pytest.raises(ValueError): RecommendationService(data)
    payload.pop("method"); payload.pop("top_k")
    clean, _ = parse_request(payload, ServiceConfig(default_method="knn_cosine",default_top_k=3))
    assert clean["method"] == "knn_cosine" and clean["top_k"] == 3
    with pytest.raises(ValueError): loads_request({})
