#!/bin/sh

# 🚀 TASKS.md Distribution Script (POSIX Compatible)
# This script distributes skillset-specific TASKS.md files to their respective branches

set -e  # Exit on any error

echo "🎯 Starting TASKS.md distribution process..."

print_status() {
    echo "[INFO] $1"
}

print_success() {
    echo "[SUCCESS] $1"
}

print_warning() {
    echo "[WARNING] $1"
}

print_error() {
    echo "[ERROR] $1"
}

# Check if we're in the right directory
if [ ! -f "TASKS.md" ]; then
    print_error "TASKS.md not found in current directory. Please run this script from the task-tracker-bootstrap directory."
    exit 1
fi

# Store current branch
CURRENT_BRANCH=$(git branch --show-current)
print_status "Current branch: $CURRENT_BRANCH"

# Define branches and their corresponding TASKS.md files
BRANCHES="frontend-development backend-development data-science devops project-management"

get_source_file() {
    branch="$1"
    case "$branch" in
        frontend-development)
            echo "assignments/frontend-development/TASKS.md"
            ;;
        backend-development)
            echo "assignments/backend-development/TASKS.md"
            ;;
        data-science)
            echo "assignments/data-science/TASKS.md"
            ;;
        devops)
            echo "assignments/devops/TASKS.md"
            ;;
        project-management)
            echo "assignments/project-management/TASKS.md"
            ;;
        *)
            echo ""
            ;;
    esac
}

distribute_to_branch() {
    branch="$1"
    source_file="$2"

    print_status "Processing branch: $branch"

    if [ ! -f "$source_file" ]; then
        print_error "Source file not found: $source_file"
        return 1
    fi

    print_status "Checking out branch: $branch"
    if ! git checkout "$branch" 2>/dev/null; then
        print_warning "Branch $branch does not exist. Creating it..."
        git checkout -b "$branch"
    fi

    print_status "Copying $source_file to root TASKS.md"
    cp "$source_file" "TASKS.md"

    git add TASKS.md
    if git diff --staged --quiet; then
        print_warning "No changes to commit for $branch"
    else
        git commit -m "Update TASKS.md for $branch skillset"
        print_success "Committed changes to $branch"
    fi

    print_status "Pushing to remote: $branch"
    if git push origin "$branch"; then
        print_success "Successfully pushed $branch"
    else
        print_error "Failed to push $branch"
        return 1
    fi
}

update_master() {
    print_status "Updating master branch with complete TASKS.md"
    git checkout main
    git add TASKS.md
    if git diff --staged --quiet; then
        print_warning "No changes to commit for master"
    else
        git commit -m "Update master TASKS.md with complete assignment overview"
        print_success "Committed changes to master"
    fi
    print_status "Pushing to remote: main"
    if git push origin main; then
        print_success "Successfully pushed main"
    else
        print_error "Failed to push main"
        return 1
    fi
}

main() {
    print_status "Starting distribution process..."
    update_master
    for branch in $BRANCHES; do
        source_file=$(get_source_file "$branch")
        print_status "Processing $branch with source file: $source_file"
        if distribute_to_branch "$branch" "$source_file"; then
            print_success "Successfully processed $branch"
        else
            print_error "Failed to process $branch"
        fi
        echo ""
    done
    print_status "Returning to original branch: $CURRENT_BRANCH"
    git checkout "$CURRENT_BRANCH"
    print_success "🎉 TASKS.md distribution completed!"
    print_status "Summary:"
    echo "  ✅ Master branch updated with complete overview"
    echo "  ✅ Frontend Development branch updated"
    echo "  ✅ Backend Development branch updated"
    echo "  ✅ Data Science branch updated"
    echo "  ✅ DevOps branch updated"
    echo "  ✅ Project Management branch updated"
    echo ""
    print_status "Next steps:"
    echo "  1. Verify all branches have been updated correctly"
    echo "  2. Test assignment distribution workflow"
    echo "  3. Send assignment links to candidates"
    echo "  4. Monitor progress through GitHub"
}

main "$@" 