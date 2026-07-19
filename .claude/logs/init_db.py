#!/usr/bin/env python3
"""
Initialize the SQLite database for agent observability.
Run once to create the schema.

Schema: Single 'events' table captures all hook events.
Pattern: IndyDevDan's claude-code-hooks-multi-agent-observability
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agent.db')

SCHEMA = """
-- Events table: captures all hook events (send_event.py writes here)
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    session_id TEXT,
    hook_event_type TEXT NOT NULL,
    tool_name TEXT,
    file_path TEXT,
    payload TEXT
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
CREATE INDEX IF NOT EXISTS idx_events_hook_type ON events(hook_event_type);
CREATE INDEX IF NOT EXISTS idx_events_tool ON events(tool_name);
"""

def init_database():
    """Initialize the database with schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

if __name__ == '__main__':
    init_database()
