
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)

CUTOFF = pd.Timestamp("2026-06-12")

# ==========================================
# 1. LOAD DATA
# ==========================================

print("Loading datasets...")

players = pd.read_csv(
    RAW / "players.csv.gz", low_memory=False
)

clubs = pd.read_csv(
    RAW / "clubs.csv.gz", low_memory=False
)

games = pd.read_csv(
    RAW / "games.csv.gz", low_memory=False
)

appearances = pd.read_csv(
    RAW / "appearances.csv.gz", low_memory=False
)

valuations = pd.read_csv(
    RAW / "player_valuations.csv.gz",
    low_memory=False
)

# ==========================================
# 2. FILTER SEASON 2025/26
# ==========================================

season_games = games.loc[
    (games["season"].astype(str) == "2025")
    & (pd.to_datetime(
        games["date"], errors="coerce"
    ) <= CUTOFF),
    ["game_id"]
].drop_duplicates()

season_appearances = appearances.merge(
    season_games,
    on="game_id",
    how="inner",
    validate="many_to_one"
)

# Chi giu cac ban ghi co ID hop le
season_appearances = season_appearances.dropna(
    subset=["player_id", "game_id"]
)

# Chuyen cac cot thong ke sang so
stats_columns = [
    "minutes_played", "goals", "assists"
]

for col in stats_columns:
    season_appearances[col] = pd.to_numeric(
        season_appearances[col], errors="coerce"
    )

# Khong tu thay missing bang 0
season_appearances = season_appearances.dropna(
    subset=stats_columns
)

# Loai gia tri bat hop ly
season_appearances = season_appearances.loc[
    (season_appearances["minutes_played"] > 0)
    & (season_appearances["goals"] >= 0)
    & (season_appearances["assists"] >= 0)
]

# Moi appearance_id chi tinh mot lan
season_appearances = (
    season_appearances
    .drop_duplicates(subset=["appearance_id"])
)

# ==========================================
# 3. AGGREGATE PLAYER STATISTICS
# ==========================================

player_stats = (
    season_appearances
    .groupby("player_id", as_index=False)
    .agg(
        matches_played=("game_id", "nunique"),
        minutes_played=("minutes_played", "sum"),
        goals=("goals", "sum"),
        assists=("assists", "sum"),
    )
)

player_stats["goals_per90"] = (
    player_stats["goals"] * 90
    / player_stats["minutes_played"]
)

player_stats["assists_per90"] = (
    player_stats["assists"] * 90
    / player_stats["minutes_played"]
)

player_stats["goal_contributions_per90"] = (
    (player_stats["goals"] + player_stats["assists"])
    * 90 / player_stats["minutes_played"]
)

# ==========================================
# 4. CLEAN PLAYER INFORMATION
# ==========================================

players["date_of_birth"] = pd.to_datetime(
    players["date_of_birth"], errors="coerce"
)

players["age"] = (
    (CUTOFF - players["date_of_birth"])
    .dt.days / 365.2425
)

players["age"] = players["age"].apply(
    lambda x: int(x) if pd.notna(x) and x >= 0
    else pd.NA
)

player_columns = [
    "player_id", "name", "position",
    "sub_position", "age", "foot",
    "height_in_cm", "current_club_id",
    "current_club_name", "image_url"
]

players_clean = (
    players[player_columns]
    .drop_duplicates(subset=["player_id"])
)

# ==========================================
# 5. SELECT LATEST MARKET VALUATION
# ==========================================

valuations["date"] = pd.to_datetime(
    valuations["date"], errors="coerce"
)

valuations["market_value_in_eur"] = pd.to_numeric(
    valuations["market_value_in_eur"],
    errors="coerce"
)

valid_valuations = valuations.loc[
    (valuations["date"] <= CUTOFF)
    & (valuations["market_value_in_eur"] > 0)
].copy()

latest_valuations = (
    valid_valuations
    .sort_values(["player_id", "date"])
    .drop_duplicates(
        subset=["player_id"], keep="last"
    )
    [[
        "player_id", "date",
        "market_value_in_eur"
    ]]
    .rename(columns={"date": "valuation_date"})
)

# ==========================================
# 6. MERGE TABLES
# ==========================================

dataset = player_stats.merge(
    players_clean,
    on="player_id",
    how="inner",
    validate="one_to_one"
)

dataset = dataset.merge(
    latest_valuations,
    on="player_id",
    how="left",
    validate="one_to_one"
)

# Chi giu cau thu co dinh gia hop le
dataset = dataset.dropna(
    subset=["market_value_in_eur"]
)

# Bo sung thong tin CLB tu bang clubs
club_info = (
    clubs[["club_id", "name"]]
    .drop_duplicates(subset=["club_id"])
    .rename(columns={
        "club_id": "current_club_id",
        "name": "club_name_verified"
    })
)

dataset = dataset.merge(
    club_info,
    on="current_club_id",
    how="left",
    validate="many_to_one"
)

# ==========================================
# 7. SAVE PROCESSED DATA
# ==========================================

output = (
    PROCESSED / "scoutiq_players_2025_26.csv"
)

dataset.to_csv(
    output, index=False, encoding="utf-8-sig"
)

print("\n===== SCOUTIQ DATASET =====")
print("Players:", len(dataset))
print("Columns:", len(dataset.columns))
print("Duplicate IDs:", dataset["player_id"].duplicated().sum())
print("Missing market values:",
      dataset["market_value_in_eur"].isna().sum())

print("\nSample:")
print(dataset[
    [
        "name", "position", "age",
        "minutes_played", "goals", "assists",
        "market_value_in_eur"
    ]
].head(10).to_string(index=False))

print(f"\nSaved to: {output}")
