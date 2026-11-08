"""Day 10 parity, deterministic JSON and local end-to-end service latency."""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import subprocess
from time import perf_counter_ns

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_info, threadpool_limits

from src.recommendation.config import METHODS, ProjectPaths
from src.recommendation.run_day8 import SCENARIOS
from src.recommendation.schemas import REQUEST_SCHEMA, RESPONSE_SCHEMA
from src.recommendation.service import RecommendationService

LEGACY_METHOD = dict(zip(METHODS, ("cosine", "weighted", "knn_cosine", "knn_weighted")))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def scenario_request(query, constraints, method, *, include_comparison=True):
    values = asdict(constraints)
    filters = values.pop("filters")
    filters.update({k: list(v) if isinstance(v, tuple) else v for k, v in values.items()})
    return {"reference_player_id": query, "filters": filters, "method": method,
            "top_k": 5, "include_comparison": include_comparison}


def latency_summary(samples):
    values = np.asarray(samples, dtype=float)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("Expected nonempty finite nonnegative latency samples")
    return {"samples": len(values), "median_ms": float(np.median(values)),
            "p95_ms": float(np.percentile(values, 95, method="linear")),
            "min_ms": float(values.min()), "max_ms": float(values.max())}


def run(output_dir=None, *, features=None, prior_day9=None, prior_day8=None, warmup=3, repeats=20):
    paths = ProjectPaths()
    destination = paths.reports / "day10" if output_dir is None else Path(output_dir)
    if destination.exists(): raise FileExistsError("Choose a new output directory")
    if type(warmup) is not int or warmup < 1 or type(repeats) is not int or repeats < 10:
        raise ValueError("warmup >= 1 and repeats >= 10 must be integers")
    features = paths.features if features is None else Path(features)
    p9 = paths.reports / "day9/evaluation.json" if prior_day9 is None else Path(prior_day9)
    p8 = paths.reports / "day8/evaluation.json" if prior_day8 is None else Path(prior_day8)
    prior9 = json.loads(p9.read_text(encoding="utf-8"))
    prior8 = json.loads(p8.read_text(encoding="utf-8"))
    if digest(features) != prior9["dataset"]["sha256"] or digest(p8) != prior9["prior_input_hashes"]["reports/day8/evaluation.json"]:
        raise ValueError("Dataset or prior Day 8 snapshot differs from Day 9")
    for name, sha in prior9["source_sha256"].items():
        if digest(paths.root / name) != sha: raise ValueError(f"Prior source changed: {name}")
    prior_hashes = {"features": digest(features), "day8": digest(p8), "day9": digest(p9)}
    saved9 = {(c["scenario"], c["engine"]): {k:v for k,v in c.items() if k not in ("scenario", "engine")}
              for c in prior9["examples"]}
    saved8 = {(c["scenario"], c["method"]): {k:v for k,v in c.items() if k not in ("scenario", "method")}
              for c in prior8["scenarios"]}
    jobs = [(name, method, scenario_request(query, constraints, method))
            for name, query, constraints in SCENARIOS for method in METHODS]
    checks, examples, top_rows, timings = [], [], [], []
    with threadpool_limits(limits=1):
        start = perf_counter_ns()
        service = RecommendationService.from_csv(features, fit_player_ids=prior9["reference"]["fit_ids"])
        startup_ms = (perf_counter_ns() - start) / 1e6
        audit_before = service.describe()
        expected = {}
        encoded_inputs = {}
        for name, method, payload in jobs:
            key = (name, method); old_key = (name, LEGACY_METHOD[method])
            text = json.dumps(payload, allow_nan=False)
            encoded_inputs[key] = text
            encoded = service.recommend_json(text)
            response = json.loads(encoded)
            if response["explanation"] != saved9[old_key] or response["explanation"]["recommendation"] != saved8[old_key]:
                raise AssertionError("Day 8/9 full response regression")
            old_comparisons = [{k:v for k,v in g.items() if k not in ("scenario", "engine", "group")}
                               for g in prior9["comparisons"] if (g["scenario"], g["engine"]) == old_key]
            if response["comparisons"] != old_comparisons: raise AssertionError("Day 9 comparison regression")
            expected[key] = encoded
            examples.append({"scenario": name, "response": response})
            checks.append({"scenario": name, "method": method, "status": response["status"],
                           **{k:response["metadata"][k] for k in ("candidate_count", "rankable_count", "returned_count", "top_k")},
                           "day8_exact": True, "day9_exact": True, "comparison_exact": True})
            for row in response["explanation"]["recommendation"]["results"]:
                top_rows.append({"scenario": name, "method": method,
                                 **{k:row[k] for k in ("rank", "player_id", "name", "position", "age", "market_value_in_eur", "minutes_played", "similarity_score")}})
        for cycle in range(warmup + repeats):
            order = jobs[cycle % len(jobs):] + jobs[:cycle % len(jobs)]
            for name, method, _ in order:
                key = (name, method)
                start = perf_counter_ns()
                encoded = service.recommend_json(encoded_inputs[key])
                elapsed = (perf_counter_ns() - start) / 1e6
                if encoded != expected[key]: raise AssertionError("Non-deterministic serialized response")
                if cycle >= warmup:
                    timings.append({"scenario": name, "method": method, "repeat": cycle - warmup,
                                    "elapsed_ms": elapsed, "response_bytes": len(encoded.encode("utf-8"))})
            if cycle in (warmup - 1, warmup + repeats - 1):
                print(f"Latency cycles completed: {cycle + 1}/{warmup + repeats}", flush=True)
        pools = [{k:v for k,v in item.items() if k != "filepath"} for item in threadpool_info()]
    if audit_before != service.describe(): raise AssertionError("Service request mutated fitted state")
    if prior_hashes != {"features": digest(features), "day8": digest(p8), "day9": digest(p9)}:
        raise AssertionError("Inputs changed")
    benchmark = [{"scenario": name, "method": method,
                  **latency_summary([r["elapsed_ms"] for r in timings if (r["scenario"],r["method"]) == (name,method)])}
                 for name, method, _ in jobs]
    report = {"run_utc": datetime.now(timezone.utc).isoformat(), "service": audit_before,
              "reference": prior9["reference"], "prior_input_hashes": prior_hashes,
              "source_sha256": {p.relative_to(paths.root).as_posix(): digest(p) for p in sorted((paths.root / "src/recommendation").glob("*.py"))},
              "environment": {"python": platform.python_version(), "os": platform.platform(),
                  "packages": {p:version(p) for p in ("numpy", "pandas", "scikit-learn", "jsonschema", "threadpoolctl")}, "threadpools": pools},
              "protocol": {"warmup_per_case": warmup, "repeats_per_case": repeats,
                  "order": "rotate 20 scenario-method cases each cycle", "threadpool_limit": 1,
                  "measured": "JSON parse + schema/semantic request validation + hard filters + ranking + Top K + evidence/text + comparisons + response validation + JSON serialization",
                  "excluded": "CSV loading, catalogue validation, fitting, startup, file I/O, network/HTTP/auth; no caching of request results",
                  "percentile": "numpy linear p95", "startup_ms_one_observation": startup_ms},
              "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=paths.root, text=True).strip(),
              "checks": checks, "examples": examples, "benchmark": benchmark,
              "reproducible_json": True, "fit_unchanged": True,
              "limitations": ["Latency measured locally, not cloud SLA or throughput", "No relevance labels, no Precision/NDCG",
                              "Defender/GK context only; similarity is not transfer probability", "No FastAPI endpoint/auth/privacy/cloud"]}
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in (("evaluation.json", report), ("request.schema.json", REQUEST_SCHEMA), ("response.schema.json", RESPONSE_SCHEMA)):
        (destination / name).write_text(json.dumps(data, ensure_ascii=False, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    for name, rows in (("checks.csv", checks), ("top5.csv", top_rows), ("timings.csv", timings), ("benchmark.csv", benchmark)):
        pd.DataFrame(rows).to_csv(destination / name, index=False, encoding="utf-8")
    lines = ["# Day 10 — Integration & Local Service Latency", "",
             "20/20 full Day 8 responses + Day 9 explanations/comparisons exact. No new weights or model selection.",
             "JSON responses reproducible; state/input hashes unchanged. Dataset 4,112 x 28; fit 4,108; cutoff 2026-06-12.", "",
             f"Warm-up {warmup}/case; {repeats} measurements/case; {len(timings)} measured calls. One thread, rotating order.",
             "Full recommend_json includes optional comparisons and response validation; excludes startup/CSV/network.",
             f"Startup (single observation): {startup_ms:.3f} ms. Local latency, not cloud performance/scouting quality.", "",
             "| Scenario | Method | Candidates | Returned | Median ms | p95 ms |", "|---|---|---:|---:|---:|---:|"]
    for check, bench in zip(checks, benchmark):
        lines.append(f"| {check['scenario']} | {check['method']} | {check['candidate_count']} | {check['returned_count']} | {bench['median_ms']:.3f} | {bench['p95_ms']:.3f} |")
    lines += ["", "## Top 5 weighted cosine", "", "| Scenario | Rank | ID | Player | Score |", "|---|---:|---:|---|---:|"]
    for r in top_rows:
        if r["method"] == "weighted_cosine":
            lines.append(f"| {r['scenario']} | {r['rank']} | {r['player_id']} | {r['name']} | {r['similarity_score']:.6f} |")
    lines += ["", "No-results: 0 candidates/results/comparisons; constraints remain unchanged.",
              "See evaluation.json for full request/evidence/text/comparisons, hashes and environment; request.schema.json/response.schema.json for contracts.",
              "No API calls/endpoints, no commit/push/deploy. Phase review and limits: "
              f"[phase_review.md]({Path(os.path.relpath(paths.reports / 'day10/phase_review.md', destination)).as_posix()})."]
    (destination / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(pd.DataFrame(benchmark).to_string(index=False), flush=True)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--features", type=Path)
    parser.add_argument("--prior-day9", type=Path)
    parser.add_argument("--prior-day8", type=Path)
    parser.add_argument("--warmup", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=20)
    run(**vars(parser.parse_args()))
