
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
REPORT_DIR = ROOT / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

TABLES = [
    "players",
    "clubs",
    "appearances",
    "games",
    "player_valuations",
]

summary = []

for name in TABLES:
    file_path = RAW_DIR / f"{name}.csv.gz"

    df = pd.read_csv(file_path, low_memory=False)

    rows, columns = df.shape
    duplicate_rows = df.duplicated().sum()
    missing_values = df.isnull().sum().sum()

    total_cells = rows * columns
    missing_percent = (
        missing_values / total_cells * 100
        if total_cells > 0 else 0
    )

    print(f"\n{'=' * 50}")
    print(f"DATASET: {name.upper()}")
    print(f"{'=' * 50}")

    print(f"Rows: {rows:,}")
    print(f"Columns: {columns}")
    print(f"Duplicate rows: {duplicate_rows:,}")
    print(f"Missing values: {missing_percent:.2f}%")

    print("\nColumn names:")
    print(df.columns.tolist())

    if "date" in df.columns:
        dates = pd.to_datetime(df["date"], errors="coerce")
        print("Earliest date:", dates.min())
        print("Latest date:", dates.max())

    summary.append({
        "dataset": name,
        "rows": rows,
        "columns": columns,
        "duplicates": duplicate_rows,
        "missing_percent": round(missing_percent, 2),
    })

report = pd.DataFrame(summary)

report.to_csv(
    REPORT_DIR / "day1_data_quality.csv",
    index=False
)

print("\n===== DATA QUALITY SUMMARY =====")
print(report.to_string(index=False))

print("\nReport saved successfully!")
