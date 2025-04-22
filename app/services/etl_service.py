import pandas as pd
import os
from sqlalchemy import create_engine
from app.config.settings import settings
from app.utils.nlp_utils import extract_nlp_fields

def normalize_text(text):
    return text.strip().title() if isinstance(text, str) else ""

def validate_row(row: dict, row_num: int) -> tuple[bool, str]:
    required_fields = ['job_type', 'job_family', 'sub_family', 'single_role', 'career_level', 'country']
    for field in required_fields:
        if pd.isna(row.get(field)) or not str(row.get(field)).strip():
            return False, f"Row {row_num}: Missing or empty '{field}'"
    return True, ""

def run_etl_pipeline_from_df(df: pd.DataFrame, file_path: str):
    print("🚀 ETL from DataFrame")
    print("🔌 DB:", settings.DATABASE_URL)

    valid_rows = []
    error_log = []

    df['title'] = ""
    df['skills'] = ""
    df['responsibilities'] = ""

    for i, row in df.iterrows():
        row_dict = {col: normalize_text(row.get(col, "")) for col in df.columns}
        is_valid, error = validate_row(row_dict, i + 2)

        if is_valid:
            extracted = extract_nlp_fields(row_dict.get('description', ''))
            row_dict['title'] = extracted['title']
            row_dict['skills'] = "; ".join(extracted['skills'])
            row_dict['responsibilities'] = "; ".join(extracted['responsibilities'])
            valid_rows.append(row_dict)
        else:
            error_log.append({"row": i + 2, "error": error})

    log_path = os.path.splitext(file_path)[0] + "_errors.csv"
    if valid_rows:
        engine = create_engine(settings.DATABASE_URL)
        clean_df = pd.DataFrame(valid_rows)
        with engine.begin() as conn:
            clean_df.to_sql('job_roles', con=conn, if_exists='append', index=False)

    if error_log:
        pd.DataFrame(error_log).to_csv(log_path, index=False)
        print(f"⚠️ Issues logged to {log_path}")

    return {
        "status": "success",
        "rows_loaded": len(valid_rows),
        "rows_failed": len(error_log),
        "error_log_path": log_path if error_log else None
    }
