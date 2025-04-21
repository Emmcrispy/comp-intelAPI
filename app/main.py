from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.routers import jobs, data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ⏳ Startup logic
    print(f"🚀 Starting API — DB: {settings.DATABASE_URL}")
    yield
    # 🧹 Shutdown logic (if needed)
    print("👋 Shutting down API")

app = FastAPI(title="Comp Intel API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Comp Intel API is running ✅"}

# Register routers
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
