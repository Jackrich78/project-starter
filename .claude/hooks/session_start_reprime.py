#!/usr/bin/env python3
"""SessionStart hook: after compact/resume, re-inject the session's salvage file."""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MAX_CHARS = 8000
FALLBACK_AGE_S = 3600


def _sid(path) -> str:
    return path.name[len("salvage-"):-len(".md")].rsplit("-", 1)[0]


def main() -> int:
    from agent_db_path import project_root

    data = json.loads(sys.stdin.read())
    if not isinstance(data, dict) or data.get("source") not in ("compact", "resume"):
        return 0
    sdir = project_root() / ".claude" / "salvage"
    files = sorted(sdir.glob("salvage-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    sid = data.get("session_id")
    pick = next((p for p in files if sid and _sid(p) == sid), None)
    if pick is None and files and time.time() - files[0].stat().st_mtime <= FALLBACK_AGE_S:
        pick = files[0]
    if pick is None:
        return 0
    text = pick.read_text(encoding="utf-8", errors="replace")[:MAX_CHARS]
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart", "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
