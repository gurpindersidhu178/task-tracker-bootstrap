# 🎯 Frontend Development Assignment

## 📝 Objective

Design and build a frontend module for a sports league platform that allows users to:

- Register and log in using GitHub or email
- View upcoming matches and team standings
- Join a team and track performance

## 💼 Project Scope

Build a responsive and interactive frontend using the following stack:

### 📦 Tech Stack

- **Framework**: Next.js (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI + Lucide Icons
- **State Management**: Zustand
- **Form Handling**: React Hook Form + Zod
- **Charts**: Recharts or Chart.js
- **Auth**: NextAuth.js

## ✅ Tasks

### 📌 1. Auth Module

- GitHub & email-based login using NextAuth.js
- Dashboard redirection after login/logout

### 📌 2. Match Schedule Module

- List of upcoming matches (mocked JSON data)
- Card UI with team logos and match date

### 📌 3. Standings Module

- League table of team rankings (mocked JSON)
- Chart: wins/losses per team using Chart.js or Recharts

### 📌 4. Join Team Module

- Form to request joining a team (name, phone, role)
- Form validation using Zod and React Hook Form

### 📌 5. Profile Module

- Display user profile with joined team
- Edit profile functionality

## 🧠 Architecture Guidelines

```
frontend/
├── app/
│   ├── auth/         # Auth pages
│   ├── schedule/     # Match schedule
│   ├── standings/    # Team rankings
│   ├── join-team/    # Join team form
│   └── profile/      # Profile handling
├── components/       # Reusable UI components
├── hooks/            # Zustand stores, useAuth, etc.
├── lib/              # API functions
├── styles/           # Tailwind config & globals
└── utils/            # Helper functions
```

## 📬 Submission Instructions

- Fork this repo: [https://github.com/gurpindersidhu178/task-tracker-bootstrap](https://github.com/gurpindersidhu178/task-tracker-bootstrap)
- Work in your assigned module directory under `frontend/app/{module-name}`
- Use the `frontend-development` branch
- Push changes to your fork
- Email your repo link to [hrlogbiz@logbizgroup.com](mailto\:hrlogbiz@logbizgroup.com)

## 🕒 Deadline

Submit within **5 days** of receiving this assignment.

## 🙌 Good Luck!

We’re excited to see how you build this!

