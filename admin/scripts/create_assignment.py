#!/usr/bin/env python3
"""
Assignment Creation Script
Automates the creation of new assignments with proper structure and templates.
"""

import os
import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import shutil

class AssignmentCreator:
    def __init__(self, base_path="assignments"):
        self.base_path = Path(base_path)
        self.templates_path = Path("admin/templates")
        
    def create_assignment(self, skillset, assignment_name, difficulty="intermediate", duration_days=7):
        """Create a new assignment with all necessary files and structure."""
        
        # Create assignment directory
        assignment_path = self.base_path / skillset / assignment_name
        assignment_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (assignment_path / "starter-code").mkdir(exist_ok=True)
        (assignment_path / "reference").mkdir(exist_ok=True)
        (assignment_path / "solutions").mkdir(exist_ok=True)
        
        # Generate assignment files
        self._create_readme(assignment_path, skillset, assignment_name, difficulty, duration_days)
        self._create_tasks(assignment_path, skillset, assignment_name)
        self._create_evaluation_rubric(assignment_path, skillset, assignment_name)
        self._create_rules_of_engagement(assignment_path, skillset, assignment_name)
        
        # Create starter code structure
        self._create_starter_code(assignment_path, skillset, assignment_name)
        
        # Create reference materials
        self._create_reference_materials(assignment_path, skillset, assignment_name)
        
        print(f"✅ Assignment '{assignment_name}' created successfully!")
        print(f"📁 Location: {assignment_path}")
        
    def _create_readme(self, assignment_path, skillset, assignment_name, difficulty, duration_days):
        """Create README.md for the assignment."""
        
        deadline = datetime.now() + timedelta(days=duration_days)
        
        readme_content = f"""# 🎯 {assignment_name.replace('-', ' ').title()} Assignment - {skillset.replace('-', ' ').title()}

## 📋 Overview
[Brief description of the assignment and what candidates will build]

## 🎯 Learning Objectives
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]
- [Learning objective 4]

## 🚀 Quick Start
```bash
# Clone this assignment
git clone <assignment-url>
cd {assignment_name}

# Install dependencies
npm install

# Start development
npm run dev
```

## 📚 Resources
- [Official Documentation](https://docs.example.com/)
- [Tutorials](https://tutorials.example.com/)
- [Examples](https://examples.example.com/)

## 📅 Timeline
- **Duration**: {duration_days} days
- **Deadline**: {deadline.strftime('%B %d, %Y')}
- **Difficulty**: {difficulty.title()}
- **Extensions**: Contact hr@logbizgroup.com

## 📤 Submission
1. Fork this repository
2. Complete the assignment following the requirements in TASKS.md
3. Create a pull request with your completed work
4. Include demo video and screenshots

## 🆘 Support
- **Technical Issues**: Create a GitHub issue
- **Assignment Questions**: Email hr@logbizgroup.com
- **Mentor Support**: Contact your assigned mentor

---
*Good luck! We're excited to see what you build! 🚀*
"""
        
        with open(assignment_path / "README.md", "w") as f:
            f.write(readme_content)
    
    def _create_tasks(self, assignment_path, skillset, assignment_name):
        """Create TASKS.md with assignment requirements."""
        
        tasks_content = f"""# 📋 Assignment Tasks - {assignment_name.replace('-', ' ').title()}

## ✅ Core Requirements (80 points)

### Backend/API (25 points)
- [ ] [Backend requirement 1]
- [ ] [Backend requirement 2]
- [ ] [Backend requirement 3]
- [ ] [Backend requirement 4]

### Frontend/UI (30 points)
- [ ] [Frontend requirement 1]
- [ ] [Frontend requirement 2]
- [ ] [Frontend requirement 3]
- [ ] [Frontend requirement 4]

### Integration (15 points)
- [ ] [Integration requirement 1]
- [ ] [Integration requirement 2]
- [ ] [Integration requirement 3]

### Code Quality (10 points)
- [ ] Use TypeScript throughout
- [ ] Follow ESLint rules
- [ ] Write meaningful commit messages
- [ ] Add proper documentation

## 🚀 Bonus Features (20 points)
- [ ] [Bonus feature 1] (10 points)
- [ ] [Bonus feature 2] (5 points)
- [ ] [Bonus feature 3] (5 points)

## 📤 Deliverables
- [ ] Working application deployed online
- [ ] GitHub repository with clean commit history
- [ ] 3-5 minute demo video
- [ ] Updated README with setup instructions
- [ ] Screenshots of all features
- [ ] Code documentation and comments

## 🧪 Testing Requirements
- [ ] Unit tests for core functionality
- [ ] Integration tests for API endpoints
- [ ] End-to-end tests for user workflows
- [ ] Performance testing (if applicable)

## 📊 Evaluation Criteria
Your submission will be evaluated on:
- **Functionality** (25%): All requirements implemented and working
- **Code Quality** (20%): Clean, maintainable, well-structured code
- **UI/UX Design** (20%): Professional, responsive, user-friendly interface
- **API Integration** (15%): Proper frontend-backend communication
- **Documentation** (10%): Clear README, comments, and setup instructions
- **Bonus Features** (10%): Extra features that demonstrate advanced skills
"""
        
        with open(assignment_path / "TASKS.md", "w") as f:
            f.write(tasks_content)
    
    def _create_evaluation_rubric(self, assignment_path, skillset, assignment_name):
        """Create EVALUATION_RUBRIC.md with detailed grading criteria."""
        
        rubric_content = f"""# 📊 Evaluation Rubric - {assignment_name.replace('-', ' ').title()}

## 🎯 Grading Criteria

| Criteria | Weight | Excellent (90-100%) | Good (70-89%) | Needs Work (50-69%) | Poor (<50%) |
|----------|--------|---------------------|---------------|---------------------|-------------|
| **Functionality** | 25% | All features work perfectly | Most features work | Some features work | Many features broken |
| **Code Quality** | 20% | Clean, well-structured, documented | Good structure, some docs | Basic structure, minimal docs | Poor structure, no docs |
| **UI/UX Design** | 20% | Professional, responsive, intuitive | Good design, mostly responsive | Basic design, some responsive | Poor design, not responsive |
| **API Integration** | 15% | Perfect integration, error handling | Good integration, basic errors | Basic integration, some errors | Poor integration, many errors |
| **Documentation** | 10% | Comprehensive README, comments | Good README, some comments | Basic README, few comments | Poor README, no comments |
| **Bonus Features** | 10% | 2+ bonus features implemented | 1 bonus feature | Partial bonus feature | No bonus features |

## 🎯 Scoring Guide
- **90-100%**: Outstanding work, ready for production
- **80-89%**: Strong work, minor improvements needed
- **70-79%**: Good work, some areas need attention
- **60-69%**: Acceptable work, significant improvements needed
- **<60%**: Needs substantial improvement

## 📝 Detailed Evaluation

### Functionality (25 points)
- **All core requirements implemented** (15 points)
- **Bonus features working** (5 points)
- **Error handling and edge cases** (5 points)

### Code Quality (20 points)
- **Clean, readable code** (8 points)
- **Proper project structure** (6 points)
- **TypeScript usage** (3 points)
- **ESLint compliance** (3 points)

### UI/UX Design (20 points)
- **Professional appearance** (8 points)
- **Responsive design** (6 points)
- **User experience** (4 points)
- **Accessibility** (2 points)

### API Integration (15 points)
- **Proper API calls** (8 points)
- **Error handling** (4 points)
- **Loading states** (3 points)

### Documentation (10 points)
- **README completeness** (5 points)
- **Code comments** (3 points)
- **Setup instructions** (2 points)

### Bonus Features (10 points)
- **Feature 1** (5 points)
- **Feature 2** (3 points)
- **Feature 3** (2 points)

## 🚫 Deductions
- **-10 points**: Code doesn't run / environment is broken
- **-5 points**: Missing key features without explanation
- **-5 points**: Poor code formatting or no README
- **-3 points**: Late submission (per day)

## 🎯 Bonus Points
- **+5 points**: Exceptional documentation
- **+5 points**: Outstanding UI/UX design
- **+5 points**: Advanced features beyond requirements
- **+3 points**: Comprehensive testing
- **+2 points**: Performance optimization
"""
        
        with open(assignment_path / "EVALUATION_RUBRIC.md", "w") as f:
            f.write(rubric_content)
    
    def _create_rules_of_engagement(self, assignment_path, skillset, assignment_name):
        """Create RULES_OF_ENGAGEMENT.md with assignment guidelines."""
        
        rules_content = f"""# 🎯 Rules of Engagement - {assignment_name.replace('-', ' ').title()}

Welcome to the **{assignment_name.replace('-', ' ').title()} Assignment**! This document outlines the rules, expectations, and guidelines for completing your technical assessment.

## 📋 Assignment Overview

You are tasked with building a {assignment_name.replace('-', ' ')} application. This is a **real-world project** that demonstrates your ability to work with modern web technologies and follow professional development practices.

## 🎯 Assignment Objectives

### ✅ Core Requirements (Must Complete)
- [List core requirements here]
- [List core requirements here]
- [List core requirements here]
- [List core requirements here]

### 🚀 Bonus Features (Optional)
- [Bonus feature 1]
- [Bonus feature 2]
- [Bonus feature 3]
- [Bonus feature 4]

## 📅 Timeline & Deadlines

- **Assignment Duration**: 5-7 days from receipt
- **Submission Deadline**: As specified in your assignment email
- **Extensions**: Contact hr@logbizgroup.com with valid reasons at least 24 hours before deadline

## 🛠 Technical Requirements

### ✅ Technology Stack
- **Frontend**: [Frontend technology]
- **Backend**: [Backend technology]
- **Database**: [Database technology]
- **Styling**: [CSS framework]
- **Package Manager**: npm or yarn

### ✅ Development Environment
- **Node.js**: Version 18 or higher
- **Git**: Latest version
- **Code Editor**: VS Code recommended
- **Browser**: Chrome/Firefox/Safari latest

## 📁 Repository Structure

```
{assignment_name}/
├── frontend/          # Frontend application
├── backend/           # Backend API
├── TASKS.md          # Detailed requirements
├── EVALUATION_RUBRIC.md # Grading criteria
└── README.md         # Setup instructions
```

## 🚀 Getting Started

### 1. Repository Access
- You will receive a **private GitHub repository** link
- **Fork** the repository to your GitHub account
- **Clone** your fork to your local machine

### 2. Initial Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/{assignment_name}.git
cd {assignment_name}

# Install dependencies
cd frontend && npm install
cd ../backend && npm install

# Start development servers
# Terminal 1: Backend
cd backend && npm run dev

# Terminal 2: Frontend  
cd frontend && npm start
```

### 3. Understanding the Codebase
- **Read** `TASKS.md` thoroughly for requirements
- **Review** `EVALUATION_RUBRIC.md` for evaluation criteria
- **Examine** existing code structure before making changes

## 📝 Development Guidelines

### ✅ Code Standards
- **TypeScript**: Use strict mode, proper typing
- **ESLint**: Follow linting rules, no warnings
- **Prettier**: Consistent code formatting
- **Comments**: Document complex logic
- **Git**: Meaningful commit messages

### ✅ Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add [feature description]"

# Push to your fork
git push origin feature/your-feature-name
```

### ✅ Commit Message Format
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code refactoring
- `test:` Adding tests

## 🧪 Testing & Quality Assurance

### ✅ Before Submission
- [ ] Application runs without errors
- [ ] All core features work as expected
- [ ] Code passes linting (`npm run lint`)
- [ ] No console errors in browser
- [ ] Responsive design works on mobile
- [ ] API endpoints return correct data

### ✅ Testing Checklist
- [ ] [Test requirement 1]
- [ ] [Test requirement 2]
- [ ] [Test requirement 3]
- [ ] [Test requirement 4]
- [ ] [Test requirement 5]
- [ ] [Test requirement 6]

## 📤 Submission Requirements

### ✅ Required Deliverables
1. **GitHub Repository**: Your completed fork with all code
2. **Demo Video**: 3-5 minute walkthrough of your application
3. **README.md**: Updated with setup instructions and screenshots
4. **Live Demo**: Deployed application (Vercel, Netlify, or similar)

### ✅ README.md Requirements
```markdown
# {assignment_name.replace('-', ' ').title()} - [Your Name]

## 🚀 Live Demo
[Link to deployed application]

## 📸 Screenshots
[Add screenshots of your application]

## 🛠 Technologies Used
- Frontend: [Frontend technologies]
- Backend: [Backend technologies]
- Deployment: [Platform used]

## 🏃‍♂️ Quick Start
[Setup instructions]

## ✨ Features Implemented
- [List of completed features]

## 🎯 Bonus Features
- [List of bonus features if any]
```

## 🚫 What NOT to Do

### ❌ Prohibited Actions
- **Copying code** from other sources without attribution
- **Using AI-generated code** without understanding it
- **Sharing your repository** with other candidates
- **Submitting incomplete work** without explanation
- **Ignoring the assignment requirements**
- **Using outdated or incompatible dependencies**

### ❌ Code Quality Issues
- Hardcoded values instead of environment variables
- No error handling
- Poor component structure
- Inconsistent naming conventions
- No TypeScript types
- Console.log statements in production code

## 🎯 Evaluation Criteria

Your submission will be evaluated on:

| Criteria | Weight | Description |
|----------|--------|-------------|
| **Functionality** | 25% | All requirements implemented and working |
| **Code Quality** | 20% | Clean, maintainable, well-structured code |
| **UI/UX Design** | 20% | Professional, responsive, user-friendly interface |
| **API Integration** | 15% | Proper frontend-backend communication |
| **Documentation** | 10% | Clear README, comments, and setup instructions |
| **Bonus Features** | 10% | Extra features that demonstrate advanced skills |

## 🆘 Getting Help

### ✅ Acceptable Help Sources
- **Official Documentation**: [Technology] docs
- **Stack Overflow**: For specific technical issues
- **GitHub Issues**: Repository-specific questions
- **Code Examples**: From official tutorials and guides

### ❌ Unacceptable Help
- **Direct code sharing** with other candidates
- **Using complete solutions** from GitHub
- **Hiring someone** to complete the assignment
- **Using AI tools** to generate entire features

## 📞 Support & Communication

### ✅ Contact Information
- **Technical Issues**: Create GitHub issue in the repository
- **Assignment Questions**: Email hr@logbizgroup.com
- **Submission Issues**: Contact immediately before deadline

### ✅ Response Times
- **Weekdays**: Within 24 hours
- **Weekends**: Within 48 hours
- **Urgent Issues**: Same day if possible

## 🏆 Success Tips

### ✅ Best Practices
1. **Start Early**: Don't wait until the last minute
2. **Plan First**: Sketch your UI and plan your API structure
3. **Test Incrementally**: Test each feature as you build it
4. **Commit Regularly**: Small, frequent commits with clear messages
5. **Document as You Go**: Write README and comments while coding
6. **Focus on Quality**: Better to submit polished core features than rushed bonus features

### ✅ Common Pitfalls to Avoid
- Over-engineering simple features
- Ignoring mobile responsiveness
- Poor error handling
- Inconsistent UI design
- Not testing edge cases
- Rushing deployment setup

## 🎉 Final Notes

This assignment is designed to:
- **Assess your technical skills** in a real-world context
- **Demonstrate your problem-solving approach**
- **Show your code quality and attention to detail**
- **Evaluate your ability to follow requirements**

**Remember**: Quality over quantity. A well-implemented core feature is better than many incomplete features.

---

**Good luck! We're excited to see what you build! 🚀**

---

*Last Updated: {datetime.now().strftime('%B %d, %Y')}*
*Version: 1.0*
"""
        
        with open(assignment_path / "RULES_OF_ENGAGEMENT.md", "w") as f:
            f.write(rules_content)
    
    def _create_starter_code(self, assignment_path, skillset, assignment_name):
        """Create starter code structure based on skillset."""
        
        starter_path = assignment_path / "starter-code"
        
        if "frontend" in skillset.lower():
            # Create React/TypeScript starter
            (starter_path / "frontend").mkdir(exist_ok=True)
            (starter_path / "backend").mkdir(exist_ok=True)
            
            # Create package.json for frontend
            frontend_package = {
                "name": f"{assignment_name}-frontend",
                "version": "1.0.0",
                "scripts": {
                    "dev": "vite",
                    "build": "tsc && vite build",
                    "preview": "vite preview",
                    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
                },
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0"
                },
                "devDependencies": {
                    "@types/react": "^18.2.0",
                    "@types/react-dom": "^18.2.0",
                    "@typescript-eslint/eslint-plugin": "^6.0.0",
                    "@typescript-eslint/parser": "^6.0.0",
                    "@vitejs/plugin-react": "^4.0.0",
                    "eslint": "^8.45.0",
                    "typescript": "^5.0.0",
                    "vite": "^4.4.0"
                }
            }
            
            with open(starter_path / "frontend" / "package.json", "w") as f:
                json.dump(frontend_package, f, indent=2)
        
        elif "backend" in skillset.lower():
            # Create Express/Node.js starter
            (starter_path / "backend").mkdir(exist_ok=True)
            
            backend_package = {
                "name": f"{assignment_name}-backend",
                "version": "1.0.0",
                "scripts": {
                    "dev": "nodemon src/index.ts",
                    "build": "tsc",
                    "start": "node dist/index.js",
                    "test": "jest"
                },
                "dependencies": {
                    "express": "^4.18.0",
                    "cors": "^2.8.5",
                    "dotenv": "^16.0.0"
                },
                "devDependencies": {
                    "@types/express": "^4.17.0",
                    "@types/cors": "^2.8.0",
                    "@types/node": "^20.0.0",
                    "typescript": "^5.0.0",
                    "nodemon": "^3.0.0",
                    "ts-node": "^10.9.0"
                }
            }
            
            with open(starter_path / "backend" / "package.json", "w") as f:
                json.dump(backend_package, f, indent=2)
    
    def _create_reference_materials(self, assignment_path, skillset, assignment_name):
        """Create reference materials and documentation."""
        
        ref_path = assignment_path / "reference"
        
        # Create docs directory
        (ref_path / "docs").mkdir(exist_ok=True)
        (ref_path / "tutorials").mkdir(exist_ok=True)
        (ref_path / "examples").mkdir(exist_ok=True)
        
        # Create reference README
        ref_readme = f"""# 📚 Reference Materials - {assignment_name.replace('-', ' ').title()}

## 📖 Documentation
- [Official Documentation](https://docs.example.com/)
- [API Reference](https://api.example.com/)
- [Best Practices](https://best-practices.example.com/)

## 🎓 Tutorials
- [Getting Started Guide](https://tutorials.example.com/getting-started)
- [Advanced Concepts](https://tutorials.example.com/advanced)
- [Common Patterns](https://tutorials.example.com/patterns)

## 💡 Examples
- [Basic Example](examples/basic-example.md)
- [Advanced Example](examples/advanced-example.md)
- [Best Practices Example](examples/best-practices.md)

## 🔗 Additional Resources
- [Community Forum](https://community.example.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/technology)
- [GitHub Discussions](https://github.com/org/repo/discussions)

## 📝 Notes
- These resources are for reference only
- Focus on understanding concepts, not copying code
- Use official documentation as your primary source
"""
        
        with open(ref_path / "README.md", "w") as f:
            f.write(ref_readme)

def main():
    parser = argparse.ArgumentParser(description="Create a new assignment")
    parser.add_argument("skillset", help="Skillset (e.g., frontend-development)")
    parser.add_argument("assignment_name", help="Assignment name (e.g., task-tracker)")
    parser.add_argument("--difficulty", default="intermediate", 
                       choices=["beginner", "intermediate", "advanced"],
                       help="Assignment difficulty level")
    parser.add_argument("--duration", type=int, default=7,
                       help="Assignment duration in days")
    
    args = parser.parse_args()
    
    creator = AssignmentCreator()
    creator.create_assignment(
        skillset=args.skillset,
        assignment_name=args.assignment_name,
        difficulty=args.difficulty,
        duration_days=args.duration
    )

if __name__ == "__main__":
    main() 