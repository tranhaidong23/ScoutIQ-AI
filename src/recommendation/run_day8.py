"""Run real-data advanced-search scenarios without replacing prior artefacts."""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess

import numpy as np
import pandas as pd
import sklearn

from src.features.build_features import validate_features
from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, ROOT, SearchFilters
from src.recommendation.constraints import AdvancedRecommender, SearchConstraints
from src.recommendation.evaluation import signature
from src.recommendation.knn import KNNRecommender
from src.recommendation.run_day5 import SCENARIOS as LEGACY_SCENARIOS
from src.recommendation.weighted import WeightedCosineRecommender, default_weights


SCENARIOS = (
    ("young_low_budget_striker", 132098, SearchConstraints(
        SearchFilters("Attack", 18, 23, 5_000_000, 1200),
        sub_positions=("Centre-Forward",), min_goals_per90=.3,
        preferred_foot="left", foot_mode="soft", excluded_club_ids=(27,))),
    ("creative_midfielder", 137576, SearchConstraints(
        SearchFilters("Midfield", 20, 29, 10_000_000, 1200),
        sub_positions=("Attacking Midfield",), min_assists_per90=.15,
        preferred_foot="left", excluded_club_ids=(2282,))),
    ("experienced_defender", 139208, SearchConstraints(
        SearchFilters("Defender", 28, 35, 5_000_000, 2000),
        sub_positions=("Centre-Back",), preferred_foot="right", excluded_club_ids=(31,))),
    ("budget_goalkeeper", 629773, SearchConstraints(
        SearchFilters("Goalkeeper", 20, 30, 3_000_000, 1800),
        sub_positions=("Goalkeeper",), preferred_foot="right", excluded_club_ids=(1075,))),
    ("no_results", 132098, SearchConstraints(
        SearchFilters("Attack", 18, 23, 0, 1200), sub_positions=("Centre-Forward",),
        min_goals_per90=.3, preferred_foot="left")),
)
OUTPUTS = ("evaluation.json", "scenarios.csv", "filter_stages.csv", "top5.csv", "rankings.csv", "summary.md")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make_engines(data, fit_ids):
    return {
        "cosine": CosineRecommender(data, fit_player_ids=fit_ids),
        "weighted": WeightedCosineRecommender(data, fit_player_ids=fit_ids),
        "knn_cosine": KNNRecommender(data, fit_player_ids=fit_ids),
        "knn_weighted": KNNRecommender(data, fit_player_ids=fit_ids, weights=default_weights()),
    }


def independent_eligible_ids(data, query, constraints):
    """Row-wise contract oracle, independent of the production staged mask."""
    f = constraints.filters
    ids = []
    for r in data.itertuples(index=False):
        if r.player_id == query or r.position != f.position:
            continue
        if not f.min_age <= r.age <= f.max_age or r.minutes_played < f.min_minutes:
            continue
        if f.max_budget_eur is not None and not r.market_value_in_eur <= f.max_budget_eur:
            continue
        if constraints.sub_positions and r.sub_position not in constraints.sub_positions:
            continue
        if constraints.min_goals_per90 is not None and not r.goals_per90 >= constraints.min_goals_per90:
            continue
        if constraints.min_assists_per90 is not None and not r.assists_per90 >= constraints.min_assists_per90:
            continue
        if constraints.preferred_foot and constraints.foot_mode == "hard":
            if pd.isna(r.foot) or r.foot != constraints.preferred_foot:
                continue
        if constraints.excluded_club_ids and (
                pd.isna(r.current_club_id) or r.current_club_id in constraints.excluded_club_ids):
            continue
        ids.append(int(r.player_id))
    return set(ids)


