from datetime import datetime

def contain(username):
    return {
        "action": "Session Blocked",
        "status": "Success",
        "username": username,
        "timestamp": datetime.now().isoformat()
    }