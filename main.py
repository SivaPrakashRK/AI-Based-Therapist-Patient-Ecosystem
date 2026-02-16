from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from valence_engine import calculate_polar_coordinates
from emotion_map import EMOTION_MAP
import sqlite3
import json
from datetime import datetime
import bcrypt

app = FastAPI()

# Add CORS middleware to allow frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for local development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Setup

def verify_password(plain_password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Database initialization
DB_PATH = "compass_prod.db"

def init_db():
    """Initialize SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('client', 'therapist')),
            therapist_id INTEGER,
            FOREIGN KEY(therapist_id) REFERENCES users(id)
        )
    """)
    
    # Create Logs Table (Updated with user_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            emotion TEXT NOT NULL,
            radius REAL NOT NULL,
            angle REAL NOT NULL,
            color_category TEXT NOT NULL,
            activities TEXT,
            people TEXT,
            places TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# ══════════════════════════════════════════
#  Pydantic Models
# ══════════════════════════════════════════

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'client' or 'therapist'
    therapist_id: Optional[int] = None

class UserLogin(BaseModel):
    username: str
    password: str

class AnalyzeRequest(BaseModel):
    """Request model for emotion analysis - text is NEVER stored."""
    text: str

class LogRequest(BaseModel):
    """Request model for logging emotion metadata linked to a user."""
    user_id: int
    emotion: str
    radius: float
    angle: float
    color_category: str
    activities: List[str]
    people: List[str]
    places: List[str]

class UpdateTherapistRequest(BaseModel):
    user_id: int
    therapist_id: int

# ══════════════════════════════════════════
#  API Endpoints
# ══════════════════════════════════════════

@app.put("/update_therapist")
def update_therapist(request: UpdateTherapistRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if therapist exists
        cursor.execute("SELECT id FROM users WHERE id = ? AND role = 'therapist'", (request.therapist_id,))
        if not cursor.fetchone():
             raise HTTPException(status_code=404, detail="Therapist ID not found")

        cursor.execute("UPDATE users SET therapist_id = ? WHERE id = ?", (request.therapist_id, request.user_id))
        conn.commit()
        return {"status": "success", "message": "Therapist updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/emotions")
def get_emotions():
    """Returns the complete EMOTION_MAP dictionary for frontend visualization."""
    return EMOTION_MAP

# ── Auth Endpoints ──

@app.post("/register")
def register_user(user: UserCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        hashed_password = get_password_hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, therapist_id) VALUES (?, ?, ?, ?)",
            (user.username, hashed_password, user.role, user.therapist_id)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"status": "success", "user_id": user_id}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")
    finally:
        conn.close()

@app.post("/login")
def login(user: UserLogin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash, role FROM users WHERE username = ?", (user.username,))
    record = cursor.fetchone()
    conn.close()

    if not record or not verify_password(user.password, record[1]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"status": "success", "user_id": record[0], "role": record[2]}

# ── Feature Endpoints ──

@app.post("/analyze")
def analyze_journal(entry: AnalyzeRequest):
    """
    Analyzes journal text and returns detected emotion with polar coordinates.
    PRIVACY: The text is processed but NEVER stored in the database.
    """
    radius, angle, emotion_name = calculate_polar_coordinates(entry.text)
    
    return {
        "emotion": str(emotion_name),
        "radius": float(radius),
        "angle": float(angle)
    }

@app.post("/log")
def log_entry(request: LogRequest):
    """
    Logs emotion metadata linked to a specific user.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    timestamp = datetime.now().isoformat()
    
    # Convert lists to JSON strings for storage
    activities_json = json.dumps(request.activities)
    people_json = json.dumps(request.people)
    places_json = json.dumps(request.places)
    
    try:
        cursor.execute("""
            INSERT INTO logs (user_id, timestamp, emotion, radius, angle, color_category, activities, people, places)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (request.user_id, timestamp, request.emotion, request.radius, request.angle, 
              request.color_category, activities_json, people_json, places_json))
        conn.commit()
        return {"status": "success", "timestamp": timestamp}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    finally:
        conn.close()

@app.get("/logs/{user_id}")
def get_user_logs(user_id: int):
    """
    Retrieves all logs for a specific user.
    Used by Clients (own logs) and Therapists (viewing client).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, timestamp, emotion, radius, angle, color_category, activities, people, places
        FROM logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "timestamp": row[1],
            "emotion": row[2],
            "radius": row[3],
            "angle": row[4],
            "color_category": row[5],
            "activities": json.loads(row[6]) if row[6] else [],
            "people": json.loads(row[7]) if row[7] else [],
            "places": json.loads(row[8]) if row[8] else []
        })
    
    return history

@app.get("/therapist/{therapist_id}/clients")
def get_therapist_clients(therapist_id: int):
    """
    Returns a list of all clients assigned to a specific therapist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username FROM users WHERE therapist_id = ?", (therapist_id,))
    clients = [{"id": row[0], "username": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return clients
