---
updated: 2026-01-24T23:00:00Z
name: logs
description: Query the observability database to see what Claude did
args: "[recent|tools|sessions|count]"
---

# /logs Command

Query the SQLite observability database to verify what Claude did.

## Quick Start

```bash
/logs           # Recent 20 events
/logs recent    # Recent events (default)
/logs tools     # Group by tool
/logs sessions  # Group by session
/logs count     # Total event count
```

## Workflow

1. **Connect to Database**
   - Open `.claude/logs/agent.db`
   - Handle missing database gracefully

2. **Query Based on Scope**

   **recent (default):**
   ```sql
   SELECT datetime(timestamp), hook_event_type, tool_name, file_path
   FROM events
   ORDER BY timestamp DESC
   LIMIT 20;
   ```

   **tools:**
   ```sql
   SELECT tool_name, COUNT(*) as count
   FROM events
   WHERE tool_name IS NOT NULL
   GROUP BY tool_name
   ORDER BY count DESC;
   ```

   **sessions:**
   ```sql
   SELECT session_id, COUNT(*) as events, MIN(timestamp) as first, MAX(timestamp) as last
   FROM events
   WHERE session_id IS NOT NULL
   GROUP BY session_id
   ORDER BY last DESC
   LIMIT 10;
   ```

   **count:**
   ```sql
   SELECT COUNT(*) as total FROM events;
   ```

3. **Format Output**
   - Concise markdown tables
   - Timestamps in readable format
   - File paths truncated for readability

## Example Output

```bash
/logs
```

```markdown
## Recent Events

| Time | Event | Tool | File |
|------|-------|------|------|
| 22:28:38 | PostToolUse | Bash | |
| 22:28:07 | PreToolUse | Bash | |
| 22:27:59 | PostToolUse | Read | .../plan-template.md |
| 22:27:53 | PostToolUse | Edit | .../settings.json |

Total: 47 events
```

## Database Schema

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    session_id TEXT,
    hook_event_type TEXT NOT NULL,
    tool_name TEXT,
    file_path TEXT,
    payload TEXT
);
```

## Notes

- Requires `.claude/logs/agent.db` to exist
- Data populated by `send_event.py` hook
- Run `python3 .claude/logs/init_db.py` if database missing
- See `docs/system/observability.md` for full documentation
