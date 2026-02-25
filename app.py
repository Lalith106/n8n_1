import streamlit as st
import requests
import uuid

WEBHOOK_URL = "https://lalith106.app.n8n.cloud/webhook/502fbd9f-1f7a-4c9a-8587-eb4cec6ee300"


st.title("🤖 NAM-BOT")

# Create session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function that runs when Send is clicked
def send_message():
    user_text = st.session_state.input_box.strip()

    if user_text != "":
        # Save user message
        st.session_state.messages.append(("user", user_text))

        # Call backend
        response = requests.post(
            WEBHOOK_URL,
            json={
                "chatInput": user_text,
                "sessionId": st.session_state.session_id
            }
        )

        reply = response.json().get("output", "No response")

        # Save bot message
        st.session_state.messages.append(("assistant", reply))

        # Clear input safely
        st.session_state.input_box = ""

# Display chat history
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"**👤 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")

st.markdown("---")

# Input field
st.text_input("Ask something...", key="input_box")

# Send button with callback
st.button("Send", on_click=send_message)