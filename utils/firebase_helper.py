import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import streamlit as st
import json

def init_firebase():
    if not firebase_admin._apps:
        config_str = st.secrets["FIREBASE_CONFIG"]
        config = json.loads(config_str)
        cred = credentials.Certificate(config)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://chat-app-98ede-default-rtdb.firebaseio.com/'  # ✅ replace if different
        })

def send_message(user, message):
    ref = db.reference("/messages")
    ref.push({
        "user": user,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })

def get_messages():
    ref = db.reference("/messages")
    data = ref.order_by_child("timestamp").limit_to_last(100).get()
    return sorted(data.values(), key=lambda x: x['timestamp']) if data else []
