"""SYNTHETIC mathematical fixtures; never labels of real football players."""

import csv
from copy import deepcopy
import json
from math import log2
from pathlib import Path

import pytest
from sklearn.metrics import ndcg_score

from src.evaluation.metrics import (
    ANNOTATION_FIELDS, assess_ranking, catalogue_coverage, load_annotations,
    ranking_stability, validate_annotations,
)
from src.evaluation.run_day11 import run, synthetic_fixture


@pytest.fixture
def labels():
    return synthetic_fixture()["annotations"]


def evaluate(rows, ranking=None, candidates=None, **kwargs):
    return assess_ranking([2, 3, 1] if ranking is None else ranking,
                          [1, 2, 3, 4] if candidates is None else candidates, rows,
                          scenario_id="SYNTHETIC_math", assessor_id="SYNTHETIC_fixture",
                          label_source="SYNTHETIC", **kwargs)


def test_formulas_and_independent_sklearn_oracle(labels):
    result = evaluate(labels, k=3)
    expected = (3 + 7 / log2(4)) / (7 + 3 / log2(3) + 1 / log2(4))
    assert result["metrics"] == pytest.approx({"precision_at_k": 2/3, "recall_at_k": 1., "ndcg_at_k": expected})
    # sklearn sums supplied gains linearly: pass 2**grade-1 and strict rank
    # surrogate scores, NOT tied cosine scores or grades as predicted scores.
    oracle = ndcg_score([[7, 3, 0, 1]], [[2, 4, 3, 1]], k=3, ignore_ties=True)
    assert result["metrics"]["ndcg_at_k"] == pytest.approx(oracle)
    assert result["interpretation"] == "SYNTHETIC_ONLY_NOT_SCOUTING_QUALITY"


@pytest.mark.parametrize("k", [1, 2, 3, 4, 10])
def test_k_and_perfect_order(labels, k):
    result = evaluate(labels, [1, 2, 4, 3], k=k)
    assert result["metrics"]["ndcg_at_k"] == pytest.approx(1.)
    assert result["metrics"]["precision_at_k"] == min(k, 2) / k
    assert result["metrics"]["recall_at_k"] == min(k, 2) / 2


def test_no_labels_are_not_zero_and_unlabeled_template(labels):
    rows = [{**r, "relevance_grade": None, "label_source": "unlabeled", "assessor_id": "",
             "evidence": "", "timestamp": ""} for r in labels]
    for records in ([], rows):
        result = evaluate(records)
        assert set(result["metrics"].values()) == {None}
        assert set(result["unavailable_reasons"].values()) == {"no_labels"}
        assert result["label_coverage"] == 0


def test_partial_labels_gate_recall_and_ideal_gain(labels):
    result = evaluate(labels[:3], k=3)
    assert result["metrics"]["precision_at_k"] == 2/3
    assert result["metrics"]["recall_at_k"] is None
    assert result["metrics"]["ndcg_at_k"] is None
    assert result["unavailable_reasons"]["ndcg_at_k"] == "incomplete_candidate_labels"
    # Unjudged returned ID is never interpreted as irrelevant.
    assert evaluate(labels[:2], k=3)["metrics"]["precision_at_k"] is None


def test_empty_universe_empty_retrieval_and_no_relevant(labels):
    empty = evaluate([], [], [], k=5)
    assert set(empty["unavailable_reasons"].values()) == {"empty_candidate_universe"}
    assert empty["label_coverage"] is None
    assert evaluate(labels, [], k=5)["metrics"] == {"precision_at_k": 0, "recall_at_k": 0, "ndcg_at_k": 0}
    assert evaluate(labels[:1], [], k=5)["metrics"]["precision_at_k"] is None
    zero = [{**r, "relevance_grade": 0} for r in labels]
    result = evaluate(zero)
    assert result["metrics"] == {"precision_at_k": 0, "recall_at_k": None, "ndcg_at_k": None}
    one = [{**r, "relevance_grade": 1} for r in labels]
    assert evaluate(one, k=3)["metrics"]["ndcg_at_k"] == pytest.approx(1.)
    assert evaluate(one)["metrics"]["recall_at_k"] is None


