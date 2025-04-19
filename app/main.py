from fastapi import FastAPI
from app.config.settings import settings
from app.routers import jobs, data, reports

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print(f"🚀 API running with Redis @ {settings.REDIS_HOST}")
    print(f"🗄️  Connected to DB: {settings.DATABASE_URL}")

app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
