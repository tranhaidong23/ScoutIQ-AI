"""SYNTHETIC edge fixtures and read-only checks of the real Day 12 snapshot."""

from copy import deepcopy
import json
from pathlib import Path

import pandas as pd
import pytest

from src.evaluation.integrity import (
    age_audit, age_band, age_values, correction_proposal, coverage_analysis,
    cutoff_date, exclusion_audit, feature_lineage,
)
from src.evaluation.run_day12 import run


@pytest.mark.parametrize("dob,cutoff,age", [
    ("1996-06-12", "2026-06-12", 30), ("1996-06-12 00:00:00", "2026-06-11", 29),
    ("1996-06-12T00:00:00.000", "2026-06-13", 30),
    ("2000-02-29", "2025-02-28", 24), ("2000-02-29", "2025-03-01", 25),
    ("2000-02-29", "2024-02-29", 24), ("2000-12-31", "2026-01-01", 25),
    ("2026-06-12", "2026-06-12", 0), ("1926-06-12", "2026-06-12", 100),
])
def test_calendar_birthdays_and_leap_day_policy(dob, cutoff, age):
    result = age_values(dob, cutoff)
    assert result["calendar_age"] == age
    assert result["dob_status"] == "valid"


@pytest.mark.parametrize("dob,status", [
    (None, "missing_dob"), (pd.NA, "missing_dob"), (float("nan"), "missing_dob"), (" ", "missing_dob"),
    ("12/06/1996", "invalid_dob_format"), ("1996-6-12", "invalid_dob_format"),
    ("1996-06-12T00:00:00Z", "invalid_dob_format"), ("1996-06-12 12:00:00", "invalid_dob_format"),
    ("1999-02-29", "invalid_dob_calendar"), ("2000-13-01", "invalid_dob_calendar"),
    (19960612, "invalid_dob_format"), ("NaT", "invalid_dob_format"),
    ("2026-06-13", "future_dob"), ("1900-01-01", "age_outside_0_100_policy"),
])
def test_dob_quality_categories(dob, status):
    assert age_values(dob)["dob_status"] == status


@pytest.mark.parametrize("cutoff", [None, "12/06/2026", "2026-02-30", "2026-6-12", "2026-06-12T00:00:00", 20260612])
def test_cutoff_is_explicit_calendar_date(cutoff):
    with pytest.raises(ValueError): cutoff_date(cutoff)
    with pytest.raises(ValueError): age_values("2000-01-01", cutoff)


def test_age_classification_proposal_and_no_mutation():
    data = pd.DataFrame({"player_id": [1, 2, 3, 4, 5], "age": [29, 28, 99, 30, -1]})
    raw = pd.DataFrame({"player_id": [1, 2, 3, 5], "date_of_birth": ["1996-06-12", "1998-01-01", "2000-01-01", "1995-01-01"]})
    saved = data.copy(deep=True); raw_saved = raw.copy(deep=True)
    audit = age_audit(data, raw)
    assert list(audit.finding) == ["approximate_year_length", "consistent", "unexplained_snapshot_age_mismatch", "missing_raw_player", "invalid_snapshot_age"]
    proposal = correction_proposal(audit, {"SYNTHETIC_input": "a"*64})
    assert proposal["status"] == "PROPOSED" and proposal["applied"] is False and proposal["approval"] is None
    assert proposal["changes"][0]["old_value"] == 29
    assert proposal["changes"][0]["proposed_value"] == 30
    assert len(proposal["changes"]) == 1
    pd.testing.assert_frame_equal(data, saved)
    pd.testing.assert_frame_equal(raw, raw_saved)


def test_conflicting_and_identical_duplicate_source_rows():
    data = pd.DataFrame({"player_id": [1], "age": [29]})
    raw = pd.DataFrame({"player_id": [1, 1], "date_of_birth": ["1996-06-12", "1997-06-12"]})
    audit = age_audit(data, raw)
    assert audit.iloc[0].finding == "conflicting_source_dob"
    assert audit.iloc[0].source_rows == 2
    assert not correction_proposal(audit, {})["changes"]
    raw.loc[1, "date_of_birth"] = raw.loc[0, "date_of_birth"]
    assert age_audit(data, raw).iloc[0].finding == "approximate_year_length"


