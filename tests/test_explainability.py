"""Day 9: provenance, output immutability, strict consistency, and comparisons."""

from copy import deepcopy
import json

import numpy as np
import pandas as pd
import pytest

from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, SearchFilters
from src.recommendation.comparison import PlayerComparison, numeric_difference
from src.recommendation.constraints import AdvancedRecommender, SearchConstraints
from src.recommendation.explainability import RecommendationExplainer, render_explanation
from src.recommendation.knn import KNNRecommender
from src.recommendation.run_day5 import SCENARIOS as LEGACY
from src.recommendation.run_day8 import SCENARIOS, make_engines
from src.recommendation.run_day9 import run
from src.recommendation.weighted import WeightedCosineRecommender, experiment_weights


@pytest.fixture(scope="module")
def data():
    return pd.read_csv(FEATURE_FILE)


@pytest.fixture(scope="module")
def engines(data):
    ids = data.loc[~data.player_id.isin({q for _, q, _ in SCENARIOS}), "player_id"].tolist()
    return make_engines(data, ids)


@pytest.fixture(scope="module", params=["cosine", "weighted", "knn_cosine", "knn_weighted"])
def engine(request, engines):
    return engines[request.param]


@pytest.mark.parametrize("name,query,constraints", SCENARIOS)
def test_advanced_explanation_keeps_entire_response(engine, data, name, query, constraints):
    wrapped = AdvancedRecommender(engine)
    presenter = RecommendationExplainer(wrapped)
    before = deepcopy(engine.describe())
    original = wrapped.recommend(query, constraints)
    snapshot = deepcopy(original)
    output = presenter.explain_response(original, query, constraints)
    assert original == snapshot == output["recommendation"]
    assert output == presenter.recommend(query, constraints)
    assert engine.describe() == before
    assert len(output["explanations"]) == len(original["results"])
    lookup = data.set_index("player_id")
    for r, x in zip(original["results"], output["explanations"]):
        ev = x["evidence"]
        assert ev["rank"] == r["rank"]
        assert ev["candidate"]["values"]["player_id"] == r["player_id"]
        assert ev["similarity"]["score"] == r["similarity_score"]
        assert ev["similarity"]["is_probability"] is False
        assert x["text"] == render_explanation(ev)
        assert all(c["passed"] for c in ev["hard_constraints"])
        assert abs(sum(f["cosine_component_sum"] for f in ev["selected_features"]) - r["similarity_score"]) < 1e-10
        assert not {"market_value_in_eur", "market_value_m", "minutes_reliability"} & {f["feature"] for f in ev["selected_features"]}
        for f in ev["selected_features"]:
            raw = lookup.loc[r["player_id"], f["source_column"]]
            assert f["candidate_value"] is None if pd.isna(raw) else f["candidate_value"] == raw
        if constraints.filters.position in ("Defender", "Goalkeeper"):
            assert ev["scope"] == "context_profile_only"
            assert not {"goals_per90", "assists_per90"} & {f["feature"] for f in ev["selected_features"]}
    assert json.loads(json.dumps(output, allow_nan=False))
    if name == "no_results":
        assert output["explanations"] == [] and output["empty_reason"] == "no_candidates"


@pytest.mark.parametrize("name,query,filters", LEGACY)
def test_legacy_cosine_weighted_knn_api_unchanged(engine, name, query, filters):
    expected = engine.recommend(query, filters)
    actual = RecommendationExplainer(engine).recommend(query, filters)
    assert actual["recommendation"] == expected
    assert actual["status"] == expected["status"]


@pytest.mark.parametrize("kind", ["id", "float_id", "bool_rank", "reference", "name", "position", "score",
                                   "nan", "inf", "price", "minutes", "rank", "order", "duplicate",
                                   "component", "feature_value", "eligibility", "status", "unit", "text"])
