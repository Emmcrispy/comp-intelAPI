from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.etl_service import run_gsa_etl, run_sam_etl
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/integrate", response_class=HTMLResponse)
async def integration_dashboard(request: Request):
    logger.info("📊 Accessed ETL integration dashboard.")
    return templates.TemplateResponse("etl_admin.html", {"request": request, "result": None})

@router.post("/integrate/gsa")
async def trigger_gsa_etl(request: Request):
    logger.info("🚀 Triggering GSA ETL from admin panel...")
    result = run_gsa_etl()
    return templates.TemplateResponse("etl_admin.html", {"request": request, "result": result})

@router.post("/integrate/sam")
async def trigger_sam_etl(request: Request):
    logger.info("🚀 Triggering SAM ETL from admin panel...")
    result = run_sam_etl()
    return templates.TemplateResponse("etl_admin.html", {"request": request, "result": result})
