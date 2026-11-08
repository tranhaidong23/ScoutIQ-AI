"""Real snapshot contract tests; invalid/missing variants only live in RAM."""

from copy import deepcopy
from dataclasses import replace
import json

import numpy as np
import pandas as pd
import pytest

from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, SearchFilters
from src.recommendation.constraints import AdvancedRecommender, SearchConstraints, filter_candidates
from src.recommendation.evaluation import signature
from src.recommendation.knn import KNNRecommender
from src.recommendation.run_day5 import SCENARIOS as LEGACY
from src.recommendation.run_day8 import SCENARIOS, independent_eligible_ids, make_engines, run
from src.recommendation.weighted import WeightedCosineRecommender, default_weights


@pytest.fixture(scope="module")
def data():
    return pd.read_csv(FEATURE_FILE)


@pytest.fixture(scope="module")
def fit_ids(data):
    return data.loc[~data.player_id.isin({q for _, q, _ in SCENARIOS}), "player_id"].tolist()


@pytest.fixture(scope="module", params=["cosine", "weighted", "knn_cosine", "knn_weighted"])
def pair(request, data, fit_ids):
    if request.param == "cosine":
        engine = CosineRecommender(data, fit_player_ids=fit_ids)
    elif request.param == "weighted":
        engine = WeightedCosineRecommender(data, fit_player_ids=fit_ids)
    else:
        engine = KNNRecommender(data, fit_player_ids=fit_ids,
                               weights=default_weights() if request.param == "knn_weighted" else None)
    return engine, AdvancedRecommender(engine)


@pytest.mark.parametrize("name,query,filters", LEGACY)
def test_legacy_full_ranking_unchanged(pair, name, query, filters):
    engine, advanced = pair
    before = deepcopy(engine.describe())
    expected = engine.recommend(query, filters, top_k=10000)
    result = advanced.recommend(query, SearchConstraints(filters), top_k=10000)
    assert signature(result) == signature(expected)
    assert result["status"] == expected["status"]
    assert result["eligible_count"] == expected["eligible_count"]
    assert engine.describe() == before


@pytest.mark.parametrize("name,query,constraints", SCENARIOS)
def test_scenarios_independent_oracle_scores_topk_and_repeat(pair, data, name, query, constraints):
    engine, advanced = pair
    before = deepcopy(engine.describe())
    full = advanced.recommend(query, constraints, top_k=10000)
    top = advanced.recommend(query, constraints, top_k=5)
    expected_ids = independent_eligible_ids(data, query, constraints)
    # Independent oracle: take full old ranking then intersect hard constraints.
    baseline = engine.recommend(query, constraints.filters, top_k=10000)
    old = {r["player_id"]: r for r in baseline["results"] if r["player_id"] in expected_ids}
    assert {r["player_id"] for r in full["results"]} == set(old)
    assert full["eligible_count"] == len(expected_ids)
    for row in full["results"]:
        assert row["similarity_score"] == old[row["player_id"]]["similarity_score"]
        assert abs(sum(row["cosine_components"].values()) - row["similarity_score"]) < 1e-10
        assert row["constraint_evidence"]["current_club_id"] not in constraints.excluded_club_ids
        assert "market value EUR=" in row["explanation"]
    assert signature(top) == signature(full)[:5]
    assert signature(top) == signature(advanced.recommend(query, constraints))
    stages = full["filter_audit"]["stages"]
    assert all(x["before"] - x["removed"] == x["after"] for x in stages)
    assert all(a["after"] == b["before"] for a, b in zip(stages, stages[1:]))
    assert stages[-1]["after"] == len(expected_ids)
    assert engine.describe() == before
    if name == "no_results":
        assert full["status"] == "no_candidates" and not top["results"]


@pytest.mark.parametrize("k", [1, 3, 10000])
def test_k_boundary_and_query_need_not_meet_constraints(pair, k):
    _, advanced = pair
    _, query, constraints = SCENARIOS[0]  # Kane older/more expensive than candidates.
    full = advanced.recommend(query, constraints, top_k=10000)
    assert signature(advanced.recommend(query, constraints, top_k=k)) == signature(full)[:k]
    assert all(r["player_id"] != query for r in full["results"])


@pytest.mark.parametrize("field", ["min_goals_per90", "min_assists_per90"])
@pytest.mark.parametrize("value", [-1, np.nan, np.inf, -np.inf, True, np.bool_(True), "0.3", []])
def test_invalid_per90(field, value):
    with pytest.raises(ValueError):
        SearchConstraints(SearchFilters("Attack"), **{field: value})


