"""Run controlled Day 6 experiments without rewriting any Day 4/5 artefact.

python -B -m src.recommendation.run_day6
Existing output files require explicit --overwrite; --output-dir permits a new run.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess

import numpy as np
import pandas as pd
import sklearn

from src.features.build_features import CUTOFF, quality_summary, validate_features
from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, ROOT
from src.recommendation.evaluation import check_response, signature, stability_metrics
from src.recommendation.run_day5 import SCENARIOS
from src.recommendation.weighted import (
    WeightedCosineRecommender, experiment_weights, unit_weights,
)

OUTPUT_NAMES = (
    "evaluation.json", "metrics.csv", "rankings.csv", "correlations.csv",
    "comparison.png", "correlations.png", "summary.md",
)
CORRELATION_COLUMNS = (
    "goals", "assists", "goal_contributions", "goals_per90", "assists_per90",
    "goal_contributions_per90", "minutes_played", "minutes_reliability", "age",
    "goals_per90_position_percentile", "assists_per90_position_percentile",
    "goal_contributions_per90_position_percentile",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def correlation_audit(reference):
    """Descriptive audit on the same fit-only reference, never feature selection on queries."""
    rows = []
    for position, group in reference.groupby("position", sort=True):
        values = group[list(CORRELATION_COLUMNS)]
        pearson, spearman = values.corr(), values.corr(method="spearman")
        for i, left in enumerate(CORRELATION_COLUMNS):
            for right in CORRELATION_COLUMNS[i + 1:]:
                p, s = pearson.loc[left, right], spearman.loc[left, right]
                rows.append({
                    "position": position, "fit_players": len(group),
                    "feature_a": left, "feature_b": right,
                    "pearson": None if pd.isna(p) else float(p),
                    "spearman": None if pd.isna(s) else float(s),
                    "undefined_reason": "constant_feature" if pd.isna(p) else None,
                    "high_pearson_abs_ge_0_8": bool(pd.notna(p) and abs(p) >= .8),
                })
    return pd.DataFrame(rows)


def _plots(metrics, reference, destination):
    import matplotlib.pyplot as plt

    scenarios = [name for name, _, _ in SCENARIOS[:4]]
    configs = list(dict.fromkeys(metrics.configuration))
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout="constrained")
    for ax, metric, title, vmin in zip(
        axes, ("overlap_at_k", "spearman_full_common"),
        ("Top-5 overlap vs Day 5 (stability only)", "Spearman: full common pool, score ties averaged"),
        (0, -1),
    ):
        matrix = metrics.pivot(index="configuration", columns="scenario", values=metric).loc[configs, scenarios]
        im = ax.imshow(matrix.to_numpy(dtype=float), vmin=vmin, vmax=1, cmap="viridis", aspect="auto")
        ax.set_xticks(range(4), ["Attack", "Midfield", "Defender*", "GK*"])
        ax.set_yticks(range(len(configs)), configs)
        for i in range(len(configs)):
            for j in range(4):
                v = matrix.iloc[i, j]
                ax.text(j, i, "N/A" if pd.isna(v) else f"{v:.3f}", ha="center", va="center",
                        color="black" if v > .6 else "white")
        ax.set_title(title, fontsize=10)
        fig.colorbar(im, ax=ax, shrink=.8)
    fig.suptitle("Same snapshot, reference split and filters; *context profiles, not skill", fontsize=11)
    fig.savefig(destination / "comparison.png", dpi=160)
    plt.close(fig)

    columns = list(CORRELATION_COLUMNS[:9])
    labels = ["goals", "assists", "G+A", "goals/90", "assists/90", "G+A/90", "minutes", "reliability", "age"]
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), layout="constrained")
    for ax, (position, group) in zip(axes.flat, reference.groupby("position", sort=True)):
        corr = group[columns].corr().to_numpy()
        im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(range(len(columns)), labels, rotation=55, ha="right", fontsize=8)
        ax.set_yticks(range(len(columns)), labels, fontsize=8)
        ax.set_title(f"{position}: fit n={len(group)}")
        for i in range(len(columns)):
            for j in range(len(columns)):
                v = corr[i, j]
                ax.text(j, i, "NA" if np.isnan(v) else f"{v:.1f}", ha="center", va="center", fontsize=6)
    fig.colorbar(im, ax=list(axes.flat), shrink=.7, label="Pearson correlation")
    fig.suptitle("Redundancy audit on reference only; correlation is not causation\n"
                 "Diagnostic columns are not all model features; no goalkeeper skill inferred")
    fig.savefig(destination / "correlations.png", dpi=160)
    plt.close(fig)


def run(output_dir=ROOT / "reports/day6", *, overwrite=False):
    destination = Path(output_dir)
    existing = [name for name in OUTPUT_NAMES if (destination / name).exists()]
    if existing and not overwrite:
        raise FileExistsError(f"Existing outputs {existing}; choose --output-dir or explicit --overwrite")
    before = digest(FEATURE_FILE)
    historical_path = ROOT / "reports/day5_recommendation_examples.json"
    historical_hash = digest(historical_path)
    old = json.loads(historical_path.read_text(encoding="utf-8"))
    if old["input_sha256"] != before:
        raise ValueError("Dataset differs from saved Day 5 snapshot; do not silently change baseline")
    data = pd.read_csv(FEATURE_FILE)
    validate_features(data)
    queries = {query for _, query, _ in SCENARIOS}
    fit_ids = data.loc[~data.player_id.isin(queries), "player_id"].tolist()
    baseline = CosineRecommender(data, fit_player_ids=fit_ids)
    old_scenarios = {row["scenario"]: row for row in old["scenarios"]}
    reproduction = []
    for name, query, filters in SCENARIOS:
        current, previous = baseline.recommend(query, filters), old_scenarios[name]
        equal = (signature(current) == signature(previous) and
                 all(current[key] == previous[key] for key in ("eligible_count", "status", "filters")) and
                 baseline.describe() == old["model"])
        if not equal:
            raise ValueError(f"Day 5 reproduction mismatch: {name}")
        reproduction.append({"scenario": name, "exact_ids_scores_filters_fit_match": True})

    configurations = {"baseline": None, **experiment_weights()}
    engines = {"baseline": baseline}
    for name, weights in configurations.items():
        if weights is not None:
            engines[name] = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=weights)
    reference = data.loc[data.player_id.isin(fit_ids)]
    correlations = correlation_audit(reference)
    metrics, rankings, responses = [], [], []
    full_baseline = {name: baseline.recommend(query, filters, top_k=len(data))
                     for name, query, filters in SCENARIOS}
    unit_engine = WeightedCosineRecommender(data, fit_player_ids=fit_ids, weights=unit_weights())
    for name, query, filters in SCENARIOS:
        if signature(unit_engine.recommend(query, filters, top_k=len(data))) != signature(full_baseline[name]):
            raise ValueError("Unit weights changed Day 5 ranking or score")

    audits = {}
    for config_name, engine in engines.items():
        weights = configurations[config_name]
        shuffled = (CosineRecommender(data.iloc[::-1], fit_player_ids=fit_ids[::-1])
                    if weights is None else WeightedCosineRecommender(
                        data.iloc[::-1], fit_player_ids=fit_ids[::-1], weights=weights))
        audit_before = deepcopy(engine.describe())
        audits[config_name] = audit_before
        for name, query, filters in SCENARIOS:
            full = engine.recommend(query, filters, top_k=len(data))
            checks = check_response(full, query, filters)
            repeat = engine.recommend(query, filters, top_k=len(data))
            reversed_rows = shuffled.recommend(query, filters, top_k=len(data))
            deterministic = (
                signature(full) == signature(repeat) == signature(reversed_rows)
                and full["status"] == repeat["status"] == reversed_rows["status"])
            if not deterministic:
                raise ValueError(f"Nondeterministic ranking: {config_name}/{name}")
            top = engine.recommend(query, filters, top_k=5)
            if signature(top) != signature(full)[:5]:
                raise ValueError("Top K not a prefix of full ranking")
            stats = stability_metrics(full_baseline[name], full, k=5)
            metrics.append({
                "configuration": config_name, "scenario": name, "position": filters.position,
                "scope": full["similarity_scope"], "eligible": full["eligible_count"],
                "excluded_zero_vectors": full["excluded_zero_vectors"], "status": full["status"],
                **checks, "deterministic": deterministic, **stats,
            })
            responses.append({"configuration": config_name, "scenario": name, **top})
            for row in full["results"]:
                rankings.append({
                    "configuration": config_name, "scenario": name, "query_id": query,
                    **{key: row[key] for key in (
                        "rank", "player_id", "name", "club", "position", "age", "minutes_played",
                        "market_value_in_eur", "similarity_score", "similarity_scope")},
                })
        if engine.describe() != audit_before:
            raise ValueError("Search changed fitted parameters")
    if digest(FEATURE_FILE) != before or digest(historical_path) != historical_hash:
        raise ValueError("An input or historical report changed during evaluation")
    metric_frame = pd.DataFrame(metrics)
    source_paths = [
        "src/features/build_features.py", "src/recommendation/baseline.py",
        "src/recommendation/run_day5.py", "src/recommendation/weighted.py",
        "src/recommendation/evaluation.py", "src/recommendation/run_day6.py",
    ]
    report = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python -B -m src.recommendation.run_day6",
        "output_directory": str(destination.resolve()),
        "dataset": {"path": FEATURE_FILE.relative_to(ROOT).as_posix(), "sha256": before,
                    "cutoff": str(CUTOFF.date()), "season": "2025/26", **quality_summary(data)},
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "pandas": pd.__version__, "numpy": np.__version__,
                        "scikit_learn": sklearn.__version__},
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_status": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines(),
        "source_sha256": {path: digest(ROOT / path) for path in source_paths},
        "reference": {"fit_count": len(fit_ids), "excluded_query_ids": sorted(queries),
                      "selection": "all catalogue IDs except the four scenario queries",
                      "not_temporal_evaluation": True},
        "baseline_reproduction": reproduction, "unit_weights_exact_full_ranking_match": True,
        "configuration_weights": configurations, "models": audits,
        "metrics_definition": {
            "overlap_at_k": "size(intersection(topK_baseline, topK_variant))/K; null if either list empty",
            "spearman_full_common": "Pearson correlation of average ranks of rounded scores on common "
                                    "full rankable pool; null if <2 players or constant ranks",
            "null_metrics": "Undefined is not 0 or perfect stability; empty filters are checked vacuously",
            "quality_metrics": "Precision@K/NDCG@K not computed: no trustworthy relevance labels",
            "conclusion_scope": "Behaviour and sensitivity only; stability does not establish scouting quality",
        },
        "metrics": metrics, "top_k_responses": responses,
        "input_and_day5_report_unchanged": True,
        "correlation_audit": {"scope": "fit-only, separately by position", "rows": len(correlations),
                              "flag_threshold": "abs(Pearson)>=0.8; descriptive, not causal",
                              "exact_dependency": "goal_contributions_per90 = goals_per90 + assists_per90",
                              "reliability": "min(minutes/2700,1), heuristic, not a skill feature or multiplier"},
    }
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "evaluation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    metric_frame.to_csv(destination / "metrics.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(rankings).to_csv(destination / "rankings.csv", index=False, encoding="utf-8-sig")
    correlations.to_csv(destination / "correlations.csv", index=False, encoding="utf-8-sig")
    _plots(metric_frame, reference, destination)
    lines = [
        "# Day 6 — Weighted cosine: hành vi và độ nhạy", "",
        f"Dataset: {before}; cutoff {CUTOFF.date()}; {len(data)} cầu thủ; fit {len(fit_ids)}, loại 4 query.",
        "Tái lập chính xác Day 5 (5 kịch bản); weights=1 khớp toàn bộ thứ hạng/score baseline.",
        "Không có relevance labels: không tính Precision@K/NDCG@K. Ổn định không phải chất lượng scouting.", "",
        "| Cấu hình | Truy vấn | Overlap@5 | Spearman full common | Eligible | Trả Top K |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in metrics:
        overlap = "N/A" if row["overlap_at_k"] is None else f"{row['overlap_at_k']:.2f}"
        rho = "N/A" if row["spearman_full_common"] is None else f"{row['spearman_full_common']:.4f}"
        lines.append(f"| {row['configuration']} | {row['scenario']} | {overlap} | {rho} | "
                     f"{row['eligible']} | {row['returned_at_k']} |")
    lines += ["", "Bộ lọc/score/order kiểm trên toàn bộ kết quả; deterministic kiểm lặp và đảo dòng/fit IDs.",
              "Defender/GK chỉ context_profile_only. Metadata CLB chưa xác minh tại cutoff.", "",
              "## Top 5 weighted_default (tham số và toàn bộ cấu hình trong evaluation.json)", ""]
    for response in responses:
        if response["configuration"] != "weighted_default":
            continue
        lines += [f"### {response['scenario']} — {response['reference']['name']}", "",
                  f"Filters: {json.dumps(response['filters'], ensure_ascii=False)}", "",
                  "| Hạng | ID | Tên | CLB | Tuổi | Phút | EUR | Score |",
                  "|---|---|---|---|---:|---:|---:|---:|"]
        for row in response["results"]:
            lines.append(f"| {row['rank']} | {row['player_id']} | {row['name']} | "
                         f"{row['club'] or 'Thiếu'} | {row['age']} | {row['minutes_played']} | "
                         f"{row['market_value_in_eur']:,.0f} | {row['similarity_score']:.6f} |")
        lines.append("")
    (destination / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(metric_frame[["configuration", "scenario", "overlap_at_k", "spearman_full_common"]].to_string(index=False))
    print(f"Saved {len(OUTPUT_NAMES)} outputs to {destination}; {len(rankings)} ranked rows; inputs unchanged.")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/day6")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace existing Day 6 outputs")
    args = parser.parse_args()
    run(args.output_dir, overwrite=args.overwrite)

