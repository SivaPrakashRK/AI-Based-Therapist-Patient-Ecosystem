import os
import time

DB_FILE = "compass_prod.db"

def reset_db():
    print(f"🛑 ATTEMPTING TO DELETE DATABASE: {DB_FILE}")
    print("Ensure the server (uvicorn) is STOPPED before proceeding.")
    print("Press Ctrl+C to cancel, or wait 3 seconds...")
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return

    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print("✅ Database file deleted successfully.")
            print("🚀 Restart the server to recreate a fresh database.")
        except PermissionError:
            print("❌ ERROR: Permission Denied. The file is likely in use.")
            print("👉 Stop the python/uvicorn server command and try again.")
    else:
        print("⚠️ Database file not found. It may have already been deleted.")

if __name__ == "__main__":
    reset_db()
