# import streamlit as st
# import requests

# st.set_page_config(page_title="Hackathon LLM Demo", layout="centered")

# st.title("🚀 Hackathon Mini-LLM Demo")

# query = st.text_area("Ask me anything:", "")

# if st.button("Generate"):
#     if query.strip():
#         with st.spinner("Thinking..."):
#             response = requests.post(
#                 "http://localhost:5000/chat",
#                 json={"query": query}
#             )
#             if response.status_code == 200:
#                 data = response.json()

#                 st.subheader("✅ Best Answer")
#                 st.success(data["best_answer"])

#                 st.subheader("💡 Other Responses")
#                 for cand in data["candidates"]:
#                     if cand != data["best_answer"]:
#                         st.write(f"- {cand}")
#             else:
#                 st.error("Backend error. Make sure Flask server is running.")






import streamlit as st
import requests

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")

# --- Session State to store conversation ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

API_URL = "http://127.0.0.1:5000/chat"  # Your Flask backend

# --- Chat UI Header ---
st.title("💎 Gemini-Style Chatbot")
st.markdown("Ask me anything! I'll generate the **best answer** based on multiple candidates + reward scoring.")

# --- Display past messages ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# --- User input box ---
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Send conversation to backend ---
    # Combine context (last assistant reply if exists) for continuity
    context = ""
    if st.session_state["messages"]:
        # Use only last assistant reply for context
        last_assistant = next((m["content"] for m in reversed(st.session_state["messages"]) if m["role"] == "assistant"), "")
        if last_assistant:
            context = f"Previous answer: {last_assistant}\n"

    data = {"query": context + prompt}
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()

        bot_reply = result["best_answer"]

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Add bot response
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)








