"""Day 9 evidence/comparison runner; old artefacts and engine code stay intact."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess

import numpy as np
import pandas as pd
import sklearn

from src.recommendation.baseline import FEATURE_FILE, ROOT
from src.recommendation.comparison import PlayerComparison
from src.recommendation.constraints import AdvancedRecommender
from src.recommendation.explainability import RecommendationExplainer, render_explanation
from src.recommendation.run_day8 import SCENARIOS, make_engines


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plot_comparison(comparison, path):
    import matplotlib.pyplot as plt
    people = comparison["players"]
    names = [p["values"]["name"] for p in people]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), layout="constrained")
    for ax, metric in zip(axes, ("goals_per90", "assists_per90", "minutes_played")):
        rows = [r for r in comparison["numeric_differences"] if r["metric"] == metric]
        ax.barh(range(len(names)), [r["value"] for r in rows],
                color=["#d28a20"] + ["#277c9e"] * (len(names) - 1))
        ax.set_yticks(range(len(names)), names)
        ax.invert_yaxis()
        ax.set_xlabel(rows[0]["unit"])
        ax.set_title(metric)
    fig.suptitle("ScoutIQ Day 9 | Reference (orange) + Top 4 weighted candidates\n"
                 "Cutoff 2026-06-12 | Descriptive comparison, no overall winner; fifth candidate in tables")
    fig.savefig(path, dpi=150)
    plt.close(fig)


def run(output_dir=ROOT / "reports/day9"):
    destination = Path(output_dir)
    if destination.exists():
        raise FileExistsError("Choose a new --output-dir; prior outputs must be preserved")
    prior_path = ROOT / "reports/day8/evaluation.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    if digest(FEATURE_FILE) != prior["dataset"]["sha256"]:
        raise ValueError("Snapshot differs from Day 8")
    for p, sha in prior["source_sha256"].items():
        if digest(ROOT / p) != sha:
            raise ValueError(f"Day 5-8 source changed: {p}")
    before_hashes = {p.relative_to(ROOT).as_posix(): digest(p) for p in (FEATURE_FILE, prior_path)}
    data = pd.read_csv(FEATURE_FILE)
    engines = make_engines(data, prior["reference"]["fit_ids"])
    audits = {k: e.describe() for k, e in engines.items()}
    comparer = PlayerComparison(data)
    saved = {(r["scenario"], r["method"]): {k: v for k, v in r.items() if k not in ("scenario", "method")}
             for r in prior["scenarios"]}
    examples, groups, top_rows, features, differences, checks = [], [], [], [], [], []
    chart_comparison = None
    for scenario, query, constraints in SCENARIOS:
        for method, engine in engines.items():
            presenter = RecommendationExplainer(AdvancedRecommender(engine))
            output = presenter.recommend(query, constraints, top_k=5)
            if output["recommendation"] != saved[(scenario, method)]:
                raise ValueError("Day 8 response regression, including score/rank/eligibility")
            ids = [r["player_id"] for r in output["recommendation"]["results"]]
            examples.append({"scenario": scenario, "engine": method, **output})
            for explanation in output["explanations"]:
                ev = explanation["evidence"]
                if explanation["text"] != render_explanation(ev):
                    raise ValueError("Text is not grounded in evidence")
                p = ev["candidate"]["values"]
                top_rows.append({"scenario": scenario, "engine": method, "rank": ev["rank"],
                                 **p, "similarity_score": ev["similarity"]["score"],
                                 "similarity_method": ev["similarity"]["method"],
                                 "scope": ev["scope"], "text": explanation["text"]})
                for feature in ev["selected_features"]:
                    features.append({"scenario": scenario, "engine": method, "player_id": p["player_id"],
                                     "reference_player_id": query,
                                     **{k: v for k, v in feature.items() if k not in ("difference", "encoded_components")},
                                     **feature.get("difference", {})})
            # Maximum five players including reference. Cover fifth result in a second pair.
            selections = [[query] + ids[:4]] if ids else []
            if len(ids) == 5:
                selections.append([query, ids[4]])
            for number, selection in enumerate(selections, 1):
                comparison = comparer.compare(selection, reference_player_id=query)
                group = {"scenario": scenario, "engine": method, "group": number, **comparison}
                groups.append(group)
                differences.extend({"scenario": scenario, "engine": method, "group": number, **r}
                                   for r in comparison["numeric_differences"])
                if scenario == "young_low_budget_striker" and method == "weighted" and number == 1:
                    chart_comparison = comparison
            checks.append({"scenario": scenario, "engine": method, "status": output["status"],
                           "eligible": output["recommendation"]["eligible_count"], "returned": len(ids),
                           "explanations": len(output["explanations"]), "comparison_groups": len(selections),
                           "day8_response_exact": True, "text_from_evidence": True})
    if audits != {k: e.describe() for k, e in engines.items()}:
        raise ValueError("Presentation mutated fitted engines")
    for p, sha in before_hashes.items():
        if digest(ROOT / p) != sha:
            raise ValueError("Input changed")
    sources = sorted((ROOT / "src/recommendation").glob("*.py"))
    report = {"run_utc": datetime.now(timezone.utc).isoformat(), "dataset": prior["dataset"],
              "reference": prior["reference"], "prior_input_hashes": before_hashes,
              "source_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
              "environment": {"python": platform.python_version(), "os": platform.platform(),
                              "pandas": pd.__version__, "numpy": np.__version__, "sklearn": sklearn.__version__},
              "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "checks": checks, "examples": examples, "comparisons": groups,
              "inputs_and_fit_unchanged": True, "no_api_calls": True,
              "limitations": ["No relevance labels/temporal evaluation", "Context-only Defender/GK",
                              "Relative percentages null for zero reference", "No overall player winner",
                              "Comparison groups include reference + Top 4, then reference + fifth result"]}
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "evaluation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    for filename, records in (("checks.csv", checks), ("top5.csv", top_rows),
                              ("feature_evidence.csv", features), ("comparisons.csv", differences)):
        pd.DataFrame(records).to_csv(destination / filename, index=False, encoding="utf-8")
    plot_comparison(chart_comparison, destination / "attack_comparison.png")
    lines = ["# Day 9 — Explainability & Player Comparison", "",
             "20 responses khớp nguyên Day 8; 80 structured explanations. Không thay score/ranking/scaler/eligibility.",
             "Snapshot 2025/26, cutoff 2026-06-12; fit 4.108/4.112 loại 4 query, không temporal split.",
             "Evidence tách text; JSON sẵn cho tích hợp sau này, chưa gọi API. Không similarity-as-probability.", "",
             "So sánh tối đa 5 người gồm reference + Top 4; người thứ 5 có pair riêng. Delta=candidate-reference; relative=100*delta/abs(reference), null nếu reference=0.", ""]
    for example in examples:
        if example["engine"] != "weighted":
            continue
        lines += [f"## {example['scenario']} — {example['reference']['values']['name']}", "",
                  f"Status: {example['status']}; eligible={example['recommendation']['eligible_count']}.", "",
                  "| Rank | ID | Tên | EUR | Cosine |", "|---|---|---|---:|---:|"]
        for item in example["explanations"]:
            ev = item["evidence"]; p = ev["candidate"]["values"]
            lines.append(f"| {ev['rank']} | {p['player_id']} | {p['name']} | {p['market_value_in_eur']:,.0f} | {ev['similarity']['score']:.6f} |")
        lines += [""] + ["- " + x["text"] for x in example["explanations"]] + [""]
        group = next((c for c in groups if c["scenario"] == example["scenario"] and c["engine"] == "weighted" and c["group"] == 1), None)
        if group:
            lines += ["So sánh (reference + Top 4; ID liên kết tên trong bảng/JSON):", "",
                      "| ID | Metric | Value | Reference | Signed delta | Relative % | Unit |",
                      "|---|---|---:|---:|---:|---:|---|"]
            for r in group["numeric_differences"]:
                if r["player_id"] == group["reference_player_id"]:
                    continue
                pct = "N/A: " + str(r["relative_reason"]) if r["relative_difference_pct"] is None else f"{r['relative_difference_pct']:.3f}"
                lines.append(f"| {r['player_id']} | {r['metric']} | {r['value']:.6g} | {r['reference_value']:.6g} | {r['signed_difference']:.6g} | {pct} | {r['unit']} |")
        else:
            lines.append("Không có ứng viên: explanations/comparisons rỗng, không thêm cầu thủ hoặc nới constraints.")
        lines += ["", *["- " + limit for limit in example["limitations"]], ""]
    lines += ["## Biểu đồ", "", "![Reference và Top 4 Attack](attack_comparison.png)", "",
              "## Giới hạn và Day 10", "", "Không tổng hợp thành điểm chất lượng, không causal attribution. Defender/GK và mixed positions chỉ so context.",
              "Metadata CLB/foot thiếu, league effects và temporal validity còn hạn chế. Day 10 dự kiến tích hợp recommendation engine; chưa triển khai."]
    (destination / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(pd.DataFrame(checks).to_string(index=False))
    print("Saved", destination, "explanations=", len(top_rows), "comparisons=", len(groups))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/day9")
    run(parser.parse_args().output_dir)
