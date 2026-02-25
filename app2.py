import streamlit as st
import requests
import uuid
import os

# -------- CONFIG --------
DATABRICKS_BASE_URL = "https://adb-4224005571705028.8.azuredatabricks.net/serving-endpoints/databricks-claude-sonnet-4-5/invocations"
MODEL_NAME = "databricks-claude-sonnet-4-5"
DATABRICKS_TOKEN =""
#DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# -------- PAGE --------
st.title("🤖 SSMB")

# Unique session per user
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

def send_message():
    user_input = st.session_state.input_box.strip()

    if user_input:
        # Save user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        # Call Databricks endpoint
        response = requests.post(
            f"{DATABRICKS_BASE_URL}",
            headers={
                "Authorization": f"Bearer {DATABRICKS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": st.session_state.messages,
                "max_tokens": 800
            }
        )

        result = response.json()
        print(result)
        bot_reply = result["choices"][0]["message"]["content"]

        # Save bot response
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

        # Clear input
        st.session_state.input_box = ""

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**👤 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {msg['content']}")

st.text_input("Ask something...", key="input_box")
st.button("Send", on_click=send_message)