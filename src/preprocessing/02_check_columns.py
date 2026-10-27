
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"

tables = [
    "players",
    "clubs",
    "appearances",
    "games",
]

for table in tables:
    path = RAW_DIR / f"{table}.csv.gz"

    df = pd.read_csv(path, nrows=5)

    print(f"\n{'=' * 45}")
    print(f"TABLE: {table.upper()}")
    print(f"{'=' * 45}")

    for column in df.columns:
        print(column)
