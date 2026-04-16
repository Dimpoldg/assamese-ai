"""
database.py — SQLite memory system for Assamese AI
Stores conversation history per session
"""

import sqlite3
from datetime import datetime
from typing import List, Dict

DB_PATH = "assamese_ai.db"


def init_db():
    """Initialize SQLite database and create tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT    NOT NULL,
            role       TEXT    NOT NULL CHECK(role IN ('user','assistant')),
            content    TEXT    NOT NULL,
            timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_session
        ON conversations(session_id, timestamp)
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")


def save_message(session_id: str, role: str, content: str):
    """Save a single message to the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()


def get_history(session_id: str, limit: int = 12) -> List[Dict]:
    """
    Retrieve last N messages for a session.
    Returns in chronological order (oldest first) for AI context.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT role, content FROM (
            SELECT role, content, timestamp
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ) ORDER BY timestamp ASC
    """, (session_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def clear_history(session_id: str):
    """Delete all messages for a session"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


def list_sessions() -> List[str]:
    """List all unique session IDs"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT session_id FROM conversations ORDER BY MAX(timestamp) DESC")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_session_stats(session_id: str) -> Dict:
    """Get statistics for a session"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*), MIN(timestamp), MAX(timestamp)
        FROM conversations WHERE session_id = ?
    """, (session_id,))
    row = c.fetchone()
    conn.close()
    return {
        "total_messages": row[0],
        "first_message":  row[1],
        "last_message":   row[2]
    }
