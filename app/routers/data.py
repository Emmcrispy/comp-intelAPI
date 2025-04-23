from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from app.services.etl_service import run_gsa_etl, run_sam_etl

class ETLSource(str, Enum):
    GSA_CALC = "GSA_CALC"
    SAM_GOV = "SAM_GOV"

class DataSource(BaseModel):
    source: ETLSource

router = APIRouter()

@router.post("/integrate", status_code=202)
async def integrate_data(source: DataSource):
    try:
        if source.source == ETLSource.GSA_CALC:
            result = run_gsa_etl()
        elif source.source == ETLSource.SAM_GOV:
            result = run_sam_etl()
        else:
            raise HTTPException(status_code=400, detail="Invalid data source.")
        return {"status": "ETL started", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
