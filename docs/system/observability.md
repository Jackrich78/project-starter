---
type: domain-doc
title: Observability
description: The opt-in event store - what is recorded, redaction scope and limits, what /logs and agile-coach read, how to turn it on and off, and what is never stored.
tags: [observability, logging, privacy]
---

# Observability

**Off by default.** Nothing is written unless `CLAUDE_HARNESS_OBSERVABILITY=1`. It exists because the retro loop (`agile-coach`) needs one citable evidence tier beyond git history, but a store that persists tool output is a liability for people who did not ask for it, so a stranger who clones the template gets none.

## Turn it on or off

```bash
export CLAUDE_HARNESS_OBSERVABILITY=1      # on, this shell
# or persist per machine, uncommitted: "env" in .claude/settings.local.json
unset CLAUDE_HARNESS_OBSERVABILITY         # off; existing rows stay until you delete the file
rm .claude/logs/agent.db                   # forget everything
```

`send_event.py` is registered on every event but exits immediately when the variable is unset.

## Store

One SQLite file, `.claude/logs/agent.db` (gitignored; path resolved by `.claude/hooks/agent_db_path.py`, which honours `CLAUDE_PROJECT_DIR`).

```sql
events(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,          -- UTC ISO-8601
  session_id TEXT,
  event TEXT NOT NULL,       -- SessionStart, SessionEnd, PreToolUse, PostToolUse,
                             -- PostToolUseFailure, SubagentStart, SubagentStop, PreCompact, Stop
  tool_name TEXT,
  agent_type TEXT,
  payload_json TEXT          -- redacted, capped at 32 KB
)
-- indexes on session_id and event
```

`payload_json` carries only these keys when present: `tool_input`, `tool_response`, `error`, `source`, `reason`, `trigger`, `agent_id`, `agent_type`, `cwd`. Over 32 KB it is replaced by a truncated head with `"truncated": true`.

## Redaction: scope and limits

Applied to every payload before the insert: private-key blocks, JWTs, GitHub tokens, Slack tokens, AWS access keys and secret keys, `Bearer` tokens, passwords in URLs, and any `api_key` / `auth_key` / `secret` / `password` / `token` / `credential` key with a value (JSON, YAML and `KEY=value` forms; the key stays, the value becomes `***`).

It is pattern-based and best effort. It does not catch a secret with no telltale key or prefix, secrets split across fields, or secrets inside binary or encoded blobs. **Do not rely on it for anything you would not commit.** The rule that matters is upstream: never expand a secret into a printed position (CLAUDE.md § Security).

## Never stored

- No transcript archive, no copy of the conversation, no model output beyond tool responses.
- No `.env` loading; the hook reads nothing but its stdin.
- No network calls; nothing leaves the machine.
- No import of repository code at runtime (stdlib plus sibling hook files only).
- Unredacted payloads, anywhere. The compaction salvage file is separate, local and gitignored (`hooks.md`).

## Readers

- **`agile-coach`** at wind-down: resolves the path with `python3 .claude/hooks/agent_db_path.py` and queries read-only for retries, failed tools and long sessions; with no file it reports `[no-observability]` and uses git history and agent memory instead.
- **`/logs`**: ad-hoc queries, for example sessions and failed tools:

```bash
sqlite3 .claude/logs/agent.db "SELECT ts, event, tool_name FROM events ORDER BY id DESC LIMIT 20;"
sqlite3 .claude/logs/agent.db "SELECT ts, tool_name FROM events WHERE event='PostToolUseFailure' ORDER BY id DESC LIMIT 20;"
```

Separate from this store, the deny hook appends redacted cautions to `.claude/logs/security.log` whether or not observability is on. Before building any new metric or dashboard on this data, name the decision it changes: with no "if X crosses Y I do Z", it is trivia (`docs/guides/agent-harness-patterns.md` principle 8).
