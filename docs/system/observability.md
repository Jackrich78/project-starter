# Observability

**Updated:** 2026-03-08
**Purpose:** Logging, checkpoints, and debugging reference

---

## Overview

Every hook event is logged to SQLite via `send_event.py`. This enables:
- **Verification:** Prove what Claude actually did
- **Debugging:** Trace issues to specific operations
- **Trust calibration:** MTTT (Mean Time To Trust) < 30 seconds

**Core principle:** "Logs are the only reliable witness in agentic systems."

---

## Architecture: IndyDevDan Pattern

Validation and observability are **separate hooks**:

```
Hook Event
    ├── pre_tool_use.py      (Validation - can block)
    └── send_event.py        (Observability - fire-and-forget)
```

Both receive the same stdin input. Validation can fail without affecting logging. Logging can fail without affecting validation.

**Source:** [github.com/disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)

---

## Events Table

**Location:** `.claude/logs/agent.db`

**Schema:**
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

**Indexes:** `timestamp`, `session_id`, `hook_event_type`

---

## Common Queries

### What did Claude do?
```bash
sqlite3 .claude/logs/agent.db "
  SELECT datetime(timestamp), hook_event_type, tool_name, file_path
  FROM events
  ORDER BY timestamp DESC
  LIMIT 20;
"
```

### Filter by tool
```bash
sqlite3 .claude/logs/agent.db "
  SELECT datetime(timestamp), file_path
  FROM events
  WHERE tool_name = 'Edit'
  ORDER BY timestamp DESC;
"
```

### Filter by session
```bash
sqlite3 .claude/logs/agent.db "
  SELECT datetime(timestamp), tool_name, file_path
  FROM events
  WHERE session_id = 'your-session-id'
  ORDER BY timestamp;
"
```

### Count by hook type
```bash
sqlite3 .claude/logs/agent.db "
  SELECT hook_event_type, COUNT(*) as count
  FROM events
  GROUP BY hook_event_type
  ORDER BY count DESC;
"
```

### View full payload
```bash
sqlite3 .claude/logs/agent.db "
  SELECT timestamp, tool_name, payload
  FROM events
  WHERE id = 123;
"
```

---

## Hook Configuration

**Location:** `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [
        {"type": "command", "command": "python3 .claude/hooks/pre_tool_use.py"},
        {"type": "command", "command": "python3 .claude/hooks/send_event.py"}
      ]
    }],
    "PostToolUse": [{
      "hooks": [
        {"type": "command", "command": "python3 .claude/hooks/post_tool_use.py"},
        {"type": "command", "command": "python3 .claude/hooks/send_event.py"}
      ]
    }],
    "PreCompact": [{
      "hooks": [
        {"type": "command", "command": "python3 .claude/hooks/pre_compact.py"},
        {"type": "command", "command": "python3 .claude/hooks/send_event.py"}
      ]
    }],
    "Stop": [{
      "hooks": [
        {"type": "command", "command": "python3 .claude/hooks/stop.py"},
        {"type": "command", "command": "python3 .claude/hooks/send_event.py"}
      ]
    }],
    "SessionStart": [{
      "hooks": [
        {"type": "command", "command": "python3 .claude/hooks/send_event.py"}
      ]
    }]
  }
}
```

---

## Session Continuity: Dual-System Design

### Overview

Two complementary systems for session recovery:
1. **session-state.json** - Automatic checkpoint (30-min staleness hint)
2. **handover.md** - Manual knowledge transfer (feature-specific)

### Automatic Recovery (session-state.json)

**Purpose:** Safety net for unexpected context compaction
**Trigger:** PreCompact hook (automatic)
**Staleness:** 30 minutes (advisory; checked by /prime at load time, not automatically enforced)
**Gating:** Branch match (age is advisory)
**Access:** `/prime FEAT-XXX`

**Location:** `.claude/session-state.json`

**Known limitation:** session-state.json is currently write-only — created by pre_compact.py but not consumed by /prime or any other command. Recovery depends on handover.md via the /handover → /prime cycle. This is a known gap.

**Written by:** PreCompact hook (before context compaction)

**Structure:**
```json
{
  "timestamp": "2026-01-26T14:30:00Z",
  "compaction_trigger": "auto",
  "git_branch": "harness-v2",
  "git_dirty_count": 3,
  "primary_feature": "FEAT-010_ci_cd_integration",
  "active_features": [
    {
      "id": "FEAT-010_ci_cd_integration",
      "path": "docs/features/FEAT-010_ci_cd_integration",
      "status": "exploring",
      "has_prd": true,
      "has_research": false,
      "has_architecture": false
    }
  ],
  "recent_changes": [
    {
      "path": "docs/features/FEAT-010/plan.md",
      "modified": "2026-01-26T14:25:00Z"
    }
  ]
}
```

**When shown:**
- Run `/prime FEAT-XXX`
- Age < 30 minutes
- Same git branch
- Example: "💾 Session state: 15m ago, 3 uncommitted"

