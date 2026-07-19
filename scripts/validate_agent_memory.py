"""Schema validator for memory/agents/{name}.md files.

Enforces the canonical schema (see memory/agents/TEMPLATE.md):

- Exactly 3 H2 sections allowed: `## Patterns`, `## Incidents`, `## Task Outcomes`.
- No other top-level (H1/H2) headings beyond the title H1 and these three H2s.
- Each H2 may be empty (passes) or contain one or more entries.
- Each entry MUST:
    - Start with `- [YYYY-MM-DD] `
    - End with a citation matching one of four patterns:
        agent.db:event_id=N
        commit:SHA       (>=7 hex chars)
        file.md:LINE     (relative path + line number)
        qa:report#section
- File size <=100 lines (excess triggers pruning, not validator failure — but warned).

Exit code:
- 0 if every file passes (or warnings only)
- 1 if any file fails schema
- 2 if the memory directory is not found or agent filter yields no match

CLI:
    python scripts/validate_agent_memory.py
    python scripts/validate_agent_memory.py --agent tdd-test-writer
    python scripts/validate_agent_memory.py --memory-dir /tmp/test-memory   # for tests
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY_AGENTS_DIR = REPO_ROOT / "memory" / "agents"

ALLOWED_SECTIONS = ("Patterns", "Incidents", "Task Outcomes")
LINE_CAP_WARNING = 100

ENTRY_DATE_RE = re.compile(r"^\s*- \[(\d{4}-\d{2}-\d{2})\] ")
# Citation patterns — accept any of the 4 formats.
CITATION_RES = [
    re.compile(r"agent\.db:event_id=\d+"),
    re.compile(r"commit:[0-9a-f]{7,40}\b"),
    re.compile(r"[\w\-./]+\.md:\d+"),
    re.compile(r"qa:[\w\-./]+#\S+"),
]


def validate_one(path: Path) -> list[str]:
    """Validate one memory file. Returns list of error strings (empty = pass)."""
    errors: list[str] = []
    if not path.exists():
        return [f"{path.name}: file not found"]

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if len(lines) > LINE_CAP_WARNING:
        errors.append(
            f"{path.name}: WARN — file is {len(lines)} lines (cap {LINE_CAP_WARNING}); "
            f"run scripts/prune_agent_memory.py"
        )

    # Find H1 and H2 headings (ignore lines inside HTML comments / fenced blocks).
    in_comment = False
    in_code = False
    h1_count = 0
    h2_sections: list[tuple[str, int]] = []  # (heading text, line number)
    for idx, line in enumerate(lines, 1):
        stripped = line.rstrip()
        if "<!--" in stripped and "-->" not in stripped:
            in_comment = True
            continue
        if "-->" in stripped:
            in_comment = False
            continue
        if in_comment:
            continue
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("# "):
            h1_count += 1
        elif stripped.startswith("## "):
            heading = stripped[3:].strip()
            h2_sections.append((heading, idx))

    if h1_count != 1:
        errors.append(f"{path.name}: must have exactly 1 H1 title (found {h1_count})")

    seen_allowed: set[str] = set()
    for heading, line_n in h2_sections:
        if heading not in ALLOWED_SECTIONS:
            errors.append(
                f"{path.name}:{line_n}: forbidden H2 '{heading}' "
                f"(allowed: {', '.join(ALLOWED_SECTIONS)})"
            )
        elif heading in seen_allowed:
            errors.append(f"{path.name}:{line_n}: duplicate H2 '{heading}'")
        else:
            seen_allowed.add(heading)

    # Validate entries inside the 3 sections.
    section_ranges: list[tuple[str, int, int]] = []
    for i, (heading, line_n) in enumerate(h2_sections):
        end_line = h2_sections[i + 1][1] - 1 if i + 1 < len(h2_sections) else len(lines)
        section_ranges.append((heading, line_n, end_line))

    in_comment = False
    in_code = False
    for heading, start, end in section_ranges:
        if heading not in ALLOWED_SECTIONS:
            continue
        for idx in range(start, end):
            if idx >= len(lines):
                break
            line = lines[idx]
            stripped = line.strip()
            # Track comment / code state.
            if "<!--" in line and "-->" not in line:
                in_comment = True
                continue
            if "-->" in line:
                in_comment = False
                continue
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_comment or in_code:
                continue
            if not stripped:
                continue
            # Section heading line itself — skip.
            if stripped.startswith("## "):
                continue
            # Entry line — must start with `- [YYYY-MM-DD]`.
            if stripped.startswith("- "):
                if not ENTRY_DATE_RE.match(line):
                    errors.append(
                        f"{path.name}:{idx + 1}: entry must start with `- [YYYY-MM-DD] ` — got: {stripped[:60]!r}"
                    )
                    continue
                # Collect the entry body (this line + any indented continuation lines).
                body_lines = [line]
                j = idx + 1
                while j < end:
                    nxt = lines[j]
                    if not nxt.strip():
                        break
                    if nxt.lstrip().startswith("- ") or nxt.lstrip().startswith("## "):
                        break
                    body_lines.append(nxt)
                    j += 1
                body = "\n".join(body_lines)
                if not any(rx.search(body) for rx in CITATION_RES):
                    errors.append(
                        f"{path.name}:{idx + 1}: entry missing citation "
                        f"(need one of: agent.db:event_id=N, commit:SHA, file.md:LINE, qa:report#section)"
                    )
            # Anything else inside a valid section is fine (prose / continuation handled above).

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", help="Validate one agent by name (e.g. tdd-test-writer)")
    parser.add_argument("--memory-dir", type=Path, default=MEMORY_AGENTS_DIR)
    args = parser.parse_args()

    mem_dir = args.memory_dir
    if not mem_dir.is_dir():
        print(f"error: memory dir not found: {mem_dir}", file=sys.stderr)
        return 2

    files = sorted(f for f in mem_dir.glob("*.md") if f.name not in ("README.md", "TEMPLATE.md"))
    if args.agent:
        files = [f for f in files if f.stem == args.agent]
        if not files:
            print(f"error: no memory file for agent '{args.agent}' in {mem_dir}", file=sys.stderr)
            return 2

    if not files:
        print("OK — 0 memory file(s) validated, no errors")
        return 0

    all_errors: list[str] = []
    for f in files:
        all_errors.extend(validate_one(f))

    if all_errors:
        warnings_only = all(" WARN " in e for e in all_errors)
        for err in all_errors:
            print(err)
        if warnings_only:
            print(f"\n{len(all_errors)} warning(s) across {len(files)} file(s) — no schema errors")
            return 0
        errors = [e for e in all_errors if " WARN " not in e]
        print(f"\n{len(errors)} error(s) across {len(files)} file(s)", file=sys.stderr)
        return 1

    print(f"OK — {len(files)} memory file(s) validated, no errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
