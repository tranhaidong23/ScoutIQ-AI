"""Day 6 real-snapshot regression and independent mathematical checks."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, POLICIES, SearchFilters
from src.recommendation.evaluation import check_response, signature, stability_metrics
from src.recommendation.run_day5 import SCENARIOS
from src.recommendation.run_day6 import run
from src.recommendation.weighted import (
    WeightedCosineRecommender, default_weights, experiment_weights, unit_weights,
)

QUERY_IDS = {query for _, query, _ in SCENARIOS}


@pytest.fixture(scope="module")
def data():
    return pd.read_csv(FEATURE_FILE)


@pytest.fixture(scope="module")
def fit_ids(data):
    return data.loc[~data.player_id.isin(QUERY_IDS), "player_id"].tolist()


@pytest.fixture(scope="module")
def engine(data, fit_ids):
    return WeightedCosineRecommender(data, fit_player_ids=fit_ids)


@pytest.fixture(scope="module")
def baseline(data, fit_ids):
    return CosineRecommender(data, fit_player_ids=fit_ids)


@pytest.mark.parametrize("position", list(POLICIES))
def test_independent_weighted_formula(data, fit_ids, engine, position):
    """Scalar oracle uses raw rows and reference statistics, not engine matrices."""
    _, query, filters = next(s for s in SCENARIOS if s[2].position == position)
    source = data.set_index("player_id")
    policy = POLICIES[position]
    fit = data.loc[data.player_id.isin(fit_ids) & data.position.eq(position)]
    mean = fit[list(policy.numeric)].mean().to_numpy()
    scale = fit[list(policy.numeric)].std(ddof=0).replace(0, 1).to_numpy()
    categories = {col: sorted(fit[col].dropna().unique()) for col in policy.categorical}
    weights = default_weights()[position]
    w = np.array([weights[col] for col in policy.numeric] +
                 [weights[col] for col, values in categories.items() for _ in values])

    def vector(player_id):
        row = source.loc[player_id]
        numeric = (row[list(policy.numeric)].to_numpy(dtype=float) - mean) / scale
        categorical = [float(pd.notna(row[col]) and row[col] == value)
                       for col, values in categories.items() for value in values]
        return np.r_[numeric, categorical]

    q = vector(query)
    for row in engine.recommend(query, filters)["results"]:
        x = vector(row["player_id"])
        expected = sum(w * q * x) / np.sqrt(sum(w * q * q) * sum(w * x * x))
        assert row["similarity_score"] == pytest.approx(expected, abs=1e-11)
        assert sum(row["cosine_components"].values()) == pytest.approx(expected, abs=1e-11)


@pytest.mark.parametrize("name,query,filters", SCENARIOS)
def test_unit_weights_full_regression(data, fit_ids, baseline, name, query, filters):
    model = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=unit_weights())
    assert signature(model.recommend(query, filters, top_k=5000)) == signature(
        baseline.recommend(query, filters, top_k=5000))


@pytest.mark.parametrize("configuration", list(experiment_weights()))
def test_all_scenarios_filters_determinism_and_top_k(data, fit_ids, configuration):
    weights = experiment_weights()[configuration]
    before = data.copy(deep=True)
    model = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=weights)
    reverse = WeightedCosineRecommender(data.iloc[::-1], fit_player_ids=fit_ids[::-1], weights=weights)
    audit = model.describe()
    for _, query, filters in SCENARIOS:
        full = model.recommend(query, filters, top_k=5000)
        check_response(full, query, filters)
        assert signature(full) == signature(reverse.recommend(query, filters, top_k=5000))
        assert signature(full) == signature(model.recommend(query, filters, top_k=5000))
        assert signature(full)[:5] == signature(model.recommend(query, filters))
        for row in full["results"][:5]:
            assert all(weights[filters.position][key] > 0 for key in row["evidence"])
    assert audit == model.describe()
    pd.testing.assert_frame_equal(before, data)


@pytest.mark.parametrize("value", [-1, np.nan, np.inf, -np.inf, True, np.bool_(True), "1", None])
def test_invalid_weight_values(data, value):
    weights = default_weights()
    weights["Attack"]["goals_per90"] = value
    with pytest.raises(ValueError, match="finite and nonnegative"):
        WeightedCosineRecommender(data, weights=weights)


@pytest.mark.parametrize("kind", ["missing_position", "extra_position", "missing_feature",
                                  "market_value", "goals_for_gk", "not_mapping"])
def test_invalid_weight_schema(data, kind):
    weights = default_weights()
    if kind == "missing_position":
        del weights["Attack"]
    elif kind == "extra_position":
        weights["Unknown"] = {}
    elif kind == "missing_feature":
        del weights["Attack"]["assists_per90"]
    elif kind == "market_value":
        weights["Attack"]["market_value_in_eur"] = 1
    elif kind == "goals_for_gk":
        weights["Goalkeeper"]["goals_per90"] = 1
    else:
        weights = []
    with pytest.raises(ValueError):
        WeightedCosineRecommender(data, weights=weights)


def test_all_zero_weights_rejected(data):
    weights = default_weights()
    weights["Attack"] = dict.fromkeys(weights["Attack"], 0)
    with pytest.raises(ValueError, match="positive weight"):
        WeightedCosineRecommender(data, weights=weights)


@pytest.mark.parametrize("factor", [1e-200, 1e200])
def test_common_weight_scale_invariance(data, fit_ids, engine, factor):
    weights = {pos: {key: value * factor for key, value in fields.items()}
               for pos, fields in default_weights().items()}
    model = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=weights)
    for _, query, filters in SCENARIOS:
        assert signature(model.recommend(query, filters)) == signature(engine.recommend(query, filters))


def test_weight_dynamic_range_rejected(data):
    weights = default_weights()
    weights["Attack"]["goals_per90"] = 1e308
    weights["Attack"]["assists_per90"] = 1e-308
    with pytest.raises(ValueError, match="underflows"):
        WeightedCosineRecommender(data, weights=weights)


def test_configuration_is_copied(data):
    weights = default_weights()
    model = WeightedCosineRecommender(data, weights=weights)
    before = model.describe()
    weights["Attack"]["goals_per90"] = 999
    audit = model.describe()
    audit["weights"]["Attack"]["goals_per90"] = 888
    assert model.describe() == before


def test_zero_vectors_and_missing_category(data):
    small = data.loc[data.position.eq("Attack")].head(3).copy()
    small["sub_position"] = pd.NA
    ids = small.player_id.tolist()
    # Fit a real single row: that row's numeric z-scores are exactly zero.
    model = WeightedCosineRecommender(small, fit_player_ids=[ids[0]])
    zero = model.recommend(ids[0], SearchFilters("Attack"))
    assert zero["status"] == "zero_reference_vector" and not zero["results"]
    nonzero = model.recommend(ids[1], SearchFilters("Attack"))
    assert nonzero["excluded_zero_vectors"] >= 1
    assert ids[0] not in [row["player_id"] for row in nonzero["results"]]
    only_role = default_weights()
    only_role["Attack"] = {"goals_per90": 0, "assists_per90": 0, "sub_position": 1}
    model = WeightedCosineRecommender(small, weights=only_role)
    assert model.recommend(ids[1], SearchFilters("Attack"))["status"] == "zero_reference_vector"


def test_filters_inclusive_boundaries_and_empty(engine):
    row = engine.recommend(132098, SearchFilters("Attack"))["results"][0]
    f = SearchFilters("Attack", row["age"], row["age"], row["market_value_in_eur"], row["minutes_played"])
    assert row["player_id"] in [r["player_id"] for r in engine.recommend(132098, f, top_k=5000)["results"]]
    f = SearchFilters("Attack", row["age"], row["age"], row["market_value_in_eur"] - 1, row["minutes_played"])
    assert row["player_id"] not in [r["player_id"] for r in engine.recommend(132098, f, top_k=5000)["results"]]
    empty = engine.recommend(132098, SearchFilters("Attack", max_budget_eur=0))
    assert empty["status"] == "no_candidates" and not empty["results"]


@pytest.mark.parametrize("kind", ["nan", "infinity", "duplicate", "empty", "wrong_type"])
def test_invalid_catalogue(data, kind):
    bad = data.copy()
    if kind == "nan":
        bad.loc[0, "goals_per90"] = np.nan
    elif kind == "infinity":
        bad.loc[0, "goals_per90"] = np.inf
    elif kind == "duplicate":
        bad = pd.concat([bad, bad.head(1)], ignore_index=True)
    elif kind == "empty":
        bad = bad.iloc[:0]
    else:
        bad = None
    with pytest.raises(ValueError):
        WeightedCosineRecommender(bad)


@pytest.mark.parametrize("query,filters,k", [
    (132098, None, 5), (True, SearchFilters("Attack"), 5),
    (-1, SearchFilters("Attack"), 5), (132098, SearchFilters("Goalkeeper"), 5),
    (132098, SearchFilters("Attack"), 0), (132098, SearchFilters("Attack"), np.nan),
    (132098, SearchFilters("Attack"), True),
])
def test_invalid_query(engine, query, filters, k):
    with pytest.raises(ValueError):
        engine.recommend(query, filters, top_k=k)


def test_weights_do_not_change_fit_or_include_held_out(data, fit_ids, engine, baseline):
    changed = data.copy(deep=True)
    mask = changed.player_id.isin(QUERY_IDS)
    changed.loc[mask, "age"] = 50
    changed.loc[mask, "minutes_played"] = 900
    changed.loc[mask, "sub_position"] = "UNSEEN_TEST_CATEGORY"
    for target, totals in [
        ("goals_per90", changed.goals), ("assists_per90", changed.assists),
        ("goal_contributions_per90", changed.goals + changed.assists),
    ]:
        changed.loc[mask, target] = totals.loc[mask] * 90 / changed.loc[mask, "minutes_played"]
    model = WeightedCosineRecommender(changed, fit_player_ids=fit_ids)
    for position, audit in engine.describe()["positions"].items():
        for key in ("scaler_mean", "scaler_scale", "categories", "fit_ids_sha256", "fit_count"):
            assert audit[key] == baseline.describe()["positions"][position][key]
            assert audit[key] == model.describe()["positions"][position][key]


def test_no_price_or_reliability_skill_and_no_goalkeeper_goals(data, fit_ids, engine):
    changed = data.copy(deep=True)
    changed["market_value_in_eur"] *= 2
    for key in ("market_value_m", "log1p_market_value_m", "minutes_reliability",
                "goals_per90_position_percentile", "assists_per90_position_percentile",
                "goal_contributions_per90_position_percentile", "height_in_cm"):
        changed[key] = 0.0
    mask = changed.position.isin(["Defender", "Goalkeeper"])
    changed.loc[mask, "goals"] += 10
    changed.loc[mask, "assists"] += 5
    changed.loc[mask, "goals_per90"] = changed.loc[mask, "goals"] * 90 / changed.loc[mask, "minutes_played"]
    changed.loc[mask, "assists_per90"] = changed.loc[mask, "assists"] * 90 / changed.loc[mask, "minutes_played"]
    changed.loc[mask, "goal_contributions_per90"] = (
        changed.loc[mask, "goals"] + changed.loc[mask, "assists"]) * 90 / changed.loc[mask, "minutes_played"]
    model = WeightedCosineRecommender(changed, fit_player_ids=fit_ids)
    for _, query, filters in SCENARIOS[:4]:
        filters = SearchFilters(filters.position)
        response = model.recommend(query, filters)
        assert signature(response) == signature(engine.recommend(query, filters))
        if filters.position in ("Defender", "Goalkeeper"):
            assert response["similarity_scope"] == "context_profile_only"
            assert all("goals_per90" not in r["evidence"] for r in response["results"])


def metric_response(scores):
    # Abstract metric identifiers, not fabricated football observations.
    return {"results": [{"player_id": i, "similarity_score": score} for i, score in scores]}


def test_stability_metric_definitions_and_undefined_cases():
    left = metric_response([(1, .9), (2, .5), (3, .1)])
    right = metric_response([(3, .9), (2, .5), (1, .1)])
    metric = stability_metrics(left, right, k=2)
    assert metric["overlap_at_k"] == .5
    assert metric["spearman_full_common"] == pytest.approx(-1)
    empty = stability_metrics(left, metric_response([]))
    assert empty["overlap_at_k"] is None and empty["spearman_full_common"] is None
    constant = stability_metrics(left, metric_response([(1, .5), (2, .5), (3, .5)]))
    assert constant["spearman_full_common"] is None
    assert constant["spearman_reason"] == "constant_score_ranks"
    short = stability_metrics(metric_response([(1, .5)]), metric_response([(1, .5)]), k=5)
    assert short["overlap_at_k"] == .2  # Denominator is requested K, not actual count.
    assert short["spearman_full_common"] is None


def test_score_ties_use_midrank_not_id_order():
    left = metric_response([(1, .9), (2, .9), (3, .1)])
    right = metric_response([(2, .9), (1, .9), (3, .1)])
    assert stability_metrics(left, right)["spearman_full_common"] == pytest.approx(1)


def test_runner_refuses_overwriting_existing_output(tmp_path):
    output = tmp_path / "evaluation.json"
    output.write_text("previous run", encoding="utf-8")
    with pytest.raises(FileExistsError):
        run(tmp_path)
    assert output.read_text(encoding="utf-8") == "previous run"

