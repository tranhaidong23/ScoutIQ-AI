"""Verify frozen inputs and review pilot submissions in a NEW output directory."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import pandas as pd

from src.evaluation.audit import digest
from src.evaluation.pilot import build_pilot, load_pilot_annotations
from src.evaluation.review import review_pilot
from src.recommendation.config import ProjectPaths


def run(output_dir=None, *, annotation_paths=(), registry_path=None):
    paths = ProjectPaths()
    output = paths.reports / 'day13' if output_dir is None else Path(output_dir)
    if output.exists():
        raise FileExistsError('Choose a new output directory; never overwrite a review')
    annotation_paths = [Path(p).resolve() for p in annotation_paths]
    if len(set(annotation_paths)) != len(annotation_paths):
        raise ValueError('Duplicate annotation input path')
    if bool(annotation_paths) != (registry_path is not None):
        raise ValueError('Provide both annotation files and an explicit reviewed registry')
    inputs = {}

    def read_json(relative):
        p = paths.root / relative
        inputs[relative] = digest(p)
        return json.loads(p.read_text(encoding='utf-8-sig'))

    audit = read_json('reports/day12/audit.json')
    for name, expected in {**audit['input_sha256'], **audit['source_sha256'], **audit['prior_evidence_sha256']}.items():
        if digest(paths.root / name) != expected:
            raise ValueError(f'Frozen source or evidence changed: {name}')
        inputs[name] = expected
    prior = read_json('reports/day11/evaluation.json')
    for name, expected in prior['source_sha256'].items():
        if digest(paths.root / name) != expected:
            raise ValueError(f'Frozen engine source changed: {name}')
        inputs[name] = expected
    manifest = read_json('reports/day12/pilot_manifest.json')
    expected_manifest = build_pilot(prior['scenarios'], pd.read_csv(paths.features), digest(paths.features), seed=12, per_scenario=8)
    if manifest != expected_manifest:
        raise ValueError('Pilot manifest no longer matches frozen seed-12 snapshot')
    proposal = read_json('reports/day12/correction_proposal.json')
    if proposal['status'] != 'PROPOSED' or proposal['applied'] is not False or proposal['approval'] is not None:
        raise ValueError('Correction state changed; review the new version explicitly')
    if proposal['input_sha256'] != audit['input_sha256']:
        raise ValueError('Correction parent hashes differ from frozen audit')
    sources = []
    if annotation_paths:
        registry_path = Path(registry_path).resolve()
        registry = json.loads(registry_path.read_text(encoding='utf-8-sig'))
        registry_hash = digest(registry_path)
        rows = []
        for i, p in enumerate(annotation_paths, 1):
            loaded = load_pilot_annotations(p)
            if not loaded:
                raise ValueError('Empty submission file')
            rows.extend(loaded)
            sources.append({'input_number': i, 'sha256': digest(p), 'rows': len(loaded)})
    else:
        registry = read_json('reports/day12/assessor_registry.json')
        p = paths.reports / 'day12/pilot_annotation_template.csv'
        inputs['reports/day12/pilot_annotation_template.csv'] = digest(p)
        rows = load_pilot_annotations(p)
        if registry or any(r['decision_status'] != 'pending' or r['assessor_id'] for r in rows):
            raise ValueError('Baseline template changed; supply explicit external submissions')
        expected_pairs = {(s['scenario_id'], pid) for s in manifest['scenarios'] for pid in s['selected_ids']}
        if {(r['scenario_id'], r['player_id']) for r in rows} != expected_pairs:
            raise ValueError('Incomplete frozen pilot template')
        registry_hash = inputs['reports/day12/assessor_registry.json']
    review = review_pilot(prior['scenarios'], rows, manifest, registry)
    review.update(run_utc=datetime.now(timezone.utc).isoformat(), input_sha256=inputs,
                  submission_sources=sources, registry_sha256=registry_hash,
                  source_sha256={p.relative_to(paths.root).as_posix(): digest(p) for p in
                                 (paths.root / 'src/evaluation/review.py', paths.root / 'src/evaluation/run_day13.py')},
                  correction={'status': 'PROPOSED', 'applied': False,
                              'decision': 'DEFERRED_PENDING_DOB_REVIEW_AND_EXPLICIT_AUTHORIZATION',
                              'proposal_sha256': inputs['reports/day12/correction_proposal.json']})
    # Complete validation before creating any output. Original submission text is
    # deliberately not copied; coordinators retain those private source files.
    payload = json.dumps(review, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    output.mkdir(parents=True, exist_ok=False)
    (output / 'review.json').write_text(payload, encoding='utf-8')
    (output / 'review_queue.json').write_text(json.dumps(review['review_queue'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return review


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--annotations', nargs='+', type=Path, default=[])
    parser.add_argument('--registry', type=Path)
    args = parser.parse_args()
    result = run(args.output_dir, annotation_paths=args.annotations, registry_path=args.registry)
    print(json.dumps({'status': result['status'], 'counts': result['annotation_counts'],
                      'reviewed_human_grades': result['reviewed_human_grades'], 'correction': result['correction']['status']}))
