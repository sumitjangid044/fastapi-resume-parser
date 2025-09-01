from app.utils.emailer import send_mail

result = send_mail(
    to_email="your_email@gmail.com",  # यहाँ अपना email डालो
    subject="Test Email",
    body="This is a test email from FastAPI project.",
    html_body="<h2>This is a test email from FastAPI project.</h2>"
)

print(result)
