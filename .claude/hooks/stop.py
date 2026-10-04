#!/usr/bin/env python3
"""Stop hook: remind about uncommitted work. Zero LLM, no network, fails open."""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _git(root, *args) -> str:
    r = subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True, timeout=5)
    return r.stdout if r.returncode == 0 else ""


def main() -> int:
    from project_root import project_root

    sys.stdin.read()
    root = project_root()
    status = [ln for ln in _git(root, "status", "--porcelain", "-uall").splitlines() if ln.strip()]
    if not status:
        return 0
    msg = f"{len(status)} changed file(s) - uncommitted changes: run /commit or /session-winddown."
    dec = "docs/decisions.md"
    added = any(ln.startswith("?? ") and ln[3:].strip() == dec for ln in status)
    for ln in _git(root, "diff", "HEAD", "--numstat", "--", dec).splitlines():
        parts = ln.split("\t")
        added = added or (parts[0].isdigit() and int(parts[0]) > 0)
    if added:
        msg += " decision log changed - confirm the entry has its REJECTED option."
    print(json.dumps({"systemMessage": msg}))
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
