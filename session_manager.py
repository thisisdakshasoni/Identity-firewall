import json
import datetime
from policy_engine import get_trust_level

SESSION_FILE = "sessions.json"

def add_session(ip, username, token):
    trust = get_trust_level(username)
    expires = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat()

    try:
        with open(SESSION_FILE, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        sessions = {}

    sessions[ip] = {
        "username": username,
        "trust": trust,
        "token": token,
        "expires_at": expires
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

    print(f"[INFO] Session added for {ip} as {username} with trust level {trust}")

def remove_session(ip):
    try:
        with open(SESSION_FILE, "r") as f:
            sessions = json.load(f)
        if ip in sessions:
            del sessions[ip]
            with open(SESSION_FILE, "w") as f:
                json.dump(sessions, f, indent=2)
            print(f"[INFO] Session removed for {ip}")
    except FileNotFoundError:
        pass
