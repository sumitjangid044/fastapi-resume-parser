import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)
DRY_RUN = os.getenv("DRY_RUN_EMAILS", "true").lower() == "true"

def send_mail(to_email: str, subject: str, body: str, html_body: str = None) -> bool:
    print(f"Sending email to {to_email} with subject: {subject}")

    if DRY_RUN:
        print("[DRY RUN MODE] Email content below:")
        print(body)
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email

        # Attach plain text
        part1 = MIMEText(body, "plain")
        msg.attach(part1)

        # Attach HTML (if provided)
        if html_body:
            part2 = MIMEText(html_body, "html")
            msg.attach(part2)

        # Send email via SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully.")
        return True

    except Exception as e:
        print(f"Email send failed: {e}")
        return False