def test_ties_preserve_supplied_service_order_and_no_mutation(labels):
    before = deepcopy(labels)
    # Even if engine scores tie, its final ID/soft-preference order is the
    # evaluated output. The evaluator has no scores and cannot label-sort ties.
    first = evaluate(labels, [1, 2, 3], k=1)
    reversed_tie = evaluate(labels, [2, 1, 3], k=1)
    assert first["metrics"]["ndcg_at_k"] == 1
    assert reversed_tie["metrics"]["ndcg_at_k"] == 3/7
    assert labels == before
    assert evaluate(labels, [1, 2, 3], k=1) == first
    json.dumps(first, allow_nan=False)


@pytest.mark.parametrize("grade", [-1, 4, 1.5, 2., True, float("nan"), float("inf"), "2", None, ""])
def test_invalid_grades(labels, grade):
    labels[0]["relevance_grade"] = grade
    with pytest.raises(ValueError): evaluate(labels)


@pytest.mark.parametrize("field,value", [
    ("scenario_id", "another"), ("player_id", 99), ("player_id", True), ("player_id", 1.),
    ("assessor_id", ""), ("assessor_id", "another"), ("timestamp", "2026-11-03"),
    ("timestamp", "not-a-date"), ("timestamp", 123), ("evidence", "  "),
    ("notes", None), ("label_source", "expert_model"), ("label_source", "independent_human"),
    ("label_source", "unlabeled"),
])
def test_invalid_records_and_provenance(labels, field, value):
    labels[0][field] = value
    with pytest.raises(ValueError): evaluate(labels)


@pytest.mark.parametrize("k", [0, -1, 1.1, True, "5", None, float("inf"), float("nan")])
def test_invalid_k(labels, k):
    with pytest.raises(ValueError): evaluate(labels, k=k)
    with pytest.raises(ValueError): ranking_stability([1], [1], k=k)


@pytest.mark.parametrize("ranking,candidates", [
    ([1, 1], [1, 2, 3, 4]), ([99], [1, 2, 3, 4]), ([0], [1, 2, 3, 4]),
    ([1.], [1, 2, 3, 4]), ([True], [1, 2, 3, 4]), ([1], [1, 1, 2, 3, 4]),
    ([1], [1, 2, 3]), ("123", [1, 2, 3, 4]), ([1], {1, 2, 3, 4}),
])
def test_invalid_ids_missing_candidates_duplicates(labels, ranking, candidates):
    with pytest.raises(ValueError): evaluate(labels, ranking, candidates)


def test_duplicate_annotations_and_no_implicit_assessor_aggregation(labels):
    with pytest.raises(ValueError): evaluate(labels + [labels[0]])
    another = {**labels[0], "assessor_id": "SYNTHETIC_second"}
    validate_annotations(labels + [another], scenario_id="SYNTHETIC_math", candidate_ids=[1, 2, 3, 4])
    with pytest.raises(ValueError): evaluate(labels + [another])
    del labels[0]["notes"]
    with pytest.raises(ValueError): evaluate(labels)


def test_provenance_claim_is_not_verified_independence(labels):
    # Validator contract test ONLY, not a real person or reported human labels.
    rows = [{**r, "label_source": "independent_human"} for r in labels]
    result = assess_ranking([1], [1, 2, 3, 4], rows, scenario_id="SYNTHETIC_math", assessor_id="SYNTHETIC_fixture")
    assert result["provenance_status"] == "declared_not_independently_verified"


def test_stability_is_fixed_k_and_empty_undefined():
    assert ranking_stability([1, 2], [2, 1], k=5) == {
        "k": 5, "left_count": 2, "right_count": 2, "overlap_at_k": .4, "same_order": False, "reason": None}
    assert ranking_stability([], [1])["overlap_at_k"] is None
    assert ranking_stability([], [])["same_order"] is None
    with pytest.raises(ValueError): ranking_stability([1, 1], [1])


def test_coverage_query_specific_pools():
    result = catalogue_coverage([[1], [2], []], [[1, 2], [2, 3], []])
    assert result["catalogue_coverage"] == 2/3
    assert result["request_coverage"] == 2/3
    assert catalogue_coverage([], [])["request_coverage"] is None
    assert catalogue_coverage([[]], [[]])["catalogue_coverage"] is None
    with pytest.raises(ValueError): catalogue_coverage([[1]], [])
    with pytest.raises(ValueError): catalogue_coverage([[1], [2]], [[2], [1]])
    with pytest.raises(ValueError): catalogue_coverage([[1, 1]], [[1]])


