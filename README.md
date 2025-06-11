# 🧱 Task Tracker Full-Stack Starter

This repository provides a ready-to-run full-stack boilerplate using:

- **Frontend**: Vite + React + TypeScript
- **Backend**: Node.js + Express + MongoDB
- **Dev Proxy**: Configured for local API routing via Vite
- **Ports**: Frontend `5173`, Backend `5050`

## 📦 How to Use

### Option 1: Clone & Run
```bash
git clone https://github.com/your-username/task-tracker-bootstrap.git
cd task-tracker-bootstrap
chmod +x task-tracker-setup-typescript.sh
./task-tracker-setup-typescript.sh
```

### Option 2: Use as Template
- Click “Use this template” on GitHub
- Create a new repo
- Clone and run the script as above

## 🧪 Local Development

### Backend
```bash
cd task-tracker/backend
npm install
npx nodemon index.js
```

### Frontend
```bash
cd task-tracker/frontend
npm install
npm run dev
```

MongoDB default URI is: `mongodb://localhost:27017/task-tracker`

## 🌍 Deployment
- **Backend**: Deploy to [Railway](https://railway.app)
- **Frontend**: Deploy to [Vercel](https://vercel.com)

## 🎓 Use Case
Perfect for bootstrapping:
- Student assessment projects
- Internal admin tools
- Rapid MVPs

---

MIT © LogbizTech