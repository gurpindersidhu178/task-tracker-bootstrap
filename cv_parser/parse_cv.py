import os
import re
import sys
import json
from docx import Document
from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_email(text):
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"(\+91[-\s]?|0)?[6-9]\d{9}", text)
    return match.group(0) if match else None

def extract_skills(text):
    known_skills = ["React", "Node.js", "JavaScript", "Python", "MongoDB", "Express", "TypeScript", "Git", "Docker"]
    skills_found = [skill for skill in known_skills if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]
    return skills_found

def extract_projects(text):
    lines = text.splitlines()
    project_keywords = ["project", "built", "developed", "created"]
    projects = [line.strip() for line in lines if any(word in line.lower() for word in project_keywords)]
    return projects[:5]  # return top 5 matches

def parse_cv(filepath):
    if filepath.endswith(".pdf"):
        text = extract_text_from_pdf(filepath)
    elif filepath.endswith(".docx"):
        text = extract_text_from_docx(filepath)
    else:
        print("❌ Unsupported file format. Use PDF or DOCX.")
        return

    profile = {
        "name": os.path.basename(filepath).split('.')[0],
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "projects": extract_projects(text),
        "raw_text_snippet": text[:1000]  # helpful for review
    }

    output_filename = f"{profile['name'].replace(' ', '_').lower()}_profile.json"
    with open(output_filename, "w") as f:
        json.dump(profile, f, indent=2)

    print(f"✅ Profile extracted and saved to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 parse_cv.py <resume.pdf|resume.docx>")
    else:
        parse_cv(sys.argv[1])