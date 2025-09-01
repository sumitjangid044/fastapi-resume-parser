from fastapi import APIRouter, UploadFile, Form, HTTPException
import os
from pathlib import Path
from datetime import datetime
from app.utils.emailer import send_mail  # ✅ Email function import

router = APIRouter()

# Directory for resumes
UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(
    name: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    resume: UploadFile = None
):
    try:
        if not resume:
            raise HTTPException(status_code=400, detail="Resume file is required")

        # Generate unique file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_ext = os.path.splitext(resume.filename)[1]
        safe_filename = f"{name}_{role}_{timestamp}{file_ext}"
        file_path = UPLOAD_DIR / safe_filename

        # Save resume file
        with open(file_path, "wb") as f:
            content = await resume.read()
            f.write(content)

        # ✅ Email content
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        link = f"{frontend_url}/schedule-exam"
        subject = f"Application Received for {role}"
        body = f"""
        <p>Dear {name},</p>
        <p>Thank you for applying for the position of <b>{role}</b> at TailentTrail.</p>
        <p>We have reviewed your resume and are pleased to inform you that you have been shortlisted for the next stage.</p>
        <p><a href="http://your-frontend-url.com/schedule-exam">👉 Schedule Your Exam</a></p>
        <p>Best regards,<br>Your HR Team</p>
        """

        # ✅ Send email (don't fail API if email fails)
        email_sent = send_mail(to_email=email, subject=subject, body=body)

        return {
            "status": "success",
            "message": "Resume uploaded successfully",
            "email_status": "sent" if email_sent else "failed",
            "role": role,
            "resume_path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
