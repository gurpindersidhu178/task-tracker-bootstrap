# 📋 TASKS.md Structure Guide

## 🎯 Overview

This document explains how TASKS.md files are organized across your GitHub branches and skillsets.

---

## 🌳 Branch Structure

```
task-tracker-bootstrap/
├── main/                           # Master branch with complete overview
│   ├── TASKS.md                    # ← Complete guide (ALL assignments)
│   ├── SKILLSETS_OVERVIEW.md       # Skillset descriptions
│   └── assignments/                # Assignment folders
│       ├── frontend-development/
│       ├── backend-development/
│       ├── data-science/
│       ├── devops/
│       └── project-management/
│
├── frontend-development/           # Frontend branch
│   └── TASKS.md                    # ← Frontend assignments only
│
├── backend-development/            # Backend branch
│   └── TASKS.md                    # ← Backend assignments only
│
├── data-science/                   # Data Science branch
│   └── TASKS.md                    # ← Data Science assignments only
│
├── devops/                         # DevOps branch
│   └── TASKS.md                    # ← DevOps assignments only
│
└── project-management/             # Project Management branch
    └── TASKS.md                    # ← Project Management assignments only
```

---

## 📋 TASKS.md Types

### 1. **Master TASKS.md** (main branch)
**Purpose**: Complete overview of ALL assignments
**Audience**: Admins, HR team, overview purposes
**Content**: 
- All 5 skillset assignments
- Complete submission guidelines
- Evaluation process
- Support resources

### 2. **Skillset-Specific TASKS.md** (individual branches)
**Purpose**: Focused guide for specific skillset
**Audience**: Students assigned to that skillset
**Content**:
- Only relevant assignments
- Skillset-specific resources
- Focused best practices

---

## 🔄 Maintenance Workflow

### When Adding New Assignments:

1. **Update Master TASKS.md** (main branch)
   ```bash
   git checkout main
   # Edit TASKS.md to add new assignment
   git add TASKS.md
   git commit -m "Add new assignment: [Assignment Name]"
   git push origin main
   ```

2. **Update Skillset-Specific TASKS.md** (relevant branch)
   ```bash
   git checkout [skillset-branch]
   # Edit assignments/[skillset]/TASKS.md
   git add assignments/[skillset]/TASKS.md
   git commit -m "Add new assignment to [skillset] track"
   git push origin [skillset-branch]
   ```

### When Updating Existing Assignments:

1. **Update both files** to maintain consistency
2. **Test the changes** in both contexts
3. **Update version numbers** and dates

---

## 🎯 Assignment Distribution Process

### For HR Team:

1. **Review candidate profile** and determine skillset
2. **Checkout appropriate branch**:
   ```bash
   git checkout [skillset-branch]
   ```
3. **Send assignment link** to candidate
4. **Monitor progress** through GitHub

### For Students:

1. **Receive assignment link** (points to specific branch)
2. **Read skillset-specific TASKS.md**
3. **Follow assignment instructions**
4. **Submit via pull request**

---

## 📊 Benefits of This Structure

### ✅ Advantages:
- **Focused Experience**: Students see only relevant assignments
- **Easy Maintenance**: Update skillset-specific content independently
- **Clear Organization**: Logical separation by skillset
- **Scalable**: Easy to add new skillsets and assignments

### ⚠️ Considerations:
- **Sync Maintenance**: Keep master and skillset files in sync
- **Version Control**: Track changes across multiple files
- **Consistency**: Ensure formatting and standards are consistent

---

## 🛠️ Tools and Scripts

### Automated Sync Script (Recommended)
Create a script to sync changes between master and skillset files:

```bash
#!/bin/bash
# sync_tasks.sh - Sync TASKS.md across branches

# Update master TASKS.md
git checkout main
# ... sync logic ...

# Update each skillset branch
for branch in frontend-development backend-development data-science devops project-management; do
    git checkout $branch
    # ... sync logic ...
    git push origin $branch
done

git checkout main
```

### Validation Script
Create a script to validate consistency:

```bash
#!/bin/bash
# validate_tasks.sh - Validate TASKS.md consistency

# Check for missing assignments
# Validate formatting
# Ensure all links work
```

---

## 📝 Best Practices

### For Admins:
1. **Always update both files** when making changes
2. **Use consistent formatting** across all TASKS.md files
3. **Version control everything** with meaningful commit messages
4. **Test the workflow** before distributing assignments

### For Students:
1. **Read the skillset-specific TASKS.md** for your assignment
2. **Refer to master TASKS.md** for general guidelines
3. **Follow the submission process** exactly as outlined
4. **Ask questions early** if anything is unclear

---

## 🔍 Quick Reference

### Branch Names:
- `main` - Complete overview
- `frontend-development` - Frontend assignments
- `backend-development` - Backend assignments
- `data-science` - Data Science assignments
- `devops` - DevOps assignments
- `project-management` - Project Management assignments

### File Locations:
- Master: `/TASKS.md` (main branch)
- Skillset: `/assignments/[skillset]/TASKS.md` (respective branch)

### Contact:
- **HR Team**: hr@logbizgroup.com
- **Technical Support**: GitHub issues
- **Mentor Support**: Assigned mentor contact

---

*This structure ensures a clean, organized, and maintainable assignment system for both admins and students.* 