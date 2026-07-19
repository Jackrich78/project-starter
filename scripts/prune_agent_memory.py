"""Apply an Agile Coach pruning manifest to memory/agents/*.md files.

Consumes the canonical pruning-manifest markdown emitted by the Agile Coach
(see `.claude/agents/agile-coach.md` § Output Format). The manifest is a
markdown doc with `### memory/agents/{name}.md` subsections; each subsection
lists bullets tagged `[PRUNE]` or `[KEEP]`.

DEFAULT behaviour is **dry-run**: parse the manifest, show what would change,
write NOTHING. The `--apply` flag is required to make any file modifications.

Auto-apply rule: an entry tagged `[PRUNE]` whose `Last updated:` is >50 days
old AND whose reason mentions codification (contains "codified", "no longer",
or "redundant") MAY be auto-applied — but ONLY when `--apply` is also passed.
Without `--apply`, even auto-eligible entries are shown as [AUTO] but never
written. This guarantees `--dry-run` (the default) mutates nothing.

`--apply` is idempotent: re-running on the same manifest after a previous
apply is a no-op (snippets already removed are reported as "already pruned").

Usage:
    # Preview only — no files are touched (default):
    python scripts/prune_agent_memory.py docs/qa/pruning-FEAT-XXX.md
    python scripts/prune_agent_memory.py docs/qa/pruning-FEAT-XXX.md --dry-run

    # Apply the manifest:
    python scripts/prune_agent_memory.py docs/qa/pruning-FEAT-XXX.md --apply

Manifest format (excerpt):

    ## Pruning Recommendations for FEAT-XXX

    ### memory/agents/librarian.md

    - [PRUNE] Line 5: "Cross-ref updates often stale on renamed fields"
      Reason: Now codified in librarian.md § Core Responsibilities #2
      Last updated: 2026-04-20

    - [KEEP] Line 8: "Frontmatter `updated` field sometimes out of sync"
      Reason: Not yet codified
      Last updated: 2026-05-11

`Line N: "..."` uses the quoted substring as the search pattern. When a snippet
matches exactly one bullet it is removed; when it matches several, the advisory
`Line N:` (1-based) is used to disambiguate, and if that still does not resolve
to a single bullet the entry is reported `[SKIP-AMBIGUOUS]` and left untouched —
the pruner never guesses which of several colliding bullets to delete. The
dry-run preview echoes the actual matched bullet (not the manifest text) so a
reviewer can see exactly which line an `--apply` would remove.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEMORY_AGENTS_DIR = REPO_ROOT / "memory" / "agents"

# Number of days an entry must be older than to qualify for auto-apply.
AUTO_APPLY_AGE_DAYS = 50

# Section heading pattern in the manifest, e.g. "### memory/agents/librarian.md"
SECTION_RE = re.compile(r"^### (memory/agents/[\w\-./]+\.md)\s*$")
ENTRY_LINE_RE = re.compile(r"^\s*-\s*\[(PRUNE|KEEP)\]\s+Line\s+(\d+):\s+\"(.+?)\"\s*$")
LAST_UPDATED_RE = re.compile(r"Last updated:\s*(\d{4}-\d{2}-\d{2})")


def parse_manifest(manifest_text: str) -> dict[str, list[dict]]:
    """Parse the manifest text -> {memory_file_path: [{tag, snippet, last_updated, reason}, ...]}."""
    result: dict[str, list[dict]] = {}
    current_file: str | None = None
    current_entry: dict | None = None
    for line in manifest_text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            current_file = m.group(1)
            result.setdefault(current_file, [])
            current_entry = None
            continue
        m = ENTRY_LINE_RE.match(line)
        if m and current_file:
            current_entry = {
                "tag": m.group(1),
                "line_hint": int(m.group(2)),
                "snippet": m.group(3),
                "last_updated": None,
                "reason": None,
            }
            result[current_file].append(current_entry)
            continue
        if current_entry is not None:
            mu = LAST_UPDATED_RE.search(line)
            if mu:
                current_entry["last_updated"] = mu.group(1)
                continue
            if line.strip().lower().startswith("reason:"):
                current_entry["reason"] = line.split(":", 1)[1].strip()
    return result


def is_auto_eligible(entry: dict, today: datetime) -> bool:
    """Return True if the entry meets the auto-apply age + codification criteria.

    Eligibility does NOT imply the entry will be applied — writes only happen
    under `--apply`. This function only classifies the entry as [AUTO] vs [DRY].
    """
    if entry["tag"] != "PRUNE":
        return False
    if not entry["last_updated"]:
        return False
    try:
        dt = datetime.strptime(entry["last_updated"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    if (today - dt).days < AUTO_APPLY_AGE_DAYS:
        return False
    reason = (entry["reason"] or "").lower()
    return "codified" in reason or "no longer" in reason or "redundant" in reason


def find_bullet_matches(file_text: str, snippet: str) -> list[tuple[int, str]]:
    """Return [(line_index, line_text), ...] for every bullet line containing the snippet.

    Read-only: used by both the dry-run preview and the apply path so the two
    agree on exactly which bullet(s) a snippet resolves to.
    """
    matches: list[tuple[int, str]] = []
    for idx, line in enumerate(file_text.splitlines()):
        if snippet in line and line.lstrip().startswith("- "):
            matches.append((idx, line))
    return matches


def resolve_target_index(
    matches: list[tuple[int, str]], line_hint: int | None
) -> tuple[int | None, str]:
    """Pick the single bullet to remove from candidate matches.

    Returns (line_index, status). status is one of: "ok", "not_found", "ambiguous".
    A non-unique snippet is disambiguated by the manifest's advisory `Line N:`
    (1-based) ONLY when it resolves to exactly one candidate; otherwise we refuse
    to guess and report "ambiguous" rather than risk deleting the wrong entry.
    """
    if not matches:
        return None, "not_found"
    if len(matches) == 1:
        return matches[0][0], "ok"
    if line_hint is not None:
        hinted = [idx for idx, _ in matches if idx + 1 == line_hint]
        if len(hinted) == 1:
            return hinted[0], "ok"
    return None, "ambiguous"


def remove_bullet_at(file_text: str, target_index: int) -> str:
    """Remove the bullet at target_index plus its continuation lines.

    Continuation lines are indented lines that follow the bullet and end at the
    next `- `, heading, or blank line.
    """
    lines = file_text.splitlines()
    new_lines: list[str] = []
    i = 0
    while i < len(lines):
        if i == target_index:
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    break
                if nxt.lstrip().startswith(("- ", "## ", "### ", "# ")):
                    break
                i += 1
            continue
        new_lines.append(lines[i])
        i += 1
    return "\n".join(new_lines) + ("\n" if file_text.endswith("\n") else "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to the pruning manifest markdown")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply the pruning and write modified files (required for any write).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicit alias for the default dry-run mode (no writes). This is the default.",
    )
    parser.add_argument("--memory-dir", type=Path, default=MEMORY_AGENTS_DIR)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repo root for resolving 'memory/agents/...' paths in manifest",
    )
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"error: manifest not found: {args.manifest}", file=sys.stderr)
        return 2

    # --dry-run and --apply are mutually exclusive; --dry-run wins if both set.
    write_enabled = args.apply and not args.dry_run

    today = datetime.now(timezone.utc)
    manifest = parse_manifest(args.manifest.read_text(encoding="utf-8"))
    if not manifest:
        print("warning: no actionable sections parsed from manifest", file=sys.stderr)
        return 0

    summary = {"prune": 0, "keep": 0, "applied": 0, "auto_applied": 0, "skipped": 0, "ambiguous": 0}
    for rel_path, entries in manifest.items():
        target = args.repo_root / rel_path
        if not target.exists():
            print(f"warn: {rel_path} not found — skipping {len(entries)} entries")
            summary["skipped"] += len(entries)
            continue
        text = target.read_text(encoding="utf-8")
        original = text
        for entry in entries:
            if entry["tag"] == "KEEP":
                summary["keep"] += 1
                print(f"  [KEEP] {rel_path}: {entry['snippet'][:80]}")
                continue
            summary["prune"] += 1
            auto = is_auto_eligible(entry, today)
            if write_enabled:
                tag = "AUTO" if auto else "APPLY"
            else:
                tag = "AUTO" if auto else "DRY"
            # Resolve the snippet to a single bullet against the CURRENT text (which
            # reflects earlier removals this run) so the preview and the apply agree.
            matches = find_bullet_matches(text, entry["snippet"])
            target_index, status = resolve_target_index(matches, entry.get("line_hint"))
            if status == "ok":
                # Echo the ACTUAL matched bullet, not the manifest text, so a reviewer
                # reading a dry-run can see precisely which line will be removed.
                matched_line = dict(matches)[target_index].strip()
                print(f"  [{tag}] {rel_path}: {matched_line[:80]}")
            elif status == "ambiguous":
                summary["ambiguous"] += 1
                print(
                    f"  [SKIP-AMBIGUOUS] {rel_path}: snippet \"{entry['snippet'][:60]}\" "
                    f"matches {len(matches)} bullets and Line {entry.get('line_hint')} "
                    f"did not disambiguate — refusing to guess (no removal)"
                )
                continue
            else:  # not_found
                print(f"  [{tag}] {rel_path}: {entry['snippet'][:80]}")
                if write_enabled:
                    print("    note: snippet not found in current file (already pruned?)")
                continue
            # CRITICAL: only mutate `text` when write_enabled is True.
            if write_enabled and target_index is not None:
                text = remove_bullet_at(text, target_index)
                if auto:
                    summary["auto_applied"] += 1
                else:
                    summary["applied"] += 1

        # Only write to disk when write_enabled AND the text actually changed.
        if write_enabled and text != original:
            target.write_text(text, encoding="utf-8")

    print()
    print(
        f"Prune: {summary['prune']} | Keep: {summary['keep']} | "
        f"Applied: {summary['applied']} | Auto-applied: {summary['auto_applied']} | "
        f"Skipped: {summary['skipped']} | Ambiguous: {summary['ambiguous']}"
    )
    if not write_enabled:
        print("\n(dry-run — re-run with --apply to commit the prunes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
