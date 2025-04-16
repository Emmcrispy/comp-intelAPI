from fastapi import FastAPI
from app.routers import jobs, data, reports
from app.dependencies.auth import setup_oauth
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="eryn Compensation Intelligence API")

app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

setup_oauth(app)
