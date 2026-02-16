import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("\n═══ Testing Multi-Tenant Auth Flow ═══")

    # 1. Register Therapist
    print("\n[1] Registering Therapist...")
    therapist_data = {
        "username": "dr_strange",
        "password": "magicpassword",
        "role": "therapist"
    }
    try:
        res = requests.post(f"{BASE_URL}/register", json=therapist_data)
        if res.status_code == 200:
            therapist_id = res.json()["user_id"]
            print(f"✅ Therapist registered. ID: {therapist_id}")
        else:
            print(f"⚠️ Therapist registration failed: {res.text}. (Might already exist)")
            # Try login to get ID
            res = requests.post(f"{BASE_URL}/login", json={"username": "dr_strange", "password": "magicpassword"})
            therapist_id = res.json()["user_id"]
            print(f"✅ Logged in as existing therapist. ID: {therapist_id}")
    except Exception as e:
        print(f"❌ Connection failed. Ensure server is running. {e}")
        return

    # 2. Register Client (linked to Therapist)
    print("\n[2] Registering Client...")
    client_data = {
        "username": "peter_parker",
        "password": "webpassword",
        "role": "client",
        "therapist_id": therapist_id
    }
    try:
        res = requests.post(f"{BASE_URL}/register", json=client_data)
        if res.status_code == 200:
            client_id = res.json()["user_id"]
            print(f"✅ Client registered. ID: {client_id}")
        else:
            print(f"⚠️ Client registration failed: {res.text}")
            res = requests.post(f"{BASE_URL}/login", json={"username": "peter_parker", "password": "webpassword"})
            client_id = res.json()["user_id"]
            print(f"✅ Logged in as existing client. ID: {client_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # 3. Login as Client
    print("\n[3] Logging in as Client...")
    login_data = {"username": "peter_parker", "password": "webpassword"}
    res = requests.post(f"{BASE_URL}/login", json=login_data)
    if res.status_code == 200:
        data = res.json()
        print(f"✅ Login successful. UserID: {data['user_id']}, Role: {data['role']}")
        assert data['user_id'] == client_id
        assert data['role'] == "client"
    else:
        print(f"❌ Login failed: {res.text}")
        return

    # 4. Log an Emotion Entry
    print("\n[4] Logging Emotion Entry...")
    log_entry = {
        "user_id": client_id,
        "emotion": "Joy",
        "radius": 0.8,
        "angle": 45.0,
        "color_category": "Joy",
        "activities": ["Swinging"],
        "people": ["MJ"],
        "places": ["Queens"]
    }
    res = requests.post(f"{BASE_URL}/log", json=log_entry)
    if res.status_code == 200:
        print("✅ Entry logged successfully.")
    else:
        print(f"❌ Logging failed: {res.text}")
        return

    # 5. Retrieve Logs for Client
    print("\n[5] Retrieving Logs (Client View)...")
    res = requests.get(f"{BASE_URL}/logs/{client_id}")
    logs = res.json()
    print(f"✅ Retrieved {len(logs)} logs.")
    if len(logs) > 0:
        print(f"   Latest log: {logs[0]['emotion']} with {logs[0]['people']}")

    # 6. Verify Therapist can see Client
    print("\n[6] Verifying Therapist Client List...")
    res = requests.get(f"{BASE_URL}/therapist/{therapist_id}/clients")
    clients = res.json()
    found = any(c['username'] == 'peter_parker' for c in clients)
    if found:
        print("✅ Therapist can see Peter Parker in client list.")
    else:
        print("❌ Peter Parker not found in therapist's client list.")

if __name__ == "__main__":
    test_auth_flow()
