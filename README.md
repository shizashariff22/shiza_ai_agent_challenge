📂 Rooman Support AI Agent

AI Agent Development Challenge Submission – by Shiza S.

🎥 Demo Video: https://shizaaiagentchallenge-5jzkr3apprack8kpvhnzuxt.streamlit.app/

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

User Interaction

Students interact with a Streamlit-based chatbot UI.

Backend Processing

Queries are sent to a Flask backend API.

The backend first checks for an FAQ match using fuzzy matching.

If no match is found, the query is passed to the Google Gemini API.

Escalation Handling

If the AI response is low-confidence or out of scope, the query is escalated.

Escalations are stored in a JSON file for tracking.

Admin Workflow

Admins access a Streamlit dashboard.

They can view, manage, and resolve escalated queries.




⚙️ Tech Stack

Frontend: Streamlit

Backend: Flask (Python)

Database: JSON/Dict-based (for FAQs & escalations)

AI Model: Google Gemini API

Deployment Ready: Can be hosted on Render, Railway, or any server

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
