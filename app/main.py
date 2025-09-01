from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

from app.database import Base, engine, SessionLocal
from app import models
from app.routers import candidates

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

        # Send email confirmation
        exam_link = f"https://your-exam-platform.com/exam?candidate_id={candidate_id}"
        send_confirmation_email(candidate.email, exam_date, exam_time, exam_link)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()

    return RedirectResponse(url="/confirmation", status_code=303)

# ✅ Confirmation Page
@app.get("/confirmation", response_class=HTMLResponse)
async def confirmation_page():
    return HTMLResponse("<h3>Your exam is scheduled successfully! Check your email for details.</h3>")

# ✅ Email Sending Function
def send_confirmation_email(receiver_email, exam_date, exam_time, exam_link):
    sender_email = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not password:
        raise Exception("Email credentials are missing in .env")

    subject = "Your Exam is Scheduled"
    body = f"""
    Hello,

    Your exam has been successfully scheduled.
    Date: {exam_date}
    Time: {exam_time}

    Click here to join: {exam_link}

    Good luck!
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# ✅ Run app locally
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
