
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

file_path = (
    ROOT / "data" / "processed"
    / "scoutiq_players_2025_26.csv"
)

df = pd.read_csv(file_path)

print("===== SCOUTIQ DATA VALIDATION =====")

print("Total players:", len(df))
print("Total columns:", len(df.columns))

print(
    "Duplicate player IDs:",
    df["player_id"].duplicated().sum()
)

print(
    "Missing player names:",
    df["name"].isna().sum()
)

print(
    "Missing positions:",
    df["position"].isna().sum()
)

print(
    "Missing market values:",
    df["market_value_in_eur"].isna().sum()
)

print("\n===== PLAYING TIME =====")

for threshold in [90, 450, 900, 1800]:
    count = (
        df["minutes_played"] >= threshold
    ).sum()

    print(f"Players >= {threshold} minutes: {count}")

print("\n===== MARKET VALUE =====")

print(
    df["market_value_in_eur"].describe()
)

print("\n===== VALUATION FRESHNESS =====")

df["valuation_date"] = pd.to_datetime(
    df["valuation_date"], errors="coerce"
)

cutoff = pd.Timestamp("2026-06-12")

df["valuation_age_days"] = (
    cutoff - df["valuation_date"]
).dt.days

print(
    "Valuations older than 365 days:",
    (df["valuation_age_days"] > 365).sum()
)

print(
    "Valuations within 180 days:",
    (df["valuation_age_days"] <= 180).sum()
)

print("\n===== INVALID VALUES =====")

print(
    "Negative ages:",
    (df["age"] < 0).sum()
)

print(
    "Negative minutes:",
    (df["minutes_played"] < 0).sum()
)

print(
    "Negative market values:",
    (df["market_value_in_eur"] < 0).sum()
)

print("\nVALIDATION COMPLETED!")
