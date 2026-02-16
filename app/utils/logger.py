import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "data/security_audit.db"

def init_db():
    """Initializes the SQLite database and enables WAL mode for concurrency."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_text TEXT,
            risk_score REAL,
            action TEXT,
            patterns TEXT,
            semantic_sim REAL,
            latency_ms REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_event(event_data: dict):
    """
    Saves a security event to the database.
    Designed to be called by FastAPI BackgroundTasks.
    """
    try:
        # Ensure DB is ready
        if not os.path.exists(DB_PATH):
            init_db()

        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO security_logs 
            (timestamp, input_text, risk_score, action, patterns, semantic_sim, latency_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.utcnow().isoformat(),
            event_data.get("input", ""),
            event_data.get("risk_score", 0.0),
            event_data.get("action", "unknown"),
            json.dumps(event_data.get("patterns", [])),
            event_data.get("semantic_similarity", 0.0),
            event_data.get("latency_ms", 0.0)
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f" Logging Error: {str(e)}")

init_db()