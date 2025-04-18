import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    return text.strip().title()

def run_etl_pipeline(file_path: str):
    #step 1: Load
    df = pd.read_csv(file_path)

    #Step 2: Clean/Normalize
    df['job_type'] = df['job_type'].apply(normalize_text)
    df['job_family'] = df['job_family'].apply(normalize_text)
    df['sub_family'] = df['sub_family'].apply(normalize_text)
    df['single_role'] = df['single_role'].apply(normalize_text)
    df['career_level'] = df['career_level'].apply(normalize_text)
    df['country'] = df['country'].apply(normalize_text)

    #Step 3: Connect to DB
    engine = create_engine(DB_URL)
    connection = engine.connect()

    #Step 4: Write to DB (append new jobs into staging or main table)
    df.to_sql('job_roles', con=engine, if_exists='append', index=False)
    return {"status": "success", "message": len(df)}
