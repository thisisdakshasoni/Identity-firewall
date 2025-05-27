# policy_engine.py

def get_trust_level(username):
    """
    Return trust level based on username or role.
    Can be enhanced to check database, token scopes, etc.
    """
    if username == "admin":
        return "HIGH"
    elif username == "user":
        return "MEDIUM"
    else:
        return "LOW"
