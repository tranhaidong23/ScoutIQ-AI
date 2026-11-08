"""Read-only audit + four demo-query assessments; creates a NEW output directory."""

import argparse
import csv
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess

import pandas as pd
from threadpoolctl import threadpool_limits

from src.evaluation.audit import audit_snapshot, digest
from src.evaluation.metrics import ANNOTATION_FIELDS, assess_ranking, catalogue_coverage, ranking_stability
from src.recommendation.config import METHODS, ProjectPaths
from src.recommendation.constraints import filter_candidates
from src.recommendation.run_day8 import SCENARIOS, independent_eligible_ids
from src.recommendation.run_day10 import scenario_request
from src.recommendation.service import RecommendationService


def synthetic_fixture():
    """Abstract test IDs/grades only. Not football data or expert assessments."""
    rows = [dict(zip(ANNOTATION_FIELDS, ("SYNTHETIC_math", i, "SYNTHETIC_fixture",
            "2026-11-03T00:00:00+00:00", grade, "SYNTHETIC mathematical fixture, not a real player",
            "No human assessor", "SYNTHETIC"))) for i, grade in [(1, 3), (2, 2), (3, 0), (4, 1)]]
    result = assess_ranking([2, 3, 1], [1, 2, 3, 4], rows, scenario_id="SYNTHETIC_math",
                            assessor_id="SYNTHETIC_fixture", label_source="SYNTHETIC", k=3)
    return {"warning": "SYNTHETIC; NOT real relevance or scouting quality", "annotations": rows,
            "ranking": [2, 3, 1], "candidate_ids": [1, 2, 3, 4], "assessment": result}


def run(output_dir=None):
    paths = ProjectPaths()
    destination = paths.reports / "day11" if output_dir is None else Path(output_dir)
    if destination.exists():
        raise FileExistsError("Choose a new --output-dir; never overwrite annotations or previous evidence")
    prior_path = paths.reports / "day10/evaluation.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    if digest(paths.features) != prior["prior_input_hashes"]["features"]:
        raise ValueError("Feature snapshot differs from Day 10")
    for name, sha in prior["source_sha256"].items():
        if digest(paths.root / name) != sha:
            raise ValueError(f"Day 5-10 source changed: {name}")
    data = pd.read_csv(paths.features)
    saved = {(r["scenario"], r["response"]["request"]["method"]): r["response"] for r in prior["examples"]}
    annotations, evidence, scenarios, checks = [], [], [], []
    per_method = {m: [] for m in METHODS}
    pools = []
    with threadpool_limits(limits=1):
        service = RecommendationService.from_csv(fit_player_ids=prior["reference"]["fit_ids"])
        before = service.describe()
        for name, query, constraints in SCENARIOS[:4]:
            mask, stages = filter_candidates(data, query, constraints)
            pool = sorted(int(i) for i in data.loc[mask, "player_id"])
            if set(pool) != independent_eligible_ids(data, query, constraints):
                raise AssertionError("Independent eligible pool mismatch")
            pools.append(pool)
            rows = [dict(zip(ANNOTATION_FIELDS, (name, i, "", "", "", "", "", "unlabeled"))) for i in pool]
            annotations.extend(rows)
            # Hide model identity/rank/similarity from the evidence packet. Order
            # is a fixed shuffle, independent of scores/labels; no fake facts.
            cols = ["player_id", "name", "position", "sub_position", "age", "minutes_played",
                    "market_value_in_eur", "valuation_date", "current_club_id", "current_club_name", "foot"]
            if constraints.filters.position in ("Attack", "Midfield"):
                cols += ["goals_per90", "assists_per90"]
            packet = data.loc[mask, cols].sample(frac=1, random_state=11)
            for record in packet.to_dict(orient="records"):
                evidence.append({"scenario_id": name, **record,
                                 "evidence_scope": "attack_output_and_role" if constraints.filters.position in ("Attack", "Midfield") else "context_profile_only"})
            case = {"scenario_id": name, "scenario_source": "developer_demo_from_Day8_not_historical_scout_request",
                    "reference_player_id": query, "constraints": constraints.describe(),
                    "candidate_ids": pool, "filter_stages": stages, "methods": {}}
            for method in METHODS:
                request = scenario_request(query, constraints, method)
                response = service.recommend(request)
                if response != saved[name, method] or response != service.recommend(request):
                    raise AssertionError("Day 10 parity or reproducibility failure")
                shortlist = [r["player_id"] for r in response["explanation"]["recommendation"]["results"]]
                if not set(shortlist) <= set(pool):
                    raise AssertionError("Hard filter violation")
                per_method[method].append(shortlist)
                case["methods"][method] = {
                    "top5_ids": shortlist,
                    "assessment": assess_ranking(shortlist, pool, rows, scenario_id=name,
                                                  assessor_id="PENDING_independent_assessor"),
                }
                checks.append({"scenario_id": name, "method": method, "day10_full_response_exact": True,
                               "repeat_exact": True, "hard_filters_pass": True, "candidate_count": len(pool)})
            case["stability_vs_cosine"] = {m: ranking_stability(case["methods"]["cosine"]["top5_ids"],
                                                         case["methods"][m]["top5_ids"]) for m in METHODS}
            scenarios.append(case)
        if before != service.describe():
            raise AssertionError("Fitted state changed")
    audit = audit_snapshot(paths.root)
    source_paths = sorted((paths.root / "src/evaluation").glob("*.py"))
    report = {"run_utc": datetime.now(timezone.utc).isoformat(), "protocol_version": "scoutiq.evaluation.v1",
              "dataset": service.describe()["dataset"], "configuration_id": service.describe()["configuration_id"],
              "reference": prior["reference"], "day10_sha256": digest(prior_path),
              "source_sha256": {**prior["source_sha256"], **{p.relative_to(paths.root).as_posix(): digest(p) for p in source_paths}},
              "environment": {"python": platform.python_version(), "platform": platform.platform(),
                              "packages": {name: version(name) for name in ("numpy", "pandas", "scikit-learn", "pytest", "jsonschema")}},
              "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=paths.root, text=True).strip(),
              "scenarios": scenarios, "checks": checks, "annotation_rows": len(annotations),
              "coverage": {m: catalogue_coverage(per_method[m], pools) for m in METHODS},
              "real_relevance_metrics_status": "UNAVAILABLE: no independent human labels",
              "limitations": ["demo query selection bias", "no temporal split", "Defender/GK context only",
                              "provenance declarations require human audit", "coverage/stability are not relevance quality"]}
    destination.mkdir(parents=True, exist_ok=False)
    for name, obj in (("evaluation.json", report), ("audit_evidence.json", audit), ("synthetic_metrics.json", synthetic_fixture())):
        (destination / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (destination / "annotation_template.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=ANNOTATION_FIELDS)
        writer.writeheader()
        writer.writerows(annotations)
    pd.DataFrame(evidence).to_csv(destination / "annotation_evidence.csv", index=False, encoding="utf-8")
    (destination / "run_summary.md").write_text(
        "# Day 11 — Kết quả runner\n\n"
        f"{len(checks)} kiểm tra Day 10 parity/repeat/filter đạt. {len(annotations)} dòng chưa gán nhãn.\n\n"
        "Relevance thực: chưa có nhãn độc lập; Precision/Recall/NDCG đều null. "
        "synthetic_metrics.json chỉ kiểm công thức SYNTHETIC. Xem evaluation.json/audit_evidence.json.\n",
        encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    result = run(args.output_dir)
    print(f"Day 11: {len(result['checks'])} parity checks; {result['annotation_rows']} UNLABELED rows; no real relevance scores")
