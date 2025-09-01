import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)
DRY_RUN = os.getenv("DRY_RUN_EMAILS", "true").lower() == "true"

def send_mail(to_email: str, subject: str, body: str, html_body: str = None) -> dict:
    """
    Sends an email using SMTP configuration from environment variables.
    
    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject.
        body (str): Plain text body.
        html_body (str, optional): HTML body.

    Returns:
        dict: {"success": bool, "message": str}
    """
    print(f"[INFO] Sending email to {to_email} with subject: {subject}")

    if DRY_RUN:
        print("[DRY RUN MODE ENABLED] Email not sent.")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        if html_body:
            print(f"HTML Body: {html_body}")
        return {"success": True, "message": "Dry run mode - email not sent."}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email

        # Attach plain text
        msg.attach(MIMEText(body, "plain"))

        # Attach HTML (if provided)
        if html_body:
            msg.attach(MIMEText(html_body, "html"))

        # Connect and send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print("[SUCCESS] Email sent successfully.")
        return {"success": True, "message": "Email sent successfully."}

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[ERROR] Failed to send email: {e}\nTraceback: {error_trace}")
        return {"success": False, "message": f"Error sending email: {str(e)}"}
