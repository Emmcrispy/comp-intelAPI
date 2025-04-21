from fastapi import FastAPI
from app.config.settings import settings
from app.routers import jobs, data, reports
from app.services.etl_service import run_etl_pipeline
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI(title="eryn Compensation Intelligence")

@app.on_event("startup")
async def startup_event():
    print(f"\U0001F680 API running with Redis @ {settings.REDIS_HOST}")
    print(f"\U0001F5C4️  Connected to DB: {settings.DATABASE_URL}")

# Mount routers
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

# 🔧 Root route to confirm app is running
@app.get("/")
async def root():
    return {"message": "Comp Intel API is running ✅"}
