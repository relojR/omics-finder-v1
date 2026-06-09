import json
from datetime import date
from pathlib import Path

import requests


# I will change these settings later

LIMIT = 100                                  
OUTPUT_DIR = Path("data/raw/gdc/files")      
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

# Use API for GDC files metadata
def main():
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

    # Save into a folder by date
    today = date.today().isoformat()
    save_dir = OUTPUT_DIR / f"date={today}"
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / "files.json"

    # get the response back
    save_path.write_text(json.dumps(data, indent=2))

    record_count = len(data["data"]["hits"])
    print(f"Done. Saved {record_count} records to {save_path}")


if __name__ == "__main__":
    main()