def test_tampered_response_rejected(engines, kind):
    engine = AdvancedRecommender(engines["weighted"])
    _, q, c = SCENARIOS[0]
    response = engine.recommend(q, c)
    r = response["results"][0]
    if kind == "id": r["player_id"] = 999999999
    elif kind == "float_id": r["player_id"] = float(r["player_id"])
    elif kind == "bool_rank": r["rank"] = True
    elif kind == "reference": response["reference"]["player_id"] = 137576
    elif kind == "name": r["name"] = "wrong identity"
    elif kind == "position": r["position"] = "Goalkeeper"
    elif kind == "score": r["similarity_score"] -= .1
    elif kind == "nan": r["similarity_score"] = np.nan
    elif kind == "inf": r["constraint_evidence"]["goals_per90"] = np.inf
    elif kind == "price": r["market_value_in_eur"] /= 1_000_000
    elif kind == "minutes": r["minutes_played"] /= 90
    elif kind == "rank": r["rank"] = 2
    elif kind == "order": response["results"].reverse()
    elif kind == "duplicate": response["results"][1] = deepcopy(r)
    elif kind == "component": r["cosine_components"]["goals_per90"] += .1
    elif kind == "feature_value": r["evidence"]["goals_per90"]["candidate"] += .1
    elif kind == "eligibility": response["eligible_count"] += 1
    elif kind == "status": response["status"] = "no_candidates"
    elif kind == "unit": response["search_constraints"]["budget_unit"] = "EUR_million"
    elif kind == "text": r["explanation"] = "Injected unsupported assertion"
    with pytest.raises(ValueError):
        RecommendationExplainer(engine).explain_response(response, q, c)


@pytest.mark.parametrize("a,b,delta,relative,reason", [(5, 2, 3, 150, None), (1, 2, -1, -50, None),
    (0, 0, 0, None, "zero_reference"), (1, 0, 1, None, "zero_reference"),
    (None, 2, None, None, "missing_value"), (2, None, None, None, "missing_value")])
def test_difference_formula_and_undefined(a, b, delta, relative, reason):
    result = numeric_difference(a, b)
    assert result["signed_difference"] == delta
    assert result["absolute_difference"] == (abs(delta) if delta is not None else None)
    assert result["relative_difference_pct"] == relative
    assert result["relative_reason"] == reason


@pytest.mark.parametrize("a,b", [(np.nan, 1), (1, np.inf), (True, 1), ("1", 1), (1e308, -1e308), (1e308, 1e-308)])
def test_invalid_difference_values(a, b):
    with pytest.raises(ValueError):
        numeric_difference(a, b)


@pytest.mark.parametrize("position", ["Attack", "Midfield", "Defender", "Goalkeeper"])
@pytest.mark.parametrize("size", [2, 3, 4, 5])
def test_comparison_sizes_units_differences_and_no_winner(data, position, size):
    ids = data.loc[data.position.eq(position), "player_id"].head(size).tolist()
    comparison = PlayerComparison(data).compare(ids)
    assert [p["values"]["player_id"] for p in comparison["players"]] == ids
    for r in comparison["numeric_differences"]:
        assert r["signed_difference"] == pytest.approx(r["value"] - r["reference_value"])
        assert r["absolute_difference"] == abs(r["signed_difference"])
        if r["reference_value"] == 0:
            assert r["relative_difference_pct"] is None and r["relative_reason"] == "zero_reference"
        else:
            assert r["relative_difference_pct"] == pytest.approx(100 * (r["value"] - r["reference_value"]) / abs(r["reference_value"]))
    metrics = {r["metric"] for r in comparison["numeric_differences"]}
    if position in ("Defender", "Goalkeeper"):
        assert metrics == {"age", "minutes_played", "market_value_in_eur"}
    assert "winner" not in comparison and "ranking" not in comparison
    json.dumps(comparison, allow_nan=False)


def test_real_zero_reference_missing_metadata_and_mixed_positions(data):
    zero = int(data.loc[data.position.eq("Attack") & data.goals.eq(0), "player_id"].iloc[0])
    missing = int(data.loc[data.position.eq("Attack") & data.foot.isna(), "player_id"].iloc[0])
    positive = 132098
    comparison = PlayerComparison(data).compare([zero, positive, missing])
    r = next(x for x in comparison["numeric_differences"] if x["player_id"] == positive and x["metric"] == "goals_per90")
    assert r["relative_reason"] == "zero_reference" and r["relative_difference_pct"] is None
    metadata = comparison["players"][2]
    assert metadata["values"]["foot"] is None and "foot" in metadata["missing_fields"]
    mixed = PlayerComparison(data).compare([132098, 629773])
    assert mixed["scope"] == "context_only"
    assert not {"goals_per90", "assists_per90"} & {r["metric"] for r in mixed["numeric_differences"]}


@pytest.mark.parametrize("ids,ref", [([], None), ([132098], None), ([132098]*6, None),
    ([132098,132098], None), ([132098,999999999], None), ([132098,True], None),
    ([132098,137576.0], None), ("132098,137576", None), ([132098,137576], 629773)])
