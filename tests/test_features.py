"""Tests use real candidate rows; fault injection stays in memory, never in data files."""

import numpy as np
import pandas as pd
import pytest

from src.features.build_features import (
    FEATURES, INPUT, PERCENTILES, PER90, build_features, validate_candidates,
    validate_features,
)


@pytest.fixture(scope="module")
def candidates():
    return pd.read_csv(INPUT)


@pytest.fixture(scope="module")
def features(candidates):
    return build_features(candidates)


def test_real_snapshot_and_preservation(candidates, features):
    before = candidates.copy(deep=True)
    result = build_features(candidates)
    pd.testing.assert_frame_equal(before, candidates)
    assert result.shape == (4112, 28)
    assert len(FEATURES) == 8
    assert len(set(result) - set(candidates)) == 7
    pd.testing.assert_series_equal(result.player_id, candidates.player_id)
    original = [col for col in candidates if col != "goal_contributions_per90"]
    pd.testing.assert_frame_equal(features[original], candidates[original])
    assert features.foot.isna().sum() == 24
    assert features.height_in_cm.isna().sum() == 23
    assert features.loc[features.player_id == 743556, "height_in_cm"].item() == 19


def test_feature_identities_and_bounds(features):
    assert (features.goal_contributions == features.goals + features.assists).all()
    np.testing.assert_allclose(features.goal_contributions_per90,
                               features.goals_per90 + features.assists_per90)
    np.testing.assert_allclose(np.expm1(features.log1p_market_value_m) * 1_000_000,
                               features.market_value_in_eur)
    assert features.minutes_reliability.between(1 / 3, 1).all()
    assert (features.loc[features.minutes_played >= 2700, "minutes_reliability"] == 1).all()
    np.testing.assert_allclose(features.loc[features.minutes_played < 2700, "minutes_reliability"] * 2700,
                               features.loc[features.minutes_played < 2700, "minutes_played"])
    assert np.isfinite(features[list(FEATURES)]).all().all()


@pytest.mark.parametrize("source,target", list(zip(PER90, PERCENTILES)))
def test_percentile_ties_and_position_reference(features, source, target):
    # Independent rank oracle: count strictly lower and equal real observations.
    for _, group in features.groupby("position"):
        for value in (group[source].min(), group[source].median(), group[source].max()):
            selected = group.loc[group[source] == value, target]
            if selected.empty:
                continue
            less = (group[source] < value).sum()
            equal = (group[source] == value).sum()
            expected = 100 * (less + (equal + 1) / 2) / len(group)
            np.testing.assert_allclose(selected, expected)
        assert group[target].between(0, 100).all()
        assert group.sort_values(source)[target].is_monotonic_increasing


def test_row_order_does_not_change_percentiles(candidates, features):
    reversed_result = build_features(candidates.iloc[::-1]).sort_values("player_id").reset_index(drop=True)
    pd.testing.assert_frame_equal(reversed_result, features.sort_values("player_id").reset_index(drop=True))


def test_csv_round_trip(features, tmp_path):
    path = tmp_path / "real_features.csv"
    features.to_csv(path, index=False, encoding="utf-8-sig")
    loaded = pd.read_csv(path)
    validate_features(loaded)
    pd.testing.assert_frame_equal(loaded, features, check_exact=False, rtol=1e-9, atol=1e-12)


@pytest.mark.parametrize("column,value,message", [
    ("goals", np.nan, "Missing required values"),
    ("assists_per90", np.inf, "Infinity"),
    ("minutes_played", 0, "minutes"),
    ("goals", -1, "nonnegative integer"),
    ("assists", 0.5, "nonnegative integer"),
    ("market_value_in_eur", 0, "Market value"),
    ("position", " ", "Missing required values"),
    ("position", "Unknown", "Unknown position"),
    ("valuation_date", "2026-06-13", "cutoff window"),
    ("valuation_date", "2025-01-01", "cutoff window"),
    ("valuation_age_days", 999, "valuation_age_days"),
    ("goals_per90", 999.0, "Inconsistent per90"),
    ("goal_contributions_per90", 999.0, "Inconsistent per90"),
])
def test_reject_invalid_inputs_in_memory(candidates, column, value, message):
    broken = candidates.head(4).copy()
    # Widen integer columns for deliberately malformed numeric values only.
    if isinstance(value, float):
        broken[column] = broken[column].astype(float)
    broken.loc[broken.index[0], column] = value
    with pytest.raises(ValueError, match=message):
        build_features(broken)


def test_reject_duplicate_ids(candidates):
    with pytest.raises(ValueError, match="Duplicate player IDs"):
        build_features(pd.concat([candidates.head(1), candidates.head(1)], ignore_index=True))


def test_reject_missing_column_and_empty(candidates):
    with pytest.raises(ValueError, match="Missing required columns"):
        build_features(candidates.drop(columns="goals"))
    with pytest.raises(ValueError, match="empty"):
        validate_candidates(candidates.iloc[:0])


def test_reject_corrupted_output(features):
    broken = features.copy()
    broken.loc[0, PERCENTILES[0]] = 101
    with pytest.raises(ValueError, match="Percentile outside"):
        validate_features(broken)
    broken = features.copy()
    broken.loc[0, PERCENTILES[0]] = 50.12345
    with pytest.raises(ValueError, match="Inconsistent percentile"):
        validate_features(broken)
    broken = features.copy()
    broken.loc[0, "log1p_market_value_m"] = 999
    with pytest.raises(ValueError, match="Inconsistent feature"):
        validate_features(broken)
