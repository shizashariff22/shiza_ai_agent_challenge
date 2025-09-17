import streamlit as st
import requests
import json
import hashlib

st.set_page_config(page_title="Rooman Support", page_icon="💬", layout="centered")
API_URL = "http://127.0.0.1:5000"

# -------------------------------
# Session State Initialization
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -------------------------------
# LOGIN PAGE
# -------------------------------
if not st.session_state["logged_in"]:
    st.title("🔑 Rooman Support Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.session_state["role"] = "admin"
        elif username == "user" and password == "user123":
            st.session_state["logged_in"] = True
            st.session_state["role"] = "user"
        else:
            st.error("❌ Invalid credentials")
    st.stop()  # Wait until user logs in

# -------------------------------
# LOGOUT BUTTON (for both roles)
# -------------------------------
if st.session_state["logged_in"]:
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.session_state["messages"] = []
        st.success("✅ Logged out. Reloading...")
        st.components.v1.html("<script>window.location.reload()</script>")

# -------------------------------
# ADMIN DASHBOARD
# -------------------------------
if st.session_state["role"] == "admin":
    st.title("📂 Admin Escalation Dashboard")

    if st.button("🔍 Refresh Escalations"):
        st.rerun()  # reload page with fresh data

    try:
        resp = requests.get(f"{API_URL}/escalations")
        escalations = resp.json()

        if not escalations:
            st.info("✅ No escalations yet.")
        else:
            for esc in escalations:
                with st.container():
                    st.markdown(f"**📝 Query:** {esc['query']}")
                    st.write(f"🤖 **AI Answer:** {esc['ai_answer']}")
                    st.write(f"📌 **Status:** {esc['status'].capitalize()}")

                    if esc["status"].lower() == "open":
                        if st.button(f"✅ Resolve", key=f"resolve-{esc['query']}"):
                            requests.post(f"{API_URL}/resolve", json={"query": esc["query"]})
                            st.success(f"Escalation for '{esc['query']}' resolved!")
                            st.experimental_rerun()

                st.markdown("---")

    except Exception as e:
        st.error(f"⚠️ Error loading escalations: {e}")

# -------------------------------
# USER CHATBOT PAGE
# -------------------------------
elif st.session_state["role"] == "user":
    st.title("💬 Rooman Support Chatbot")
    st.write("Ask me anything about Rooman courses, admissions, placements, or support.")

    # Reset chat
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state["messages"] = []
        try:
            requests.post(f"{API_URL}/reset")
        except:
            pass
        st.success("Chat history cleared!")

    # Display chat history
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Chat input
    if query := st.chat_input("Type your question..."):
        st.chat_message("user").write(query)
        st.session_state["messages"].append({"role": "user", "content": query})

        try:
            response = requests.post(f"{API_URL}/chat", json={"query": query})
            data = response.json()
            answer = data.get("best_answer", "Sorry, I couldn't answer that.")
            escalate_message = data.get("escalate_message", None)
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}"
            escalate_message = None

        st.chat_message("assistant").write(answer)
        st.session_state["messages"].append({"role": "assistant", "content": answer})

        # --- Show escalation warning if present ---
        if escalate_message:
            st.warning(escalate_message)