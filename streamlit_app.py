import streamlit as st
import requests

st.title("🏥 AI Healthcare Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask something about your health...")

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Call FastAPI backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "patient_id": "P001",
                "user_input": user_input
            }
        )

        bot_reply = response.json().get("response", "No response")

    except Exception as e:
        bot_reply = str(e)

    # Save bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    # Refresh UI
    st.rerun()