import os
from services.etl_service import run_etl_pipeline

def ingest_all(directory="data/uploads"):
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            path = os.path.join(directory, file)
            print(f"📥 Ingesting: {file}")
            result = run_etl_pipeline(path)
            print(f"✅ {file} → {result.get('rows_loaded', 0)} rows loaded")

if __name__ == "__main__":
    ingest_all()
