#!/bin/bash

echo "📁 Navigating to project root..."
cd ~/LogbizTech/task-tracker || { echo '❌ Directory not found'; exit 1; }

echo "🔄 Initializing Git repository..."
git init

echo "📄 Creating .gitignore..."
cat <<EOF > .gitignore
# Ignore Node modules
node_modules/
.env
dist/
.vscode/
.DS_Store
EOF

echo "📝 Creating README.md..."
cat <<EOF > README.md
# Task Tracker App

A full-stack application built with:
- Frontend: Vite + React + TypeScript
- Backend: Node.js + Express + MongoDB
- Dev Proxy: Vite proxying API to Express
- Local Ports: 5173 (frontend), 5050 (backend)

## Setup

### Backend
1. \`cd backend\`
2. \`npm install\`
3. Set your MongoDB URI in \`.env\`
4. \`npx nodemon index.js\`

### Frontend
1. \`cd frontend\`
2. \`npm install\`
3. \`npm run dev\`

### Deployment (Next Steps)
- Backend → Railway
- Frontend → Vercel
EOF

echo "✅ Adding all files to Git..."
git add .

echo "📌 Commiting initial setup..."
git commit -m 'Initial commit: full-stack task tracker app'

echo "🌐 Git repo is ready. To push to GitHub:"
echo "1. Create a new repo on GitHub (empty)"
echo "2. Run:"
echo "   git remote add origin https://github.com/your-username/your-repo.git"
echo "   git branch -M main"
echo "   git push -u origin main"

echo "✅ Local git setup complete."