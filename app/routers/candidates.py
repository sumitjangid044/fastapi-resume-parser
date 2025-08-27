from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.utils.resume_parser import parse_resume
from app.utils.emailer import send_mail

router = APIRouter()

@router.post("/candidates/upload")
async def upload_candidate(
    target_role: str = Form(...),
    resume: UploadFile = File(...)
):
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if resume.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed")

    # Read file bytes
    file_bytes = await resume.read()
    if len(file_bytes) < 500:
        raise HTTPException(status_code=400, detail="Uploaded file is too small or empty")

    # Parse resume
    try:
        parsed = parse_resume(resume.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    parsed["target_role"] = target_role

    email = parsed.get("email")
    if not email:
        return {"status": "success", "message": "No email found in resume", "data": parsed}

    # Eligibility check
    eligible = parsed.get("eligible", True)

    # Prepare email
    subject = f"Application received for {target_role.replace('_', ' ').title()}"
    candidate_name = parsed.get("name", "Candidate")
    exam_link = f"https://your-app.vercel.app/exam?candidate_id={parsed['id']}"

    if eligible:
        text_body = f"""
Dear {candidate_name},

Thank you for applying for the position of {target_role.replace('_',' ').title()} at Your Company.
We have reviewed your resume and are pleased to inform you that you have been shortlisted for the next stage.

Schedule your exam here: {exam_link}

Best regards,
Your HR Team
"""
        html_body = f"""
<html>
<body>
<p>Dear {candidate_name},</p>
<p>Thank you for applying for the position of <b>{target_role.replace('_',' ').title()}</b> at <b>Your Company</b>.</p>
<p>We have reviewed your resume and are pleased to inform you that you have been shortlisted for the next stage.</p>
<p><a href="{exam_link}" style="background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Schedule Your Exam</a></p>
<p>Best regards,<br>Your HR Team</p>
</body>
</html>
"""
        send_mail(email, subject, text_body, html_body)
        message = f"Email sent to {email} (Eligible)"
    else:
        text_body = f"""
Hi {candidate_name},

We received your application for the role: {target_role}.
Unfortunately, you are not eligible at this time.

Thanks!
"""
        send_mail(email, subject, text_body)
        message = f"Email sent to {email} (Not Eligible)"

    return {"status": "success", "message": message, "data": parsed}
