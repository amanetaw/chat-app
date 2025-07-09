import streamlit as st
from utils.firebase_helper import init_firebase, send_message, get_messages

# Initialize Firebase (once)
if 'firebase_initialized' not in st.session_state:
    init_firebase()
    st.session_state['firebase_initialized'] = True

# App UI
st.set_page_config(page_title="💬 Chat App", layout="centered")
st.title("💬 Real-Time Chat App")

# Ask for username
username = st.text_input("Enter your name to join the chat:", key="username")

if username:
    st.success(f"You're chatting as **{username}**")

    # Display messages
    st.markdown("### Chat Messages")
    messages = get_messages()

    for msg in messages:
        st.markdown(f"**{msg['user']}**: {msg['message']}")

    st.markdown("---")

    # Message input box
    msg = st.text_input("Type your message:", key="msg_input")

    if st.button("Send"):
        if msg.strip():
            send_message(username, msg.strip())
            st.rerun()
import json

# Load original JSON file
with open("firebase_config.json", "r") as f:
    config = json.load(f)

# Escape newlines in private_key
config["private_key"] = config["private_key"].replace("\n", "\\n")

# Wrap the full config in triple quotes
streamlit_secret = f'FIREBASE_CONFIG = """\n{json.dumps(config, indent=2)}\n"""'

# Save or print result
with open("streamlit_secret.txt", "w") as f:
    f.write(streamlit_secret)

print("✅ Streamlit secret prepared: saved to streamlit_secret.txt")
