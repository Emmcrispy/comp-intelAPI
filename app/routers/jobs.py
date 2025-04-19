from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from app.services.etl_service import run_etl_pipeline
from app.services.classification_service import get_taxonomy_options
from app.services.profile_generator import generate_role_profile

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.post("/upload")
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    file_path = f"temp_uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    result = run_etl_pipeline(file_path)
    return {"message": "Upload and ETL successful", "rows_loaded": result["rows_loaded"]}

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
    """
    Expects a dictionary with job_type, job_family, sub_family, single_role, career_level
    """
    return generate_role_profile(role_data)
