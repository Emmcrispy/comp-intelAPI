import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.config.settings import settings

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    return text.strip().title()

def run_etl_pipeline(file_path: str):
    try:
        print("🚀 Starting ETL Pipeline...")
        print(f"🔌 Using DB URL: {settings.DATABASE_URL}")
        print(f"📄 Reading file: {file_path}")

        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} rows")

        expected_columns = ['job_type', 'job_family', 'sub_family', 'single_role', 'career_level', 'country']
        for col in expected_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: '{col}'")
            df[col] = df[col].apply(normalize_text)

        print("🧼 Normalized all required text fields.")

        engine = create_engine(settings.DATABASE_URL)
        with engine.begin() as conn:
            df.to_sql('job_roles', con=conn, if_exists='append', index=False)

        print("✅ Successfully wrote data to job_roles table.")

        return {
            "status": "success",
            "rows_loaded": len(df)
        }

    except ValueError as ve:
        print(f"❌ Column validation failed: {ve}")
        raise ve

    except SQLAlchemyError as se:
        print(f"❌ Database write failed: {se}")
        raise se

    except Exception as e:
        print(f"❌ ETL failed: {e}")
        raise e
