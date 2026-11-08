
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"

games = pd.read_csv(RAW / "games.csv.gz")
appearances = pd.read_csv(RAW / "appearances.csv.gz")
valuations = pd.read_csv(RAW / "player_valuations.csv.gz")

print("=== GAMES COLUMNS ===")
print(games.columns.tolist())

print("\n=== APPEARANCES COLUMNS ===")
print(appearances.columns.tolist())

print("\n=== VALUATIONS COLUMNS ===")
print(valuations.columns.tolist())

# Mua giai 2025/26
if "season" in games.columns:
    season_games = games[
        games["season"].astype(str) == "2025"
    ]

    print("\n=== SEASON 2025/26 ===")
    print("Games:", len(season_games))

    if "game_id" in appearances.columns:
        season_appearances = appearances[
            appearances["game_id"].isin(
                season_games["game_id"]
            )
        ]

        print("Appearances:", len(season_appearances))
        print(
            "Unique players:",
            season_appearances["player_id"].nunique()
        )

# Gia tri thi truong nam 2026
if "date" in valuations.columns:
    valuations["date"] = pd.to_datetime(
        valuations["date"], errors="coerce"
    )

    recent = valuations[
        valuations["date"].dt.year == 2026
    ]

    print("\n=== MARKET VALUES 2026 ===")
    print("Valuation records:", len(recent))
    print("Unique players:", recent["player_id"].nunique())
    print("Latest date:", valuations["date"].max())

# Cau thu thi dau mua 2025/26
season_player_ids = set(
    season_appearances["player_id"].dropna()
)

# Cau thu co dinh gia nam 2026
valued_player_ids = set(
    recent.loc[
        recent["market_value_in_eur"].notna()
        & (recent["market_value_in_eur"] > 0),
        "player_id"
    ]
)

# Giao cua hai tap hop
eligible_players = season_player_ids & valued_player_ids

print("\n=== SCOUTIQ ELIGIBLE PLAYERS ===")
print("Players with appearances:", len(season_player_ids))
print("Players with 2026 valuation:", len(valued_player_ids))
print("Players with both:", len(eligible_players))
