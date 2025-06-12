# evaluate_submission.py

rubric = {
    "functionality": 25,
    "ui_ux": 18,
    "api_integration": 20,
    "code_quality": 14,
    "testing_validation": 9,
    "git_deployment": 10,
    "bonus": 5,
    "deductions": -5
}

def calculate_total(r):
    return sum(r.values())

def print_rubric_score(rubric):
    print("📊 Evaluation Breakdown:")
    for key, value in rubric.items():
        print(f"- {key.replace('_', ' ').title()}: {value} pts")
    print(f"✅ Total Score: {calculate_total(rubric)} / 100")

if __name__ == "__main__":
    print_rubric_score(rubric)