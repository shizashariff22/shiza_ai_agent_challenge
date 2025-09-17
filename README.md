📂 Rooman Support AI Agent

AI Agent Development Challenge Submission – by Shiza S.

🎥 Demo Video

Watch the full walkthrough demo here:
👉 Google Drive Link to Demo Video: https://drive.google.com/file/d/1NTgFD6_LeSPQYpVr93p68uXpjKtEbupp/view?usp=sharing

🚀 Overview

The Rooman Support AI Agent is an intelligent support system designed for students and administrators.
It provides instant answers using FAQs, AI-powered responses for complex queries, and escalation to admins when confidence is low.

This ensures:

Faster student support

Reduced admin workload

Seamless escalation workflow

🧩 Key Features

✅ Student Chatbot

Matches student questions against a curated FAQ dataset

Uses Google Gemini AI for complex/unseen queries

Escalates unresolved/low-confidence queries automatically

✅ Admin Dashboard

Secure login for admins

View pending escalations

Resolve queries and mark them complete

✅ Complete Workflow

Student asks a question in the chatbot

If match → return FAQ answer

If no match → query sent to Gemini AI

If AI confidence low → escalation raised for admin review

🏗️ System Architecture
         +------------------+
         |   Streamlit UI   |
         | (Student Chatbot)|
         +--------+---------+
                  |
                  v
        +---------------------+
        |     Flask Backend   |
        +---------------------+
        | 1. FAQ Retrieval    |
        | 2. Gemini AI Query  |
        | 3. Escalation Mgmt  |
        +---------------------+
                  |
                  v
         +-------------------+
         |  Admin Dashboard  |
         | (Streamlit)       |
         +-------------------+

⚙️ Tech Stack

Frontend: Streamlit

Backend: Flask (Python)

Database: JSON/Dict-based (for FAQs & escalations)

AI Model: Google Gemini API

Deployment Ready: Can be hosted on Render, Railway, or any server

📂 Project Structure
rooman-support-ai-agent/
│
├── app.py                 # Streamlit frontend (chatbot + dashboard)
├── backend/
│   └── app.py             # Flask backend (FAQ + AI + escalation API)
├── rooman_faq.json        # FAQ dataset
├── requirements.txt       # Python dependencies
├── README.md              # Documentation (this file)
└── demo/ (optional)
    └── demo.mp4           # Demo video (if kept inside repo)

🖥️ Installation & Running Locally

Clone repo

git clone https://github.com/<your-username>/rooman-support-ai-agent.git
cd rooman-support-ai-agent


Create virtual environment (recommended)

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows


Install dependencies

pip install -r requirements.txt


Start backend (Flask)

cd backend
python app.py


Start frontend (Streamlit)

cd ..
streamlit run app.py


Open in browser:
👉 http://localhost:8501

🔑 Admin Login (for dashboard)

Username: admin

Password: admin123

✅ Submission Checklist

 Working AI Agent with FAQ + Gemini AI + Escalation

 Admin Dashboard for resolving escalations

 Demo Video (Google Drive link included)

 Architecture explained in README

 Deployment ready with clear setup instructions

📧 Contact

Made with ❤️ by Shiza S.
Submission for Rooman AI Agent Development Challenge.
