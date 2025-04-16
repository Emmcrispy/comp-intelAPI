from pydantic import BaseModel, Field
from typing import List

class JobDescription(BaseModel):
    description: str = Field(..., example="Senior Data Analyst position requiring SQL and Python.")

class JobMatchResult(BaseModel):
    title: str
    score: float

class JobSearchResponse(BaseModel):
    matches: List[JobMatchResult]

class DataSource(BaseModel):
    source: str = Field(..., example="GSA_CALC")

class ETLResponse(BaseModel):
    status: str
    detail: str

class ReportResponse(BaseModel):
    report: str
    content: str
