"""SYNTHETIC contract fixtures, never real human assessments."""

from copy import deepcopy
import csv
import json
from pathlib import Path

import pandas as pd
import pytest

from src.evaluation.pilot import PILOT_FIELDS, annotation_template, build_pilot
from src.evaluation.review import review_pilot
from src.evaluation.run_day13 import run


@pytest.fixture
def sample():
    scenarios = [{'scenario_id': 'SYNTHETIC', 'candidate_ids': [1, 2, 3],
                  'methods': {'cosine': {'top5_ids': [1, 2, 3]}}}]
    manifest = build_pilot(scenarios, pd.DataFrame({'player_id': [1, 2, 3],
                          'age': [20, 21, 22], 'position': ['Attack'] * 3}), 'a' * 64)
    # These declared-human records exist ONLY to test the production contract.
    registry = {a: {'label_source': 'independent_human', 'independence_confirmed': True,
                    'review_evidence': 'SYNTHETIC TEST ONLY, no real assessor'} for a in ('Fixture_A', 'Fixture_B')}
    rows = []
    for assessor in registry:
        for r in annotation_template(manifest):
            rows.append({**r, 'assessor_id': assessor, 'timestamp': '2026-11-06T10:00:00+07:00',
                         'relevance_grade': 2 if assessor == 'Fixture_A' else 3,
                         'decision_status': 'graded', 'uncertainty': 'low',
                         'label_source': 'independent_human', 'evidence': 'SYNTHETIC TEST ONLY'})
    return scenarios, rows, manifest, registry


def test_empty_real_template_stays_blocked(sample):
    scenarios, _, manifest, _ = sample
    result = review_pilot(scenarios, annotation_template(manifest), manifest, {})
    assert result['status'] == 'BLOCKED_NO_REVIEWED_HUMAN_LABELS'
    assert result['reviewed_human_grades'] == 0
    assert result['actual_final_relevance_metrics'] is None
    assert result['review_queue'] == []
    assert result['annotation_counts']['pending'] == 3


def test_disagreements_preserved_without_adjudication(sample):
    before = deepcopy(sample)
    result = review_pilot(*sample)
    assert sample == before
    assert len(result['review_queue']) == 3
    assert all(r['grades'] == [2, 3] and r['adjudicated_grade'] is None for r in result['review_queue'])
    assert result['readiness']['cases'][0]['agreement']['pairs'][0]['exact_agreement'] == 0
    assert result['actual_final_relevance_metrics'] is None


def test_single_overlap_still_queues_disagreement(sample):
    scenarios, rows, manifest, registry = sample
    rows = [r for r in rows if r['player_id'] == 1]
    result = review_pilot(scenarios, rows, manifest, registry)
    assert sum('grade_disagreement' in q['reasons'] for q in result['review_queue']) == 1
    assert result['readiness']['cases'][0]['agreement']['status'] == 'BLOCKED'
    assert all(c['missing'] == 2 for c in result['coverage'])


def test_abstention_uncertainty_and_pending_not_zero(sample):
    scenarios, rows, manifest, registry = sample
    rows[0].update(decision_status='abstain', relevance_grade=None, label_source='unlabeled',
                   uncertainty='high', missing_evidence='SYNTHETIC missing source')
    rows[1].update(decision_status='pending', relevance_grade=None, label_source='unlabeled',
                   timestamp='', uncertainty='')
    result = review_pilot(scenarios, rows, manifest, registry)
    assert result['annotation_counts'] == {'rows': 6, 'graded': 4, 'abstain': 1, 'pending': 1}
    assert result['coverage'][0]['uncertainty']['high'] == 1
    assert any(q['reasons'] == ['abstain', 'high_uncertainty', 'missing_evidence'] for q in result['review_queue'])


def test_unreviewed_declarations_do_not_unlock_metrics(sample):
    for r in sample[3].values():
        r['independence_confirmed'] = False
    result = review_pilot(*sample)
    assert result['reviewed_human_grades'] == 0
    assert result['status'].startswith('BLOCKED')
    assert result['readiness']['cases'][0]['agreement']['status'] == 'BLOCKED'


