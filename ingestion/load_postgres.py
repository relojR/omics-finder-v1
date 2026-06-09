import json
from pathlib import Path
import psycopg2


RAW_DIR = Path("data/raw/gdc/files")   


DB = {
    "host": "localhost",
    "port": 5432,
    "dbname": "omics_finder",
    "user": "omics_finder",
    "password": "omics_finder",        
}


def main():
   
    date_folders = sorted(RAW_DIR.glob("date=*"))
    
    if not date_folders:
        raise SystemExit(f"No data in {RAW_DIR}. Run the ingestion script first.")
    json_path = date_folders[-1] / "files.json"
    print(f"Loading from {json_path}")

  
    data = json.loads(json_path.read_text())
    hits = data["data"]["hits"]

   
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_gdc_files (
            file_id   TEXT,
            payload   JSONB,
            loaded_at TIMESTAMP DEFAULT now()
        );
    """)

   
    cur.execute("TRUNCATE raw_gdc_files;")
    for hit in hits:
        cur.execute(
            "INSERT INTO raw_gdc_files (file_id, payload) VALUES (%s, %s)",
            (hit.get("file_id") or hit.get("id"), json.dumps(hit)),
        )

  
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(hits)} rows into raw_gdc_files")


if __name__ == "__main__":
    main()