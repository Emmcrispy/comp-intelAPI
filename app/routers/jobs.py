from fastapi import APIRouter, Depends, HTTPException, status
from services.nlp_service import process_job_description
from pydantic import BaseModel

class JobDescription(BaseModel):
    description: str

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_job(job: JobDescription):
    if not job.description:
        raise HTTPException(status_code=400, detail="Description required.")
    result = await process_job_description(job.description)
    return {"status": "success", "processed": result}

@router.get("/search")
async def search_jobs(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword required.")
    # Placeholder for matching logic integration
    return {"matches": [{"title": "Data Analyst", "score": 97.5}]}
