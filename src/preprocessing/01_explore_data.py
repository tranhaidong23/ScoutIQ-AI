
from pathlib import Path
import pandas as pd

# 1. Xac dinh thu muc goc du an
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"

# 2. Danh sach cac bang
TABLES = [
    "players",
    "clubs",
    "games",
    "appearances",
    "player_valuations",
]

# 3. Doc va kiem tra tung bang
for name in TABLES:
    file_path = RAW_DIR / f"{name}.csv.gz"

    print("\n" + "=" * 60)
    print(f"DATASET: {name.upper()}")
    print("=" * 60)

    # Doc 5 dong de xem cau truc, tranh ton RAM
    sample = pd.read_csv(file_path, nrows=5)

    print("\nCOLUMNS AND DATA TYPES:")
    print(sample.dtypes.to_string())

    print("\nFIRST 3 ROWS:")
    print(sample.head(3).to_string(index=False))

    print("\nIMPORTANT COLUMNS:")
    keywords = [
        "id", "position", "date", "season",
        "value", "goals", "assists", "minutes",
        "height", "birth", "foot", "club"
    ]

    important = [
        col for col in sample.columns
        if any(word in col.lower() for word in keywords)
    ]

    print(important)

print("\nDATA EXPLORATION COMPLETED!")
