import smtplib
from email.message import EmailMessage
import os

def send_email(subject, body, to_email, attachment_path=None):
    EMAIL_ADDRESS = os.environ.get("GMAIL_USER")
    EMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise EnvironmentError("GMAIL_USER or GMAIL_APP_PASSWORD not set in environment variables.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"📧 Email sent to {to_email}")