@pytest.mark.parametrize("grade", ["", "0", "3"])
def test_csv_roundtrip(tmp_path, labels, grade):
    path = tmp_path / "SYNTHETIC.csv"
    labels[0]["relevance_grade"] = grade
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=ANNOTATION_FIELDS)
        writer.writeheader(); writer.writerows(labels)
    rows = load_annotations(path)
    assert rows[0]["relevance_grade"] == (None if grade == "" else int(grade))
    assert rows[0]["player_id"] == 1


@pytest.mark.parametrize("row", ["1,2", ",".join(["x"]*8),
                                 "x,1,a,t,NaN,e,n,SYNTHETIC", "x,1.0,a,t,2,e,n,SYNTHETIC",
                                 "x,1,a,t,2,e,n,SYNTHETIC,extra"])
def test_invalid_csv(tmp_path, row):
    path = tmp_path / "invalid.csv"
    path.write_text(",".join(ANNOTATION_FIELDS) + "\n" + row, encoding="utf-8")
    with pytest.raises(ValueError): load_annotations(path)


def test_runner_never_overwrites_or_reads_raw_if_destination_exists(tmp_path):
    marker = tmp_path / "human_labels.csv"
    marker.write_text("preserve", encoding="utf-8")
    with pytest.raises(FileExistsError): run(tmp_path)
    assert marker.read_text(encoding="utf-8") == "preserve"


@pytest.fixture(scope="module")
def evidence_report():
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / "reports/day11/evaluation.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("scenario_index,pool_count", [(0, 22), (1, 10), (2, 94), (3, 47)])
def test_real_snapshot_unlabeled_and_no_false_relevance(evidence_report, scenario_index, pool_count):
    scenario = evidence_report["scenarios"][scenario_index]
    assert len(scenario["candidate_ids"]) == pool_count
    for method in scenario["methods"].values():
        assessment = method["assessment"]
        assert assessment["judged_count"] == 0
        assert assessment["label_coverage"] == 0
        assert set(assessment["metrics"].values()) == {None}
        assert set(method["top5_ids"]) <= set(scenario["candidate_ids"])


def test_annotation_packet_complete_blinded_and_context_only(evidence_report):
    root = Path(__file__).resolve().parents[1]
    rows = load_annotations(root / "reports/day11/annotation_template.csv")
    assert len(rows) == 173
    assert all(r["relevance_grade"] is None and r["label_source"] == "unlabeled" for r in rows)
    for scenario in evidence_report["scenarios"]:
        selected = [r for r in rows if r["scenario_id"] == scenario["scenario_id"]]
        assert {r["player_id"] for r in selected} == set(scenario["candidate_ids"])
        validate_annotations(selected, scenario_id=scenario["scenario_id"], candidate_ids=scenario["candidate_ids"])
    with (root / "reports/day11/annotation_evidence.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert not {"rank", "similarity_score", "method", "relevance_grade"} & set(reader.fieldnames)
        packet = list(reader)
    assert len(packet) == len(rows)
    for row in packet:
        if row["position"] in ("Defender", "Goalkeeper"):
            assert row["evidence_scope"] == "context_profile_only"
            assert row["goals_per90"] == row["assists_per90"] == ""


def test_snapshot_audit_and_source_provenance(evidence_report):
    from src.evaluation.audit import digest
    root = Path(__file__).resolve().parents[1]
    for name, sha in evidence_report["source_sha256"].items():
        assert digest(root / name) == sha
    audit = json.loads((root / "reports/day11/audit_evidence.json").read_text(encoding="utf-8"))
    assert audit["eligibility_ids_exact"]
    assert audit["shape"] == [4112, 28]
    assert audit["appearances"]["joined_after_cutoff"] == 0
    assert audit["valuations"]["feature_dates_after_cutoff"] == 0
    assert all(v["mismatched_players"] == v["missing_source"] == 0
               for v in audit["appearances"]["feature_aggregate_check"].values())
    assert len(evidence_report["checks"]) == 16
    assert all(r["day10_full_response_exact"] and r["repeat_exact"] and r["hard_filters_pass"]
               for r in evidence_report["checks"])
