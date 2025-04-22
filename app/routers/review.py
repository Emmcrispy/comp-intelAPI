from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.models.job_upload import JobUpload
from app.config.db import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/review", response_class=HTMLResponse)
def review_jobs(request: Request, db: Session = Depends(get_db)):
    pending_jobs = db.query(JobUpload).filter(JobUpload.status == "pending").all()
    return templates.TemplateResponse("review_list.html", {"request": request, "jobs": pending_jobs})

@router.get("/review/{job_id}", response_class=HTMLResponse)
def edit_job(job_id: int, request: Request, db: Session = Depends(get_db)):
    job = db.query(JobUpload).filter(JobUpload.id == job_id).first()
    return templates.TemplateResponse("edit_job.html", {"request": request, "job": job})

@router.post("/review/{job_id}")
def update_job(job_id: int, title: str = Form(...), skills: str = Form(...), responsibilities: str = Form(...), db: Session = Depends(get_db)):
    job = db.query(JobUpload).filter(JobUpload.id == job_id).first()
    job.title = title
    job.skills = skills
    job.responsibilities = responsibilities
    job.status = "reviewed"
    db.commit()
    return RedirectResponse(url="/review", status_code=303)
