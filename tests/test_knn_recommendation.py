"""Real-snapshot KNN parity/robustness; mathematical fixtures are not player data."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, SearchFilters
from src.recommendation.evaluation import check_response, signature
from src.recommendation.knn import KNNRecommender, cosine_neighbors
from src.recommendation.run_day5 import SCENARIOS
from src.recommendation.run_day7 import compare_results, run, summarize_timings
from src.recommendation.weighted import WeightedCosineRecommender, default_weights, experiment_weights

QUERY_IDS = {query for _, query, _ in SCENARIOS}


@pytest.fixture(scope="module")
def data():
    return pd.read_csv(FEATURE_FILE)


@pytest.fixture(scope="module")
def fit_ids(data):
    return data.loc[~data.player_id.isin(QUERY_IDS), "player_id"].tolist()


@pytest.fixture(scope="module", params=[False, True], ids=["day5", "day6"])
def pair(request, data, fit_ids):
    weights = default_weights() if request.param else None
    direct = (CosineRecommender(data, fit_player_ids=fit_ids) if weights is None else
              WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=weights))
    knn = KNNRecommender(data, fit_player_ids=fit_ids, weights=weights)
    reverse = KNNRecommender(data.iloc[::-1], fit_player_ids=fit_ids[::-1], weights=weights)
    return direct, knn, reverse


@pytest.mark.parametrize("name,query,filters", SCENARIOS)
def test_full_ranking_and_distance_parity(pair, name, query, filters):
    direct, knn, reverse = pair
    expected = direct.recommend(query, filters, top_k=10000)
    actual = knn.recommend(query, filters, top_k=10000)
    check_response(actual, query, filters)
    assert compare_results(expected, actual)["parity_passed"]
    assert signature(actual) == signature(reverse.recommend(query, filters, top_k=10000))
    assert signature(actual) == signature(knn.recommend(query, filters, top_k=10000))
    for left, right in zip(expected["results"], actual["results"]):
        assert right["cosine_distance"] == pytest.approx(1 - left["similarity_score"], abs=1e-11)
        assert right["evidence"] == left["evidence"]
        for key in ("name", "club", "age", "minutes_played", "market_value_in_eur", "similarity_scope"):
            assert right[key] == left[key]
        assert 0 <= right["cosine_distance"] <= 2


@pytest.mark.parametrize("k", [1, 3, 5, 50, 10000])
def test_top_k_prefix_and_large_k(pair, k):
    direct, knn, _ = pair
    _, query, filters = SCENARIOS[0]
    full = knn.recommend(query, filters, top_k=10000)
    response = knn.recommend(query, filters, top_k=k)
    assert signature(response) == signature(full)[:k]
    assert len(response["results"]) == min(k, full["eligible_count"] - full["excluded_zero_vectors"])
    assert compare_results(direct.recommend(query, filters, top_k=k), response)["parity_passed"]


def test_knn_is_called_on_filtered_pool_and_all_neighbors(pair, monkeypatch):
    from sklearn.neighbors import NearestNeighbors
    _, knn, _ = pair
    calls = []
    original = NearestNeighbors.kneighbors

    def spy(self, X=None, n_neighbors=None, return_distance=True):
        calls.append((self.metric, self.algorithm, self.n_jobs, self.n_samples_fit_, n_neighbors))
        return original(self, X, n_neighbors, return_distance)
    monkeypatch.setattr(NearestNeighbors, "kneighbors", spy)
    _, query, filters = SCENARIOS[0]
    response = knn.recommend(query, filters, top_k=3)
    n = response["eligible_count"] - response["excluded_zero_vectors"]
    assert calls == [("cosine", "brute", 1, n, n)]


def test_fit_unchanged_by_filters_and_reference_equal(pair):
    direct, knn, _ = pair
    before = deepcopy(knn.describe())
    assert before["representation"] == direct.describe()
    for _, query, filters in SCENARIOS:
        knn.recommend(query, filters)
    assert knn.describe() == before


def test_ties_across_k_boundary_use_player_id(data, fit_ids):
    weights = default_weights()
    weights["Goalkeeper"] = {"age": 0, "minutes_played": 0, "foot": 1}
    direct = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=weights)
    knn = KNNRecommender(data.iloc[::-1], fit_player_ids=fit_ids[::-1], weights=weights)
    _, query, filters = SCENARIOS[3]
    full = direct.recommend(query, filters, top_k=10000)
    assert len(full["results"]) > 5
    assert sum(r["similarity_score"] == full["results"][0]["similarity_score"] for r in full["results"]) > 5
    top = knn.recommend(query, filters, top_k=3)
    assert signature(top) == signature(full)[:3]
    assert [r["player_id"] for r in top["results"]] == sorted(r["player_id"] for r in top["results"])


def test_zero_query_and_zero_candidates(data):
    small = data.loc[data.position.eq("Attack")].head(3).copy()
    small["sub_position"] = pd.NA
    ids = small.player_id.tolist()
    model = KNNRecommender(small, fit_player_ids=[ids[0]])
    zero = model.recommend(ids[0], SearchFilters("Attack"))
    assert zero["status"] == "zero_reference_vector" and not zero["results"]
    nonzero = model.recommend(ids[1], SearchFilters("Attack"))
    assert nonzero["excluded_zero_vectors"] >= 1
    assert ids[0] not in [r["player_id"] for r in nonzero["results"]]


@pytest.mark.parametrize("matrix,query", [
    ([[1, 0]], [0, 0]), ([[0, 0]], [1, 0]),
    ([[np.nan, 1]], [1, 0]), ([[1, 0]], [np.inf, 1]),
    ([[1, 0]], [1]), ([1, 0], [1, 0]),
])
def test_invalid_neighbor_vectors(matrix, query):
    with pytest.raises(ValueError):
        cosine_neighbors(matrix, query)


def test_distance_math_and_empty_matrix():
    # Abstract vector arithmetic only: no fabricated football observations.
    matrix = np.array([[1., 0.], [0., 1.], [-1., 0.]])
    distances, indices = cosine_neighbors(matrix, np.array([1., 0.]))
    assert dict(zip(indices, distances)) == pytest.approx({0: 0, 1: 1, 2: 2})
    d, i = cosine_neighbors(np.empty((0, 2)), np.array([1., 0.]))
    assert not len(d) and not len(i)


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
        KNNRecommender(bad)


@pytest.mark.parametrize("query,filters,k", [
    (132098, None, 5), (True, SearchFilters("Attack"), 5),
    (-1, SearchFilters("Attack"), 5), (132098, SearchFilters("Goalkeeper"), 5),
    (132098, SearchFilters("Attack"), 0), (132098, SearchFilters("Attack"), 1.5),
    (132098, SearchFilters("Attack"), np.nan), (132098, SearchFilters("Attack"), True),
])
def test_invalid_request(pair, query, filters, k):
    with pytest.raises(ValueError):
        pair[1].recommend(query, filters, top_k=k)


def test_filter_boundaries_no_relaxation(pair):
    _, knn, _ = pair
    row = knn.recommend(132098, SearchFilters("Attack"))["results"][0]
    f = SearchFilters("Attack", row["age"], row["age"], row["market_value_in_eur"], row["minutes_played"])
    assert row["player_id"] in [r["player_id"] for r in knn.recommend(132098, f, top_k=10000)["results"]]
    f = SearchFilters("Attack", row["age"], row["age"], row["market_value_in_eur"] - 1, row["minutes_played"])
    assert row["player_id"] not in [r["player_id"] for r in knn.recommend(132098, f, top_k=10000)["results"]]
    assert knn.recommend(132098, SearchFilters("Attack", max_budget_eur=0))["status"] == "no_candidates"


@pytest.mark.parametrize("config", list(experiment_weights()))
def test_day6_alternative_weights_preserved(data, fit_ids, config):
    weights = experiment_weights()[config]
    direct = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=weights)
    knn = KNNRecommender(data, fit_player_ids=fit_ids, weights=weights)
    for _, query, filters in SCENARIOS:
        assert compare_results(direct.recommend(query, filters), knn.recommend(query, filters))["parity_passed"]


def test_query_mutations_do_not_fit_scaler_or_categories(data, fit_ids):
    before = KNNRecommender(data, fit_player_ids=fit_ids).describe()["representation"]["positions"]
    changed = data.copy(deep=True)
    mask = changed.player_id.isin(QUERY_IDS)
    changed.loc[mask, "age"] = 50
    changed.loc[mask, "sub_position"] = "UNSEEN_TEST_CATEGORY"
    after = KNNRecommender(changed, fit_player_ids=fit_ids).describe()["representation"]["positions"]
    for position in before:
        for key in ("scaler_mean", "scaler_scale", "categories", "fit_count", "fit_ids_sha256"):
            assert before[position][key] == after[position][key]


def test_market_value_unused_and_goalkeeper_context_only(data, fit_ids):
    before = data.copy(deep=True)
    original = KNNRecommender(data, fit_player_ids=fit_ids)
    changed = data.copy(deep=True)
    changed["market_value_in_eur"] *= 2
    changed["minutes_reliability"] = 0.
    mask = changed.position.isin(["Defender", "Goalkeeper"])
    changed.loc[mask, "goals"] += 10
    changed.loc[mask, "assists"] += 5
    for target, values in (("goals_per90", changed.goals), ("assists_per90", changed.assists),
                           ("goal_contributions_per90", changed.goals + changed.assists)):
        changed.loc[mask, target] = values.loc[mask] * 90 / changed.loc[mask, "minutes_played"]
    model = KNNRecommender(changed, fit_player_ids=fit_ids)
    for _, query, filters in SCENARIOS[:4]:
        f = SearchFilters(filters.position)
        result = model.recommend(query, f)
        assert signature(result) == signature(original.recommend(query, f))
        if f.position in ("Defender", "Goalkeeper"):
            assert result["similarity_scope"] == "context_profile_only"
            assert all("goals_per90" not in r["evidence"] for r in result["results"])
    pd.testing.assert_frame_equal(data, before)


def test_latency_summary_percentile_math():
    # Known timing numbers test aggregation only; never exported as benchmark evidence.
    frame = pd.DataFrame({"representation": ["test"] * 5, "scenario": ["test"] * 5,
                          "method": ["test"] * 5, "elapsed_ms": [1., 2., 3., 4., 100.]})
    row = summarize_timings(frame).iloc[0]
    assert row.median_ms == 3.
    assert row.p95_ms == pytest.approx(80.8)
    assert row.measured_runs == 5


@pytest.mark.parametrize("warmup,repeats", [(0, 50), (1, 1), (True, 50), (5, np.nan)])
def test_benchmark_invalid_parameters(tmp_path, warmup, repeats):
    with pytest.raises(ValueError):
        run(tmp_path, warmup=warmup, repeats=repeats)


def test_runner_refuses_overwrite(tmp_path):
    prior = tmp_path / "evaluation.json"
    prior.write_text("keep", encoding="utf-8")
    with pytest.raises(FileExistsError):
        run(tmp_path)
    assert prior.read_text(encoding="utf-8") == "keep"

