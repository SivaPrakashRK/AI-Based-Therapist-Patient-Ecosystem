import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def get_timestamp():
    return int(time.time())

def log(msg, status="INFO"):
    symbol = "✅" if status == "SUCCESS" else "❌" if status == "ERROR" else "ℹ️"
    print(f"{symbol} [{status}] {msg}")

def run_verification():
    print("\n═══ 🚀 POLAR COMPASS DEPLOYMENT VERIFICATION ═══\n")
    
    # 1. Health Check
    log("Checking Server Status...", "INFO")
    try:
        # We don't have a root endpoint, so we use /emotions which is public
        res = requests.get(f"{BASE_URL}/emotions")
        if res.status_code == 200:
            log("Server is UP and running!", "SUCCESS")
        else:
            log(f"Server reachable but returned {res.status_code}", "ERROR")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        log("Connection Failed. Is the server running? (python -m uvicorn main:app --reload)", "ERROR")
        sys.exit(1)

    # 2. Register User
    username = f"test_user_{get_timestamp()}"
    password = "secure_password_123"
    log(f"Attempting Registration for '{username}'...", "INFO")
    
    try:
        res = requests.post(f"{BASE_URL}/register", json={
            "username": username,
            "password": password,
            "role": "client"
        })
        
        if res.status_code == 200:
            user_data = res.json()
            user_id = user_data["user_id"]
            log(f"Registration Successful! User ID: {user_id}", "SUCCESS")
        else:
            log(f"Registration Failed: {res.text}", "ERROR")
            sys.exit(1)
            
    except Exception as e:
        log(f"Registration Exception: {e}", "ERROR")
        sys.exit(1)

    # 3. Login
    log("Attempting Login...", "INFO")
    try:
        res = requests.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": password
        })
        
        if res.status_code == 200:
            login_data = res.json()
            log(f"Login Successful! Role: {login_data['role']}", "SUCCESS")
        else:
            log(f"Login Failed: {res.text}", "ERROR")
            sys.exit(1)
            
    except Exception as e:
        log(f"Login Exception: {e}", "ERROR")
        sys.exit(1)

    # 4. Log Entry
    log("Logging Test Emotion...", "INFO")
    try:
        res = requests.post(f"{BASE_URL}/log", json={
            "user_id": user_id,
            "emotion": "Joy",
            "radius": 0.9,
            "angle": 15.0,
            "color_category": "Joy",
            "activities": ["Testing"],
            "people": ["Bot"],
            "places": ["localhost"]
        })
        
        if res.status_code == 200:
            log("Emotion Logged Successfully", "SUCCESS")
        else:
            log(f"Logging Failed: {res.text}", "ERROR")
            sys.exit(1)
            
    except Exception as e:
        log(f"Logging Exception: {e}", "ERROR")
        sys.exit(1)

    # 5. Retrieve Logs
    log("Verifying Data Persistence...", "INFO")
    try:
        res = requests.get(f"{BASE_URL}/logs/{user_id}")
        logs = res.json()
        
        if len(logs) > 0 and logs[0]['emotion'] == "Joy":
            log(f"Data Retrieved Successfully. Found {len(logs)} logs.", "SUCCESS")
        else:
            log("Data Retrieval Failed or mismatch.", "ERROR")
            sys.exit(1)
            
    except Exception as e:
        log(f"Retrieval Exception: {e}", "ERROR")
        sys.exit(1)

    print("\n══════════════════════════════════════════════════")
    print("   🎉 SYSTEM VERIFIED. ALL SYSTEMS GO.  🎉")
    print("══════════════════════════════════════════════════")

if __name__ == "__main__":
    run_verification()
