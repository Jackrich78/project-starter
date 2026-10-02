"""Schema validator for `.claude/agent-memory/<agent>/MEMORY.md` files.

Layout: one subdirectory per agent under the memory dir, each holding a
`MEMORY.md` (glob `<memory-dir>/*/MEMORY.md`).

Entry format: `- YYYY-MM-DD · <method> · source: <src>` where `<src>` is one of:
    file:line     a path with a line number, e.g. `scripts/x.py:35`
    commit:SHA    `commit:` followed by 7-40 hex chars
    http(s)://... a URL
    session:<id>  `session:` followed by an id

Allowed besides entries: blank lines, `#` headings, HTML comments (single or
multi-line). Any other line (a prose paragraph, a non-entry bullet) is an
error: memory holds methods as one-line entries, nothing else.

LINE_CAP = 150 is a HARD error. Every error names `path:line`.

--check-roster also requires every `.claude/agents/*.md` (except TEMPLATE.md
and README.md) to have a memory dir with a MEMORY.md, and every memory dir to
have an agent file.

Exit codes:
    0  every file passed
    1  at least one file failed
    2  usage error (missing dir, or --agent matches no memory file)

CLI:
    python3 scripts/validate_agent_memory.py
    python3 scripts/validate_agent_memory.py --agent tdd-test-writer
    python3 scripts/validate_agent_memory.py --memory-dir /tmp/mem
    python3 scripts/validate_agent_memory.py --check-roster [--agents-dir DIR]
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MEMORY_DIR = REPO_ROOT / ".claude" / "agent-memory"
DEFAULT_AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
NON_AGENT_FILES = {"TEMPLATE.md", "README.md"}

LINE_CAP = 150

ENTRY_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) · .+ · source: (.+)$")

SOURCE_RES = [
    re.compile(r"^[\w\-./]+:\d+(?:-\d+)?$"),
    re.compile(r"^commit:[0-9a-f]{7,40}$"),
    re.compile(r"^https?://\S+$"),
    re.compile(r"^session:\S+$"),
]


def _is_valid_source(source: str) -> bool:
    return any(rx.match(source.strip()) for rx in SOURCE_RES)


def _is_real_date(value: str) -> bool:
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_one(path: Path) -> list[str]:
    """Validate one memory file. Returns error strings (empty = pass)."""
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    if len(lines) > LINE_CAP:
        errors.append(
            f"{path}:{LINE_CAP + 1}: file is {len(lines)} lines, "
            f"over the {LINE_CAP}-line cap"
        )

    in_comment = False
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()

        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped:
                in_comment = True
            continue
        if not stripped or stripped.startswith("#"):
            continue

        if not stripped.startswith("- "):
            errors.append(
                f"{path}:{idx}: not an entry (prose is not allowed) — got: {stripped[:80]!r}"
            )
            continue

        m = ENTRY_RE.match(stripped)
        if not m:
            if "source:" not in stripped:
                errors.append(
                    f"{path}:{idx}: entry missing ' · source: <src>' — got: {stripped[:80]!r}"
                )
            else:
                errors.append(
                    f"{path}:{idx}: entry does not match "
                    f"'- YYYY-MM-DD · <method> · source: <src>' — got: {stripped[:80]!r}"
                )
            continue

        if not _is_real_date(m.group(1)):
            errors.append(f"{path}:{idx}: invalid date {m.group(1)!r}")
        if not _is_valid_source(m.group(2)):
            errors.append(
                f"{path}:{idx}: unknown source kind {m.group(2)!r} "
                f"(need file:line, commit:SHA, http(s):// URL, or session:<id>)"
            )

    return errors


def check_roster(agents_dir: Path, memory_dir: Path) -> list[str]:
    """Agents and memory dirs must pair up one-to-one."""
    errors: list[str] = []
    agents = {
        f.stem for f in agents_dir.glob("*.md") if f.name not in NON_AGENT_FILES
    }
    mems = {d.name for d in memory_dir.iterdir() if d.is_dir()}
    for name in sorted(agents - mems):
        errors.append(f"{memory_dir / name}: missing memory dir for agent '{name}'")
    for name in sorted(mems - agents):
        errors.append(f"{memory_dir / name}: memory dir has no agent file '{name}.md'")
    for name in sorted(agents & mems):
        if not (memory_dir / name / "MEMORY.md").is_file():
            errors.append(f"{memory_dir / name}: missing MEMORY.md")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--agent", help="validate one agent by directory name")
    parser.add_argument("--memory-dir", type=Path, default=DEFAULT_MEMORY_DIR)
    parser.add_argument("--agents-dir", type=Path, default=DEFAULT_AGENTS_DIR)
    parser.add_argument("--check-roster", action="store_true",
                        help="require agent files and memory dirs to match 1:1")
    args = parser.parse_args(argv)

    mem_dir = args.memory_dir
    if not mem_dir.is_dir():
        print(f"error: memory dir not found: {mem_dir}", file=sys.stderr)
        return 2
    if args.check_roster and not args.agents_dir.is_dir():
        print(f"error: agents dir not found: {args.agents_dir}", file=sys.stderr)
        return 2

    files = sorted(mem_dir.glob("*/MEMORY.md"))
    if args.agent:
        files = [f for f in files if f.parent.name == args.agent]
        if not files:
            print(f"error: no MEMORY.md for agent '{args.agent}' in {mem_dir}", file=sys.stderr)
            return 2

    errors: list[str] = []
    for f in files:
        errors.extend(validate_one(f))
    if args.check_roster:
        errors.extend(check_roster(args.agents_dir, mem_dir))

    if errors:
        for err in errors:
            print(err)
        print(f"\n{len(errors)} error(s) across {len(files)} memory file(s)", file=sys.stderr)
        return 1

    print(f"OK — {len(files)} memory file(s) validated, no errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