### Manual Handover (handover.md)

**Purpose:** Intentional knowledge transfer between sessions
**Trigger:** `/handover FEAT-XXX` (manual)
**TTL:** Until feature complete
**Scope:** Feature-specific (rich context)
**Access:** Read `docs/features/FEAT-XXX/handover.md` or `/prime FEAT-XXX`

**Location:** `docs/features/FEAT-XXX/handover.md`

**Structure:**
```markdown
# Session Handover - FEAT-XXX
*Generated: 2026-01-26 14:30*
*Updated: 2026-01-26 16:45*

## Current State
[Context and progress]

## Progress This Session
- [x] Completed items
- [ ] In-progress items

## Key Decisions
[Technical choices and rationale]

## What Didn't Work
[Failed approaches]

## Blockers/Uncertainties
[Open questions]

## Next Steps
1. [Priority actions]

## Relevant Files
- path/to/file:line - Description

## Git State
- Branch, status, last commit
```

**When shown:**
- Run `/prime FEAT-XXX`
- Always shown if exists
- Example: "📄 Handover: 2 hours old"

### Decision Tree

```
Ending session intentionally?
├─ Yes → Run /handover FEAT-XXX (creates rich handover.md)
└─ No → session-state.json saves automatically

Starting new session?
├─ Run /prime (normal overview)
└─ Run /prime FEAT-XXX (focused view + recovery context)

Unexpected compaction mid-work?
└─ session-state.json captured automatically
    Next session: /prime FEAT-XXX shows recent state
```

### Best Practices

**End of session:**
```bash
/handover FEAT-XXX    # Rich context for next session
```

**Start of session:**
```bash
/prime                 # Quick overview
/prime FEAT-XXX        # Focus on specific feature + recovery check
```

**Recovery context:**
- session-state: Recent (< 30 min), automatic, lightweight
- handover.md: Rich, intentional, feature-specific

### Feature Status Detection

| Files Present | Status |
|--------------|--------|
| PRD only | `exploring` |
| PRD + plan | `planning` |
| PRD + plan + code | `implementing` |

---

## Security Logging

Security events from `pre_tool_use.py` are logged to:
- `.claude/logs/security.log` (JSONL file)
- `events` table (via `send_event.py`)

### Security Log Format
```json
{"action": "blocked", "command": "rm -rf /", "reason": "Blocked pattern: rm\\s+-rf\\s+/"}
```

### Query Security Events
```bash
# From SQLite
sqlite3 .claude/logs/agent.db "
  SELECT datetime(timestamp), tool_name, payload
  FROM events
  WHERE hook_event_type = 'PreToolUse'
  ORDER BY timestamp DESC
  LIMIT 10;
"

# From JSONL
tail -20 .claude/logs/security.log
```

---

## Debugging

### Hooks Not Firing

1. Check configuration:
   ```bash
   cat .claude/settings.json | jq '.hooks'
   ```

2. Test hook manually:
   ```bash
   echo '{"hook_event_name":"PreToolUse","tool_name":"Bash"}' | python3 .claude/hooks/send_event.py
   sqlite3 .claude/logs/agent.db "SELECT * FROM events ORDER BY id DESC LIMIT 1;"
   ```

3. Check for Python errors (hooks write errors to stderr)

### No Events in Database

1. Verify send_event.py is in settings.json for each hook type
2. Session may need restart after settings.json changes
3. Check database path is correct

### Session State Outdated

```bash
# Delete to force fresh start
rm .claude/session-state.json

# Reload context
/prime
```

---

## Maintenance

### Log Retention

- **Retention period:** Manual (no automatic cleanup; recommended: purge >30-day events periodically)
- **Cleanup:** Manual

### Cleanup Commands

```bash
# Clear events older than 30 days
sqlite3 .claude/logs/agent.db "DELETE FROM events WHERE timestamp < datetime('now', '-30 days');"

# Reset database completely
rm .claude/logs/agent.db
python3 .claude/logs/init_db.py
```

### Vacuum Database

```bash
sqlite3 .claude/logs/agent.db "VACUUM;"
```

---

## Testing Observability

### Manual Test

```bash
# 1. Trigger a test event
echo '{"hook_event_name":"PostToolUse","session_id":"test","tool_name":"Edit","tool_input":{"file_path":"/test.py"}}' | python3 .claude/hooks/send_event.py

# 2. Verify it was logged
sqlite3 .claude/logs/agent.db "SELECT * FROM events ORDER BY id DESC LIMIT 1;"
```

### Real Usage Test

1. Start new Claude Code session in project directory
2. Perform any action (read file, edit, bash command)
3. Query: `sqlite3 .claude/logs/agent.db "SELECT * FROM events ORDER BY id DESC LIMIT 5;"`

---

## See Also

- [architecture.md](architecture.md) - Hook system overview
- [integrations.md](integrations.md) - External tool integration
- `.claude/hooks/send_event.py` - Observability hook implementation
