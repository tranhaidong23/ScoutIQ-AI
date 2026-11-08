"""Real-data retrieval tests. Fault injections affect in-memory copies only."""

import copy

import numpy as np
import pandas as pd
import pytest

from src.recommendation.baseline import (
    CosineRecommender, FEATURE_FILE, POLICIES, SearchFilters, _unit_vectors,
)
from src.recommendation.run_day5 import SCENARIOS

QUERY_IDS = {player_id for _, player_id, _ in SCENARIOS}


@pytest.fixture(scope="module")
def data():
    return pd.read_csv(FEATURE_FILE)


@pytest.fixture(scope="module")
def fit_ids(data):
    return data.loc[~data.player_id.isin(QUERY_IDS), "player_id"].tolist()


@pytest.fixture(scope="module")
def engine(data, fit_ids):
    return CosineRecommender(data, fit_player_ids=fit_ids)


def signature(response):
    return [(r["player_id"], r["similarity_score"]) for r in response["results"]]


@pytest.mark.parametrize("name,query,filters", SCENARIOS)
def test_scenarios_filters_order_explanations(engine, data, name, query, filters):
    response = engine.recommend(query, filters)
    rows = response["results"]
    assert len(rows) == (0 if name == "empty_budget" else 5)
    assert rows == sorted(rows, key=lambda r: (-r["similarity_score"], r["player_id"]))
    assert len({r["player_id"] for r in rows}) == len(rows)
    source = data.set_index("player_id")
    for row in rows:
        assert row["player_id"] != query
        assert row["position"] == filters.position
        assert filters.min_age <= row["age"] <= filters.max_age
        assert row["minutes_played"] >= filters.min_minutes
        assert row["market_value_in_eur"] <= filters.max_budget_eur
        assert -1 <= row["similarity_score"] <= 1 and np.isfinite(row["similarity_score"])
        assert abs(sum(row["cosine_components"].values()) - row["similarity_score"]) < 1e-10
        for col, evidence in row["evidence"].items():
            assert evidence["candidate"] == source.loc[row["player_id"], col]
            assert evidence["reference"] == source.loc[query, col]
        assert row["name"] == source.loc[row["player_id"], "name"]
        assert row["explanation"] and response["warnings"]


def test_cosine_against_independent_scalar_calculation(engine, data, fit_ids):
    query = 132098
    response = engine.recommend(query, SearchFilters("Attack"))
    reference = data.loc[data.player_id.isin(fit_ids) & data.position.eq("Attack")]
    columns = ["goals_per90", "assists_per90"]
    mean = reference[columns].mean().to_numpy()
    scale = reference[columns].std(ddof=0).to_numpy()
    roles = sorted(reference.sub_position.unique())
    source = data.set_index("player_id")

    def vector(player_id):
        row = source.loc[player_id]
        return np.r_[(row[columns].to_numpy(dtype=float) - mean) / scale,
                     [float(row.sub_position == role) for role in roles]]

    q = vector(query)
    for result in response["results"]:
        c = vector(result["player_id"])
        expected = sum(float(a * b) for a, b in zip(q, c)) / (np.linalg.norm(q) * np.linalg.norm(c))
        assert result["similarity_score"] == pytest.approx(expected, abs=1e-11)


def test_all_candidates_ranked_before_top_k(engine):
    filters = SearchFilters("Attack", 18, 29, 30_000_000, 1800)
    full = engine.recommend(132098, filters, top_k=5000)
    top = engine.recommend(132098, filters, top_k=5)
    assert signature(top) == signature(full)[:5]
    assert len(full["results"]) == full["eligible_count"] - full["excluded_zero_vectors"]


def test_inclusive_filter_boundaries(engine):
    row = engine.recommend(132098, SearchFilters("Attack"))["results"][0]
    filters = SearchFilters("Attack", row["age"], row["age"], row["market_value_in_eur"], row["minutes_played"])
    assert row["player_id"] in {r["player_id"] for r in engine.recommend(132098, filters, top_k=5000)["results"]}
    tighter = SearchFilters("Attack", row["age"], row["age"], row["market_value_in_eur"] - 1, row["minutes_played"])
    assert row["player_id"] not in {r["player_id"] for r in engine.recommend(132098, tighter, top_k=5000)["results"]}


def test_shortlist_does_not_invent_players(data):
    two = data.loc[data.position.eq("Attack")].head(2)
    model = CosineRecommender(two)
    result = model.recommend(int(two.player_id.iloc[0]), SearchFilters("Attack"), top_k=5)
    assert len(result["results"]) == 1 and result["eligible_count"] == 1


def test_money_and_unused_features_do_not_change_similarity(data, fit_ids, engine):
    changed = data.copy(deep=True)
    changed["market_value_in_eur"] *= 2
    for col in ("market_value_m", "log1p_market_value_m", "minutes_reliability",
                "goals_per90_position_percentile", "assists_per90_position_percentile",
                "goal_contributions_per90_position_percentile", "height_in_cm"):
        changed[col] = 0.0
    changed["current_club_name"] = pd.NA
    changed["club_name_verified"] = pd.NA
    model = CosineRecommender(changed, fit_player_ids=fit_ids)
    for _, query, filters in SCENARIOS[:4]:
        no_budget = SearchFilters(filters.position)
        actual = model.recommend(query, no_budget)
        assert signature(actual) == signature(engine.recommend(query, no_budget))
        assert all(row["club"] is None for row in actual["results"])


