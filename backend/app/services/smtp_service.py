# backend/app/services/smtp_service.py
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from app.core.config import get_settings

settings = get_settings()

def send_email(to_email: str, subject: str, body: str, from_email: str = "noreply@emailproai.com"):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = formataddr(("EmailProAI", from_email))
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.sendmail(from_email, [to_email], msg.as_string())


