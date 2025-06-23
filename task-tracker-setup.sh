#!/bin/bash

echo "🔧 Creating Task Tracker Full-Stack Project..."

# Create root project folder
mkdir task-tracker && cd task-tracker

# ------------------ Backend Setup ------------------

echo "📦 Setting up Node.js backend..."

mkdir backend && cd backend
npm init -y

# Install dependencies
npm install express mongoose dotenv cors

# Install dev dependencies
npm install --save-dev nodemon

# Create basic files and folders
mkdir models routes
touch index.js .env .gitignore
touch routes/tasks.js
touch models/Task.js

# Populate .gitignore
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore

# Add basic server code to index.js
cat <<EOF > index.js
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB connection error:", err));

const taskRoutes = require("./routes/tasks");
app.use("/api/tasks", taskRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(\`🚀 Server running on port \${PORT}\`));
EOF

# Add basic task model
cat <<EOF > models/Task.js
const mongoose = require("mongoose");

const taskSchema = new mongoose.Schema({
  title: { type: String, required: true },
  completed: { type: Boolean, default: false }
});

module.exports = mongoose.model("Task", taskSchema);
EOF

# Add basic task route
cat <<EOF > routes/tasks.js
const express = require("express");
const Task = require("../models/Task");
const router = express.Router();

router.get("/", async (req, res) => {
  const tasks = await Task.find();
  res.json(tasks);
});

router.post("/", async (req, res) => {
  const task = new Task(req.body);
  await task.save();
  res.json(task);
});

router.put("/:id", async (req, res) => {
  const updated = await Task.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(updated);
});

router.delete("/:id", async (req, res) => {
  await Task.findByIdAndDelete(req.params.id);
  res.json({ message: "Deleted" });
});

module.exports = router;
EOF

# Create .env placeholder
cat <<EOF > .env
MONGO_URI=your-mongodb-uri-here
EOF

cd ..

# ------------------ Frontend Setup ------------------

echo "🌐 Setting up React frontend..."

npm create vite@latest frontend --template react
cd frontend
npm install
npm install axios

# Add proxy to package.json for API
npx json -I -f package.json -e 'this.proxy="http://localhost:5000"'

# Replace App.jsx
cat <<EOF > src/App.jsx
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const res = await axios.get("/api/tasks");
    setTasks(res.data);
  };

  const createTask = async () => {
    await axios.post("/api/tasks", { title });
    setTitle("");
    fetchTasks();
  };

  const toggleTask = async (id, currentStatus) => {
    await axios.put(\`/api/tasks/\${id}\`, { completed: !currentStatus });
    fetchTasks();
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Task Tracker</h1>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <button onClick={createTask}>Add</button>
      <ul>
        {tasks.map(task => (
          <li key={task._id}>
            <span style={{ textDecoration: task.completed ? "line-through" : "none" }}>
              {task.title}
            </span>
            <button onClick={() => toggleTask(task._id, task.completed)}>Toggle</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
EOF

cd ../..

echo "✅ Project structure created. Now:"
echo "1️⃣ Add your MongoDB URI to backend/.env"
echo "2️⃣ Run backend with: cd task-tracker/backend && npx nodemon index.js"
echo "3️⃣ Run frontend with: cd task-tracker/frontend && npm run dev"

