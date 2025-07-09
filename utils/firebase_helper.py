import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_config.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://chat-app-98ede-default-rtdb.firebaseio.com/'  # 👈 Replace this
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
