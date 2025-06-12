# generate_feedback.py

import json
from datetime import datetime

rubric = {
    "candidate": "Aisha Verma",
    "score_breakdown": {
        "functionality": 25,
        "ui_ux": 20,
        "api_integration": 20,
        "code_quality": 13,
        "testing_validation": 7,
        "git_deployment": 10,
        "bonus": 0,
        "deductions": -3
    }
}

def calculate_total(score_breakdown):
    return sum(score_breakdown.values())

def generate_feedback(rubric_data):
    total = calculate_total(rubric_data["score_breakdown"])
    candidate = rubric_data["candidate"]
    feedback = {
        "candidate": candidate,
        "total_score": total,
        "result": "Passed with Distinction" if total >= 80 else "Completed",
        "feedback_summary": "",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    if total >= 90:
        feedback["feedback_summary"] = f"{candidate} demonstrated excellent technical proficiency and clean implementation."
    elif total >= 80:
        feedback["feedback_summary"] = f"{candidate} showed strong understanding with minor improvement areas."
    elif total >= 70:
        feedback["feedback_summary"] = f"{candidate} completed the task with acceptable quality. Suggest refining code structure."
    else:
        feedback["feedback_summary"] = f"{candidate} needs improvement in core areas. Suggest guided mentorship."

    with open("feedback_report.json", "w") as f:
        json.dump(feedback, f, indent=2)

    print(f"✅ Feedback generated for {candidate} (Total Score: {total})")
    return feedback

if __name__ == "__main__":
    generate_feedback(rubric)