import sqlite3
import os
import json
from datetime import datetime
from .crypto import encrypt

DB_FILE = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            encrypted_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_event(event_type: str, file_path: str, src_path: str = "", dest_path: str = "", user: str = "System", process: str = "Unknown", is_suspicious: bool = False, details: str = ""):
    """Logs an event to the database, encrypting the details."""
    payload = {
        "event_type": event_type,
        "file_path": file_path,
        "src_path": src_path,
        "dest_path": dest_path,
        "user": user,
        "process": process,
        "is_suspicious": is_suspicious,
        "details": details
    }
    json_data = json.dumps(payload)
    encrypted_data = encrypt(json_data)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (timestamp, encrypted_data)
        VALUES (?, ?)
    ''', (datetime.now().isoformat(), encrypted_data))
    conn.commit()
    conn.close()

def get_all_logs():
    """Retrieves all encrypted logs."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, timestamp, encrypted_data FROM audit_logs ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return rows
