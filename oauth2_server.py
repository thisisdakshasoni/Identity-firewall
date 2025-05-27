from flask import Flask, request, jsonify
import uuid
import json
import subprocess
from datetime import datetime, timedelta

app = Flask(__name__)

# Hardcoded user database (username: password)
users = {
    "admin": {"password": "adminpass", "trust": "HIGH"},
    "user": {"password": "userpass", "trust": "MEDIUM"},
    "guest": {"password": "guestpass", "trust": "LOW"}
}

# Login route (mock OAuth2 flow)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_ip = request.remote_addr

    if username in users and users[username]['password'] == password:
        session_token = str(uuid.uuid4())
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
        session_entry = {
            user_ip: {
                "username": username,
                "trust": users[username]['trust'],
                "token": session_token,
                "expires_at": expires_at
            }
        }

        # Update sessions.json
        try:
            with open("sessions.json", "r") as f:
                sessions = json.load(f)
        except FileNotFoundError:
            sessions = {}

        sessions.update(session_entry)

        with open("sessions.json", "w") as f:
            json.dump(sessions, f, indent=2)

        # Auto-trigger the firewall manager with sudo
        try:
            subprocess.run(["sudo", "python3", "firewall_manager.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to run firewall_manager.py: {e}")

        return jsonify({"token": session_token, "trust": users[username]['trust']}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Root endpoint
@app.route('/')
def home():
    return "OAuth2 Mock Server Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
