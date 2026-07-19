#!/usr/bin/env python3
"""
PreCompact Hook — Session State Snapshot

Saves minimal session state before context compaction.
CLAUDE.md is re-read after compaction, so any recovery instruction
there can point Claude to this file.

Reads the standard Claude Code hook payload from stdin.
Always exits 0 — never blocks compaction.
"""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone


def find_project_root():
    """Find project root by looking for CLAUDE.md."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_git_state():
    """Get current branch, dirty file count, and last commit."""
    result = {"branch": "unknown", "dirty_count": 0, "last_commit": ""}
    try:
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=2
        )
        if branch.returncode == 0:
            result["branch"] = branch.stdout.strip()

        status = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, timeout=2
        )
        if status.returncode == 0 and status.stdout.strip():
            result["dirty_count"] = len(status.stdout.strip().splitlines())

        log = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True, text=True, timeout=2
        )
        if log.returncode == 0:
            result["last_commit"] = log.stdout.strip()
    except Exception:
        pass
    return result


def scan_features(project_root):
    """List FEAT-XXX directories and whether they have prd.md / plan.md."""
    features_dir = project_root / "docs" / "features"
    if not features_dir.exists():
        return []

    features = []
    for feat_dir in sorted(features_dir.iterdir()):
        if feat_dir.is_dir() and feat_dir.name.startswith("FEAT-"):
            has_prd = (feat_dir / "prd.md").exists()
            has_plan = (feat_dir / "plan.md").exists()
            features.append({
                "id": feat_dir.name,
                "has_prd": has_prd,
                "has_plan": has_plan,
            })
    return features


def main():
    try:
        input_data = json.load(sys.stdin)

        session_id = input_data.get("session_id")
        transcript_path = input_data.get("transcript_path")

        project_root = find_project_root()
        git = get_git_state()
        features = scan_features(project_root)

        state = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "source": "pre_compact",
            "session_id": session_id,
            "transcript_path": transcript_path,
            "git": git,
            "features": features,
        }

        # Write to .claude/session-state.json
        state_file = project_root / ".claude" / "session-state.json"
        state_file.parent.mkdir(exist_ok=True)
        state_file.write_text(json.dumps(state, indent=2))

        # Summary to stdout
        print(json.dumps({
            "message": "Session state saved",
            "state_file": str(state_file.relative_to(project_root)),
            "git_branch": git["branch"],
            "dirty_files": git["dirty_count"],
        }))

        sys.exit(0)

    except Exception as e:
        # Never block compaction
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
