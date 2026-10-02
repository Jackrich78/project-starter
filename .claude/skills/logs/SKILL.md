---
name: logs
description: "Show what Claude did this session or recently, from the observability log. Use on \"logs\", \"what did you just run\", \"which tools failed\", \"how many sub-agents\". Meaningful only when CLAUDE_HARNESS_OBSERVABILITY=1."
type: skill
disable-model-invocation: true
argument-hint: "[sessions|tools|agents|failures]"
---

# Logs

## Context

Opt-in log: `.claude/hooks/README.md`. Off by default; `.claude/logs/agent.db` is gitignored. Table `events(id, ts, session_id, event, tool_name, agent_type, payload_json)`. Payloads are redacted; do not print them wholesale.

## Pattern

1. `[ -f .claude/logs/agent.db ]` fails, or `CLAUDE_HARNESS_OBSERVABILITY` is not `1` -> say "observability is off" and how to enable it (README). Stop.
2. Read-only queries, `sqlite3 -readonly .claude/logs/agent.db`:
   - sessions: `SELECT session_id, COUNT(*) n, MIN(ts), MAX(ts) FROM events GROUP BY session_id ORDER BY MAX(ts) DESC LIMIT 10;`
   - tools: `SELECT tool_name, COUNT(*) FROM events WHERE tool_name IS NOT NULL GROUP BY 1 ORDER BY 2 DESC;`
   - agents: `SELECT agent_type, COUNT(*) FROM events WHERE event='SubagentStart' GROUP BY 1;`
   - failures: `SELECT ts, tool_name FROM events WHERE event='PostToolUseFailure' ORDER BY ts DESC LIMIT 20;`
3. Summarise in a few lines; no raw payloads.

## Example

`/logs tools` -> "Bash 212, Read 148, Edit 61; 3 failures, all Bash."

## Anti-patterns

- Writing to the DB: read-only flag always.
- Dumping `payload_json`: redaction is best effort.
- Inventing numbers when the DB is absent.
