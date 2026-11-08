"""Day 7: reproducible exact KNN comparison and local latency measurements.

No prior outputs are overwritten. Timings are descriptive for this machine/run.
Run: python -B -m src.recommendation.run_day7
"""

from copy import deepcopy
from datetime import datetime, timezone
import argparse
import hashlib
import json
from numbers import Integral
import os
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import pandas as pd
import sklearn
import matplotlib
from threadpoolctl import threadpool_info, threadpool_limits

from src.features.build_features import validate_features
from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, ROOT
from src.recommendation.evaluation import check_response, signature, stability_metrics
from src.recommendation.knn import KNNRecommender
from src.recommendation.run_day5 import SCENARIOS
from src.recommendation.weighted import WeightedCosineRecommender, default_weights

OUTPUT_NAMES = (
    "evaluation.json", "comparisons.csv", "robustness.csv", "timings.csv",
    "benchmark.csv", "rankings.csv", "latency.png", "summary.md",
)
SCORE_TOLERANCE = 1e-11


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compare_results(direct, knn):
    """Strict ordered IDs/count/status; numerical score equality has a tolerance."""
    a, b = direct["results"], knn["results"]
    same_ids = [r["player_id"] for r in a] == [r["player_id"] for r in b]
    score_error = max((abs(x["similarity_score"] - y["similarity_score"])
                       for x, y in zip(a, b)), default=0.0) if same_ids else None
    distance_error = max((abs(row["cosine_distance"] - (1 - row["similarity_score"]))
                          for row in b), default=0.0)
    dot_error = max((abs(row["cosine_distance"] - (1 - sum(row["cosine_components"].values())))
                     for row in b), default=0.0)
    parity = (
        same_ids and score_error <= SCORE_TOLERANCE and distance_error <= SCORE_TOLERANCE
        and dot_error <= SCORE_TOLERANCE
        and all(direct[key] == knn[key] for key in (
            "status", "eligible_count", "excluded_zero_vectors", "filters", "similarity_scope"))
    )
    if not parity:
        raise ValueError(f"KNN parity failed: ids={same_ids}, score={score_error}, distance={distance_error}")
    return {
        "ordered_ids_match": same_ids, "score_max_abs_error": score_error,
        "distance_vs_rounded_score_max_error": distance_error,
        "distance_vs_dot_components_max_error": dot_error, "parity_passed": parity,
    }


def summarize_timings(frame):
    rows = []
    for (representation, scenario, method), group in frame.groupby(
            ["representation", "scenario", "method"], sort=False):
        values = group.elapsed_ms.to_numpy()
        rows.append({
            "representation": representation, "scenario": scenario, "method": method,
            "measured_runs": len(values), "median_ms": float(np.median(values)),
            "p95_ms": float(np.percentile(values, 95, method="linear")),
            "min_ms": float(values.min()), "max_ms": float(values.max()),
        })
    return pd.DataFrame(rows)


def benchmark_pair(methods, query, filters, expected, *, representation, scenario, warmup, repeats):
    """Time the full recommend call; check signatures outside measured interval."""
    names = list(methods)
    records = []
    for _ in range(warmup):
        for name in names:
            methods[name].recommend(query, filters, top_k=5)
    for repeat in range(repeats):
        order = names if repeat % 2 == 0 else names[::-1]
        for slot, name in enumerate(order):
            start = time.perf_counter_ns()
            result = methods[name].recommend(query, filters, top_k=5)
            elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
            if signature(result) != expected[name]:
                raise ValueError("A timed request changed ranking/score")
            records.append({
                "representation": representation, "scenario": scenario,
                "method": name, "repeat": repeat, "order_in_pair": slot,
                "elapsed_ms": elapsed_ms,
            })
    return records


