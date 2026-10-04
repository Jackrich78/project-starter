#!/usr/bin/env python3
"""Print a session transcript as redacted text turns: the one sanctioned way to read it.

    python3 scripts/recall.py [SESSION_UUID] [--grep PHRASE]

Default: the newest top-level session of this project (sub-agent runs skipped).
Prints only user/assistant text as `U:`/`A:` lines. Tool inputs and tool results
are dropped (that is where most secrets land); every line passes through
pre_compact.redact. Read-only; never writes a file.
"""
import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("pre_compact", Path(__file__).resolve().parents[1] / ".claude/hooks/pre_compact.py")
pre_compact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pre_compact)


def turns(path):
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            m = json.loads(raw).get("message") or {}
        except (ValueError, AttributeError):
            continue
        c = m.get("content")
        if isinstance(c, list):
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if m.get("role") in ("user", "assistant") and isinstance(c, str):
            for line in filter(str.strip, c.splitlines()):
                yield ("U: " if m["role"] == "user" else "A: ") + line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?")
    ap.add_argument("--grep")
    a = ap.parse_args()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
    d = Path.home() / ".claude" / "projects" / str(root).replace("/", "-")
    files = [p for p in d.glob("*.jsonl") if not p.name.startswith("agent-")] if d.is_dir() else []
    if a.session:
        files = [p for p in files if p.stem == a.session]
    if not files:
        sys.exit(f"recall: no transcript found in {d}")
    for line in turns(max(files, key=lambda p: p.stat().st_mtime)):
        line = pre_compact.redact(line)
        if not a.grep or a.grep.lower() in line.lower():
            print(line)


main()