def test_goalkeeper_and_defender_do_not_use_goals(data, fit_ids, engine):
    changed = data.copy(deep=True)
    mask = changed.position.isin(["Goalkeeper", "Defender"])
    changed.loc[mask, "goals"] += 10
    changed.loc[mask, "assists"] += 5
    changed.loc[mask, "goals_per90"] = changed.loc[mask, "goals"] * 90 / changed.loc[mask, "minutes_played"]
    changed.loc[mask, "assists_per90"] = changed.loc[mask, "assists"] * 90 / changed.loc[mask, "minutes_played"]
    changed.loc[mask, "goal_contributions_per90"] = (changed.loc[mask, "goals"] + changed.loc[mask, "assists"]) * 90 / changed.loc[mask, "minutes_played"]
    model = CosineRecommender(changed, fit_player_ids=fit_ids)
    for _, query, filters in SCENARIOS[2:4]:
        result = model.recommend(query, filters)
        assert signature(result) == signature(engine.recommend(query, filters))
        assert result["similarity_scope"] == "context_profile_only"
        assert not any("goals" in name or "assists" in name for name in model.describe()["positions"][filters.position]["encoded_features"])


def test_scaler_reference_excludes_queries_and_is_not_refitted(engine, data, fit_ids):
    before = copy.deepcopy(engine.describe())
    assert not QUERY_IDS.intersection(fit_ids)
    for position, audit in before["positions"].items():
        fit = data.loc[data.player_id.isin(fit_ids) & data.position.eq(position)]
        np.testing.assert_allclose(audit["scaler_mean"], fit[audit["numeric"]].mean())
        np.testing.assert_allclose(audit["scaler_scale"], fit[audit["numeric"]].std(ddof=0))
    for _, query, filters in SCENARIOS:
        engine.recommend(query, filters)
    assert before == engine.describe()


def test_held_out_data_cannot_change_fit(data, fit_ids, engine):
    changed = data.copy(deep=True)
    mask = changed.player_id.isin(QUERY_IDS)
    changed.loc[mask, "age"] = 50
    changed.loc[mask, "minutes_played"] = 900
    changed.loc[mask, "sub_position"] = "UNSEEN_TEST_CATEGORY"
    changed.loc[mask, "goals_per90"] = changed.loc[mask, "goals"] * 90 / changed.loc[mask, "minutes_played"]
    changed.loc[mask, "assists_per90"] = changed.loc[mask, "assists"] * 90 / changed.loc[mask, "minutes_played"]
    changed.loc[mask, "goal_contributions_per90"] = (changed.loc[mask, "goals"] + changed.loc[mask, "assists"]) * 90 / changed.loc[mask, "minutes_played"]
    after = CosineRecommender(changed, fit_player_ids=fit_ids).describe()
    for position, prior in engine.describe()["positions"].items():
        for key in ("scaler_mean", "scaler_scale", "categories", "fit_ids_sha256", "fit_count"):
            assert after["positions"][position][key] == prior[key]


def test_missing_categories_and_zero_vectors(data):
    single = data.loc[data.position.eq("Attack")].head(1).copy()
    single["sub_position"] = pd.NA
    model = CosineRecommender(single)
    result = model.recommend(int(single.player_id.iloc[0]), SearchFilters("Attack"))
    assert result["status"] == "zero_reference_vector" and not result["results"]
    unit, valid = _unit_vectors(np.zeros((2, 3)))
    assert not valid.any() and np.isfinite(unit).all()


def test_order_and_input_preserved(data, engine, fit_ids):
    before = data.copy(deep=True)
    reversed_engine = CosineRecommender(data.iloc[::-1], fit_player_ids=fit_ids)
    for _, query, filters in SCENARIOS:
        assert signature(reversed_engine.recommend(query, filters)) == signature(engine.recommend(query, filters))
    pd.testing.assert_frame_equal(data, before)


@pytest.mark.parametrize("kwargs", [
    {"position": "Invalid"}, {"min_age": 30, "max_age": 20}, {"min_age": -1},
    {"max_age": 101}, {"min_minutes": -1}, {"max_budget_eur": -1},
    {"max_budget_eur": float("inf")}, {"min_age": float("nan")},
    {"max_budget_eur": "EUR 10M"}, {"min_minutes": True},
])
def test_invalid_filters(kwargs):
    with pytest.raises(ValueError):
        SearchFilters(**{"position": "Attack", **kwargs})


@pytest.mark.parametrize("top_k", [0, -1, 1.5, True])
def test_invalid_top_k(engine, top_k):
    with pytest.raises(ValueError, match="top_k"):
        engine.recommend(132098, SearchFilters("Attack"), top_k=top_k)


def test_invalid_reference_and_fit_ids(engine, data):
    with pytest.raises(ValueError, match="Unknown reference"):
        engine.recommend(-1, SearchFilters("Attack"))
    with pytest.raises(ValueError, match="position must match"):
        engine.recommend(132098, SearchFilters("Goalkeeper"))
    for ids in ([], [132098, 132098], [-1]):
        with pytest.raises(ValueError, match="Fit IDs"):
            CosineRecommender(data, fit_player_ids=ids)


@pytest.mark.parametrize("kind", ["duplicate", "future", "missing", "infinity"])
def test_invalid_catalogue(data, kind):
    bad = data.copy(deep=True)
    if kind == "duplicate":
        bad = pd.concat([bad, bad.head(1)], ignore_index=True)
    elif kind == "future":
        bad.loc[0, "valuation_date"] = "2026-06-13"
    elif kind == "missing":
        bad.loc[0, "goals_per90"] = np.nan
    elif kind == "infinity":
        bad.loc[0, "goals_per90"] = np.inf
    with pytest.raises(ValueError):
        CosineRecommender(bad)
