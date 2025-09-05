from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
from reward import reward_function
from dotenv import load_dotenv
# --- Gemini API import and configuration ---
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# -------------------------------------------

app = Flask(__name__)
CORS(app)

DATA_FILE = "data/improved_data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data["query"]

    # Stronger prompt to reduce nonsense
    prompt = f"Human: {query}\nAI: Please answer in 2-3 clear sentences without repeating yourself.\nAI:"

    # --- Use Gemini to generate candidates ---
    model = genai.GenerativeModel("gemini-2.5-flash")
    candidates = []
    for _ in range(3):
        response = model.generate_content(prompt)
        candidates.append(response.text.strip())
    # -----------------------------------------

    # Score candidates
    scored = [(ans, reward_function(ans)) for ans in candidates]
    best_answer, best_score = max(scored, key=lambda x: x[1])

    # Fallback if all candidates are bad
    if best_score < 0:
        best_answer = "I'm not sure, but that's an interesting question!"
        best_score = 0

    # Save interaction to dataset
    with open(DATA_FILE, "r+") as f:
        history = json.load(f)
        history.append({
            "prompt": query,
            "candidates": candidates,
            "best": best_answer,
            "score": best_score
        })
        f.seek(0)
        json.dump(history, f, indent=2)

    return jsonify({
        "query": query,
        "candidates": candidates,
        "best_answer": best_answer,
        "score": best_score
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)















# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import json, os
# from reward import reward_function
# import google.generativeai as genai

# # --- Gemini API configuration ---
# genai.configure(api_key="AIzaSyATa_Hy6cTjOscUBkud9wgH5-5fsVf7ypI")  # Replace with your Gemini API key

# app = Flask(__name__)
# CORS(app)

# DATA_FILE = "data/improved_data.json"
# if not os.path.exists(DATA_FILE):
#     os.makedirs("data", exist_ok=True)
#     with open(DATA_FILE, "w") as f:
#         json.dump([], f)

# # In-memory chat history (per session)
# chat_history = []


# @app.route("/chat", methods=["POST"])
# def chat():
#     global chat_history
#     data = request.json
#     query = data["query"]

#     # Add user message to history
#     chat_history.append({"role": "user", "content": query})

#     # Build conversation context
#     conversation = "The following is a friendly conversation between a human and an AI.\n"
#     conversation += "The AI should always reply in 2–3 clear sentences, directly answering the user without repeating the question.\n\n"

#     for msg in chat_history[-10:]:  # keep only last 10 exchanges to avoid long prompts
#         role = "Human" if msg["role"] == "user" else "AI"
#         conversation += f"{role}: {msg['content']}\n"

#     conversation += "AI:"

#     # --- Use Gemini to generate candidates ---
#     model = genai.GenerativeModel("gemini-2.5-flash")
#     candidates = []
#     for _ in range(3):
#         response = model.generate_content(conversation)
#         candidates.append(response.text.strip())
#     # -----------------------------------------

#     # Score candidates
#     scored = [(ans, reward_function(ans)) for ans in candidates]
#     best_answer, best_score = max(scored, key=lambda x: x[1])

#     # Fallback if all candidates are bad
#     if best_score < 0:
#         best_answer = "I'm not sure, but that's an interesting question!"
#         best_score = 0

#     # Save bot reply to history
#     chat_history.append({"role": "assistant", "content": best_answer})

#     # Save interaction to dataset
#     with open(DATA_FILE, "r+") as f:
#         history = json.load(f)
#         history.append({
#             "prompt": query,
#             "candidates": candidates,
#             "best": best_answer,
#             "score": best_score
#         })
#         f.seek(0)
#         json.dump(history, f, indent=2)

#     return jsonify({
#         "query": query,
#         "candidates": candidates,
#         "best_answer": best_answer,
#         "score": best_score,
#         "history": chat_history
#     })


# @app.route("/reset", methods=["POST"])
# def reset():
#     """Clear chat history for a new session"""
#     global chat_history
#     chat_history = []
#     return jsonify({"message": "Chat history cleared"})


# if __name__ == "__main__":
#     app.run(port=5000, debug=True)
