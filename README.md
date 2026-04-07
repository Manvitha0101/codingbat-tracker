# 🏆 Coding Tracker 

---

## 📌 Project Overview
Coding Tracker  is a  real-time monitoring system designed to track student progress on CodingBat.  

## ✨ Outstanding Features
* **🔥 Velocity Engine**: Automated detection for students active in the last 24h.
* **🎉 Milestone Celebrations**: Interactive confetti triggers for 50+ solved problems.
* **📈 Progress Graphs**: Time-series Area Charts showing individual growth trajectory.
* **⚡ Background Scraper**: Robust FastAPI-based scheduler syncing every 10 minutes.

---

## 🛠️ Tech Stack
* **Frontend**: React.js, Tailwind CSS, Recharts, Lucide Icons
* **Backend**: FastAPI (Python), APScheduler
* **Database**: PostgreSQL, SQLAlchemy ORM
* **Scraping**: BeautifulSoup4, Requests

---

## 💻 How to Run Locally

### 1. Backend Setup

cd backend
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

### 2.Frontend Setup
cd frontend
npm install
npm start
