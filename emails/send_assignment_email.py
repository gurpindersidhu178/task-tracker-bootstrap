import json
from email_utils import send_email

def load_profile(profile_file):
    with open(profile_file) as f:
        return json.load(f)

def build_assignment_email(profile):
    name = profile["name"]
    skills = ", ".join(profile["skills"])
    subject = f"Logbiz Task Assignment for {name}"
    body = f"""
Hi {name},

Based on your skills ({skills}), we’ve matched you to a project-based assignment hosted on GitHub.

🔗 Assignment Branch: https://github.com/logbiz/task-tracker-bootstrap/tree/{profile['skills'][0].lower()}

Please follow the instructions in the README.md to complete and submit it within 5 days.

Good luck!
Team Logbiz
"""
    return subject, body

if __name__ == "__main__":
    profile = load_profile("aisha_verma_profile.json")
    subject, body = build_assignment_email(profile)
    send_email(subject, body, profile["email"])