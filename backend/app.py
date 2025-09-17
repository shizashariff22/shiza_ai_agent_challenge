
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import difflib
from reward import reward_function
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Gemini API import and configuration ---
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------
app = Flask(__name__)
CORS(app)

# ---------------------------
DATA_DIR = "data"
CHAT_FILE = os.path.join(DATA_DIR, "chat_history.json")
ESCALATION_FILE = os.path.join(DATA_DIR, "escalations.json")
FAQ_FILE = os.path.join(DATA_DIR, "rooman_faq.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize files if they don't exist
for file_path, default in [
    (CHAT_FILE, []),
    (ESCALATION_FILE, []),
    (FAQ_FILE, [])
]:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(default, f, indent=2)

# ---------------------------
# Helper functions
# ---------------------------

def load_faq():
    with open(FAQ_FILE, "r") as f:
        return json.load(f)

def load_chat_history():
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

def save_chat_history(history):
    with open(CHAT_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_escalations():
    with open(ESCALATION_FILE, "r") as f:
        return json.load(f)

def save_escalations(escalations):
    with open(ESCALATION_FILE, "w") as f:
        json.dump(escalations, f, indent=2)

# ✅ Improved FAQ matching using fuzzy search
def check_faq_match(query, threshold=0.6):
    """Return the best matching FAQ answer using fuzzy matching"""
    faq = load_faq()
    questions = [item["question"] for item in faq]

    # Find the closest match
    best_match = difflib.get_close_matches(query.lower(), [q.lower() for q in questions], n=1, cutoff=threshold)

    if best_match:
        for item in faq:
            if item["question"].lower() == best_match[0]:
                return item["answer"]
    return None

# ---------------------------
# Routes
# ---------------------------

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "").strip()

    # Load previous conversation context
    history = load_chat_history()
    context = "\n".join([f"Human: {m.get('query', '')}\nAI: {m.get('answer', '')}" 
                         for m in history[-3:]])  # last 3 messages

    # 1️⃣ Check FAQ first
    faq_answer = check_faq_match(query)
    if faq_answer:
        best_answer = faq_answer
        escalate = False
        escalate_message = None
    else:
        # 2️⃣ Use Gemini AI
        prompt = f"{context}\nHuman: {query}\nAI: Answer in 2-3 clear sentences."
        model = genai.GenerativeModel("gemini-2.5-flash")
        candidates = []
        for _ in range(3):
            response = model.generate_content(prompt)
            candidates.append(response.text.strip())

        # Score answers
        scored = [(ans, reward_function(ans)) for ans in candidates]
        best_answer, best_score = max(scored, key=lambda x: x[1])

        # Determine if escalation is needed
        escalate_phrases = [
            "i don't know", "i am not sure", "please contact support",
            "cannot tell", "not able to", "unsure", "no information"
        ]
        escalate = best_score <= 1 or any(phrase in best_answer.lower() for phrase in escalate_phrases)

        # If escalation is needed, log it immediately (no button for user)
        if escalate:
            escalate_message = "⚠️ This answer might be inaccurate. Your query has been escalated to human support."
            # Log escalation directly
            escalations = load_escalations()
            escalations.append({"query": query, "ai_answer": best_answer, "status": "open"})
            save_escalations(escalations)
        else:
            escalate_message = None

    # Save to chat history
    history.append({"query": query, "answer": best_answer})
    save_chat_history(history)

    return jsonify({
        "best_answer": best_answer,
        "escalate": escalate,
        "escalate_message": escalate_message
    })

@app.route("/escalate", methods=["POST"])
def escalate():
    data = request.json
    query = data.get("query")
    ai_answer = data.get("ai_answer")

    print(f"Escalation received: {query} | {ai_answer}")  # Debug print

    escalations = load_escalations()
    escalations.append({"query": query, "ai_answer": ai_answer, "status": "open"})
    save_escalations(escalations)
    return jsonify({"message": "Escalation logged"})


@app.route("/resolve", methods=["POST"])
def resolve():
    data = request.json
    query = data.get("query")

    escalations = load_escalations()
    for esc in escalations:
        if esc["query"] == query:
            esc["status"] = "resolved"
    save_escalations(escalations)
    return jsonify({"message": "Escalation resolved"})


@app.route("/escalations", methods=["GET"])
def get_escalations():
    return jsonify(load_escalations())


@app.route("/reset", methods=["POST"])
def reset_chat():
    save_chat_history([])
    return jsonify({"message": "Chat history cleared"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
