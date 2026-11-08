"""Audit original snapshot and prepare an UNLABELED pilot in a NEW directory."""

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess

import numpy as np
import pandas as pd

from src.evaluation.audit import audit_snapshot, digest
from src.evaluation.integrity import age_audit, age_values, correction_proposal, coverage_analysis, exclusion_audit, feature_lineage
from src.evaluation.pilot import PILOT_FIELDS, annotation_template, build_pilot, readiness_report, validate_pilot_annotations
from src.features.build_features import validate_features
from src.recommendation.config import ProjectPaths


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def run(output_dir=None, *, seed=12, per_scenario=8):
    paths = ProjectPaths()
    output = paths.reports / "day12" if output_dir is None else Path(output_dir)
    if output.exists():
        raise FileExistsError("Choose a new --output-dir; never overwrite evidence or human annotations")
    prior_path = paths.reports / "day11/evaluation.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    old_audit = json.loads((paths.reports / "day11/audit_evidence.json").read_text(encoding="utf-8"))
    for name, sha in {**prior["source_sha256"], **old_audit["input_sha256"]}.items():
        if digest(paths.root / name) != sha:
            raise ValueError(f"Frozen source/snapshot changed: {name}")
    candidates = pd.read_csv(paths.features)
    validate_features(candidates)
    integrated = pd.read_csv(paths.root / "data/processed/scoutiq_players_2025_26.csv")
    players = pd.read_csv(paths.root / "data/raw/players.csv.gz", keep_default_na=False,
                          usecols=["player_id", "date_of_birth", "current_club_domestic_competition_id"])
    ages = age_audit(candidates, players)
    exclusions, stages = exclusion_audit(integrated, candidates.player_id.tolist())
    coverage = coverage_analysis(integrated, candidates, players)
    lineage = feature_lineage(candidates.columns)
    fresh_audit = audit_snapshot(paths.root)
    if fresh_audit != old_audit:
        raise ValueError("Read-only Day 11 probes no longer reproduce; investigate before pilot")
    hashes = fresh_audit["input_sha256"]
    proposal = correction_proposal(ages, hashes)
    manifest = build_pilot(prior["scenarios"], candidates, digest(paths.features), seed=seed, per_scenario=per_scenario)
    if manifest != build_pilot(list(reversed(prior["scenarios"])), candidates.iloc[::-1], digest(paths.features), seed=seed, per_scenario=per_scenario):
        raise AssertionError("Pilot sampling depends on input row order")
    rows = annotation_template(manifest)
    registry = {}  # No real assessors provided. Never fabricate expert identities.
    checks = validate_pilot_annotations(rows, manifest, registry)
    readiness = readiness_report(prior["scenarios"], rows, manifest, registry)
    packet = pd.read_csv(paths.reports / "day11/annotation_evidence.csv")
    order = {(r["scenario_id"], r["player_id"]): i for i, r in enumerate(rows)}
    packet = packet[[tuple(r) in order for r in packet[["scenario_id", "player_id"]].itertuples(index=False, name=None)]].copy()
    packet["presentation_order"] = [order[tuple(r)] for r in packet[["scenario_id", "player_id"]].itertuples(index=False, name=None)]
    packet.sort_values("presentation_order", inplace=True)
    fields = [c for c in packet if c not in ("scenario_id", "player_id", "presentation_order", "evidence_scope", "goals_per90", "assists_per90")]
    packet["missing_fields"] = packet[fields].apply(lambda r: "|".join(c for c in fields if pd.isna(r[c])), axis=1)
    packet["known_limitations"] = packet.evidence_scope.map({
        "attack_output_and_role": "no league/opponent normalization; no xG/xA; metadata as-of unverified",
        "context_profile_only": "no defensive/goalkeeping skill metrics; metadata as-of unverified"})
    if len(packet) != len(rows):
        raise ValueError("Incomplete pilot evidence packet")
    raw_date_counts = Counter(age_values(v)["dob_status"] for v in players.date_of_birth)
    legacy_parsed = pd.to_datetime(players.date_of_birth, errors="coerce")
    missing = {c: int(n) for c, n in candidates.isna().sum().items()}
    numeric = candidates.select_dtypes(include=np.number)
    audit = {"run_utc": datetime.now(timezone.utc).isoformat(), "cutoff": "2026-06-12", "shape": list(candidates.shape),
             "dataset_sha256": digest(paths.features), "input_sha256": hashes,
             "prior_evidence_sha256": {"reports/day11/evaluation.json": digest(prior_path),
                 "reports/day11/audit_evidence.json": digest(paths.reports / "day11/audit_evidence.json"),
                 "reports/day11/annotation_evidence.csv": digest(paths.reports / "day11/annotation_evidence.csv")},
             "age_findings": {str(k): int(v) for k, v in ages.finding.value_counts().items()},
             "candidate_dob_status": {str(k): int(v) for k, v in ages.dob_status.value_counts().items()},
             "raw_dob_status": dict(raw_date_counts), "raw_player_rows": len(players),
             "raw_duplicate_player_ids": int(players.player_id.duplicated().sum()),
             "raw_legacy_parser_nat": int(legacy_parsed.isna().sum()),
             "raw_nonmissing_unparseable_legacy": int((players.date_of_birth.str.strip().ne("") & legacy_parsed.isna()).sum()),
             "missing_features": missing, "infinite_numeric_features": int(np.isinf(numeric.to_numpy(dtype=float)).sum()),
             "height_review_ids": candidates.loc[candidates.height_in_cm.notna() & ~candidates.height_in_cm.between(100, 230), "player_id"].tolist(),
             "height_policy_note": "100..230 cm review flag only, not automatic correction",
             "eligibility_stages": stages, "eligible_ids_exact": True,
             "day11_read_only_audit_reproduced": True, "pilot_validation": checks,
             "pilot_reproducible_under_row_permutation": True,
             "correction_applied": False, "independent_human_labels": 0,
             "environment": {"python": platform.python_version(), "platform": platform.platform(),
                             "packages": {n: version(n) for n in ("pandas", "numpy", "scikit-learn", "pytest")}},
             "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, cwd=paths.root).strip(),
             "source_sha256": {p.relative_to(paths.root).as_posix(): digest(p) for p in sorted((paths.root / "src/evaluation").glob("*.py"))}}
    output.mkdir(parents=True, exist_ok=False)
    for name, table in (("age_integrity_audit.csv", ages), ("age_discrepancies.csv", ages[ages.finding.ne("consistent")]),
                        ("coverage_analysis.csv", coverage), ("eligibility_exclusions.csv", exclusions),
                        ("feature_lineage.csv", lineage), ("pilot_evidence.csv", packet)):
        table.to_csv(output / name, index=False, encoding="utf-8")
    with (output / "pilot_annotation_template.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=PILOT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    for name, obj in (("audit.json", audit), ("correction_proposal.json", proposal),
                      ("pilot_manifest.json", manifest), ("assessor_registry.json", registry),
                      ("readiness.json", readiness)):
        write_json(output / name, obj)
    return audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--seed", type=int, default=12)
    parser.add_argument("--per-scenario", type=int, default=8)
    args = parser.parse_args()
    result = run(args.output_dir, seed=args.seed, per_scenario=args.per_scenario)
    print(json.dumps({"age_findings": result["age_findings"], "pilot": result["pilot_validation"], "correction_applied": False}))
