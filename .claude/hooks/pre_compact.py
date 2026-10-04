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
    from project_root import project_root

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
