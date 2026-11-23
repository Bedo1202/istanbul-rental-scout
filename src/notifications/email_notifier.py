
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


def send_email(subject, body):
    """Send a plain-text email using SMTP."""

    load_dotenv()

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("EMAIL_FROM")
    recipient = os.getenv("EMAIL_TO")

    if not all([host, username, password, sender, recipient]):
        raise ValueError("Missing email configuration.")

    if os.getenv("SMTP_USE_TLS", "True").lower() != "true":
        raise ValueError("TLS must be enabled.")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.send_message(message)

        return True

    except smtplib.SMTPException as error:
        print(f"Email delivery failed: {type(error).__name__}")
        return False

    except OSError as error:
        print(f"Network error: {type(error).__name__}")
        return False
