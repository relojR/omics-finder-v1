"""
Pull public file metadata from the NCI GDC API and save it as raw JSON.

This is the "ingestion" step: grab data from the source exactly as it comes
and save it to disk untouched. We clean and reshape it later, in a separate
step. Keeping raw data separate from cleaned data is a core habit.
"""

import json
from datetime import date
from pathlib import Path

import requests


# --- Settings you can change ---------------------------------------------

LIMIT = 100                                  # how many records to pull
OUTPUT_DIR = Path("data/raw/gdc/files")      # where to save the raw data
GDC_FILES_URL = "https://api.gdc.cancer.gov/files"

# The fields we want back for each file.
FIELDS = [
    "file_id",
    "file_name",
    "data_category",
    "data_type",
    "experimental_strategy",
    "file_format",
    "access",
    "cases.case_id",
    "cases.project.project_id",
    "cases.project.name",
    "cases.disease_type",
    "cases.primary_site",
]


# --- The script ----------------------------------------------------------

def main():
    # 1. Ask the GDC API for file metadata.
    print(f"Fetching {LIMIT} records from GDC...")
    params = {
        "size": LIMIT,
        "fields": ",".join(FIELDS),
        "format": "JSON",
        "sort": "file_id:asc",
    }
    response = requests.post(GDC_FILES_URL, json=params, timeout=60)
    response.raise_for_status()  # stops with a clear message if the request failed
    data = response.json()

    # 2. Decide where to save it — one folder per day.
    today = date.today().isoformat()
    save_dir = OUTPUT_DIR / f"date={today}"
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / "files.json"

    # 3. Save the raw response to disk, exactly as we got it.
    save_path.write_text(json.dumps(data, indent=2))

    # 4. Report what happened.
    record_count = len(data["data"]["hits"])
    print(f"Done. Saved {record_count} records to {save_path}")


if __name__ == "__main__":
    main()
