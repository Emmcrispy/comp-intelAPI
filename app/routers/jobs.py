import os
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Path, Body
from typing import Optional
from app.services.etl_service import run_etl_pipeline_from_df
from app.services.classification_service import get_taxonomy_options
from app.services.profile_generator import generate_role_profile
from app.utils.text_extractor import extract_text_from_file
from app.config.db import SessionLocal
from app.models.job_roles import JobRole
from sqlalchemy import update

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
            extracted_rows = extract_text_from_file(file_path)
            df = pd.DataFrame(extracted_rows)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

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

@router.get("/taxonomy/{stage}")
def get_taxonomy(stage: str, job_type: Optional[str] = None, job_family: Optional[str] = None, sub_family: Optional[str] = None, single_role: Optional[str] = None):
    previous_selection = {
        "job_type": job_type,
        "job_family": job_family,
        "sub_family": sub_family,
        "single_role": single_role
    }
    previous_selection = {k: v for k, v in previous_selection.items() if v}
    return get_taxonomy_options(stage, previous_selection)

@router.post("/generate-profile")
def get_role_profile(role_data: dict):
    return generate_role_profile(role_data)

@router.patch("/{id}/attributes")
async def update_job_attributes(id: int = Path(...), updates: dict = Body(...)):
    db = SessionLocal()
    try:
        stmt = update(JobRole).where(JobRole.id == id).values(**updates)
        db.execute(stmt)
        db.commit()
        return {"status": "updated", "id": id, "updates": updates}
    finally:
        db.close()
