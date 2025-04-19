import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from app.config.settings import settings
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

executor = ThreadPoolExecutor()

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    return text.strip().title()

def load_and_clean_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    # Normalize key fields
    for col in ['job_type', 'job_family', 'sub_family', 'single_role', 'career_level', 'country']:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)
        else:
            raise ValueError(f"Missing required column: {col}")

    return df

def write_to_db(df: pd.DataFrame):
    engine = create_engine(settings.DATABASE_URL)
    with engine.begin() as conn:
        df.to_sql('job_roles', con=conn, if_exists='append', index=False)

def _etl_from_file(file_path: str):
    df = load_and_clean_csv(file_path)
    write_to_db(df)
    return f"✅ Loaded {len(df)} job records into job_roles"

async def run_etl_pipeline(file_path: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _etl_from_file, file_path)

# Optional: Source-based ETL placeholder
def run_source_etl(source: str):
    # Simulated behavior — replace with real GSA/SAM ETL logic
    print(f"⚙️ Running ETL for {source}...")
    return f"{source} integration completed"
