# Identity-Based Adaptive Firewall System 🔐

This project implements a dynamic, identity-based adaptive firewall system using `iptables` and a Python backend. It enforces real-time network access rules based on user authentication and assigned trust levels (HIGH, MEDIUM, LOW), simulating a Zero Trust architecture.

---

## 🚀 Features

- 🔐 OAuth2-style login with identity-based sessions
- 🧠 Trust level assignment via `policy_engine.py`
- 🔄 Real-time firewall updates using `iptables`
- 📡 Session-based control with automatic IP binding
- 🧪 Tested across `admin`, `user`, and `guest` roles
- 🔍 Logs and test-friendly session tracking

---

## 📁 File Structure

| File                     | Description                                      |
|--------------------------|--------------------------------------------------|
| `oauth2_server.py`       | Flask server handling login & session creation   |
| `firewall_manager.py`    | Applies and updates iptables rules dynamically   |
| `policy_engine.py`       | Maps identity to trust level                     |
| `session_manager.py`     | (Optional) Manages session lifecycle             |
| `sessions.json`          | Stores active session state                      |
| `iptables_ruleset.txt`   | Exported firewall configuration                  |

---

## 🛠️ How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/identity-firewall.git
   cd identity-firewall
Run the Flask login server:

bash

python3 oauth2_server.py
From another machine:



curl -X POST http://<linux-ip>:5000/login -H "Content-Type: application/json" -d '{"username":"admin", "password":"adminpass"}'
Check firewall rules:



sudo iptables -L -n
🔐 Trust Levels and Access Rules
User Role	Trust Level	Access Behavior
admin	HIGH	Full access (all ports)
user	MEDIUM	Only HTTP (port 80) allowed
guest	LOW	All access blocked