def run(output_dir=ROOT / "reports/day8"):
    destination = Path(output_dir)
    if destination.exists():
        raise FileExistsError("Choose a new --output-dir; Day 8 never overwrites an existing directory")
    prior_paths = [FEATURE_FILE, ROOT / "reports/day5_recommendation_examples.json",
                   ROOT / "reports/day6/evaluation.json", ROOT / "reports/day7/evaluation.json"]
    prior_hashes = {p.relative_to(ROOT).as_posix(): digest(p) for p in prior_paths}
    day7 = json.loads(prior_paths[-1].read_text(encoding="utf-8"))
    if day7["dataset"]["sha256"] != digest(FEATURE_FILE):
        raise ValueError("Dataset differs from Day 7")
    for name, sha in day7["source_sha256"].items():
        if digest(ROOT / name) != sha:
            raise ValueError(f"Prior source changed: {name}")
    data = pd.read_csv(FEATURE_FILE)
    validate_features(data)
    queries = {q for _, q, _ in SCENARIOS}
    fit_ids = data.loc[~data.player_id.isin(queries), "player_id"].tolist()
    engines = make_engines(data, fit_ids)
    wrappers = {name: AdvancedRecommender(engine) for name, engine in engines.items()}
    audits = {name: engine.describe() for name, engine in engines.items()}
    # No advanced constraints: preserve the existing public engine behaviour.
    legacy_checks = []
    for method, engine in engines.items():
        for name, query, filters in LEGACY_SCENARIOS:
            expected = engine.recommend(query, filters, top_k=10000)
            actual = wrappers[method].recommend(query, SearchConstraints(filters), top_k=10000)
            if signature(expected) != signature(actual):
                raise ValueError("Legacy ranking regression")
            legacy_checks.append({"method": method, "scenario": name, "exact_ranking_score": True})
    responses, summaries, stages, rankings, top_rows = [], [], [], [], []
    for scenario, query, constraints in SCENARIOS:
        expected_ids = independent_eligible_ids(data, query, constraints)
        same_query = {}
        for method, wrapper in wrappers.items():
            full = wrapper.recommend(query, constraints, top_k=10000)
            top = wrapper.recommend(query, constraints, top_k=5)
            repeated = wrapper.recommend(query, constraints, top_k=5)
            if full["eligible_count"] != len(expected_ids):
                raise ValueError("Independent hard-filter counts disagree")
            ids = {r["player_id"] for r in full["results"]}
            if not ids <= expected_ids or len(ids) != len(full["results"]):
                raise ValueError("Hard filter/unique-ID contract failed")
            if signature(top) != signature(full)[:5] or signature(top) != signature(repeated):
                raise ValueError("Top K or repeat regression")
            for r in full["results"]:
                if not np.isfinite(r["similarity_score"]) or not -1 <= r["similarity_score"] <= 1:
                    raise ValueError("Invalid cosine score")
                if abs(sum(r["cosine_components"].values()) - r["similarity_score"]) > 1e-10:
                    raise ValueError("Evidence does not sum to score")
            rank_key = lambda r: (-r["similarity_score"], -int(r["soft_preference_match"]), r["player_id"])
            if full["results"] != sorted(full["results"], key=rank_key):
                raise ValueError("Deterministic ordering contract failed")
            same_query[method] = full
            record = {"scenario": scenario, "method": method, **top}
            responses.append(record)
            summaries.append({"scenario": scenario, "method": method,
                              "catalogue_before": len(data),
                              "position_before": int(data.position.eq(constraints.filters.position).sum()),
                              "after_hard": len(expected_ids), "rankable": len(ids),
                              "returned": len(top["results"]), "status": top["status"],
                              "filter_correct": True, "score_valid": True,
                              "deterministic": True, "prefix_correct": True})
            stages.extend({"scenario": scenario, "method": method, **stage}
                          for stage in top["filter_audit"]["stages"])
            for r in full["results"]:
                row = {"scenario": scenario, "method": method, "rank": r["rank"],
                       "player_id": r["player_id"], "name": r["name"], "club": r["club"],
                       "position": r["position"], **r["constraint_evidence"],
                       "similarity_score": r["similarity_score"],
                       "soft_preference_match": r["soft_preference_match"], "explanation": r["explanation"]}
                rankings.append(row)
                if r["rank"] <= 5:
                    top_rows.append(row)
        for direct, knn in (("cosine", "knn_cosine"), ("weighted", "knn_weighted")):
            if signature(same_query[direct]) != signature(same_query[knn]):
                raise ValueError("Direct/KNN parity failed")
    if audits != {name: engine.describe() for name, engine in engines.items()}:
        raise ValueError("Search mutated fitted engine")
    if prior_hashes != {p.relative_to(ROOT).as_posix(): digest(p) for p in prior_paths}:
        raise ValueError("Input artefact changed")
    source_paths = sorted((ROOT / "src/recommendation").glob("*.py"))
    report = {
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python -B -m src.recommendation.run_day8 --output-dir <new directory>",
        "dataset": {"path": FEATURE_FILE.relative_to(ROOT).as_posix(), "sha256": digest(FEATURE_FILE),
                    "rows": len(data), "columns": len(data.columns), "season": "2025/26", "cutoff": "2026-06-12"},
        "environment": {"python": platform.python_version(), "os": platform.platform(),
                        "numpy": np.__version__, "pandas": pd.__version__, "sklearn": sklearn.__version__},
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "prior_input_hashes": prior_hashes,
        "source_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in source_paths},
        "reference": {"fit_count": len(fit_ids), "query_ids_excluded": sorted(queries),
                      "fit_ids": fit_ids, "temporal_split": False},
        "engines_before_and_after_unchanged": audits, "legacy_checks": legacy_checks,
        "direct_knn_full_parity": True, "inputs_unchanged": True,
        "scenarios": responses,
        "limitations": ["No relevance labels or scouting-quality metrics", "Defender/GK context only",
                        "Soft foot only breaks equal rounded-score ties", "Club metadata not audited at cutoff",
                        "Request-local adapter uses private representation; no search refit", "No latency benchmark in Day 8"],
    }
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "evaluation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    for filename, records in (("scenarios.csv", summaries), ("filter_stages.csv", stages),
                              ("rankings.csv", rankings), ("top5.csv", top_rows)):
        pd.DataFrame(records).to_csv(destination / filename, index=False, encoding="utf-8")
    lines = ["# Day 8 — Advanced Filtering & Search Constraints", "",
             "Dữ liệu thật: 4.112 người, cutoff 2026-06-12; fit 4.108, loại 4 query.",
             "20 legacy checks và 20 advanced requests đạt; direct/KNN cùng representation khớp full ranking.",
             "Hard filters trước ranking. Soft foot chỉ phá hòa; similarity không phải skill/xác suất.", "",
             "| Scenario | Position trước lọc | Sau hard | Trả Top K |", "|---|---:|---:|---:|"]
    for summary in summaries:
        if summary["method"] == "weighted":
            lines.append(f"| {summary['scenario']} | {summary['position_before']} | {summary['after_hard']} | {summary['returned']} |")
    lines += ["", "## Top 5 weighted (cấu hình giả thuyết Day 6, không khẳng định tối ưu)", ""]
    for response in responses:
        if response["method"] != "weighted":
            continue
        lines += [f"### {response['scenario']} — {response['reference']['name']}", "",
                  "Constraints: `" + json.dumps(response["search_constraints"], ensure_ascii=False) + "`.", "",
                  f"Status: {response['status']}; eligible: {response['eligible_count']}.", "",
                  "| Rank | ID | Tên | CLB | Tuổi | EUR | Score |", "|---|---|---|---|---:|---:|---:|"]
        for r in response["results"]:
            lines.append(f"| {r['rank']} | {r['player_id']} | {r['name']} | {r['club']} | {r['age']} | {r['market_value_in_eur']:,.0f} | {r['similarity_score']:.6f} |")
        lines += [""] + [f"- **{r['name']}**: {r['explanation']}" for r in response["results"]] + [""]
    lines += ["## Giới hạn", "", "Không có nhãn relevance, temporal evaluation hoặc app web. Không đo latency Day 8.",
              "Các ngưỡng là kịch bản kiểm hành vi. Missing metadata/CLB lịch sử và snapshot ngoài Git vẫn cần xử lý.",
              "Day 9 dự kiến chuẩn hóa explanation và dữ liệu so sánh, không bịa chỉ số GK/Defender."]
    (destination / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(pd.DataFrame(summaries).to_string(index=False))
    print("Saved", destination, "; inputs and reference unchanged")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/day8")
    run(parser.parse_args().output_dir)