def test_invalid_comparison_ids(data, ids, ref):
    with pytest.raises(ValueError):
        PlayerComparison(data).compare(ids, reference_player_id=ref)


@pytest.mark.parametrize("column,value", [("age", np.nan), ("minutes_played", np.inf),
    ("goals_per90", np.nan), ("assists_per90", -1), ("market_value_m", 999999),
    ("market_value_in_eur", 0), ("minutes_played", 0), ("goals_per90", 1234)])
def test_catalogue_quality_units_and_per90(data, column, value):
    modified = data.copy(deep=True)
    # Permit invalid non-finite test input even with pandas' strict integer dtype.
    modified[column] = modified[column].astype(float)
    modified.loc[0, column] = value
    with pytest.raises(ValueError):
        PlayerComparison(modified)


def test_duplicate_dataset_id_and_schema(data):
    for modified in (pd.concat([data, data.head(1)]), data.drop(columns="foot")):
        with pytest.raises(ValueError):
            PlayerComparison(modified)


@pytest.mark.parametrize("configuration", ["ablate_categories", "ablate_first_numeric"])
def test_ablated_features_not_given_credit(data, configuration):
    weights = experiment_weights()[configuration]
    engine = WeightedCosineRecommender(data, weights=weights)
    query = 132098
    output = RecommendationExplainer(engine).recommend(query, SearchFilters("Attack"))
    keys = {key for key, weight in weights["Attack"].items() if weight > 0}
    for ex in output["explanations"]:
        assert {f["feature"] for f in ex["evidence"]["selected_features"]} == keys


def test_missing_and_unseen_categories_are_not_invented(data):
    modified = data.copy(deep=True)
    modified.loc[modified.player_id == 629773, "foot"] = None
    engine = CosineRecommender(modified, fit_player_ids=data.loc[data.player_id.ne(629773), "player_id"].tolist())
    result = RecommendationExplainer(engine).recommend(629773, SearchFilters("Goalkeeper"))
    f = next(f for f in result["explanations"][0]["evidence"]["selected_features"] if f["feature"] == "foot")
    assert f["reference_value"] is None and f["raw_match"] is None
    assert not f["reference_known_in_reference_vocabulary"] and f["cosine_component_sum"] == 0


@pytest.mark.parametrize("knn", [False, True])
def test_zero_query_has_no_fabricated_explanation(data, knn):
    small = data.loc[data.position.eq("Attack")].head(3).copy()
    small["sub_position"] = None
    query = int(small.player_id.iloc[0])
    cls = KNNRecommender if knn else CosineRecommender
    model = cls(small, fit_player_ids=[query])
    result = RecommendationExplainer(model).recommend(query, SearchFilters("Attack"))
    assert result["status"] == "zero_reference_vector" and result["explanations"] == []


def test_no_refit_during_explain_and_no_aliasing(engines, monkeypatch):
    from sklearn.preprocessing import StandardScaler
    presenter = RecommendationExplainer(AdvancedRecommender(engines["weighted"]))
    def forbidden(*args, **kwargs):
        raise AssertionError("Presentation must never fit a scaler")
    monkeypatch.setattr(StandardScaler, "fit", forbidden)
    _, q, c = SCENARIOS[0]
    original = presenter._engine.recommend(q, c)
    frozen = deepcopy(original)
    result = presenter.explain_response(original, q, c)
    result["recommendation"]["results"][0]["name"] = "changed in returned copy"
    assert original == frozen


def test_comparison_order_permutation_only_changes_display(data):
    compare = PlayerComparison(data)
    ids = [132098, 1360186, 818445]
    a = compare.compare(ids, reference_player_id=132098)
    b = PlayerComparison(data.iloc[::-1]).compare(ids[::-1], reference_player_id=132098)
    key = lambda r: (r["player_id"], r["metric"])
    assert sorted(a["numeric_differences"], key=key) == sorted(b["numeric_differences"], key=key)


def test_invalid_request_response_engine_and_output(engines, tmp_path):
    presenter = RecommendationExplainer(engines["cosine"])
    for request in (None, {}, SCENARIOS[0][2]):
        with pytest.raises(ValueError):
            presenter.recommend(132098, request)
    with pytest.raises(ValueError):
        presenter.explain_response([], 132098, SearchFilters("Attack"))
    with pytest.raises(ValueError):
        RecommendationExplainer(object())
    with pytest.raises(FileExistsError):
        run(tmp_path)
