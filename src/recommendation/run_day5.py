"""Reproducible real-data scenarios: python -B -m src.recommendation.run_day5."""

import hashlib
import json
import platform

import numpy as np
import pandas as pd
import sklearn

from src.features.build_features import quality_summary, validate_features
from src.recommendation.baseline import CosineRecommender, FEATURE_FILE, ROOT, SearchFilters

SCENARIOS = (
    ("attack_budget_30m", 132098, SearchFilters("Attack", 18, 29, 30_000_000, 1800)),
    ("midfield_budget_15m", 137576, SearchFilters("Midfield", 20, 30, 15_000_000, 1800)),
    ("defender_context_15m", 139208, SearchFilters("Defender", 22, 32, 15_000_000, 2000)),
    ("goalkeeper_context_10m", 629773, SearchFilters("Goalkeeper", 20, 30, 10_000_000, 1800)),
    ("empty_budget", 132098, SearchFilters("Attack", 18, 29, 0, 1800)),
)


def run():
    before = hashlib.sha256(FEATURE_FILE.read_bytes()).hexdigest()
    data = pd.read_csv(FEATURE_FILE)
    validate_features(data)
    query_ids = {player_id for _, player_id, _ in SCENARIOS}
    fit_ids = data.loc[~data.player_id.isin(query_ids), "player_id"].tolist()
    engine = CosineRecommender(data, fit_player_ids=fit_ids)
    scenarios = []
    for name, player_id, filters in SCENARIOS:
        result = engine.recommend(player_id, filters, top_k=5)
        rows = result["results"]
        for row in rows:
            assert row["position"] == filters.position
            assert filters.min_age <= row["age"] <= filters.max_age
            assert row["market_value_in_eur"] <= filters.max_budget_eur
            assert row["minutes_played"] >= filters.min_minutes
            assert row["player_id"] != player_id
            assert np.isfinite(row["similarity_score"]) and -1 <= row["similarity_score"] <= 1
            assert abs(sum(row["cosine_components"].values()) - row["similarity_score"]) < 1e-10
        assert rows == sorted(rows, key=lambda row: (-row["similarity_score"], row["player_id"]))
        assert len({row["player_id"] for row in rows}) == len(rows)
        assert len(rows) == (0 if name == "empty_budget" else 5)
        scenarios.append({"scenario": name, **result, "scenario_checks": "passed"})
        print(name, "eligible=", result["eligible_count"], "returned=", len(rows), "checks=passed")
    assert hashlib.sha256(FEATURE_FILE.read_bytes()).hexdigest() == before
    report = {
        "input_path": FEATURE_FILE.relative_to(ROOT).as_posix(), "input_sha256": before,
        "environment": {"python": platform.python_version(), "pandas": pd.__version__,
                        "numpy": np.__version__, "scikit_learn": sklearn.__version__},
        "input_quality": quality_summary(data), "model": engine.describe(),
        "preprocessing_check": {"fit_players": len(fit_ids), "query_ids_excluded_from_fit": sorted(query_ids),
                                "query_overlap_with_fit": len(query_ids.intersection(fit_ids)),
                                "not_a_temporal_split_or_quality_evaluation": True,
                                "input_hash_unchanged": True},
        "scenarios": scenarios,
    }
    destination = ROOT / "reports/day5_recommendation_examples.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    lines = ["# Day 5 — Ví dụ chạy baseline trên dữ liệu thật", "",
             "Tự sinh bởi `python -B -m src.recommendation.run_day5`. Đây là kiểm tra hành vi, chưa phải đánh giá chất lượng scouting.",
             "", f"Input SHA-256: `{before}`. Cutoff: 2026-06-12. Fit trên {len(fit_ids)} cầu thủ, loại 4 tham chiếu trước khi fit.", ""]
    for result in scenarios:
        lines += [f"## {result['scenario']}", "", f"Tham chiếu: **{result['reference']['name']}** (ID {result['reference']['player_id']}).",
                  "", f"Bộ lọc: `{json.dumps(result['filters'], ensure_ascii=False)}`.", "",
                  f"Ứng viên sau lọc/loại bản thân: {result['eligible_count']}; trạng thái: `{result['status']}`.", "",
                  "| Hạng | ID | Cầu thủ | CLB | Vị trí | Tuổi | Phút | Market value EUR | Cosine |",
                  "|---|---|---|---|---|---:|---:|---:|---:|"]
        for row in result["results"]:
            lines.append(f"| {row['rank']} | {row['player_id']} | {row['name']} | {row['club'] or 'Thiếu dữ liệu'} | {row['position']} | {row['age']} | {row['minutes_played']} | {row['market_value_in_eur']:,.0f} | {row['similarity_score']:.6f} |")
        lines.append("")
        for row in result["results"]:
            lines += [f"- **{row['name']}:** {row['explanation']}"]
        lines += ["", *[f"- {warning}" for warning in result["warnings"]], ""]
    (ROOT / "reports/day5_recommendation_examples.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Saved reports/day5_recommendation_examples.json and .md; input unchanged.")


if __name__ == "__main__":
    run()
