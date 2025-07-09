import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import json
import os

# Initialize Firebase
def init_firebase():
    if not firebase_admin._apps:
        config_str = os.environ.get("FIREBASE_CONFIG")
        if not config_str:
            raise ValueError("FIREBASE_CONFIG secret not found. Make sure it's set in Streamlit Cloud.")
        config = json.loads(config_str)
        cred = credentials.Certificate(config)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://console.firebase.google.com/u/0/project/chat-app-98ede/database/chat-app-98ede-default-rtdb/data/~2F'  # ⬅️ Replace with your actual Firebase DB URL
        })

# Send message to database
def send_message(user, message):
    ref = db.reference("/messages")
    ref.push({
        "user": user,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })

# Get messages
def get_messages():
    ref = db.reference("/messages")
    data = ref.order_by_child("timestamp").limit_to_last(100).get()
    if not data:
        return []
    return sorted(data.values(), key=lambda x: x['timestamp'])
