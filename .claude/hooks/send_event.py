#!/usr/bin/env python3
"""Opt-in observability logger. No-op unless CLAUDE_HARNESS_OBSERVABILITY=1.

One SQLite table (.claude/logs/agent.db). tool_input / tool_response are
stored only after redaction, capped at 32 KB. No network, no transcript
archive, no .env loading. Fails open: any error exits 0 silently.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EVENTS = {
    "SessionStart", "SessionEnd", "PreToolUse", "PostToolUse",
    "PostToolUseFailure", "SubagentStart", "SubagentStop", "PreCompact", "Stop",
}
MAX_PAYLOAD = 32 * 1024

# Key names, with any snake/kebab prefix or suffix (SECRET_KEY, DB_PASS, MYSQL_PWD, CLIENT_SECRET_V2).
_KEYS = (
    r"\b(?:[a-z0-9]+[_-])*(?:api[_-]?key|auth[_-]?key|auth|secret|password|passwd|passphrase|pwd|pass|token"
    r"|credentials?|private[_-]?key|access[_-]?key)(?:[_-][a-z0-9]+)*"
)
# Order matters: block/structured patterns first, generic key=value last.
_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY(?: BLOCK)?-----.*?(?:-----END [A-Z ]*PRIVATE KEY(?: BLOCK)?-----|\Z)", re.S),
     "[REDACTED PRIVATE KEY]"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{5,}\.eyJ[A-Za-z0-9_-]{5,}(?:\.[A-Za-z0-9_-]*)?"), "[REDACTED JWT]"),
    (re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}"), "[REDACTED API KEY]"),
    (re.compile(r"\b(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]{10,}"), "[REDACTED API KEY]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "[REDACTED GH TOKEN]"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), "[REDACTED GH TOKEN]"),
    (re.compile(r"\b(?:glpat-|hf_|npm_|dop_v1_|pypi-|AGE-SECRET-KEY-)[A-Za-z0-9_-]{10,}"), "[REDACTED TOKEN]"),
    (re.compile(r"\bxox[abpe]-[A-Za-z0-9-]{10,}|\bxapp-[A-Za-z0-9-]{10,}"), "[REDACTED SLACK TOKEN]"),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "[REDACTED AWS KEY]"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{30,}"), "[REDACTED GOOGLE KEY]"),
    (re.compile(r"\bSG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}"), "[REDACTED SENDGRID KEY]"),
    (re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{30,}"), "[REDACTED TELEGRAM TOKEN]"),
    (re.compile(r"(?i)(aws_secret_access_key[\"']?\s*[:=]\s*[\"']?)[A-Za-z0-9/+=]{40}"), r"\1***"),
    (re.compile(r"(?i)\b(Bearer\s+)[A-Za-z0-9._~+/=-]{8,}"), r"\1***"),
    (re.compile(r"(?i)\b(Authorization:\s*(?:Basic|Token|Digest)?\s*)(?!Bearer)[A-Za-z0-9._~+/=-]{8,}"), r"\1***"),
    (re.compile(r"(?i)\b([a-z][a-z0-9+.-]*://[^\s:/@]+:)[^\s@]+(@)"), r"\1***\2"),
    (re.compile(r"(?i)\b([a-z][a-z0-9+.-]*://)[A-Za-z0-9_-]{16,}(@)"), r"\1***\2"),
    (re.compile(r"(?i)([?&](?:key|api_?key|token|access_token|secret|password|sig|signature|auth)=)[^&\s\"']+"), r"\1***"),
    (re.compile(r"(?i)(\s-u\s+[^\s:]+:)\S+"), r"\1***"),
    (re.compile(r"(\s-p)[^\s-]\S*"), r"\1***"),
    (re.compile(r"(?i)(\s--?(?:token|password|passwd|api[-_]?key|secret|auth|private[-_]?key)(?:=|\s+))[^\s-]\S*"), r"\1***"),
    (re.compile(r"(?i)\b((?:session|sid|sessionid|csrftoken|xsrf-token|auth_token|jwt|remember_token)=)[^;\s\"']{6,}"), r"\1***"),
    (re.compile(r"(?i)(" + _KEYS + r"\\?[\"']?\s*[:=]\s*\\?[\"']?)[^\s\"'\[\\]{3,}"), r"\1***"),
]


def redact(text: str) -> str:
    """Pure: replace secret values with *** keeping the key/shape."""
    if not isinstance(text, str):
        return text
    for pat, repl in _PATTERNS:
        text = pat.sub(repl, text)
    return text


def _redact_obj(obj):
    if isinstance(obj, str):
        return redact(obj)
    if isinstance(obj, dict):
        return {k: _redact_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_redact_obj(v) for v in obj]
    return obj


def _connect(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            session_id TEXT,
            event TEXT NOT NULL,
            tool_name TEXT,
            agent_type TEXT,
            payload_json TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
        CREATE INDEX IF NOT EXISTS idx_events_event ON events(event);
        """
    )
    return conn


def main() -> int:
    if os.environ.get("CLAUDE_HARNESS_OBSERVABILITY") != "1":
        return 0
    data = json.loads(sys.stdin.read())
    if not isinstance(data, dict):
        return 0
    event = data.get("hook_event_name")
    if event not in EVENTS:
        return 0
    from agent_db_path import agent_db_path

    payload = _redact_obj({
        k: data[k] for k in (
            "tool_input", "tool_response", "error", "source", "reason",
            "trigger", "agent_id", "agent_type", "cwd",
        ) if k in data
    })
    text = redact(json.dumps(payload, default=str))
    if len(text) > MAX_PAYLOAD:
        text = json.dumps({"truncated": True, "head": text[:MAX_PAYLOAD - 64]})
    conn = _connect(agent_db_path())
    try:
        conn.execute(
            "INSERT INTO events (ts, session_id, event, tool_name, agent_type, payload_json)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                data.get("session_id"),
                event,
                data.get("tool_name"),
                data.get("agent_type"),
                text,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
