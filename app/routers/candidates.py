from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Candidate
from app.emailer import send_mail
import shutil
import os

router = APIRouter(prefix="/candidates", tags=["Candidates"])

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/apply")
async def apply_candidate(
    full_name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile = None,
    db: Session = Depends(get_db)
):
    try:
        # ✅ Save resume to uploads folder
        resume_path = None
        if resume:
            resume_path = os.path.join(UPLOAD_DIR, resume.filename)
            with open(resume_path, "wb") as buffer:
                shutil.copyfileobj(resume.file, buffer)

        # ✅ Save candidate info to DB
        candidate = Candidate(full_name=full_name, email=email, position=position, resume_path=resume_path)
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ✅ Send confirmation email
        subject = f"Application received for {position}"
        body = f"""
        <p>Dear {full_name},</p>
        <p>Thank you for applying for the position of <strong>{position}</strong> at Your Company.</p>
        <p>We have reviewed your resume and are pleased to inform you that you have been shortlisted for the next stage.</p>
        <p><a href="http://localhost:3000/schedule-exam?candidate_id={candidate.id}" style="color:blue;">Schedule Your Exam</a></p>
        <br>
        <p>Best regards,<br>Your HR Team</p>
        """

        email_sent = send_mail(email, subject, body)

        if not email_sent:
            raise HTTPException(status_code=500, detail="Candidate saved but email not sent.")

        return {"message": "Application submitted successfully. Email sent."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
