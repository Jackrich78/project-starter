#!/usr/bin/env python3
"""Create or update the GitHub issue labels the issue flow uses. Idempotent.

Labels and states are described in docs/system/issue-flow.md. State labels
follow Matt Pocock's triage skill (MIT, https://github.com/mattpocock/skills);
priorities and kinds are this template's.

Usage:
  python3 scripts/github/setup_labels.py [--dry-run] [--repo OWNER/REPO] [--prune-defaults]

--prune-defaults deletes GitHub's unused default labels; off by default so an
existing repo's live labels are never removed. Exits non-zero on first failure.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

LABELS = [
    # (name, colour, description)
    ("needs-triage", "fbca04", "Needs a human's evaluation"),
    ("needs-info", "d4c5f9", "Waiting on more information"),
    ("ready-for-agent", "0e8a16", "Fully specified; an agent can pick it up"),
    ("ready-for-human", "1d76db", "Needs a human to act, decide or check live"),
    ("wontfix", "ffffff", "Will not be actioned; closed as not planned"),
    ("P0", "b60205", "Priority 0: drop everything"),
    ("P1", "d93f0b", "Priority 1: next up"),
    ("P2", "fef2c0", "Priority 2: when there is room"),
    ("bug", "d73a4a", "Something is broken"),
    ("enhancement", "a2eeef", "New capability or improvement"),
    ("chore", "c5def5", "Internal tidiness: no user-visible change, no incident behind it"),
    ("feature", "5319e7", "Parent issue holding a feature's spec; never picked up by agents"),
]

# CUSTOMIZE: your areas. Also list them in docs/system/issue-flow.md.
AREA_LABELS: list[tuple[str, str, str]] = [
    # ("area:core", "c2e0c6", "Core product code"),
    # ("area:ops", "c2e0c6", "CI, deploys, scheduled jobs"),
]

# GitHub's defaults. `wontfix` is kept: the flow uses it.
DEFAULTS_TO_DELETE = ["documentation", "duplicate", "good first issue", "help wanted", "invalid", "question"]


def _gh(args: list[str], repo: str | None) -> subprocess.CompletedProcess:
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo]
    return subprocess.run(cmd, capture_output=True, text=True)


def _existing(repo: str | None) -> set[str]:
    r = _gh(["label", "list", "--limit", "200", "--json", "name", "--jq", ".[].name"], repo)
    if r.returncode:
        print(f"FAILED listing labels: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return set(r.stdout.split("\n")) - {""}


def _repo_from_origin() -> str | None:
    """OWNER/REPO of this checkout's origin, so gh never acts on whatever repo the caller's cwd resolves to."""
    root = Path(__file__).resolve().parents[2]
    r = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"], capture_output=True, text=True)
    m = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?/?$", r.stdout.strip()) if r.returncode == 0 else None
    return m.group(1) if m else None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--repo", metavar="OWNER/REPO", help="target repo (default: this checkout's origin)")
    ap.add_argument("--prune-defaults", action="store_true")
    a = ap.parse_args(argv)
    dry, prune = a.dry_run, a.prune_defaults
    repo = a.repo or _repo_from_origin()
    if not repo:
        print("cannot determine the target repo: pass --repo OWNER/REPO", file=sys.stderr)
        return 2
    print(f"repo: {repo}")
    labels = LABELS + AREA_LABELS

    if dry:
        have = _existing(repo)
        create = [n for n, _, _ in labels if n not in have]
        update = [n for n, _, _ in labels if n in have]
        for n in create:
            print(f"create {n}")
        for n in update:
            print(f"update {n}")
        deletes = [n for n in DEFAULTS_TO_DELETE if n in have] if prune else []
        for n in deletes:
            print(f"delete {n}")
        # Dry run never deletes; the count is reported for the opt-in path.
        print(f"{len(create)} to create, {len(update)} to update, {len(deletes)} to delete")
        return 0

    for name, colour, desc in labels:
        r = _gh(["label", "create", name, "--color", colour, "--description", desc, "--force"], repo)
        if r.returncode:
            print(f"FAILED {name}: {r.stderr.strip()}", file=sys.stderr)
            return 1
        print(f"ok {name}")
    if prune:
        for name in DEFAULTS_TO_DELETE:
            r = _gh(["label", "delete", name, "--yes"], repo)
            if r.returncode == 0:
                print(f"deleted {name}")
            elif "not found" in r.stderr.lower():
                print(f"ok {name} (absent)")
            else:
                print(f"FAILED delete {name}: {r.stderr.strip()}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