@pytest.mark.parametrize("ids", [[1, 1], [1.5], [True], [None], []])
def test_bad_candidate_ids(ids):
    with pytest.raises(ValueError):
        age_audit(pd.DataFrame({"player_id": ids, "age": [20]*len(ids)}), pd.DataFrame({"player_id": [1], "date_of_birth": ["2000-01-01"]}))


@pytest.mark.parametrize("age,band", [(16,"0-16"),(17,"17-20"),(20,"17-20"),(21,"21-24"),(24,"21-24"),
                                     (25,"25-28"),(29,"29-32"),(33,"33-36"),(37,"37+"),(None,"MISSING_OR_INVALID"),(float('inf'),"MISSING_OR_INVALID")])
def test_explicit_coverage_age_bands(age, band):
    assert age_band(age) == band


def test_exclusion_boundaries_overlap_and_coverage():
    data = pd.DataFrame({"player_id": [1, 2, 3, 4], "age": [20, 24, 30, None],
                         "minutes_played": [900, 899, 900, 1000], "market_value_in_eur": [1, 0, 10, 10],
                         "valuation_date": ["2025-06-12", "2026-06-13", "2025-06-11", "2026-06-12"],
                         "position": ["Attack", "Attack", "Defender", " "]})
    rows, stages = exclusion_audit(data, [1])
    assert rows.eligible.tolist() == [True, False, False, False]
    assert stages[0]["removed_at_stage"] == 1
    assert stages[1]["independent_failed"] == 1 and stages[1]["removed_at_stage"] == 0
    assert stages[-1]["after"] == 1
    with pytest.raises(ValueError): exclusion_audit(data, [1, 2])
    raw = pd.DataFrame({"player_id": [1,2,3,4], "current_club_domestic_competition_id": ["L1","L1","GB1",""]})
    coverage = coverage_analysis(data, data.iloc[:1], raw)
    for _, group in coverage.groupby('dimension'):
        assert group.integrated_count.sum() == 4
        assert group.candidate_count.sum() == 1
    assert "MISSING" in set(coverage.category)


def test_lineage_schema_fails_on_new_unreviewed_feature():
    columns = pd.read_csv(Path(__file__).resolve().parents[1] / 'data/processed/scoutiq_features_2025_26.csv', nrows=0).columns
    lineage = feature_lineage(columns)
    assert len(lineage) == 28
    assert lineage.feature.is_unique
    with pytest.raises(ValueError): feature_lineage(list(columns)+["invented_skill"])


def test_runner_refuses_existing_directory_before_io(tmp_path):
    marker = tmp_path / 'labels.csv'; marker.write_text('preserve')
    with pytest.raises(FileExistsError): run(tmp_path)
    assert marker.read_text() == 'preserve'


def test_real_audit_all_4112_and_proposed_only():
    root = Path(__file__).resolve().parents[1]
    audit = pd.read_csv(root / 'reports/day12/age_integrity_audit.csv')
    findings = pd.read_csv(root / 'reports/day12/age_discrepancies.csv')
    assert len(audit) == 4112 and audit.player_id.nunique() == 4112
    assert findings.player_id.tolist() == [341429]
    assert findings.iloc[0].snapshot_age == 29 and findings.iloc[0].calendar_age == 30
    assert findings.iloc[0].finding == 'approximate_year_length'
    proposal = json.loads((root / 'reports/day12/correction_proposal.json').read_text(encoding='utf-8'))
    assert proposal['applied'] is False and proposal['approval'] is None
    from src.evaluation.audit import digest
    for name, sha in proposal['input_sha256'].items():
        assert digest(root / name) == sha
