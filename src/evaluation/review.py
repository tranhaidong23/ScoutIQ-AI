"""Pilot intake and coordinator review; never adjudicate or invent labels."""

from collections import Counter
from itertools import combinations

from src.evaluation.pilot import readiness_report, validate_pilot_annotations


def review_pilot(scenarios, rows, manifest, registry):
    """Validate all submissions together; keep uncertainty and missingness explicit.

    Production review refuses SYNTHETIC registrations. Unit tests may use clearly
    identified synthetic fixtures to exercise the human declaration contract;
    registry declarations themselves are never proof of independence.
    """
    counts = validate_pilot_annotations(rows, manifest, registry)
    if any(r['label_source'] != 'independent_human' for r in registry.values()):
        raise ValueError('Pilot review accepts human registry declarations only')
    if registry and any(not r['assessor_id'] for r in rows):
        raise ValueError('Assign pending rows to an assessor before combining submissions')
    readiness = readiness_report(scenarios, rows, manifest, registry)
    coverage, queue = [], []
    for case in sorted(manifest['scenarios'], key=lambda c: c['scenario_id']):
        sid = case['scenario_id']
        selected = set(case['selected_ids'])
        by_person = {}
        for assessor, record in sorted(registry.items()):
            own = {r['player_id']: r for r in rows if r['scenario_id'] == sid and r['assessor_id'] == assessor}
            by_person[assessor] = own
            statuses = Counter(r['decision_status'] for r in own.values())
            uncertainty = Counter(r['uncertainty'] for r in own.values() if r['decision_status'] != 'pending')
            coverage.append({'scenario_id': sid, 'assessor_id': assessor,
                             'assessment_scope': case['assessment_scope'],
                             'pilot_items': len(selected), 'submitted': len(own),
                             'graded': statuses['graded'], 'abstain': statuses['abstain'],
                             'pending': statuses['pending'], 'missing': len(selected - own.keys()),
                             'uncertainty': {k: uncertainty[k] for k in ('low', 'medium', 'high')},
                             'independence_reviewed': record['independence_confirmed']})
            for pid in sorted(selected):
                row = own.get(pid)
                reasons = []
                if row is None:
                    reasons.append('missing_submission')
                elif row['decision_status'] != 'graded':
                    reasons.append(row['decision_status'])
                if row and row['uncertainty'] == 'high':
                    reasons.append('high_uncertainty')
                if row and row['missing_evidence'].strip():
                    reasons.append('missing_evidence')
                if not record['independence_confirmed']:
                    reasons.append('provenance_review_required')
                if reasons:
                    queue.append({'scenario_id': sid, 'player_id': pid, 'assessors': [assessor],
                                  'reasons': reasons, 'status': 'OPEN', 'adjudicated_grade': None})
        for left, right in combinations(sorted(by_person), 2):
            for pid in sorted(by_person[left].keys() & by_person[right].keys()):
                a, b = by_person[left][pid], by_person[right][pid]
                if a['decision_status'] == b['decision_status'] == 'graded' and a['relevance_grade'] != b['relevance_grade']:
                    queue.append({'scenario_id': sid, 'player_id': pid, 'assessors': [left, right],
                                  'reasons': ['grade_disagreement'], 'grades': [a['relevance_grade'], b['relevance_grade']],
                                  'status': 'OPEN', 'adjudicated_grade': None})
    reviewed = sum(r['decision_status'] == 'graded' and registry[r['assessor_id']]['independence_confirmed'] for r in rows)
    return {'schema_version': 'scoutiq.pilot-review.v1',
            'status': 'REVIEW_AVAILABLE' if reviewed else 'BLOCKED_NO_REVIEWED_HUMAN_LABELS',
            'annotation_counts': counts, 'reviewed_human_grades': reviewed,
            'registered_assessors': len(registry), 'coverage': coverage, 'review_queue': queue,
            'readiness': readiness, 'actual_final_relevance_metrics': None,
            'final_evaluation_status': 'BLOCKED_PILOT_IS_NOT_FINAL_EVALUATION',
            'interpretation': 'Registry is a declaration requiring external review; no automatic adjudication. '
                              'Agreement is per scenario on common graded items only; missing is never zero.'}
