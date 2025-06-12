import subprocess

def run_script(script, *args):
    command = ["python3", script, *args]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ ERROR:", result.stderr)

if __name__ == "__main__":
    print("🔍 1. Parsing CV...")
    run_script("parse_cv.py", "aisha_cv.pdf")  # Replace with your actual CV file

    print("📬 2. Sending Assignment Email...")
    run_script("send_assignment_email.py")

    print("🧪 3. Running Evaluation...")
    run_script("evaluate_submission.py")

    print("📝 4. Generating Feedback Report...")
    run_script("generate_feedback.py")

    print("🏆 5. Generating Certificate...")
    run_script("generate_certificate.py")

    print("📩 6. Sending Feedback Email...")
    run_script("send_feedback_email.py")

    print("✅ Workflow complete.")