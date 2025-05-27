import json
import subprocess

SESSIONS_FILE = "sessions.json"

print("[DEBUG] firewall_manager.py triggered.")

def remove_existing_rules(ip):
    # Remove any existing rules for this IP
    subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "ACCEPT"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-p", "tcp", "--dport", "80", "-j", "ACCEPT"], stderr=subprocess.DEVNULL)

def apply_rule(ip, trust):
    if trust == "HIGH":
        print(f"[+] Applying HIGH trust rule: ACCEPT all from {ip}")
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "ACCEPT"])
    elif trust == "MEDIUM":
        print(f"[+] Applying MEDIUM trust rule: ACCEPT port 80 from {ip}")
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "80", "-j", "ACCEPT"])
    elif trust == "LOW":
        print(f"[+] Applying LOW trust rule: DROP all from {ip}")
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

def main():
    try:
        with open(SESSIONS_FILE, "r") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        print("[!] sessions.json not found.")
        return

    for ip, details in sessions.items():
        trust = details.get("trust")
        if not trust:
            continue
        remove_existing_rules(ip)
        apply_rule(ip, trust)

if __name__ == "__main__":
    main()
