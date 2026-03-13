#!/usr/bin/env python3
"""
Stop Hook - Git Workflow Preparation

Runs when the main agent finishes responding to:
- Show git status and changed files
- Draft conventional commit message based on changes
- Detect commit type and scope from file paths
- Suggest next steps (/commit or /test)

This helps maintain development momentum by prompting for the next action.
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from collections import Counter

def run_git_command(args, timeout=5):
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            ['git'] + args,
            capture_output=True,
            timeout=timeout,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except:
        return None

def get_git_status():
    """Get git status information"""
    status = run_git_command(['status', '--short'])
    if status is None:
        return None

    # Parse git status output
    changes = {
        'modified': [],
        'added': [],
        'deleted': [],
        'untracked': []
    }

    for line in status.split('\n'):
        if not line:
            continue

        status_code = line[:2]
        file_path = line[3:]

        if status_code.strip() == 'M' or 'M' in status_code:
            changes['modified'].append(file_path)
        elif status_code.strip() == 'A' or 'A' in status_code:
            changes['added'].append(file_path)
        elif status_code.strip() == 'D' or 'D' in status_code:
            changes['deleted'].append(file_path)
        elif status_code.strip() == '??':
            changes['untracked'].append(file_path)

    return changes

def get_current_branch():
    """Get current git branch name"""
    return run_git_command(['branch', '--show-current'])

def detect_commit_type(changes):
    """Detect commit type from changed files"""
    all_files = (
        changes['modified'] +
        changes['added'] +
        changes['deleted']
    )

    if not all_files:
        return 'chore'

    # Count file patterns
    patterns = Counter()

    for file_path in all_files:
        path = Path(file_path)

        # Feature documentation
        if 'docs/features/FEAT-' in file_path:
            patterns['feat'] += 2

        # Test files
        if 'test' in file_path.lower() or path.suffix in ['.test.js', '.test.ts', '.spec.js', '.spec.ts', '_test.py']:
            patterns['test'] += 2

        # Documentation
        if path.suffix == '.md' and 'docs/' in file_path:
            patterns['docs'] += 2

        # Source code
        if path.suffix in ['.js', '.ts', '.py', '.rs', '.go', '.java', '.rb']:
            # If in src/ or lib/, likely a feature
            if 'src/' in file_path or 'lib/' in file_path:
                patterns['feat'] += 1

        # Configuration files
        if path.suffix in ['.json', '.yml', '.yaml', '.toml'] or path.name in ['.eslintrc', '.prettierrc']:
            patterns['chore'] += 1

        # CI/CD
        if '.github/' in file_path or '.gitlab/' in file_path or 'Dockerfile' in file_path:
            patterns['ci'] += 1

        # Claude tooling
        if '.claude/' in file_path:
            patterns['chore'] += 1

    # Return most common type, default to feat
    if not patterns:
        return 'feat'

    return patterns.most_common(1)[0][0]

def detect_scope(changes):
    """Detect scope from changed file paths"""
    all_files = (
        changes['modified'] +
        changes['added'] +
        changes['deleted']
    )

    if not all_files:
        return None

    # Check for FEAT-XXX in paths
    feat_pattern = re.compile(r'FEAT-\d+')
    for file_path in all_files:
        match = feat_pattern.search(file_path)
        if match:
            return match.group(0)

    # Check for common directory-based scopes
    scope_dirs = Counter()
    for file_path in all_files:
        parts = Path(file_path).parts

        # Look for meaningful directory names
        if 'src' in parts:
            idx = parts.index('src')
            if idx + 1 < len(parts):
                scope_dirs[parts[idx + 1]] += 1
        elif 'lib' in parts:
            idx = parts.index('lib')
            if idx + 1 < len(parts):
                scope_dirs[parts[idx + 1]] += 1
        elif 'docs' in parts:
            scope_dirs['docs'] += 1
        elif '.claude' in parts:
            scope_dirs['tooling'] += 1
        elif 'test' in file_path or 'tests' in file_path:
            scope_dirs['test'] += 1

    # Return most common scope
    if scope_dirs:
        return scope_dirs.most_common(1)[0][0]

    return None

def generate_commit_summary(changes, commit_type):
    """Generate a brief summary of changes"""
    summaries = []

    if changes['added']:
        summaries.append(f"{len(changes['added'])} files added")

    if changes['modified']:
        summaries.append(f"{len(changes['modified'])} files modified")

    if changes['deleted']:
        summaries.append(f"{len(changes['deleted'])} files deleted")

    if not summaries:
        return "No changes"

    return ", ".join(summaries)

def draft_commit_message(changes, commit_type, scope):
    """Draft a conventional commit message"""
    # Generate description based on commit type
    descriptions = {
        'feat': 'Add new feature',
        'fix': 'Fix bug',
        'docs': 'Update documentation',
        'test': 'Add or update tests',
        'refactor': 'Refactor code',
        'style': 'Format code',
        'chore': 'Update tooling or configuration',
        'perf': 'Improve performance',
        'ci': 'Update CI/CD configuration'
    }

    description = descriptions.get(commit_type, 'Make changes')

    # Build commit message
    if scope:
        message = f"{commit_type}({scope}): {description}"
    else:
        message = f"{commit_type}: {description}"

    return message

def suggest_next_action(changes, branch):
    """Suggest next action based on current state"""
    total_changes = (
        len(changes['modified']) +
        len(changes['added']) +
        len(changes['deleted']) +
        len(changes['untracked'])
    )

    if total_changes == 0:
        return {
            "action": "none",
            "message": "No changes to commit. Keep coding!"
        }

    # Check if on main branch
    if branch in ['main', 'master']:
        return {
            "action": "create_branch",
            "message": "You're on the main branch. Create a feature branch first.",
            "command": "git checkout -b feat/your-feature-name"
        }

    # Check if there are test files
    test_files = [f for f in changes['modified'] + changes['added']
                  if 'test' in f.lower() or '.test.' in f or '.spec.' in f]

    if test_files:
        return {
            "action": "test",
            "message": "Test files changed. Run tests before committing.",
            "command": "/test"
        }

    # Otherwise, suggest commit
    return {
        "action": "commit",
        "message": "Ready to commit? Run the commit command.",
        "command": "/commit"
    }

def format_output(changes, branch, commit_type, scope, commit_message, next_action):
    """Format the hook output"""
    total_changes = (
        len(changes['modified']) +
        len(changes['added']) +
        len(changes['deleted']) +
        len(changes['untracked'])
    )

    output = {
        "hook": "Stop",
        "git_status": {
            "branch": branch,
            "total_changes": total_changes,
            "modified": len(changes['modified']),
            "added": len(changes['added']),
            "deleted": len(changes['deleted']),
            "untracked": len(changes['untracked'])
        }
    }

    # Only add commit info if there are changes
    if total_changes > 0:
        output["suggested_commit"] = {
            "type": commit_type,
            "scope": scope,
            "message": commit_message,
            "summary": generate_commit_summary(changes, commit_type)
        }

        output["next_action"] = next_action

        # Add file lists if not too many
        if total_changes <= 10:
            output["changed_files"] = {
                "modified": changes['modified'],
                "added": changes['added'],
                "deleted": changes['deleted'],
                "untracked": changes['untracked']
            }

    return output

def main():
    """Main hook execution"""
    try:
        # Read JSON input from stdin (not used currently, but available)
        try:
            input_data = json.load(sys.stdin)
        except:
            input_data = {}

        # Check if we're in a git repository
        branch = get_current_branch()
        if branch is None:
            # Not a git repo, silently exit
            sys.exit(0)

        # Get git status
        changes = get_git_status()
        if changes is None:
            sys.exit(0)

        # Detect commit type and scope
        commit_type = detect_commit_type(changes)
        scope = detect_scope(changes)

        # Draft commit message
        commit_message = draft_commit_message(changes, commit_type, scope)

        # Suggest next action
        next_action = suggest_next_action(changes, branch)

        # Format and output
        output = format_output(changes, branch, commit_type, scope, commit_message, next_action)

        # Only output if there are changes or meaningful info
        total_changes = (
            len(changes['modified']) +
            len(changes['added']) +
            len(changes['deleted']) +
            len(changes['untracked'])
        )

        if total_changes > 0:
            print(json.dumps(output, indent=2))

        # Always exit 0
        sys.exit(0)

    except Exception as e:
        # Log error but don't block
        error_msg = {
            "hook": "Stop",
            "error": str(e),
            "note": "Hook failed but execution continued"
        }
        print(json.dumps(error_msg, indent=2), file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