def test_order_independence(sample):
    scenarios, rows, manifest, registry = sample
    assert review_pilot(*sample) == review_pilot(scenarios, rows[::-1], manifest, dict(reversed(list(registry.items()))))


@pytest.mark.parametrize('field,value', [('dataset_sha256', 'b'*64), ('rubric_version', 'other'),
    ('pilot_version', 'other'), ('assessment_scope', 'context_profile_only'),
    ('player_id', 999), ('assessor_id', 'Unknown'), ('relevance_grade', 4),
    ('relevance_grade', True), ('timestamp', '2026-11-06'), ('evidence', '')])
def test_bad_submission_fails_closed(sample, field, value):
    sample[1][0][field] = value
    with pytest.raises(ValueError):
        review_pilot(*sample)


def test_duplicate_across_submissions_rejected(sample):
    sample[1].append(deepcopy(sample[1][0]))
    with pytest.raises(ValueError, match='Duplicate'):
        review_pilot(*sample)


def test_synthetic_registry_rejected(sample):
    for r in sample[3].values():
        r['label_source'] = 'SYNTHETIC'
    for r in sample[1]:
        r['label_source'] = 'SYNTHETIC'
    with pytest.raises(ValueError, match='human registry'):
        review_pilot(*sample)


def test_anonymous_pending_not_mixed_with_assigned(sample):
    sample[1].append(annotation_template(sample[2])[0])
    with pytest.raises(ValueError, match='Assign pending'):
        review_pilot(*sample)


def test_runner_refuses_existing_output_before_reading(tmp_path):
    marker = tmp_path / 'keep.txt'
    marker.write_text('keep')
    with pytest.raises(FileExistsError):
        run(tmp_path)
    assert marker.read_text() == 'keep'


@pytest.mark.parametrize('annotations,registry', [(['absent.csv'], None), ([], 'absent.json'),
    (['same.csv', 'same.csv'], 'absent.json')])
def test_runner_argument_pairs_fail_before_output(tmp_path, annotations, registry):
    output = tmp_path / 'new'
    with pytest.raises(ValueError):
        run(output, annotation_paths=annotations, registry_path=registry)
    assert not output.exists()


def test_real_frozen_snapshot_run_is_read_only(tmp_path):
    root = Path(__file__).resolve().parents[1]
    from src.evaluation.audit import digest
    preserved = [p for folder in ('data/raw', 'data/processed', 'reports/day12')
                 for p in (root / folder).glob('*') if p.is_file()]
    before = {p: digest(p) for p in preserved}
    result = run(tmp_path / 'review')
    assert result['annotation_counts'] == {'rows': 32, 'graded': 0, 'abstain': 0, 'pending': 32}
    assert result['correction']['status'] == 'PROPOSED'
    assert result['actual_final_relevance_metrics'] is None
    assert before == {p: digest(p) for p in preserved}


def test_external_intake_no_private_text_copied(tmp_path):
    root = Path(__file__).resolve().parents[1]
    from src.evaluation.pilot import load_pilot_annotations
    rows = load_pilot_annotations(root / 'reports/day12/pilot_annotation_template.csv')
    rows = rows[:1]
    rows[0].update(assessor_id='Fixture_A', notes='PRIVATE_TEST_MARKER')
    registry = {'Fixture_A': {'label_source': 'independent_human', 'independence_confirmed': False,
                             'review_evidence': 'PRIVATE_TEST_MARKER'}}
    annotations = tmp_path / 'private.csv'
    with annotations.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=PILOT_FIELDS)
        writer.writeheader(); writer.writerows(rows)
    registry_path = tmp_path / 'registry.json'
    registry_path.write_text(json.dumps(registry))
    result = run(tmp_path / 'result', annotation_paths=[annotations], registry_path=registry_path)
    assert result['registered_assessors'] == 1
    assert result['reviewed_human_grades'] == 0
    assert 'PRIVATE_TEST_MARKER' not in (tmp_path / 'result/review.json').read_text()
    assert str(tmp_path) not in json.dumps(result)
