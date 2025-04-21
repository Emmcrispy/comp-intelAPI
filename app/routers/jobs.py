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
async def upload_csv(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 🔥 FIXED: Sync function should not be awaited
        result = run_etl_pipeline(file_path)

        return {
            "status": result["status"],
            "rows_processed": result["rows_loaded"],
            "file": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ETL failed: {str(e)}")
