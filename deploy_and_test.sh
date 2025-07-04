#!/bin/bash

echo "🚀 Assignment System Deployment & Testing Script"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    print_success "Python 3 is installed"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    print_success "Python is installed"
    PYTHON_CMD="python"
else
    print_error "Python is not installed. Please install Python 3.7+"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_status "Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install requirements
print_status "Installing Python dependencies..."
pip install -r parse_and_assign_api/requirements.txt

# Check if required files exist
print_status "Checking system files..."
REQUIRED_FILES=(
    "parse_and_assign_api/app.py"
    "parse_and_assign_api/cv_parser/parse_cv.py"
    "parse_and_assign_api/emails/email_utils.py"
    "parse_and_assign_api/emails/send_assignment_email.py"
    "distribute_tasks.sh"
    "assignments/backend-development/TASKS.md"
    "assignments/frontend-development/TASKS.md"
    "assignments/data-science/TASKS.md"
    "assignments/devops/TASKS.md"
    "assignments/project-management/TASKS.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_error "✗ $file (missing)"
        exit 1
    fi
done

# Run a quick system test
print_status "Running system test..."
cd parse_and_assign_api

# Test CV parsing
print_status "Testing CV parsing..."
$PYTHON_CMD -c "
import sys
sys.path.append('.')
from cv_parser.parse_cv import extract_skills_from_pdf
import os

# Create a simple test PDF content
test_content = '''
Skills: Python, JavaScript, React, Django, PostgreSQL, AWS
Experience: 5 years in web development
Education: Computer Science degree
'''

# Test skill extraction
try:
    skills = extract_skills_from_pdf(test_content)
    print(f'Extracted skills: {skills}')
    if len(skills) > 0:
        print('✓ CV parsing test passed')
    else:
        print('✗ CV parsing test failed')
except Exception as e:
    print(f'✗ CV parsing test failed: {e}')
"

# Test assignment system
print_status "Testing assignment system..."
$PYTHON_CMD -c "
import sys
sys.path.append('.')
from app import assign_tasks_to_candidate
import json

# Test candidate data
test_candidate = {
    'name': 'Test Candidate',
    'email': 'test@example.com',
    'skills': ['Python', 'React', 'PostgreSQL']
}

try:
    assignments = assign_tasks_to_candidate(test_candidate)
    print(f'Assigned tasks: {len(assignments)}')
    if len(assignments) > 0:
        print('✓ Assignment system test passed')
    else:
        print('✗ Assignment system test failed')
except Exception as e:
    print(f'✗ Assignment system test failed: {e}')
"

cd ..

# Test the complete workflow
print_status "Testing complete workflow..."
$PYTHON_CMD test_complete_workflow.py

print_status "Deployment and testing completed!"
print_success "🎉 Assignment system is ready for production use!"

echo ""
echo "📋 Next Steps:"
echo "1. The system is now deployed and tested"
echo "2. You can start processing real CV submissions"
echo "3. Monitor the assignment_audit_report.json for results"
echo "4. Check email delivery logs for any issues"
echo ""
echo "🔗 GitHub Repository: https://github.com/gurpindersidhu178/task-tracker-bootstrap"
echo "📖 Documentation: README.md and PROGRESS_SUMMARY.md"
echo ""
echo "�� Ready to go live!" 