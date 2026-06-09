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


