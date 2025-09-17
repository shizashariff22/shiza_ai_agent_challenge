import streamlit as st
import requests
import os

st.set_page_config(page_title="Rooman Support Portal", page_icon="🔑")

# --- Check if already logged in ---
if "role" in st.session_state:
    role = st.session_state["role"]
    if role == "admin":
        st.info("Already logged in as Admin. Redirecting...")
        os.system("streamlit run admin_ui.py")
    else:
        st.info("Already logged in as User. Redirecting...")
        os.system("streamlit run ui.py")
    st.stop()  # stop further execution

st.title("🔑 Rooman Support Portal")
st.write("Login to continue...")

# --- Login form ---
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/login",
            json={"username": username, "password": password}
        )
        data = response.json()
        if data["success"]:
            st.success(f"✅ Welcome {username}!")

            # Store role in session_state
            st.session_state["role"] = data["role"]

            # Redirect based on role
            if data["role"] == "admin":
                st.info("Opening Admin Dashboard...")
                os.system("streamlit run admin_ui.py")
            else:
                st.info("Opening User Chatbot...")
                os.system("streamlit run ui.py")
        else:
            st.error("❌ Invalid username or password")
    except Exception as e:
        st.error(f"⚠️ Error connecting to backend: {e}")
