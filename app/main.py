from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from app.config.settings import settings
from app.routers import jobs, data, review, admin
from app.services.etl_service import run_gsa_etl, run_sam_etl

# Initialize scheduler
scheduler = BackgroundScheduler()

def start_scheduled_tasks():
    scheduler.add_job(run_gsa_etl, 'interval', days=1, id='gsa_etl')
    scheduler.add_job(run_sam_etl, 'interval', days=1, id='sam_etl')
    scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting API — DB: {settings.DATABASE_URL}")
    start_scheduled_tasks()
    yield
    scheduler.shutdown()
    print("👋 Shutting down API")

app = FastAPI(title="Comp Intel API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Comp Intel API is running ✅"}

# ✅ Register all routers AFTER app is defined
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(review.router, prefix="/api/review", tags=["Review"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