@pytest.mark.parametrize("payload", [
    {}, {"position": "invalid"}, {"position": []},
    {"position": "Attack", "min_age": 30, "max_age": 20},
    {"position": "Attack", "min_age": np.nan},
    {"position": "Attack", "max_age": np.inf},
    {"position": "Attack", "min_minutes": -1},
    {"position": "Attack", "min_minutes": True},
    {"position": "Attack", "max_budget_eur": -1},
    {"position": "Attack", "max_budget_eur": np.nan},
    {"position": "Attack", "budget_value": 5},
    {"position": "Attack", "budget_unit": "EUR"},
    {"position": "Attack", "budget_value": 5, "budget_unit": "USD"},
    {"position": "Attack", "budget_value": "5m", "budget_unit": "EUR"},
    {"position": "Attack", "budget_value": True, "budget_unit": "EUR"},
    {"position": "Attack", "budget_value": -1, "budget_unit": "EUR"},
    {"position": "Attack", "budget_value": np.inf, "budget_unit": "EUR"},
    {"position": "Attack", "budget_value": 1e308, "budget_unit": "EUR_million"},
    {"position": "Attack", "budget_value": 5, "budget_unit": "EUR", "max_budget_eur": 5},
    {"position": "Attack", "max_budget_m": 5},
    {"position": "Attack", "minimum_goal": .2},
    {"position": "Attack", "preferred_foot": "Left"},
    {"position": "Attack", "preferred_foot": []},
    {"position": "Attack", "foot_mode": "maybe"},
    {"position": "Attack", "foot_mode": "soft"},
    {"position": "Attack", "sub_positions": "Centre-Forward"},
    {"position": "Attack", "sub_positions": [""]},
    {"position": "Attack", "sub_positions": [" Left Winger"]},
    {"position": "Attack", "sub_positions": ["Left Winger", "Left Winger"]},
    {"position": "Attack", "excluded_club_ids": [True]},
    {"position": "Attack", "excluded_club_ids": [1.0]},
    {"position": "Attack", "excluded_club_ids": [0]},
    {"position": "Attack", "excluded_club_ids": [1, 1]},
    {"position": "Goalkeeper", "min_goals_per90": 0},
    {"position": "Goalkeeper", "min_assists_per90": .1},
])
def test_invalid_request_is_not_ignored(payload):
    with pytest.raises(ValueError):
        SearchConstraints.from_request(payload)


def test_explicit_eur_million_and_json_contract():
    request = {"position": "Attack", "budget_value": 5, "budget_unit": "EUR_million"}
    constraints = SearchConstraints.from_request(request)
    assert constraints.filters.max_budget_eur == 5_000_000
    assert request["budget_unit"] == "EUR_million"  # no request mutation
    assert SearchConstraints.from_request({"position": "Attack", "max_budget_eur": 5}).filters.max_budget_eur == 5
    numeric = replace(constraints, min_goals_per90=np.float32(.3), excluded_club_ids=(np.int64(27),))
    json.dumps(numeric.describe(), allow_nan=False)


@pytest.mark.parametrize("change", [dict(sub_positions=("Centre-Back",)),
                                    dict(sub_positions=("not_a_role",)),
                                    dict(excluded_club_ids=(999999999,))])
def test_unknown_snapshot_constraints_fail_even_for_empty_budget(pair, change):
    _, advanced = pair
    c = SearchConstraints(SearchFilters("Attack", max_budget_eur=0), **change)
    with pytest.raises(ValueError):
        advanced.recommend(132098, c)


def test_all_inclusive_boundaries_and_exact_foot(data):
    r = data.loc[(data.position == "Attack") & (data.player_id != 132098) & data.foot.notna()].iloc[0]
    c = SearchConstraints(SearchFilters("Attack", r.age, r.age, r.market_value_in_eur, r.minutes_played),
                          sub_positions=(r.sub_position,), min_goals_per90=r.goals_per90,
                          min_assists_per90=r.assists_per90, preferred_foot=r.foot)
    mask, _ = filter_candidates(data, 132098, c)
    assert r.player_id in set(data.loc[mask, "player_id"])
    assert set(data.loc[mask, "foot"]) == {r.foot}
    assert r.player_id not in independent_eligible_ids(data, 132098, replace(
        c, filters=replace(c.filters, max_budget_eur=np.nextafter(float(r.market_value_in_eur), -np.inf))))


@pytest.mark.parametrize("col", ["foot", "sub_position", "current_club_id", "goals_per90", "assists_per90"])
def test_missing_active_constraint_excludes_without_imputation(data, col):
    changed = data.copy(deep=True)
    r = changed.loc[(changed.position == "Attack") & changed.foot.notna() & (changed.player_id != 132098)].iloc[0]
    c = SearchConstraints(SearchFilters("Attack"), sub_positions=(r.sub_position,),
                          preferred_foot=r.foot, excluded_club_ids=(27,),
                          min_goals_per90=0, min_assists_per90=0)
    changed.loc[changed.player_id == r.player_id, col] = np.nan
    mask, _ = filter_candidates(changed, 132098, c)
    assert r.player_id not in set(changed.loc[mask, "player_id"])
    pd.testing.assert_frame_equal(data, pd.read_csv(FEATURE_FILE))


