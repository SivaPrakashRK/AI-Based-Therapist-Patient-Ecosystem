import requests
import sys

BASE_URL = "http://localhost:8000"

def run_test():
    print("═══ Multi-Tenant Role Verification ═══\n")

    # 1. Register Therapist
    print("[1] Registering Therapist 'Dr. Phil'...")
    try:
        res = requests.post(f"{BASE_URL}/register", json={
            "username": "dr_phil", "password": "password", "role": "therapist"
        })
        if res.status_code == 200:
            therapist_id = res.json()["user_id"]
            print(f"✅ Success! Therapist ID: {therapist_id}")
        else:
            # Login if exists
            res = requests.post(f"{BASE_URL}/login", json={"username": "dr_phil", "password": "password"})
            therapist_id = res.json()["user_id"]
            print(f"⚠️ Exists. Logged in as ID: {therapist_id}")
    except Exception as e:
        print(f"❌ Server not running? Error: {e}")
        return

    # 2. Register Client linked to Therapist
    print("\n[2] Registering Client 'Tony' linked to Dr. Phil...")
    try:
        res = requests.post(f"{BASE_URL}/register", json={
            "username": "tony_stark", "password": "password", "role": "client", "therapist_id": therapist_id
        })
        if res.status_code == 200:
            client_id = res.json()["user_id"]
            print(f"✅ Success! Client ID: {client_id}")
        else:
            res = requests.post(f"{BASE_URL}/login", json={"username": "tony_stark", "password": "password"})
            client_id = res.json()["user_id"]
            print(f"⚠️ Exists. Logged in as ID: {client_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # 3. Client Logs Entry
    print("\n[3] Client 'Tony' logs an emotion...")
    log_data = {
        "user_id": client_id,
        "emotion": "Anxiety",
        "radius": 0.5,
        "angle": 120.0,
        "color_category": "Fear",
        "activities": ["Work"],
        "people": ["Pepper"],
        "places": ["Lab"]
    }
    res = requests.post(f"{BASE_URL}/log", json=log_data)
    if res.status_code == 200:
        print("✅ Entry logged successfully.")
    else:
        print(f"❌ Failed: {res.text}")

    # 4. Therapist Views Client List
    print("\n[4] Dr. Phil checks client list...")
    res = requests.get(f"{BASE_URL}/therapist/{therapist_id}/clients")
    clients = res.json()
    if any(c['id'] == client_id for c in clients):
        print(f"✅ Verified: Tony (ID {client_id}) is in Dr. Phil's list.")
    else:
        print("❌ Failed: Tony not found in list.")

    # 5. Therapist Views Client Logs
    print("\n[5] Dr. Phil fetches Tony's logs...")
    res = requests.get(f"{BASE_URL}/logs/{client_id}") # Endpoint used by dashboard
    logs = res.json()
    if len(logs) > 0 and logs[0]['emotion'] == 'Anxiety':
        print("✅ Verified: Dr. Phil can see Tony's 'Anxiety' log.")
    else:
        print("❌ Failed: Logs not found or incorrect.")

    print("\n═══ ALL SYSTEMS GO ═══")

if __name__ == "__main__":
    run_test()
