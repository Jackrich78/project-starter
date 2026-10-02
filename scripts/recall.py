#!/usr/bin/env python3
"""Search this project's Claude Code transcripts (main sessions and their sub-agents) for a term.

    python3 scripts/recall.py <term> [--session ID] [--limit 40] [--days 30]
    python3 scripts/recall.py --list [--days 30]        # sessions newest first, redacted first message

Why: after a compaction, "I have never seen this" is not "this did not happen".
Before calling a path, id or citation invented, look it up. Transcripts live
outside the repo under ~/.claude/projects/<project-slug>/ (one JSONL per
session, sub-agents under <session>/subagents/). Read-only; prints matching
lines with session, role and timestamp, each passed through send_event.redact
(this is the one sanctioned way to search transcripts, which the Read tool and
the deny hook otherwise refuse); never prints a line longer than 240 chars.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude" / "hooks"))
from send_event import redact  # noqa: E402  (transcripts hold pasted tokens; never print them raw)


def project_dir() -> Path:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = str(Path(root).resolve()).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def _text(obj) -> str:
    """Flatten a transcript record's message content to plain text."""
    msg = obj.get("message") if isinstance(obj, dict) else None
    content = msg.get("content") if isinstance(msg, dict) else obj.get("content") if isinstance(obj, dict) else None
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                parts.append(c.get("text") or json.dumps(c.get("input") or c.get("content") or "", ensure_ascii=False))
            else:
                parts.append(str(c))
        return "\n".join(parts)
    return ""


def _first_real_message(path: Path) -> str:
    """The first user message that is prose, not a slash-command or system wrapper; '' if none."""
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                msg = obj.get("message") if isinstance(obj, dict) else None
                if not isinstance(msg, dict) or msg.get("role") != "user":
                    continue
                c = _text(obj).strip()
                if c and not c.startswith("<") and "command-name" not in c and "command-message" not in c:
                    return c
    except OSError:
        pass
    return ""


def list_sessions(days: int) -> int:
    """Newest first: session id, modified time, size, redacted 80-char topic. Sub-agent files are skipped."""
    pdir = project_dir()
    if not pdir.exists():
        print(f"no transcripts at {pdir}", file=sys.stderr)
        return 1
    cutoff = time.time() - days * 86400
    files = sorted((p for p in pdir.glob("*.jsonl") if p.stat().st_mtime >= cutoff),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    shown = 0
    for p in files:
        topic = _first_real_message(p)
        if not topic:
            continue
        st = p.stat()
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
        print(f"{p.stem} | {when} | {st.st_size // 1024:>5} KB | {redact(' '.join(topic.split()))[:80]}")
        shown += 1
    if shown == 0:
        print(f"no sessions with a user message in {len(files)} transcript(s) under {pdir}")
    return 0


def search(term: str, session: str | None, limit: int, days: int) -> int:
    pdir = project_dir()
    if not pdir.exists():
        print(f"no transcripts at {pdir}", file=sys.stderr)
        return 1
    rx = re.compile(re.escape(term), re.I)
    cutoff = time.time() - days * 86400
    files = sorted((p for p in pdir.rglob("*.jsonl") if p.stat().st_mtime >= cutoff),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if session:
        files = [p for p in files if session in str(p)]
    shown = 0
    for path in files:
        sid = path.relative_to(pdir)
        try:
            with path.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    text = _text(obj)
                    if not text or not rx.search(text):
                        continue
                    role = obj.get("type") or (obj.get("message") or {}).get("role") or "?"
                    ts = str(obj.get("timestamp") or "")[:19]
                    for frag in (ln for ln in text.replace("\\n", "\n").splitlines() if rx.search(ln)):
                        print(f"{sid} | {ts} | {role}: {redact(' '.join(frag.split()))[:240]}")
                        shown += 1
                        if shown >= limit:
                            print(f"... stopped at --limit {limit}")
                            return 0
        except OSError:
            continue
    if shown == 0:
        print(f"no match for {term!r} in {len(files)} transcript(s) under {pdir}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("term", nargs="?", help="text to search for (omit with --list)")
    ap.add_argument("--list", action="store_true", help="list this project's sessions, newest first, redacted topic")
    ap.add_argument("--session", help="only transcripts whose path contains this id")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()
    if a.list:
        sys.exit(list_sessions(a.days))
    if not a.term:
        ap.error("a search term is required unless --list is given")
    sys.exit(search(a.term, a.session, a.limit, a.days))
