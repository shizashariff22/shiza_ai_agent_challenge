import streamlit as st
import requests
import hashlib

st.set_page_config(page_title="Rooman Support Chatbot", page_icon="💬")

# --- Logout button ---
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.success("✅ Logged out. Reloading page...")
    st.components.v1.html("<script>window.location.reload()</script>")

st.title("💬 Rooman Support Chatbot")
st.write("Ask me anything about Rooman courses, admissions, placements, or support.")

# --- Initialize chat messages in session state ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Reset Chat ---
if st.button("🔄 Reset Chat", use_container_width=True):
    st.session_state["messages"] = []
    try:
        requests.post("http://127.0.0.1:5000/reset")
    except:
        pass
    st.success("Chat history cleared!")

# --- Display chat history ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# --- Chat input ---
if query := st.chat_input("Type your question..."):
    st.chat_message("user").write(query)
    st.session_state["messages"].append({"role": "user", "content": query})

    try:
        response = requests.post("http://127.0.0.1:5000/chat", json={"query": query})
        data = response.json()
        answer, escalate = data["best_answer"], data["escalate"]

        st.chat_message("assistant").write(answer)
        st.session_state["messages"].append({"role": "assistant", "content": answer})

        if escalate:
            st.error("⚠️ This query might need human support.")

            # --- Generate a safe unique key for the button ---
            query_hash = hashlib.md5(query.encode()).hexdigest()
            escalate_key = f"escalated_{query_hash}"

            # Initialize session_state for this key if not exists
            if escalate_key not in st.session_state:
                st.session_state[escalate_key] = False

            # Show button only if not escalated yet
            if not st.session_state[escalate_key]:
                if st.button("📞 Escalate to Human Support", key=query_hash):
                    # Find last assistant message for this query
                    ai_answer = ""
                    for msg in reversed(st.session_state["messages"]):
                        if msg["role"] == "assistant":
                            ai_answer = msg["content"]
                            break

                    # Post escalation
                    try:
                        resp = requests.post(
                            "http://127.0.0.1:5000/escalate",
                            json={"query": query, "ai_answer": ai_answer}
                        )
                        if resp.status_code == 200:
                            st.session_state[escalate_key] = True
                            st.success("✅ Escalation logged. Rooman team will reach out.")
                        else:
                            st.error("❌ Failed to escalate. Try again.")
                    except Exception as e:
                        st.error(f"❌ Error escalating: {e}")
            else:
                st.info("✅ Escalation already logged. Rooman team will reach out.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# --- Escalation Dashboard ---
st.sidebar.title("📂 Escalation Dashboard")

if st.sidebar.button("🔍 View Escalations"):
    try:
        resp = requests.get("http://127.0.0.1:5000/escalations")
        escalations = resp.json()
        if not escalations:
            st.sidebar.write("No escalations yet.")
        else:
            for esc in escalations:
                st.sidebar.write(f"**Query:** {esc['query']}")
                st.sidebar.write(f"AI Answer: {esc['ai_answer']}")
                st.sidebar.write(f"Status: {esc['status']}")
                if esc["status"] == "open":
                    if st.sidebar.button(f"✅ Resolve: {esc['query']}", key=esc["query"]):
                        requests.post("http://127.0.0.1:5000/resolve", json={"query": esc["query"]})
                        st.sidebar.success(f"Escalation for '{esc['query']}' resolved!")
                st.sidebar.markdown("---")
    except Exception as e:
        st.sidebar.error(f"Error loading escalations: {e}")