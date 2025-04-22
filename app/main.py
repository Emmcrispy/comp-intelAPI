from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.routers import jobs, data, review

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting API — DB: {settings.DATABASE_URL}")
    yield
    print("👋 Shutting down API")

app = FastAPI(title="Comp Intel API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Comp Intel API is running ✅"}

# ✅ Register all routers
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(review.router, prefix="/api/review", tags=["Review"])
