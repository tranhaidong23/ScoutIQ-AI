
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================
# 1. CONFIGURATION
# ======================================

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")

df = pd.read_csv(
    DATA / "scoutiq_candidates_2025_26.csv"
)

print("===== SCOUTIQ EDA =====")
print("Total players:", len(df))
print("Columns:", len(df.columns))

# Convert EUR to million EUR
df["market_value_m"] = (
    df["market_value_in_eur"] / 1_000_000
)

# ======================================
# 2. MARKET VALUE DISTRIBUTION
# ======================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="market_value_m",
    bins=50,
    color="#4568dc"
)

plt.title("Market Value Distribution")
plt.xlabel("Market Value (Million EUR)")
plt.ylabel("Number of Players")

plt.tight_layout()
plt.savefig(
    FIGURES / "01_market_value_distribution.png",
    dpi=300
)
plt.close()

# ======================================
# 3. AGE VS MARKET VALUE
# ======================================

age_data = df.dropna(
    subset=["age", "market_value_m"]
)

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=age_data,
    x="age",
    y="market_value_m",
    alpha=0.45,
    s=35
)

plt.title("Age vs Market Value")
plt.xlabel("Age")
plt.ylabel("Market Value (Million EUR)")

plt.tight_layout()
plt.savefig(
    FIGURES / "02_age_vs_market_value.png",
    dpi=300
)
plt.close()

# ======================================
# 4. MARKET VALUE BY POSITION
# ======================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="position",
    y="market_value_m",
    order=[
        "Goalkeeper",
        "Defender",
        "Midfield",
        "Attack"
    ],
    showfliers=False
)

plt.title("Market Value by Position")
plt.xlabel("Position")
plt.ylabel("Market Value (Million EUR)")

plt.tight_layout()
plt.savefig(
    FIGURES / "03_market_value_by_position.png",
    dpi=300
)
plt.close()

# ======================================
# 5. GOALS AND ASSISTS PER 90
# ======================================

attackers = df.loc[
    df["position"] == "Attack"
].copy()

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=attackers,
    x="goals_per90",
    y="assists_per90",
    size="minutes_played",
    sizes=(20, 160),
    alpha=0.6,
    legend=False
)

plt.title("Attacking Players: Goals vs Assists per 90")
plt.xlabel("Goals per 90")
plt.ylabel("Assists per 90")

plt.tight_layout()
plt.savefig(
    FIGURES / "04_attacking_performance.png",
    dpi=300
)
plt.close()

# ======================================
# 6. CORRELATION HEATMAP
# ======================================

numeric_cols = [
    "age",
    "height_in_cm",
    "minutes_played",
    "goals",
    "assists",
    "goals_per90",
    "assists_per90",
    "market_value_m"
]

corr = df[numeric_cols].corr()

plt.figure(figsize=(10, 7))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Between Player Features")

plt.tight_layout()
plt.savefig(
    FIGURES / "05_correlation_heatmap.png",
    dpi=300
)
plt.close()

# ======================================
# 7. STATISTICAL SUMMARY
# ======================================

print("\n===== MARKET VALUE =====")
print(df["market_value_m"].describe())

print("\n===== AGE =====")
print(df["age"].describe())

print("\n===== POSITION SUMMARY =====")

summary = df.groupby("position").agg(
    players=("player_id", "count"),
    median_value_m=("market_value_m", "median"),
    avg_age=("age", "mean"),
    avg_goals_per90=("goals_per90", "mean"),
    avg_assists_per90=("assists_per90", "mean")
)

print(summary.round(2))

summary.to_csv(
    ROOT / "reports" / "day3_position_summary.csv"
)

print("\nEDA COMPLETED!")
print("Figures saved to:", FIGURES)
