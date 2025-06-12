# generate_certificate.py

from fpdf import FPDF
import json
from datetime import datetime

def generate_certificate(candidate_name, score):
    if score < 80:
        print(f"⛔ Score {score} is below 80. Certificate not generated.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    pdf.cell(200, 10, txt="Logbiz Certificate of Completion", ln=1, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, f"This certifies that {candidate_name} has successfully completed the Logbiz Task Tracker Challenge with a score of {score}%.")
    pdf.ln(5)
    pdf.cell(0, 10, txt=f"Issued on: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    filename = f"{candidate_name.replace(' ', '_').lower()}_certificate.pdf"
    pdf.output(filename)
    print(f"🏆 Certificate saved as {filename}")

if __name__ == "__main__":
    with open("feedback_report.json") as f:
        data = json.load(f)
        generate_certificate(data["candidate"], data["total_score"])