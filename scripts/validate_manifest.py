#!/usr/bin/env python3
"""
Bidirectional manifest consistency check.

Verifies that:
  1. Every agent file with `template-owned: true` in its frontmatter
     appears in .claude/agents/.template-manifest  (flag → manifest)
  2. Every entry in .template-manifest resolves to an existing agent file
     (manifest → file)

Exit codes:
  0 — all checks pass
  1 — one or more checks fail (details printed to stdout)

Usage:
  python scripts/validate_manifest.py
  python scripts/validate_manifest.py --agents-dir /path/to/.claude/agents
"""

import argparse
import re
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--agents-dir",
        default=None,
        help="Path to the .claude/agents/ directory (default: auto-detected relative to this script)",
    )
    return p.parse_args()


def find_agents_dir(script_path: Path) -> Path:
    """Locate .claude/agents/ relative to the repo root (two levels up from scripts/)."""
    repo_root = script_path.parent.parent
    return repo_root / ".claude" / "agents"


def load_manifest(agents_dir: Path) -> tuple[set[str], bool]:
    """Parse .template-manifest; return (set of filenames, version_header_found)."""
    manifest_path = agents_dir / ".template-manifest"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}")
        sys.exit(1)

    filenames: set[str] = set()
    version_found = False
    for raw_line in manifest_path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if "template-version:" in line:
                version_found = True
            continue
        filenames.add(line)
    return filenames, version_found


def find_template_owned_agents(agents_dir: Path) -> set[str]:
    """Return filenames of all .md files (excluding TEMPLATE.md and README.md)
    that contain `template-owned: true` in their YAML frontmatter."""
    owned: set[str] = set()
    for md_file in sorted(agents_dir.glob("*.md")):
        if md_file.name in ("TEMPLATE.md", "README.md"):
            continue
        text = md_file.read_text()
        # frontmatter is between the first two `---` fences
        if re.search(r"^template-owned:\s*true\s*$", text, re.MULTILINE):
            owned.add(md_file.name)
    return owned


def main() -> int:
    args = parse_args()
    script_path = Path(__file__).resolve()

    agents_dir = Path(args.agents_dir).resolve() if args.agents_dir else find_agents_dir(script_path)

    if not agents_dir.is_dir():
        print(f"ERROR: agents directory not found: {agents_dir}")
        return 1

    manifest_entries, version_found = load_manifest(agents_dir)
    template_owned = find_template_owned_agents(agents_dir)

    errors: list[str] = []

    # Check 1 — version header present
    if not version_found:
        errors.append(
            "MANIFEST MISSING VERSION: .template-manifest must contain a "
            "'# template-version: X.Y.Z' header line."
        )

    # Check 2 — flag → manifest (every template-owned agent must be in the manifest)
    flagged_not_listed = template_owned - manifest_entries
    for name in sorted(flagged_not_listed):
        errors.append(
            f"FLAGGED BUT NOT LISTED: '{name}' has `template-owned: true` "
            f"but is absent from .template-manifest — it will NOT be synced downstream."
        )

    # Check 3 — manifest → file (every manifest entry must exist)
    for entry in sorted(manifest_entries):
        target = agents_dir / entry
        if not target.exists():
            errors.append(
                f"LISTED BUT MISSING: '{entry}' is in .template-manifest "
                f"but the file does not exist at {target}"
            )

    if errors:
        print("validate_manifest: FAILED\n")
        for err in errors:
            print(f"  {err}")
        print(f"\n{len(errors)} error(s) found.")
        return 1

    flagged_count = len(template_owned)
    manifest_count = len(manifest_entries)
    print(
        f"validate_manifest: OK — {flagged_count} template-owned agent(s) all "
        f"present in manifest ({manifest_count} entries total)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
