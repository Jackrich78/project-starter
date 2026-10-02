#!/usr/bin/env python3
"""SessionStart hook: inject current priorities and a harness-health nudge."""
from __future__ import annotations

import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MAX_BYTES = 4096
PRIORITIES_STALE_DAYS = 14
HEALTH_STALE_DAYS = 30


def _frontmatter(text: str):
    """Return (dict, body). Hand-rolled; no yaml dependency."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = {}
            for ln in lines[1:i]:
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    fm[k.strip()] = v.strip().strip("\"'")
            return fm, "\n".join(lines[i + 1:])
    return {}, text


def _age_days(value):
    try:
        return (date.today() - date.fromisoformat(value)).days
    except Exception:
        return None


def main() -> int:
    from agent_db_path import project_root
    from send_event import redact

    root = project_root()
    parts = []
    pri = root / "docs" / "system" / "current-priorities.md"
    if pri.is_file():
        fm, body = _frontmatter(pri.read_text(encoding="utf-8", errors="replace"))
        updated = fm.get("updated")
        age = _age_days(updated) if updated else None
        body = redact(body).encode("utf-8")[:MAX_BYTES].decode("utf-8", "ignore").strip()
        head = "Current priorities (docs/system/current-priorities.md):"
        if age is None or age > PRIORITIES_STALE_DAYS:
            head += f" PRIORITIES MAY BE STALE (updated: {updated or 'unknown'})"
        parts.append(head + "\n\n" + body)
    ref = root / "docs" / "reference" / "claude-code.md"
    if ref.is_file():
        fm, _ = _frontmatter(ref.read_text(encoding="utf-8", errors="replace"))
        checked = fm.get("last_checked")
        age = _age_days(checked) if checked else None
        if age is None or age > HEALTH_STALE_DAYS:
            parts.append(f"harness-health due (last checked {checked or 'never'}): run /harness-health")
    if parts:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": "\n\n".join(parts)}}))
    return 0


if __name__ == "__main__":
    try:
        sys.stdin.read()
        main()
    except Exception:
        pass
    sys.exit(0)
