from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from app.services.etl_service import run_etl_pipeline

# Better validation using Enum
class ETLSource(str, Enum):
    GSA_CALC = "GSA_CALC"
    SAM_GOV = "SAM_GOV"

class DataSource(BaseModel):
    source: ETLSource

router = APIRouter()

@router.post("/integrate", status_code=202)
async def integrate_data(source: DataSource):
    try:
        result = await run_etl_pipeline(source.source)
        return {"status": "ETL started", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
