#!/usr/bin/env python3
"""Audit CLAUDE.md for size, soft language, stale paths and orphan scoped rules.

    python3 scripts/audit_claude_md.py [--json] [--strict]

Deterministic checks only, no LLM. Thresholds follow the official guidance that a
CLAUDE.md should carry load-bearing rules only: warn above 120 lines, alert above
150. `--strict` exits 1 on any alert, stale path or orphan rule (used by CI).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WARN_LINES = 120
ALERT_LINES = 150

HEDGE_WORDS = [
    "consider using",
    "might want to",
    "you could",
    "it's a good idea",
    "try to ",
    "ideally ",
    "you may want",
    "it would be nice",
]

# Backtick-quoted relative paths that look like file references.
_PATH_RE = re.compile(r"`((?:docs|scripts|src|tests|\.claude|\.github)/[^`\s]+)`")


def check_line_count(path: Path) -> dict:
    count = len(path.read_text().splitlines())
    status = "alert" if count > ALERT_LINES else "warn" if count > WARN_LINES else "ok"
    return {"lines": count, "status": status}


def check_soft_language(path: Path) -> list[dict]:
    findings = []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        lower = line.lower()
        for word in HEDGE_WORDS:
            if word in lower:
                findings.append({"line": i, "text": line.strip(), "word": word})
                break
    return findings


def check_stale_paths(path: Path, repo_root: Path | None = None) -> list[dict]:
    root = repo_root or REPO_ROOT
    text = path.read_text()
    results, seen = [], set()
    for match in _PATH_RE.finditer(text):
        ref = match.group(1).rstrip(".,;:)")
        if "<" in ref or "{" in ref or "*" in ref:  # placeholders and globs
            continue
        if ":" in ref:
            ref = ref.split(":")[0]
        if ref in seen:
            continue
        seen.add(ref)
        line_num = text[: match.start()].count("\n") + 1
        results.append({"path": ref, "exists": (root / ref).exists(), "line": line_num})
    return results


def check_scoped_rules(rules_dir: Path, repo_root: Path | None = None) -> list[dict]:
    root = repo_root or REPO_ROOT
    results = []
    if not rules_dir.exists():
        return results
    for rule_file in sorted(rules_dir.glob("*.md")):
        paths, in_fm, in_paths = [], False, False
        for line in rule_file.read_text().splitlines():
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
                continue
            if in_fm and line.strip().startswith("paths:"):
                in_paths = True
                continue
            if in_paths and line.strip().startswith("- "):
                paths.append(line.strip()[2:].strip("\"'"))
            elif in_paths and line.strip() and not line.strip().startswith("- "):
                in_paths = False
        for pattern in paths:
            results.append({"rule": rule_file.name, "glob": pattern,
                            "matches": len(list(root.glob(pattern)))})
    return results


def run_all(claude_md: Path | None = None, rules_dir: Path | None = None,
            repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    md = claude_md or (root / "CLAUDE.md")
    rules = rules_dir or (root / ".claude" / "rules")
    return {
        "line_count": check_line_count(md),
        "soft_language": check_soft_language(md),
        "stale_paths": [p for p in check_stale_paths(md, root) if not p["exists"]],
        "orphan_rules": [r for r in check_scoped_rules(rules, root) if r["matches"] == 0],
    }


def format_human(report: dict) -> str:
    lc = report["line_count"]
    out = ["CLAUDE.md audit", "=" * 40,
           f"Line count: {lc['lines']} ({lc['status'].upper()}; warn >{WARN_LINES}, alert >{ALERT_LINES})"]
    for key, label in (("soft_language", "SOFT"), ("stale_paths", "STALE"), ("orphan_rules", "ORPHAN")):
        items = report[key]
        out.append(f"{key.replace('_', ' ').capitalize()}: {len(items) or 'clean'}")
        for f in items:
            if key == "soft_language":
                out.append(f"  {label} L{f['line']}: \"{f['text'][:100]}\" (uses '{f['word']}')")
            elif key == "stale_paths":
                out.append(f"  {label} L{f['line']}: `{f['path']}` not found")
            else:
                out.append(f"  {label}: {f['rule']} glob '{f['glob']}' matches 0 files")
    return "\n".join(out)


def has_failures(report: dict) -> bool:
    return (report["line_count"]["status"] == "alert"
            or bool(report["stale_paths"]) or bool(report["orphan_rules"]))


if __name__ == "__main__":
    rep = run_all()
    print(json.dumps(rep, indent=2) if "--json" in sys.argv else format_human(rep))
    sys.exit(1 if "--strict" in sys.argv and has_failures(rep) else 0)
