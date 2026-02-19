URL Shortener – Full Stack

A full-stack URL shortener built using FastAPI and React.

🚀 Tech Stack

Backend: FastAPI (Python)

Database: SQLite

Frontend: React (Vite)

API Architecture: REST

Version Control: Git & GitHub

✨ Features

Generate short URLs

Automatic expiry (7 days)

Redirect to original URL

Last accessed tracking

Clean React UI

Modular backend structure

🛠 Project Structure
url_shortener/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│
├── frontend/
│
└── README.md

▶️ How To Run Locally
Backend
cd backend
uvicorn main:app --reload


Runs on:

http://127.0.0.1:8000

Frontend
cd frontend
npm install
npm run dev


Runs on:

http://localhost:5173
📌 Future Improvements

Click analytics

Custom short codes

Deployment (Render + Vercel)

Authentication system