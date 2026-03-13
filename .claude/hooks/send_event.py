#!/usr/bin/env python3
"""
Observability Hook - Fire-and-Forget Event Logger

Logs ALL hook events to SQLite for observability.
Runs as a second hook alongside validation hooks.
Always exits 0 (never blocks).

Pattern from IndyDevDan's claude-code-hooks-multi-agent-observability.
"""

import json
import sqlite3
import sys
import os
from datetime import datetime, timezone

# Database path relative to this script
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'agent.db')


def ensure_events_table(conn: sqlite3.Connection) -> None:
    """Create events table if it doesn't exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT,
            hook_event_type TEXT NOT NULL,
            tool_name TEXT,
            file_path TEXT,
            payload TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_hook_type ON events(hook_event_type)
    """)
    conn.commit()


def extract_file_path(tool_input: dict, tool_name: str) -> str | None:
    """Extract file path from tool input based on tool type."""
    if not tool_input:
        return None

    # Different tools use different parameter names
    if tool_name in ('Read', 'Write', 'Edit', 'MultiEdit'):
        return tool_input.get('file_path') or tool_input.get('path')
    elif tool_name == 'Glob':
        return tool_input.get('pattern')
    elif tool_name == 'Grep':
        return tool_input.get('path')
    elif tool_name == 'Task':
        # Extract subagent type for agent invocation tracking
        return tool_input.get('subagent_type')
    elif tool_name == 'Bash':
        # Could extract from command, but not reliable
        return None

    return None


def log_event(data: dict) -> None:
    """Log event to SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        ensure_events_table(conn)

        # Extract fields from hook input
        timestamp = datetime.now(timezone.utc).isoformat()
        session_id = data.get('session_id')
        hook_event_type = data.get('hook_event_name', 'unknown')
        tool_name = data.get('tool_name')
        tool_input = data.get('tool_input', {})

        # Extract file path if present
        file_path = extract_file_path(tool_input, tool_name)

        # Store full payload as JSON for debugging
        payload = json.dumps({
            'tool_input': tool_input,
            'tool_response': data.get('tool_response'),
            'cwd': data.get('cwd'),
            'transcript_path': data.get('transcript_path')
        }, default=str)

        # Insert event
        conn.execute("""
            INSERT INTO events (timestamp, session_id, hook_event_type, tool_name, file_path, payload)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, session_id, hook_event_type, tool_name, file_path, payload))

        conn.commit()
        conn.close()

    except Exception as e:
        # Fire-and-forget: log error but never fail
        sys.stderr.write(f"[send_event] Error logging event: {e}\n")


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        # Log the event
        log_event(input_data)

    except json.JSONDecodeError:
        # No valid JSON input, skip
        pass
    except Exception as e:
        # Never fail, just log
        sys.stderr.write(f"[send_event] Unexpected error: {e}\n")

    # Always exit 0 (fire-and-forget)
    sys.exit(0)


if __name__ == '__main__':
    main()
