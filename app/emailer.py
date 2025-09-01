import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# SMTP Configuration from environment
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)

# Validate configuration
if not all([SMTP_USERNAME, SMTP_PASSWORD]):
    logging.warning("⚠ SMTP credentials are missing! Please set SMTP_USERNAME and SMTP_PASSWORD in environment variables.")

def send_mail(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email using SMTP.
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): HTML content of the email
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Prepare message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connect to SMTP server
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, to_email, msg.as_string())

        logging.info(f"✅ Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        logging.error("❌ SMTP Authentication failed. Check your username/password.")
    except smtplib.SMTPConnectError:
        logging.error("❌ Failed to connect to SMTP server.")
    except smtplib.SMTPException as e:
        logging.error(f"❌ SMTP error occurred: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")

    return False
