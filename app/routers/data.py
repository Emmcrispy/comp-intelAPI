from fastapi import APIRouter, HTTPException
from services.etl_service import run_etl
from pydantic import BaseModel

class DataSource(BaseModel):
    source: str  # 'GSA_CALC' or 'SAM_GOV'

router = APIRouter()

@router.post("/integrate", status_code=202)
async def integrate_data(source: DataSource):
    if source.source not in ["GSA_CALC", "SAM_GOV"]:
        raise HTTPException(status_code=400, detail="Invalid data source.")
    etl_status = await run_etl(source.source)
    return {"status": "ETL started", "detail": etl_status}
