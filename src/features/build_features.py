"""Day 4: derive auditable features from the real, fixed-cutoff candidate snapshot.

Run: .venv/Scripts/python.exe -B src/features/build_features.py
Only the designated Day 4 outputs are written. No imputation or skill score.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/processed/scoutiq_candidates_2025_26.csv"
OUTPUT = ROOT / "data/processed/scoutiq_features_2025_26.csv"
REPORT = ROOT / "reports/day4_feature_quality.json"
FIGURE = ROOT / "reports/figures/day4_market_value_transformation.png"
CUTOFF = pd.Timestamp("2026-06-12")
POSITIONS = {"Attack", "Midfield", "Defender", "Goalkeeper"}
PER90 = ("goals_per90", "assists_per90", "goal_contributions_per90")
PERCENTILES = tuple(f"{name}_position_percentile" for name in PER90)
FEATURES = (
    "goal_contributions", "goal_contributions_per90", "market_value_m",
    "log1p_market_value_m", "minutes_reliability", *PERCENTILES,
)
CORE_NUMERIC = (
    "player_id", "matches_played", "minutes_played", "goals", "assists",
    *PER90, "age", "market_value_in_eur", "valuation_age_days",
)
RTOL, ATOL = 1e-9, 1e-12


def require(condition: bool, message: str) -> None:
    """Use explicit errors: validation must also run under python -O."""
    if not condition:
        raise ValueError(message)


def missing_counts(df: pd.DataFrame) -> dict:
    """Count nulls and whitespace-only strings without altering the input."""
    return {
        col: int((df[col].isna() | df[col].astype("string").str.strip().eq("").fillna(False)).sum())
        for col in df.columns
    }


def per90_errors(df: pd.DataFrame) -> dict:
    totals = (df["goals"], df["assists"], df["goals"] + df["assists"])
    return {
        name: float((df[name] - total * 90 / df["minutes_played"]).abs().max())
        for name, total in zip(PER90, totals)
    }


def quality_summary(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include="number")
    return {
        "rows": len(df), "columns": len(df.columns),
        "schema": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "unique_player_ids": int(df["player_id"].nunique()),
        "duplicate_player_ids": int(df["player_id"].duplicated().sum()),
        "missing_by_column": missing_counts(df),
        "infinity_by_column": {col: int(np.isinf(numeric[col]).sum()) for col in numeric},
        "numeric_ranges": {
            col: {"min": float(numeric[col].min()), "max": float(numeric[col].max())}
            for col in numeric
        },
        "position_counts": {key: int(value) for key, value in df["position"].value_counts().items()},
        "max_absolute_per90_error": per90_errors(df),
    }


def validate_candidates(df: pd.DataFrame) -> None:
    require(not df.empty, "Candidate dataset is empty")
    require(df.columns.is_unique, "Duplicate column names")
    required = {*CORE_NUMERIC, "position", "name", "valuation_date"}
    require(required.issubset(df.columns), f"Missing required columns: {sorted(required - set(df.columns))}")
    missing = missing_counts(df)
    require(not any(missing[col] for col in required), "Missing required values")
    for col in CORE_NUMERIC:
        require(pd.api.types.is_numeric_dtype(df[col]), f"Non-numeric column: {col}")
    require(not np.isinf(df.select_dtypes(include="number").to_numpy()).any(), "Infinity in numeric data")
    require(not df["player_id"].duplicated().any(), "Duplicate player IDs")
    require(df["position"].isin(POSITIONS).all(), "Unknown position")
    for col in ("player_id", "matches_played", "minutes_played", "goals", "assists", "age", "valuation_age_days"):
        require((df[col] >= 0).all() and (df[col] % 1 == 0).all(), f"Invalid nonnegative integer: {col}")
    require((df["player_id"] > 0).all(), "Player IDs must be positive")
    require((df["matches_played"] > 0).all(), "Matches must be positive")
    require((df["minutes_played"] >= 900).all(), "Candidate minutes must be >= 900")
    require(df["age"].between(0, 100).all(), "Age outside validation range [0, 100]")
    require((df["market_value_in_eur"] > 0).all(), "Market value must be positive")
    dates = pd.to_datetime(df["valuation_date"], errors="coerce", format="%Y-%m-%d")
    days = (CUTOFF - dates).dt.days
    require(dates.notna().all() and days.between(0, 365).all(), "Valuation date outside cutoff window")
    require((days == df["valuation_age_days"]).all(), "Inconsistent valuation_age_days")
    totals = (df["goals"], df["assists"], df["goals"] + df["assists"])
    for col, total in zip(PER90, totals):
        require((df[col] >= 0).all(), f"Negative per90: {col}")
        require(np.allclose(df[col], total * 90 / df["minutes_played"], rtol=RTOL, atol=ATOL),
                f"Inconsistent per90: {col}")


def validate_features(df: pd.DataFrame) -> None:
    validate_candidates(df)
    require(set(FEATURES).issubset(df.columns), "Missing engineered columns")
    require(np.isfinite(df[list(FEATURES)].to_numpy(dtype=float)).all(), "Nonfinite engineered features")
    expected = {
        "goal_contributions": df["goals"] + df["assists"],
        "market_value_m": df["market_value_in_eur"] / 1_000_000,
        "log1p_market_value_m": np.log1p(df["market_value_in_eur"] / 1_000_000),
        "minutes_reliability": (df["minutes_played"] / 2700).clip(upper=1),
    }
    for col, values in expected.items():
        require(np.allclose(df[col], values, rtol=RTOL, atol=ATOL), f"Inconsistent feature: {col}")
    require(df["minutes_reliability"].between(0, 1).all(), "Reliability outside [0, 1]")
    for source, col in zip(PER90, PERCENTILES):
        require(df[col].between(0, 100).all(), f"Percentile outside [0, 100]: {col}")
        expected_rank = df.groupby("position", observed=True)[source].rank(method="average", pct=True) * 100
        require(np.allclose(df[col], expected_rank, rtol=RTOL, atol=ATOL), f"Inconsistent percentile: {col}")


def build_features(candidates: pd.DataFrame) -> pd.DataFrame:
    """Average rank / group size * 100; ties share rank, no imputation.

    Percentiles reference ALL candidates at this cutoff, before user filters.
    They are descriptive attacking statistics, not an overall quality score.
    """
    validate_candidates(candidates)
    new_columns = set(FEATURES) - {"goal_contributions_per90"}
    require(not new_columns.intersection(candidates.columns), "Input already contains Day 4 columns")
    df = candidates.copy(deep=True)
    df["goal_contributions"] = df["goals"] + df["assists"]
    # Validate the existing Day 2 column before recomputing, never hide errors.
    df["goal_contributions_per90"] = df["goal_contributions"] * 90 / df["minutes_played"]
    df["market_value_m"] = df["market_value_in_eur"] / 1_000_000
    df["log1p_market_value_m"] = np.log1p(df["market_value_m"])
    df["minutes_reliability"] = (df["minutes_played"] / 2700).clip(upper=1)
    for source, target in zip(PER90, PERCENTILES):
        df[target] = df.groupby("position", observed=True)[source].rank(method="average", pct=True) * 100
    validate_features(df)
    return df


def plot_market_value(df: pd.DataFrame, path: Path) -> None:
    """Equal-width bins on each separate scale; show every observation."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for ax, col, label, color in zip(
        axes, ("market_value_m", "log1p_market_value_m"),
        ("Market value (million EUR)", "ln(1 + market value in million EUR)"),
        ("#31688e", "#218f78"),
    ):
        series = df[col]
        ax.hist(series, bins=40, color=color, edgecolor="white", linewidth=0.4)
        ax.axvline(series.median(), color="#b23a48", linestyle="--", label="Median")
        ax.set(xlabel=label, ylabel="Players", title=f"Skewness = {series.skew():.3f}")
        ax.legend(frameon=False)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(f"ScoutIQ | Market value before and after log1p | n = {len(df):,}")
    fig.text(0.5, 0.015, "2025/26 snapshot | Cutoff: 2026-06-12 | Historical estimates, not transfer fees or skill scores",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.055, 1, 0.95))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    input_hash = sha256(INPUT)
    candidates = pd.read_csv(INPUT)
    features = build_features(candidates)
    # Height screening is a review heuristic, not a correction or exclusion rule.
    height = pd.to_numeric(features["height_in_cm"], errors="coerce")
    suspicious = features.loc[height.notna() & ~height.between(140, 220),
                              ["player_id", "name", "height_in_cm"]]
    market_stats = {}
    for col in ("market_value_m", "log1p_market_value_m"):
        series = features[col]
        market_stats[col] = {**{k: float(v) for k, v in series.describe().items()},
                             "skewness": float(series.skew())}
    report = {
        "cutoff": str(CUTOFF.date()), "season": "2025/26",
        "environment": {"python": platform.python_version(), "pandas": pd.__version__,
                        "numpy": np.__version__, "matplotlib": matplotlib.__version__},
        "input_path": str(INPUT.relative_to(ROOT)), "input_sha256": input_hash,
        "output_path": str(OUTPUT.relative_to(ROOT)),
        "input_quality": quality_summary(candidates), "output_quality": quality_summary(features),
        "engineered_columns": list(FEATURES),
        "new_columns": [col for col in features if col not in candidates],
        "percentile_method": "100 * average rank / position group size; ties averaged; range (0,100]",
        "percentile_reference": f"All {len(candidates)} candidates at cutoff, before user search filters",
        "per90_tolerance": {"rtol": RTOL, "atol": ATOL},
        "market_value_distribution": market_stats,
        "minutes_reliability": {
            "formula": "min(minutes_played / 2700, 1); heuristic, not a probability or skill",
            "capped_players": int((features["minutes_reliability"] == 1).sum()),
            "median": float(features["minutes_reliability"].median()),
        },
        "zero_goals_by_position": {
            position: {"players": len(group), "zero_goals": int((group["goals"] == 0).sum()),
                       "zero_goals_percentile": float(group.loc[group["goals"] == 0, PERCENTILES[0]].iloc[0])}
            for position, group in features.groupby("position") if (group["goals"] == 0).any()
        },
        "warnings": {
            "optional_metadata_missing_preserved": {k: v for k, v in missing_counts(candidates).items() if v},
            "height_review_range_cm": [140, 220],
            "height_values_requiring_source_review": suspicious.to_dict(orient="records"),
            "market_value_is_not_skill_or_transfer_fee": True,
            "defender_goalkeeper_quality_not_fully_measured": True,
            "recommendation_quality_not_evaluated": True,
        },
    }
    # Fixed output paths never target raw data or the candidate input.
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    reloaded = pd.read_csv(OUTPUT)
    validate_features(reloaded)
    pd.testing.assert_frame_equal(features, reloaded, check_exact=False, rtol=RTOL, atol=ATOL)
    require(sha256(INPUT) == input_hash, "Candidate file changed during run")
    plot_market_value(features, FIGURE)
    report["output_sha256"] = sha256(OUTPUT)
    report["checks"] = {"candidate_validation": "passed", "feature_validation": "passed",
                        "csv_round_trip": "passed", "input_hash_unchanged": True}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Input: {candidates.shape}; output: {features.shape}; engineered: {len(FEATURES)}; added: {len(report['new_columns'])}")
    print(f"Skewness: {market_stats['market_value_m']['skewness']:.6f} -> {market_stats['log1p_market_value_m']['skewness']:.6f}")
    print("Warnings:", json.dumps(report["warnings"], ensure_ascii=True))
    print("Validation and CSV round-trip passed. Input SHA-256 unchanged.")
    print(f"Saved: {OUTPUT}\nSaved: {REPORT}\nSaved: {FIGURE}")
    return report


if __name__ == "__main__":
    run()