def _plot(benchmark, destination, warmup, repeats):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout="constrained")
    for ax, representation in zip(axes, ("day5", "day6_default")):
        for offset, method, color in [(-.16, "direct", "#238b8e"), (.16, "knn", "#e5a238")]:
            group = benchmark.loc[(benchmark.representation == representation)
                                  & (benchmark.method == method)].set_index("scenario")
            ordered = group.loc[[s[0] for s in SCENARIOS]]
            x = np.arange(len(SCENARIOS)) + offset
            ax.bar(x, ordered.median_ms, width=.3, label=method + " median", color=color)
            ax.scatter(x, ordered.p95_ms, marker="_", s=130, color="black",
                       label="p95" if method == "direct" else None, zorder=3)
        ax.set_xticks(range(5), ["Attack", "Midfield", "Defender*", "GK*", "Empty"], rotation=20)
        ax.set_ylabel("Full recommend latency (ms)")
        ax.set_title(representation + " — same filtered candidates, K=5")
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=8)
    fig.suptitle(f"{warmup} warm-ups + {repeats} alternating repeats; one thread; *context only\n"
                 "Local latency is not scouting quality or a cloud SLA")
    fig.savefig(destination, dpi=160)
    plt.close(fig)


def run(output_dir=ROOT / "reports/day7", *, warmup=5, repeats=50):
    for value, minimum, name in ((warmup, 1, "warmup"), (repeats, 10, "repeats")):
        if isinstance(value, bool) or not isinstance(value, Integral) or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}")
    destination = Path(output_dir)
    if any((destination / name).exists() for name in OUTPUT_NAMES):
        raise FileExistsError("Day 7 output already exists; choose a new --output-dir")
    prior_paths = [FEATURE_FILE, ROOT / "reports/day5_recommendation_examples.json",
                   ROOT / "reports/day6/evaluation.json"]
    hashes = {p.relative_to(ROOT).as_posix(): digest(p) for p in prior_paths}
    day5 = json.loads(prior_paths[1].read_text(encoding="utf-8"))
    day6 = json.loads(prior_paths[2].read_text(encoding="utf-8"))
    if day5["input_sha256"] != digest(FEATURE_FILE) or day6["dataset"]["sha256"] != digest(FEATURE_FILE):
        raise ValueError("Input snapshot differs from Day 5/6")
    if any(digest(ROOT / p) != sha for p, sha in day6["source_sha256"].items()):
        raise ValueError("Day 5/6 source differs from its recorded audit")
    data = pd.read_csv(FEATURE_FILE)
    validate_features(data)
    query_ids = {query for _, query, _ in SCENARIOS}
    fit_ids = data.loc[~data.player_id.isin(query_ids), "player_id"].tolist()
    pairs = {
        "day5": {
            "direct": CosineRecommender(data, fit_player_ids=fit_ids),
            "knn": KNNRecommender(data, fit_player_ids=fit_ids),
        },
        "day6_default": {
            "direct": WeightedCosineRecommender(data, fit_player_ids=fit_ids),
            "knn": KNNRecommender(data, fit_player_ids=fit_ids, weights=default_weights()),
        },
    }
    comparisons, robustness, rankings, top_responses, timings = [], [], [], [], []
    models = {}
    # No tests or other project jobs should be run concurrently with this block.
    with threadpool_limits(limits=1):
        pools = [{key: item.get(key) for key in (
            "user_api", "internal_api", "prefix", "num_threads", "version", "architecture")}
                 for item in threadpool_info()]
        for representation, methods in pairs.items():
            direct, knn = methods["direct"], methods["knn"]
            audit = deepcopy(knn.describe())
            if audit["representation"] != direct.describe():
                raise ValueError("KNN preprocessing/reference differs from direct baseline")
            models[representation] = audit
            weights = None if representation == "day5" else default_weights()
            reversed_knn = KNNRecommender(data.iloc[::-1], fit_player_ids=fit_ids[::-1], weights=weights)
            saved = (day5["scenarios"] if representation == "day5" else
                     [r for r in day6["top_k_responses"] if r["configuration"] == "weighted_default"])
            saved_by_name = {row["scenario"]: row for row in saved}
            for scenario, query, filters in SCENARIOS:
                current_top = direct.recommend(query, filters)
                previous = saved_by_name[scenario]
                if (signature(current_top) != signature(previous)
                        or any(current_top[k] != previous[k] for k in ("filters", "eligible_count", "status"))):
                    raise ValueError("Saved baseline reproduction failed")
                full_direct = direct.recommend(query, filters, top_k=len(data))
                full_knn = knn.recommend(query, filters, top_k=len(data))
                check_response(full_direct, query, filters)
                checks = check_response(full_knn, query, filters)
                parity = compare_results(full_direct, full_knn)
                repeated = knn.recommend(query, filters, top_k=len(data))
                reversed_result = reversed_knn.recommend(query, filters, top_k=len(data))
                deterministic = signature(full_knn) == signature(repeated) == signature(reversed_result)
                if not deterministic:
                    raise ValueError("KNN is not row-order/repeat invariant")
                comparisons.append({
                    "representation": representation, "scenario": scenario,
                    "eligible": full_knn["eligible_count"],
                    "excluded_zero_vectors": full_knn["excluded_zero_vectors"],
                    **checks, **parity, "deterministic": deterministic,
                    **stability_metrics(full_direct, full_knn, k=5),
                })
                for k in (1, 3, 5, 50, 10000):
                    direct_k = direct.recommend(query, filters, top_k=k)
                    knn_k = knn.recommend(query, filters, top_k=k)
                    match = compare_results(direct_k, knn_k)
                    prefix = signature(knn_k) == signature(full_knn)[:k]
                    if not prefix:
                        raise ValueError("KNN Top K is not a prefix of full ranking")
                    robustness.append({
                        "representation": representation, "scenario": scenario, "requested_k": k,
                        "returned": len(knn_k["results"]), "status": knn_k["status"],
                        "top_k_prefix": prefix, **match,
                    })
                expected = {}
                for method, engine in methods.items():
                    top = engine.recommend(query, filters, top_k=5)
                    expected[method] = signature(top)
                    top_responses.append({"representation": representation, "method": method,
                                          "scenario": scenario, **top})
                    full = full_direct if method == "direct" else full_knn
                    for row in full["results"]:
                        rankings.append({
                            "representation": representation, "method": method, "scenario": scenario,
                            **{key: row[key] for key in (
                                "rank", "player_id", "name", "club", "position", "age", "minutes_played",
                                "market_value_in_eur", "similarity_score", "similarity_scope")},
                            "cosine_distance": row.get("cosine_distance"),
                        })
                timings.extend(benchmark_pair(
                    methods, query, filters, expected, representation=representation,
                    scenario=scenario, warmup=warmup, repeats=repeats))
            if knn.describe() != audit:
                raise ValueError("Querying modified the fitted representation")
    if any(digest(ROOT / p) != sha for p, sha in hashes.items()):
        raise ValueError("An input or prior artefact was modified")
    timing_frame = pd.DataFrame(timings)
    benchmark = summarize_timings(timing_frame)
    source_paths = [*day6["source_sha256"], "src/recommendation/knn.py", "src/recommendation/run_day7.py"]
    report = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": day6["dataset"], "prior_input_hashes": hashes,
        "source_sha256": {p: digest(ROOT / p) for p in source_paths},
        "reference": day6["reference"], "models": models,
        "saved_baselines_reproduced": True,
        "environment": {
            "python": platform.python_version(), "os": platform.platform(),
            "processor": platform.processor(), "logical_cpus": os.cpu_count(),
            "numpy": np.__version__, "pandas": pd.__version__, "sklearn": sklearn.__version__,
            "matplotlib": matplotlib.__version__, "threadpools_during_benchmark": pools,
            "clock": "perf_counter_ns", "clock_resolution_seconds": time.get_clock_info("perf_counter").resolution,
        },
        "benchmark_protocol": {
            "warmup_per_method_per_query": warmup, "measured_runs_per_method_per_query": repeats,
            "top_k": 5, "thread_limit": 1, "n_jobs_knn": 1,
            "order": "direct/knn on even repeats; knn/direct on odd repeats",
            "scope": "full recommend including filters, retrieval, sorting, evidence/explanation; "
                     "KNN.fit on filtered encoded vectors included; scaler/category fitting, "
                     "CSV I/O, checks and report writing excluded",
            "pool": "identical filtered nonzero candidates; all neighbors requested before tie handling/K",
            "p95_method": "numpy.percentile(method='linear')",
            "limits": "one local machine/session; OS/background jitter uncontrolled; no concurrency/load "
                      "test, no cold start measurement, no confidence interval or cloud SLA",
        },
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines(),
        "comparisons": comparisons, "robustness": robustness,
        "benchmark": benchmark.to_dict(orient="records"), "top_k_responses": top_responses,
        "metric_limits": {
            "score_tolerance": SCORE_TOLERANCE,
            "overlap": "intersection/K, null when either list empty; not relevance",
            "spearman": "full common candidates, score midranks; null for empty/constant",
            "quality_metrics": "No Precision@K/NDCG@K: trustworthy relevance labels unavailable",
            "defender_goalkeeper": "context_profile_only, no invented skill statistics",
        },
        "inputs_unchanged": True,
    }
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "evaluation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    for filename, frame in (
        ("comparisons.csv", pd.DataFrame(comparisons)), ("robustness.csv", pd.DataFrame(robustness)),
        ("timings.csv", timing_frame), ("benchmark.csv", benchmark), ("rankings.csv", pd.DataFrame(rankings)),
    ):
        frame.to_csv(destination / filename, index=False, encoding="utf-8-sig")
    _plot(benchmark, destination / "latency.png", warmup, repeats)
    lines = [
        "# Day 7 — KNN cosine benchmark và robustness", "",
        "KNN dùng cùng representation, reference và bộ lọc Day 5/6. Không mặc định tốt hơn.",
        f"Warm-up {warmup}, measured {repeats} lần/method/query, thread limit=1, Top K=5.",
        "Đo full recommend; gồm KNN.fit trên pool đã lọc, không gồm fit scaler/đọc CSV/ghi báo cáo.",
        "Kết quả timing thuộc máy/phiên này; không là cloud SLA hoặc chất lượng tuyển trạch.", "",
        "| Representation | Scenario | Method | Median ms | p95 ms |",
        "|---|---|---|---:|---:|",
    ]
    for row in benchmark.itertuples(index=False):
        lines.append(f"| {row.representation} | {row.scenario} | {row.method} | "
                     f"{row.median_ms:.4f} | {row.p95_ms:.4f} |")
    lines += ["", "## Parity và giới hạn", "",
              f"{len(comparisons)} cặp full ranking đạt parity/filter/score/reproducibility; "
              f"{len(robustness)} kiểm tra K=1/3/5/50/10000 đạt.",
              "Nonempty overlap@5=1; empty=N/A. Dùng score tolerance 1e-11, tie round12 rồi ID tăng dần.",
              "Không tính Precision/NDCG khi thiếu labels. Defender/GK chỉ hồ sơ bối cảnh.",
              "Top 5 đầy đủ tên/CLB/giá/score/evidence trong evaluation.json; toàn ranking trong rankings.csv.",
              "Không thay baseline, không đổi dữ liệu. Day 8 dự kiến hoàn thiện bộ lọc hiệu suất và điều kiện biên."]
    (destination / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(benchmark.to_string(index=False))
    print(f"Saved {len(OUTPUT_NAMES)} files; parity={len(comparisons)}, K checks={len(robustness)}, "
          f"timed calls={len(timings)}, ranked rows={len(rankings)}.")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/day7")
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--repeats", type=int, default=50)
    args = parser.parse_args()
    run(args.output_dir, warmup=args.warmup, repeats=args.repeats)

