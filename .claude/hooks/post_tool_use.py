#!/usr/bin/env python3
"""PostToolUse hook (Edit|Write|MultiEdit): nudge when a docs/ file is not in docs/index.md."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    from project_root import project_root

    data = json.loads(sys.stdin.read())
    if not isinstance(data, dict) or data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0
    fp = (data.get("tool_input") or {}).get("file_path")
    if not fp:
        return 0
    root = project_root().resolve()
    path = os.path.realpath(fp if os.path.isabs(fp) else os.path.join(root, fp))
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    if not rel.startswith("docs/") or rel == "docs/index.md":
        return 0
    index = root / "docs" / "index.md"
    if not index.is_file():
        return 0
    base = os.path.basename(rel)
    if base in index.read_text(encoding="utf-8", errors="replace"):
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": f"docs/index.md does not list {base} - add it"}}))
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