def test_soft_missing_retained_and_does_not_filter(data):
    base = SearchConstraints(SearchFilters("Attack"))
    a, _ = filter_candidates(data, 132098, base)
    b, _ = filter_candidates(data, 132098, replace(base, preferred_foot="left", foot_mode="soft"))
    assert a.equals(b)
    assert data.loc[b].foot.isna().any()


def test_hard_pool_is_applied_before_knn_ranking(data, fit_ids, monkeypatch):
    from sklearn.neighbors import NearestNeighbors
    calls = []
    original = NearestNeighbors.kneighbors
    def spy(self, X=None, n_neighbors=None, return_distance=True):
        calls.append((self.n_samples_fit_, n_neighbors))
        return original(self, X, n_neighbors, return_distance)
    monkeypatch.setattr(NearestNeighbors, "kneighbors", spy)
    _, q, c = SCENARIOS[1]
    engine = AdvancedRecommender(KNNRecommender(data, fit_player_ids=fit_ids))
    r = engine.recommend(q, c)
    n = r["eligible_count"] - r["excluded_zero_vectors"]
    assert n > 0 and calls == [(n, n)]


def test_soft_foot_ties_across_k_and_permutations(data, fit_ids):
    # Real Attack rows, role-only representation yields exact ties across feet.
    w = default_weights()
    w["Attack"] = {"goals_per90": 0, "assists_per90": 0, "sub_position": 1}
    c = SearchConstraints(SearchFilters("Attack"), sub_positions=("Centre-Forward",),
                          preferred_foot="left", foot_mode="soft")
    signatures = []
    for frame, ids in ((data, fit_ids), (data.iloc[::-1], fit_ids[::-1])):
        for model in (WeightedCosineRecommender(frame, fit_player_ids=ids, weights=w),
                      KNNRecommender(frame, fit_player_ids=ids, weights=w)):
            advanced = AdvancedRecommender(model)
            full = advanced.recommend(132098, c, top_k=10000)
            top = advanced.recommend(132098, c, top_k=5)
            assert len(full["results"]) > 5
            assert all(r["soft_preference_match"] for r in top["results"])
            assert len({r["similarity_score"] for r in full["results"]}) == 1
            assert signature(top) == signature(full)[:5]
            signatures.append(signature(top))
    assert all(s == signatures[0] for s in signatures)


@pytest.mark.parametrize("knn", [False, True])
def test_zero_query_and_zero_candidates(data, knn):
    small = data.loc[data.position.eq("Attack")].head(3).copy()
    small["sub_position"] = pd.NA
    ids = small.player_id.tolist()
    cls = KNNRecommender if knn else CosineRecommender
    engine = AdvancedRecommender(cls(small, fit_player_ids=[ids[0]]))
    c = SearchConstraints(SearchFilters("Attack"))
    assert engine.recommend(ids[0], c)["status"] == "zero_reference_vector"
    r = engine.recommend(ids[1], c, top_k=10000)
    assert r["excluded_zero_vectors"] >= 1
    assert ids[0] not in {x["player_id"] for x in r["results"]}
    # Internal full-ranking K must not generate a false user-facing shortage.
    top = engine.recommend(ids[1], c, top_k=1)
    assert len(top["results"]) == 1
    assert "Không đủ ứng viên hợp lệ để trả đủ K; không tự nới điều kiện." not in top["warnings"]


@pytest.mark.parametrize("query,k", [(True, 5), ("132098", 5), (-1, 5), (999999999, 5),
                                    (132098, 0), (132098, True), (132098, np.nan)])
def test_bad_query_and_k(pair, query, k):
    with pytest.raises(ValueError):
        pair[1].recommend(query, SCENARIOS[0][2], top_k=k)


def test_no_mutation_or_refit_even_after_failed_request(pair, data, monkeypatch):
    from sklearn.preprocessing import StandardScaler
    engine, wrapper = pair
    before = deepcopy(engine.describe())
    def forbidden(*args, **kwargs):
        raise AssertionError("Search must not fit a scaler")
    monkeypatch.setattr(StandardScaler, "fit", forbidden)
    with pytest.raises(ValueError):
        wrapper.recommend(132098, SearchConstraints(SearchFilters("Goalkeeper")))
    wrapper.recommend(SCENARIOS[0][1], SCENARIOS[0][2])
    assert engine.describe() == before
    pd.testing.assert_frame_equal(data, pd.read_csv(FEATURE_FILE))


def test_existing_output_refused(tmp_path):
    with pytest.raises(FileExistsError):
        run(tmp_path)
