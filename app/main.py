from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.database import Base, engine, SessionLocal
from app import models
from app.routers import candidates
from app.utils.emailer import send_mail  # ✅ Centralized email function

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TalentTrail")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "API is running on Vercel!"}

# Include candidate router
app.include_router(candidates.router)

# ✅ Schedule Exam Page
@app.get("/schedule", response_class=HTMLResponse)
async def schedule_page(request: Request, candidate_id: int):
    return templates.TemplateResponse("schedule.html", {"request": request, "candidate_id": candidate_id})

# ✅ Schedule Confirmation Route
@app.post("/schedule-confirm")
async def schedule_confirm(candidate_id: int = Form(...), exam_date: str = Form(...), exam_time: str = Form(...)):
    db: Session = SessionLocal()
    try:
        candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        # Update DB
        candidate.exam_date = exam_date
        candidate.exam_time = exam_time
        db.commit()

        # ✅ Send email using emailer.py
        subject = "Your Exam is Scheduled"
        body = f"""
        <p>Hello {candidate.name},</p>
        <p>Your exam has been successfully scheduled.</p>
        <p><b>Date:</b> {exam_date}</p>
        <p><b>Time:</b> {exam_time}</p>
        <p><a href="https://your-exam-platform.com/exam?candidate_id={candidate_id}">Click here to join</a></p>
        <p>Good luck!</p>
        """

        email_sent = send_mail(candidate.email, subject, body)

        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()

    return RedirectResponse(url="/confirmation", status_code=303)

# ✅ Confirmation Page
@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation_page():
    return HTMLResponse("<h3>Your exam is scheduled successfully! Check your email for details.</h3>")
