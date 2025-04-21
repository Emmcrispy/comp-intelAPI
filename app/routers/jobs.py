from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from app.services.etl_service import run_etl_pipeline
from app.services.classification_service import get_taxonomy_options
from app.services.profile_generator import generate_role_profile
import os

router = APIRouter()
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", status_code=201)
async def upload_job_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        ext = os.path.splitext(file.filename)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext == ".json":
            df = pd.read_json(file_path)
        elif ext in [".pdf", ".docx"]:
            from app.utils.text_extractor import extract_text_from_file
            extracted_rows = extract_text_from_file(file_path)
            df = pd.DataFrame(extracted_rows)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Pass to shared ETL
        result = run_etl_pipeline_from_df(df, file_path)

        return {
            "status": result["status"],
            "rows_processed": result["rows_loaded"],
            "rows_failed": result["rows_failed"],
            "file": file.filename,
            "errors": result["error_log_path"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ETL failed: {str(e)}")
