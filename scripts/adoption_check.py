#!/usr/bin/env python3
"""Report which `.claude/agents/*.md` miss a required block.

    python3 scripts/adoption_check.py

Greps agent definitions for contract markers. Always fresh: no maintained
table to rot. Contract: .claude/rules/agents.md. Exit 0 always (a report).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
SKIP = {"TEMPLATE.md", "README.md"}
MEMORY_HEADING = "## Your memory (read first)"


def frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return m.group(1) if m else ""


def first_h2(text: str) -> str | None:
    body = re.sub(r"^---\n.*?\n---\n?", "", text, count=1, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    in_fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("## "):
            return line.rstrip()
    return None


def model_of(text: str) -> str | None:
    m = re.search(r"^model:\s*(\w+)", frontmatter(text), re.MULTILINE)
    return m.group(1) if m else None


# (label, predicate(text) -> bool, applies(text) -> bool)
CHECKS = [
    ("Memory block is first section", lambda t: first_h2(t) == MEMORY_HEADING, lambda t: True),
    ("Self-healing (Failure Recovery)", lambda t: "## Failure Recovery" in t, lambda t: True),
    ("ESCALATION sentinel", lambda t: "ESCALATION" in t, lambda t: True),
    ("Model pin", lambda t: model_of(t) in {"sonnet", "haiku", "opus"}, lambda t: True),
    ("Effort pin", lambda t: re.search(r"^effort:\s*\w+", frontmatter(t), re.MULTILINE) is not None, lambda t: True),
    ("Stance (opus agents)", lambda t: "## Stance" in t, lambda t: model_of(t) == "opus"),
]


def main() -> None:
    agents = sorted(f for f in AGENTS_DIR.glob("*.md") if f.name not in SKIP)
    print(f"Agent contract adoption ({len(agents)} agents)\n")
    for label, ok, applies in CHECKS:
        scope = [f for f in agents if applies(f.read_text(encoding="utf-8"))]
        missing = [f.stem for f in scope if not ok(f.read_text(encoding="utf-8"))]
        total = len(scope)
        status = "ok" if not missing else "gap"
        print(f"  {label}: {total - len(missing)}/{total} ({status})")
        if missing:
            print(f"    missing: {', '.join(missing)}")
    print()


if __name__ == "__main__":
    main()
