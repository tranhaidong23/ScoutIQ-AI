
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    ROOT / "data/processed/scoutiq_candidates_2025_26.csv"
)

df["market_value_m"] = (
    df["market_value_in_eur"] / 1_000_000
)

bins = [16, 20, 24, 28, 32, 36, 100]
labels = ["17-20", "21-24", "25-28", "29-32", "33-36", "37+"]

df["age_group"] = pd.cut(
    df["age"],
    bins=bins,
    labels=labels
)

summary = df.groupby(
    "age_group",
    observed=True
).agg(
    players=("player_id", "count"),
    median_value_m=("market_value_m", "median"),
    mean_value_m=("market_value_m", "mean")
)

print("\n===== MARKET VALUE BY AGE GROUP =====")
print(summary.round(2))

summary.to_csv(
    ROOT / "reports/day3_age_group_summary.csv"
)
