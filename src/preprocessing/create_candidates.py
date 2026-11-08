
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"

INPUT = PROCESSED / "scoutiq_players_2025_26.csv"
OUTPUT = PROCESSED / "scoutiq_candidates_2025_26.csv"

CUTOFF = pd.Timestamp("2026-06-12")

# 1. Doc du lieu
df = pd.read_csv(INPUT)

print("===== INITIAL DATASET =====")
print("Total players:", len(df))

# 2. Chuan hoa ngay dinh gia
df["valuation_date"] = pd.to_datetime(
    df["valuation_date"], errors="coerce"
)

df["valuation_age_days"] = (
    CUTOFF - df["valuation_date"]
).dt.days

# 3. Tao cac dieu kien
valid_minutes = df["minutes_played"] >= 900

valid_value = df["market_value_in_eur"] > 0

valid_valuation_date = (
    df["valuation_age_days"].between(0, 365)
)

valid_position = (
    df["position"].notna()
    & df["position"].astype(str).str.strip().ne("")
)

# 4. Loc cau thu
candidates = df.loc[
    valid_minutes
    & valid_value
    & valid_valuation_date
    & valid_position
].copy()

# 5. Kiem tra
print("\n===== CANDIDATE FILTERING =====")
print("Players >= 900 minutes:", valid_minutes.sum())
print("Players with valid value:", valid_value.sum())
print(
    "Players with recent valuation:",
    valid_valuation_date.sum()
)
print("Players with known position:", valid_position.sum())

print("\n===== FINAL CANDIDATES =====")
print("Total candidates:", len(candidates))
print(
    "Unique player IDs:",
    candidates["player_id"].nunique()
)

print("\nPosition distribution:")
print(candidates["position"].value_counts())

# 6. Luu du lieu
candidates.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nSaved to: {OUTPUT}")
