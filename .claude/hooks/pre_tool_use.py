#!/usr/bin/env python3
"""
Security Guard Hook - Pre-Tool Use
Blocks dangerous commands before execution.

Output schema (verified 2026-06-12, https://code.claude.com/docs/en/hooks):
  Allow: exit 0 with no output — normal permission flow applies
  Deny:  exit 0 with JSON:
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "<reason>"
      }
    }

The old schema {"decision": "allow"/"block"} was not recognised by Claude Code
and caused hook_non_blocking_error entries without actually blocking anything.
"""

import json
import re
import sys
import os

# Dangerous command patterns
BLOCKED_PATTERNS = [
    r'rm\s+-rf\s+/',              # Recursive delete root
    r'rm\s+-rf\s+~',              # Recursive delete home
    r'rm\s+-rf\s+\*',             # Recursive delete all
    r'sudo\s+rm',                 # Sudo remove
    r'chmod\s+777',               # World-writable
    r'chmod\s+-R\s+777',          # Recursive world-writable
    r'curl.*\|\s*bash',           # Pipe to bash
    r'wget.*\|\s*bash',           # Wget pipe to bash
    r'curl.*\|\s*sh',             # Pipe to sh
    r'eval\s*\(',                 # Eval execution
    r'>\s*/dev/sd',               # Write to disk devices
    r'mkfs\.',                    # Format commands
    r'dd\s+if=',                  # Disk operations
    r':\(\)\{.*\};\:',             # Fork bomb
    r'>\s*/etc/',                 # Write to /etc
    r'rm\s+/etc/',                # Remove from /etc
]

# Commands requiring extra caution (log but allow)
CAUTION_PATTERNS = [
    r'git\s+push\s+.*--force',    # Force push
    r'git\s+reset\s+--hard',      # Hard reset
    r'npm\s+publish',             # Publish package
    r'docker\s+system\s+prune',   # Docker cleanup
]


def _deny_output(reason: str) -> str:
    """Return the correct JSON deny payload for PreToolUse hooks."""
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    })


def get_project_root():
    """Get the project root directory."""
    return os.getcwd()

def is_path_safe(command: str, project_root: str) -> bool:
    """Check if command operates within safe directories."""
    # Allow operations in project dir and /tmp
    safe_dirs = [project_root, '/tmp', '/var/folders']

    # Extract paths from command (simplified)
    # This is a basic check - production would need more robust parsing
    return True  # For now, rely on pattern matching

def check_command(command: str) -> dict:
    """Check if a command is safe to execute."""
    result = {
        'allowed': True,
        'reason': None,
        'severity': None
    }

    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            result['allowed'] = False
            result['reason'] = f"Blocked pattern: {pattern}"
            result['severity'] = 'critical'
            return result

    # Check caution patterns (allow but log)
    for pattern in CAUTION_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            result['severity'] = 'warning'
            result['reason'] = f"Caution: {pattern}"
            # Still allowed, just flagged

    return result

def main():
    """Main entry point for the hook."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Only check Bash commands; exit 0 with no output = allow for everything else
        if tool_name != 'Bash':
            return

        command = tool_input.get('command', '')

        if not command:
            return

        # Check the command
        check_result = check_command(command)

        if not check_result['allowed']:
            # Block the command using the correct PreToolUse deny schema
            print(_deny_output(f"Security guard: {check_result['reason']}"))

            # Log to file
            log_entry = {
                'action': 'blocked',
                'command': command[:200],  # Truncate for safety
                'reason': check_result['reason']
            }
            log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'security.log')
            try:
                with open(log_path, 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
            except Exception:
                pass  # Don't fail if logging fails

        # Allowed: exit 0 with no output — Claude Code normal flow allows the tool

    except Exception as e:
        # On error, fail open (exit 0, no output = allow) but log to stderr
        sys.stderr.write(f"Security hook error: {e}\n")

if __name__ == '__main__':
    main()
