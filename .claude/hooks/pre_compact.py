#!/usr/bin/env python3
"""
PreCompact Hook - Session State Backup

Runs before context compaction to save critical session state that helps
Claude recover context after compaction or in new sessions.

This hook receives JSON input via stdin with compaction trigger info.
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def find_project_root():
    """Find project root by looking for CLAUDE.md"""
    current = Path.cwd()
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path.cwd()

def scan_active_features():
    """Scan docs/features/ for features currently being worked on"""
    project_root = find_project_root()
    features_dir = project_root / "docs" / "features"

    if not features_dir.exists():
        return []

    active_features = []
    for feat_dir in features_dir.iterdir():
        if feat_dir.is_dir() and feat_dir.name.startswith("FEAT-"):
            # Check if planning is complete
            has_prd = (feat_dir / "prd.md").exists()
            has_research = (feat_dir / "research.md").exists()
            has_architecture = (feat_dir / "architecture.md").exists()

            status = "unknown"
            if has_architecture:
                status = "ready_for_implementation"
            elif has_research:
                status = "planning"
            elif has_prd:
                status = "exploring"

            active_features.append({
                "id": feat_dir.name,
                "path": str(feat_dir.relative_to(project_root)),
                "status": status,
                "has_prd": has_prd,
                "has_research": has_research,
                "has_architecture": has_architecture
            })

    return active_features

def get_recent_changes():
    """Get list of recently modified files in docs/"""
    project_root = find_project_root()
    docs_dir = project_root / "docs"

    if not docs_dir.exists():
        return []

    recent_files = []
    for md_file in docs_dir.rglob("*.md"):
        try:
            mtime = md_file.stat().st_mtime
            recent_files.append({
                "path": str(md_file.relative_to(project_root)),
                "modified": datetime.fromtimestamp(mtime).isoformat()
            })
        except:
            pass

    # Sort by modification time, most recent first
    recent_files.sort(key=lambda x: x["modified"], reverse=True)
    return recent_files[:10]  # Keep top 10

def get_git_state():
    """Get current git state"""
    try:
        # Get current branch
        branch_result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=2
        )
        git_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

        # Get count of uncommitted changes
        status_result = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True,
            text=True,
            timeout=2
        )
        git_status = status_result.stdout.strip() if status_result.returncode == 0 else ""
        git_dirty_count = len(git_status.split('\n')) if git_status else 0

        return {
            "git_branch": git_branch,
            "git_dirty_count": git_dirty_count
        }
    except Exception as e:
        # If git fails, return defaults
        return {
            "git_branch": "unknown",
            "git_dirty_count": 0
        }

def identify_primary_feature(active_features):
    """Identify most recently modified feature as primary"""
    if not active_features:
        return None

    project_root = find_project_root()
    most_recent_time = 0
    primary_feature = None

    for feat in active_features:
        feat_path = project_root / feat['path']
        if feat_path.exists():
            try:
                # Get most recent file modification time in feature directory
                latest_mtime = 0
                for file in feat_path.rglob("*"):
                    if file.is_file():
                        mtime = file.stat().st_mtime
                        if mtime > latest_mtime:
                            latest_mtime = mtime

                if latest_mtime > most_recent_time:
                    most_recent_time = latest_mtime
                    primary_feature = feat['id']
            except:
                pass

    # Fallback to first feature if detection fails
    return primary_feature or (active_features[0]['id'] if active_features else None)

def save_session_state(trigger, instructions, active_features, recent_changes):
    """Save session state to .claude/session-state.json"""
    project_root = find_project_root()
    claude_dir = project_root / ".claude"
    claude_dir.mkdir(exist_ok=True)

    state_file = claude_dir / "session-state.json"

    # Get git state and primary feature
    git_state = get_git_state()
    primary_feature = identify_primary_feature(active_features)

    state = {
        "timestamp": datetime.now().isoformat(),
        "compaction_trigger": trigger,
        "user_instructions": instructions,
        "git_branch": git_state["git_branch"],
        "git_dirty_count": git_state["git_dirty_count"],
        "primary_feature": primary_feature,
        "active_features": active_features,
        "recent_changes": recent_changes,
        "phase": "Phase 1 - Planning & Documentation",
        "recovery_hints": {
            "what_to_say": "I've recovered from context compaction. Let me review the session state...",
            "files_to_read": [f["path"] for f in active_features] if active_features else [],
            "suggested_action": f"Continue working on {primary_feature or active_features[0]['id'] if active_features else 'unknown'}"
        }
    }

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

    return state_file

def main():
    """Main hook execution"""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        trigger = input_data.get("trigger", "unknown")
        instructions = input_data.get("instructions", "")

        # Gather session state
        active_features = scan_active_features()
        recent_changes = get_recent_changes()

        # Save state
        state_file = save_session_state(trigger, instructions, active_features, recent_changes)

        # Output recovery message to stdout (will be added to context)
        recovery_msg = {
            "message": "Session state saved before compaction",
            "state_file": str(state_file.relative_to(find_project_root())),
            "active_features": len(active_features),
            "compaction_type": trigger
        }

        print(json.dumps(recovery_msg, indent=2))

        # Exit 0 = success (allow compaction to proceed)
        sys.exit(0)

    except Exception as e:
        # Log error but don't block compaction
        error_msg = {
            "error": "PreCompact hook failed",
            "details": str(e),
            "note": "Compaction will proceed anyway"
        }
        print(json.dumps(error_msg, indent=2), file=sys.stderr)
        sys.exit(0)  # Don't block compaction even if hook fails

if __name__ == "__main__":
    main()
