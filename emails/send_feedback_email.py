import json
from email_utils import send_email

def load_feedback():
    with open("feedback_report.json") as f:
        return json.load(f)

def build_feedback_email(report):
    name = report["candidate"]
    result = report["result"]
    score = report["total_score"]
    summary = report["feedback_summary"]
    subject = f"Logbiz Feedback Report for {name}"
    body = f"""
Hi {name},

Here is your feedback from the Logbiz assignment review:

📊 Score: {score}%
🎯 Result: {result}

💬 Summary:
{summary}

Thank you for participating!

Team Logbiz
"""
    return subject, body

if __name__ == "__main__":
    report = load_feedback()
    cert_file = f"{report['candidate'].replace(' ', '_').lower()}_certificate.pdf"
    send_email(subject=build_feedback_email(report)[0],
               body=build_feedback_email(report)[1],
               to_email="example@example.com",  # replace with report["email"] if available
               attachment_path=cert_file if report["total_score"] >= 80 else None)