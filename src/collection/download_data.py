
from pathlib import Path
import requests

# Duong dan thu muc goc ScoutIQ
ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Nguon du lieu
BASE_URL = "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data"

TABLES = [
    "players",
    "clubs",
    "appearances",
    "games",
    "player_valuations",
]


def download_table(table):
    filename = f"{table}.csv.gz"
    output = RAW_DIR / filename
    url = f"{BASE_URL}/{filename}"

    if output.exists() and output.stat().st_size > 0:
        print(f"[SKIP] {filename}")
        return

    print(f"[DOWNLOADING] {filename}")

    try:
        with requests.get(
            url,
            stream=True,
            timeout=(15, 120)
        ) as response:
            response.raise_for_status()

            with output.open("wb") as file:
                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):
                    if chunk:
                        file.write(chunk)

        size = output.stat().st_size / (1024 * 1024)
        print(f"[OK] {filename}: {size:.2f} MB")

    except requests.RequestException as error:
        output.unlink(missing_ok=True)
        print(f"[ERROR] {filename}: {error}")


if __name__ == "__main__":
    for table in TABLES:
        download_table(table)

    print("\nData collection finished!")
