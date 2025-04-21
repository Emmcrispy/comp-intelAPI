import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from app.services.etl_service import run_etl_pipeline
from app.services.classification_service import get_taxonomy_options
from app.services.profile_generator import generate_role_profile

router = APIRouter()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", status_code=201)
async def upload_csv(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # ✅ Await the ETL pipeline
        result = await run_etl_pipeline(file_path)

        return {
            "status": result["status"],
            "rows_processed": result["rows_loaded"],
            "file": file.filename
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
