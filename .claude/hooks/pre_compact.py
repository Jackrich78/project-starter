#!/usr/bin/env python3
"""PreCompact hook: zero-LLM structural salvage of the session transcript.

Writes .claude/salvage/salvage-<session_id>-<ts>.md (gitignored, <=6 KB, newest
10 kept) and .claude/session-state.json. Fails open.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MAX_BYTES = 6 * 1024
KEEP = 10


def _blocks(msg):
    c = (msg or {}).get("content")
    if isinstance(c, str):
        return [{"type": "text", "text": c}]
    return [b for b in c if isinstance(b, dict)] if isinstance(c, list) else []


def _text(msg) -> str:
    return "\n".join(b.get("text", "") for b in _blocks(msg) if b.get("type") == "text").strip()


def parse(path):
    users, last_assistant, files, cmds, agents = [], "", [], [], []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if not isinstance(e, dict):
                continue
            msg = e.get("message") if isinstance(e.get("message"), dict) else {}
            kind = e.get("type")
            if kind == "user":
                t = _text(msg)
                if t and not t.startswith("<"):
                    users.append(t)
            elif kind == "assistant":
                t = _text(msg)
                if t:
                    last_assistant = t
                for b in _blocks(msg):
                    if b.get("type") != "tool_use":
                        continue
                    name, inp = b.get("name"), b.get("input") or {}
                    if name in ("Edit", "Write", "MultiEdit") and inp.get("file_path"):
                        files.append(inp["file_path"])
                    elif name == "Bash" and inp.get("command"):
                        cmds.append(inp["command"])
                    elif name in ("Task", "Agent"):
                        agents.append(f"{inp.get('subagent_type', '?')}: {inp.get('description', '')}")
                    elif name == "Skill" and inp.get("skill"):
                        agents.append(f"skill {inp['skill']}")
    return users, last_assistant, files, cmds, agents


def _dedupe(seq):
    return list(dict.fromkeys(seq))


def build(session_id, parsed) -> str:
    from send_event import redact

    users, last_a, files, cmds, agents = parsed
    # redact the whole string first, then cut: a cut-off token would otherwise keep its real prefix
    one = lambda s, n: redact(" ".join(s.split()))[:n]
    out = [f"# Salvage {session_id}", "", "## Last user messages"]
    out += [f"- {one(u, 400)}" for u in users[-5:]] or ["- (none)"]
    out += ["", "## Last assistant text", one(last_a, 600) or "(none)", "", "## Files edited"]
    out += [f"- {redact(f)}" for f in _dedupe(files)[-20:]] or ["- (none)"]
    out += ["", "## Commands run"]
    out += [f"- {one(c, 120)}" for c in cmds[-10:]] or ["- (none)"]
    out += ["", "## Agents / skills dispatched"]
    out += [f"- {one(a, 160)}" for a in agents[-10:]] or ["- (none)"]
    text = "\n".join(out) + "\n"
    return text.encode("utf-8")[:MAX_BYTES].decode("utf-8", "ignore")


def main() -> int:
    from agent_db_path import project_root

    data = json.loads(sys.stdin.read())
    tp = data.get("transcript_path")
    if not isinstance(data, dict) or not tp or not os.path.isfile(tp):
        return 0
    sid = re.sub(r"[^A-Za-z0-9_-]", "", str(data.get("session_id") or "unknown")) or "unknown"
    parsed = parse(tp)
    root = project_root()
    sdir = root / ".claude" / "salvage"
    sdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    path = sdir / f"salvage-{sid}-{ts}.md"
    path.write_text(build(sid, parsed), encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    for old in sorted(sdir.glob("salvage-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[KEEP:]:
        old.unlink(missing_ok=True)
    state = {
        "session_id": sid, "ts": ts, "salvage": str(path.relative_to(root)),
        "files_edited": len(_dedupe(parsed[2])), "commands_run": len(parsed[3]),
    }
    (root / ".claude" / "session-state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
