#!/bin/bash

echo "🚀 Deployment Assistant for Task Tracker Project"

echo ""
echo "🔧 STEP 1: BACKEND DEPLOYMENT TO RAILWAY"
echo "----------------------------------------"
echo "If you don't have a Railway account:"
echo " 👉 Visit: https://railway.app"
echo " 👉 Sign up using GitHub"

echo ""
echo "To deploy the backend:"
echo "1. Go to: https://railway.app/new"
echo "2. Select 'Deploy from GitHub Repo'"
echo "3. Choose this repo: task-tracker-bootstrap"
echo "4. Set Environment Variables:"
echo "   - MONGO_URI = your MongoDB URI (local or Atlas)"
echo "   - PORT = 5050"
echo "5. Deploy!"

echo ""
echo "📂 Your backend will be live at: https://<project-name>.up.railway.app"

echo ""
echo "🌐 STEP 2: FRONTEND DEPLOYMENT TO VERCEL"
echo "----------------------------------------"
echo "If you don’t have a Vercel account:"
echo " 👉 Visit: https://vercel.com"
echo " 👉 Sign up using GitHub"

echo ""
echo "To deploy the frontend:"
echo "1. Go to: https://vercel.com/new"
echo "2. Import your GitHub repo: task-tracker-bootstrap"
echo "3. Set project root to: frontend/"
echo "4. Set Environment Variables (if needed)"
echo "5. Add these build settings:"
echo "   - Framework Preset: Vite"
echo "   - Build Command: npm run build"
echo "   - Output Directory: dist"

echo ""
echo "✅ Once deployed, your app will be live at: https://<your-project>.vercel.app"

echo ""
echo "🌟 All Done! Your full-stack app is now cloud-hosted and production-ready."