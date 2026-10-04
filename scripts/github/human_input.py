#!/usr/bin/env python3
"""List the human's input since the assistant's last signed comment.

Stdlib only. Reads the agent signature from CLAUDE.md `## Workflow`; `gh` is one account for
human and agent, so the signature is the only tell (docs/system/issue-flow.md).
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

FIELDS = "number,title,state,createdAt,closedAt,updatedAt,body,comments,labels"
CLOSE_WINDOW = timedelta(seconds=60)
ASK_LINE = re.compile(r"^(\*\*Ask\b|Ask:)", re.M)
ROOT_CLAUDE_MD = Path(__file__).resolve().parents[2] / "CLAUDE.md"


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def read_signature(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    section = re.search(r"^## Workflow[ \t]*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    text = section.group(1) if section else ""
    m = re.search(r"^- Agent signature on issues and comments:\s*`([^`]*)`", text, re.M)
    sig = m.group(1).strip() if m else ""
    return sig


def entries(issue, sig):
    """(time, signed, body) for the issue body and every comment."""
    # a whole line equal to the signature: a quote-reply ("> > sig") or an inline quote is not
    return [(ts(e["createdAt"]), any(l.strip() == sig for l in e["body"].splitlines()), e["body"])
            for e in [issue, *issue["comments"]]]


def classify(issue, sig):
    signed_at = unsigned_at = None
    signed_body = ""
    for when, signed, body in entries(issue, sig):
        if signed and (signed_at is None or when > signed_at):
            signed_at, signed_body = when, body
        elif not signed and (unsigned_at is None or when > unsigned_at):
            unsigned_at = when
    closed = issue["state"] == "CLOSED"
    if closed and (signed_at is None or signed_at < ts(issue["closedAt"]) - CLOSE_WINDOW):
        return "closed"
    if unsigned_at is not None and (signed_at is None or unsigned_at > signed_at):
        return "replied"
    if closed:
        return None
    # an Ask line, or the label that marks asks written before the Ask block existed
    labels = {lab["name"] for lab in issue.get("labels", [])}
    if ASK_LINE.search(signed_body) or "ready-for-human" in labels:
        return "waiting"
    return None


def fetch_issues(now_arg, days):
    """(issues, stderr, returncode) from `gh issue list` for the last `days` days."""
    now = ts(now_arg) if now_arg else datetime.now().astimezone()
    since = (now - timedelta(days=days)).date().isoformat()
    res = subprocess.run(
        ["gh", "issue", "list", "--state", "all", "--limit", "200",
         "--search", f"updated:>={since}", "--json", FIELDS],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        return None, res.stderr, res.returncode
    return json.loads(res.stdout), "", 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-json")
    ap.add_argument("--claude-md", default=ROOT_CLAUDE_MD)
    ap.add_argument("--now")
    ap.add_argument("--days", type=int, default=14)
    a = ap.parse_args()

    sig = read_signature(a.claude_md)
    if not sig:
        sys.stderr.write("human_input.py: no agent signature found in CLAUDE.md\n")
        return 1

    if a.from_json:
        with open(a.from_json, encoding="utf-8") as f:
            issues = json.load(f)
    else:
        issues, err, code = fetch_issues(a.now, a.days)
        if code:
            sys.stderr.write(err)
            return code

    headers = {"replied": "Human replied:", "closed": "Human closed:",
               "waiting": "Waiting on you:"}  # print order
    groups = {kind: [] for kind in headers}
    for i in sorted(issues, key=lambda i: ts(i["updatedAt"]), reverse=True):
        kind = classify(i, sig)
        if kind:
            num = f"#{i['number']}"
            # titles here already carry "#N · " (issue-flow.md); print the number once
            title = i["title"] if i["title"].startswith(num + " ") else f"{num} {i['title']}"
            groups[kind].append(title)

    lines = []
    for kind, header in headers.items():
        if groups[kind]:
            lines += [header, *groups[kind]]
    print("\n".join(lines) if lines else "Human input: nothing new")
    return 0


if __name__ == "__main__":
    sys.exit(main())
