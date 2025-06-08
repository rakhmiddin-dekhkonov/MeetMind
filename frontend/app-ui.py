import streamlit as st
import requests

st.set_page_config(page_title="Meeting Memory Chat", layout="centered")

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hi! I’m your meeting memory bot. Ask me anything about past meetings! 💬"}
    ]

st.title("🧠 Meeting Memory Chat")

# --- Display chat history ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["text"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["text"])

# --- Chat input ---
user_input = st.chat_input("Ask about the meeting...")

if user_input:
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post("http://127.0.0.1:8000/query", json={"question": user_input})
                data = res.json()
                answer = data["answer"]
                excerpts = data.get("matched_contexts", [])
                reply = answer + "\n\n" + "\n".join([f"> 💡 {c}" for c in excerpts])
            except Exception as e:
                reply = "❌ Oops! Could not reach the backend server."

        st.markdown(reply)
        st.session_state.messages.append({"role": "bot", "text": reply})
