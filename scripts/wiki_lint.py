#!/usr/bin/env python3
"""Deterministic wiki lint for docs/ and .claude/skills/*/SKILL.md.

Contract: .claude/rules/wiki.md; schema: docs/guides/knowledge-architecture.md.

Errors (exit 1): missing/unparseable frontmatter, missing or unknown `type`,
unknown `decay_tier`, over-cap page with no `# SPLIT-DEFERRED <reason>` line,
`supersedes` target that does not exist.
Warnings (exit 0): broken local .md links, page not linked from docs/index.md,
stale page (`stale_after`, or `decay_tier` interval from the later of
frontmatter `updated` and the file's last git commit), SPLIT-DEFERRED over-cap.
`--strict` promotes warnings to errors.

Usage:
    python3 scripts/wiki_lint.py --all [--json] [--strict]
    python3 scripts/wiki_lint.py --path docs/guides [--path FILE ...]

Output: `path:line LEVEL message`, then `wiki_lint: E errors, W warnings over N files`.
SPLIT-DEFERRED over-cap pages collapse to one count line in text mode; `--strict`
and `--json` keep the per-file entries.
Exit: 0 clean/warnings only, 1 errors, 2 bad usage or missing pyyaml.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # degrade with a clear message, never a traceback
    yaml = None

SIZE_CAP = 300
SPLIT_MARKER = "# SPLIT-DEFERRED"
ALLOWED_TYPES = frozenset({
    "domain-doc", "guide", "reference", "decision-record", "overview",
    "template", "skill", "research", "qa-report",
})
# days until a page of this tier is due for a re-read
DECAY_INTERVALS = {"reference": 365, "process": 182, "active": 91, "figures": 30}
RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)[^)]*\)")
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def split_frontmatter(text: str):
    """Return (data, error, body_offset_lines). error in {None,'missing','unparseable'}."""
    if not text.startswith("---\n"):
        return None, "missing", 0
    end = text.find("\n---", 4)
    if end < 0:
        return None, "missing", 0
    block = text[4:end]
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError:
        return None, "unparseable", 0
    if not isinstance(data, dict):
        return None, "unparseable", 0
    return data, None, block.count("\n") + 2


def as_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def git_date(root: Path, f: Path) -> date | None:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(f)],
                             cwd=root, capture_output=True, text=True, timeout=10)
        return datetime.fromisoformat(out.stdout.strip()).date() if out.returncode == 0 and out.stdout.strip() else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def key_line(text: str, key: str) -> int:
    for i, line in enumerate(text.splitlines(), 1):
        if i > 1 and line.startswith("---"):
            break
        if line.startswith(key + ":"):
            return i
    return 1


def local_links(text: str):
    """Yield (line, target) for local .md links outside code fences/spans."""
    in_fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in LINK_RE.finditer(INLINE_CODE_RE.sub("", line)):
            t = m.group(1).strip("<>")
            if t.startswith(("http://", "https://", "#", "mailto:")):
                continue
            t = unquote(t.split("#", 1)[0])
            if t.endswith(".md"):
                yield n, t


def supersedes_ok(root: Path, f: Path, target: str) -> bool:
    head = target.split("§", 1)[0].split(",", 1)[0].strip()
    return bool(head) and any(p.exists() for p in (f.parent / head, root / head, f.parent / "archive" / head))


def lint_file(root: Path, f: Path, indexed: set[Path] | None, today: date) -> list[tuple[int, str, str]]:
    """Findings for one file as (line, level, message)."""
    out: list[tuple[int, str, str]] = []
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    reserved = f.name in RESERVED
    data = None

    if not reserved:
        data, err, _ = split_frontmatter(text)
        if err:
            out.append((1, "ERROR", f"{err} frontmatter"))
        else:
            t = data.get("type")
            if not isinstance(t, str) or not t.strip():
                out.append((1, "ERROR", "missing 'type' in frontmatter"))
            elif t.strip() not in ALLOWED_TYPES:
                out.append((key_line(text, "type"), "ERROR",
                            f"unknown type '{t}' (allowed: {', '.join(sorted(ALLOWED_TYPES))})"))
            tier = data.get("decay_tier")
            if tier is not None and tier not in DECAY_INTERVALS:
                out.append((key_line(text, "decay_tier"), "ERROR",
                            f"unknown decay_tier '{tier}' (allowed: {', '.join(DECAY_INTERVALS)})"))
            sup = data.get("supersedes")
            for s in ([sup] if isinstance(sup, str) else sup if isinstance(sup, list) else []):
                if not isinstance(s, str) or not supersedes_ok(root, f, s):
                    out.append((key_line(text, "supersedes"), "ERROR", f"supersedes target not found: {s!r}"))
            if sup is not None and not isinstance(sup, (str, list)):
                out.append((key_line(text, "supersedes"), "ERROR", "supersedes must be a path or list of paths"))

        if len(lines) > SIZE_CAP:
            if any(ln.strip().startswith(SPLIT_MARKER) for ln in lines):
                out.append((SIZE_CAP + 1, "WARNING", f"{len(lines)} lines, over the {SIZE_CAP}-line cap (SPLIT-DEFERRED)"))
            else:
                out.append((SIZE_CAP + 1, "ERROR", f"{len(lines)} lines, over the {SIZE_CAP}-line cap; split it or add '{SPLIT_MARKER} <reason>'"))

        if isinstance(data, dict):
            out.extend(stale(root, f, data, today))

    for n, t in local_links(text):
        if not (f.parent / t).exists():
            out.append((n, "WARNING", f"broken link: {t}"))

    if indexed is not None and not reserved and f.resolve() not in indexed:
        out.append((1, "WARNING", "not indexed: add a line to docs/index.md"))
    return out


def stale(root: Path, f: Path, data: dict, today: date) -> list[tuple[int, str, str]]:
    sa = as_date(data.get("stale_after"))
    if sa is not None:
        return [(key_line(f.read_text(encoding="utf-8"), "stale_after"), "WARNING", f"stale: stale_after {sa} has passed")] if sa < today else []
    tier = data.get("decay_tier")
    if tier not in DECAY_INTERVALS:
        return []
    touched = [d for d in (as_date(data.get("updated")), git_date(root, f)) if d]
    if not touched:
        return []
    due = max(touched) + timedelta(days=DECAY_INTERVALS[tier])
    return [(1, "WARNING", f"stale: decay_tier '{tier}' last touched {max(touched)}, due {due}")] if due < today else []


def is_archived(root: Path, f: Path) -> bool:
    try:
        return "archive" in f.resolve().relative_to(root.resolve()).parts[:-1]
    except ValueError:
        return "archive" in f.parts[:-1]


def gather(root: Path, paths: list[Path] | None) -> list[Path] | None:
    if paths is None:
        found = sorted((root / "docs").rglob("*.md")) + sorted((root / ".claude" / "skills").glob("*/SKILL.md"))
    else:
        found = []
        for p in paths:
            if p.is_file():
                found.append(p)  # a named file is always scanned
            elif p.is_dir():
                found += sorted(p.rglob("*.md"))
            else:
                print(f"error: path not found: {p}", file=sys.stderr)
                return None
        found = [f for f in found if f.is_file() and (f in paths or not is_archived(root, f))]
        return found
    return [f for f in found if not is_archived(root, f)]


def index_targets(root: Path) -> set[Path] | None:
    idx = root / "docs" / "index.md"
    if not idx.exists():
        return None
    return {(idx.parent / t).resolve() for _, t in local_links(idx.read_text(encoding="utf-8"))}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic wiki lint.")
    ap.add_argument("--all", action="store_true", help="scan docs/**/*.md and .claude/skills/*/SKILL.md (default)")
    ap.add_argument("--path", type=Path, action="append", help="file or directory to scan (repeatable)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="warnings become errors")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                    help="repo root (default: parent of scripts/)")
    args = ap.parse_args(argv)
    if yaml is None:
        print("wiki_lint: pyyaml is required. Install it: python3 -m pip install pyyaml", file=sys.stderr)
        return 2
    root = args.root.resolve()
    files = gather(root, args.path)
    if files is None:
        return 2

    docs_dir = (root / "docs").resolve()
    indexed = index_targets(root)
    today = date.today()
    findings = []
    for f in files:
        under_docs = docs_dir in f.resolve().parents
        idx = indexed if under_docs else None
        for line, level, msg in lint_file(root, f, idx, today):
            if args.strict and level == "WARNING":
                level = "ERROR"
            try:
                shown = str(f.resolve().relative_to(root))
            except ValueError:
                shown = str(f)
            findings.append({"path": shown, "line": line, "level": level, "message": msg})

    errors = sum(1 for x in findings if x["level"] == "ERROR")
    warnings = len(findings) - errors
    summary = f"wiki_lint: {errors} errors, {warnings} warnings over {len(files)} files"
    if args.json:
        print(json.dumps({"summary": summary, "errors": errors, "warnings": warnings,
                          "files": len(files), "findings": findings}, indent=2))
    else:
        # SPLIT-DEFERRED is acknowledged debt: one count per run, per-file only under --strict or --json.
        deferred = [x for x in findings if x["level"] == "WARNING" and "(SPLIT-DEFERRED)" in x["message"]]
        for x in findings:
            if x not in deferred:
                print(f"{x['path']}:{x['line']} {x['level']} {x['message']}")
        if deferred:
            print(f"{len(deferred)} page(s) over the {SIZE_CAP}-line cap with SPLIT-DEFERRED (run with --strict to list them)")
        print(summary)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
