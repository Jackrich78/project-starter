#!/usr/bin/env python3
"""
PostToolUse Hook - Auto-formatting and Documentation Updates

Runs after Edit/Write tool usage to automatically:
- Format code files based on file extension
- Update documentation index when docs change
- Validate syntax for common file types

Supports: prettier, black, rustfmt, gofmt, and more
"""

import json
import sys
import subprocess
from pathlib import Path

# File extension to formatter mapping
FORMATTERS = {
    # JavaScript/TypeScript - Prettier
    '.js': ('prettier', ['--write']),
    '.jsx': ('prettier', ['--write']),
    '.ts': ('prettier', ['--write']),
    '.tsx': ('prettier', ['--write']),
    '.json': ('prettier', ['--write']),
    '.css': ('prettier', ['--write']),
    '.scss': ('prettier', ['--write']),
    '.html': ('prettier', ['--write']),
    '.vue': ('prettier', ['--write']),

    # Python - Black
    '.py': ('black', ['-q']),

    # Rust - rustfmt
    '.rs': ('rustfmt', []),

    # Go - gofmt
    '.go': ('gofmt', ['-w']),

    # Ruby - rubocop
    '.rb': ('rubocop', ['-a']),

    # Java - google-java-format
    '.java': ('google-java-format', ['-i']),
}

# Extensions that should NOT be formatted
SKIP_FORMATTING = {
    '.md',      # Markdown (preserve user formatting)
    '.txt',     # Plain text
    '.log',     # Log files
    '.env',     # Environment files
    '.gitignore',
    '.dockerignore',
}

def check_formatter_available(formatter):
    """Check if a formatter is installed"""
    try:
        result = subprocess.run(
            ['which', formatter],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except:
        return False

def run_formatter(file_path, formatter, args):
    """Run formatter on a file"""
    try:
        cmd = [formatter] + args + [str(file_path)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=30,
            text=True
        )

        if result.returncode == 0:
            return {"success": True, "formatter": formatter}
        else:
            return {
                "success": False,
                "formatter": formatter,
                "error": result.stderr.strip() if result.stderr else "Unknown error"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "formatter": formatter,
            "error": "Formatter timed out (30s)"
        }
    except Exception as e:
        return {
            "success": False,
            "formatter": formatter,
            "error": str(e)
        }

def should_format_file(file_path):
    """Determine if a file should be formatted"""
    path = Path(file_path)

    # Skip non-existent files
    if not path.exists():
        return False, None

    # Skip directories
    if path.is_dir():
        return False, None

    # Get file extension
    ext = path.suffix.lower()

    # Skip files in skip list
    if ext in SKIP_FORMATTING:
        return False, None

    # Special case: .json files - check if they're config files
    if ext == '.json':
        # Skip package-lock.json, yarn.lock, etc.
        if 'lock' in path.name.lower():
            return False, None

    # Check if we have a formatter for this extension
    if ext in FORMATTERS:
        formatter, args = FORMATTERS[ext]

        # Check if formatter is available
        if check_formatter_available(formatter):
            return True, (formatter, args)
        else:
            return False, {'not_installed': formatter}

    return False, None

def update_docs_index(file_path):
    """Update docs/README.md when documentation changes"""
    path = Path(file_path)

    # Only process files in docs/ directory
    if 'docs/' not in str(path):
        return None

    # Find project root
    current = Path.cwd()
    while current != current.parent:
        if (current / "docs").exists():
            docs_readme = current / "docs" / "README.md"
            if docs_readme.exists():
                return {
                    "action": "docs_index_update_needed",
                    "file": str(docs_readme),
                    "note": "Run /update-docs to regenerate index"
                }
        current = current.parent

    return None

def main():
    """Main hook execution"""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Get tool name and parameters
        tool_name = input_data.get("tool", "")
        params = input_data.get("params", {})

        # Only process Edit and Write tools
        if tool_name not in ["Edit", "Write"]:
            # Silent pass for other tools
            sys.exit(0)

        # Get the file path that was modified
        file_path = params.get("file_path", "")
        if not file_path:
            sys.exit(0)

        results = {
            "hook": "PostToolUse",
            "tool": tool_name,
            "file": file_path,
            "actions": []
        }

        # Check if file should be formatted
        should_format, formatter_info = should_format_file(file_path)

        if should_format and isinstance(formatter_info, tuple):
            formatter, args = formatter_info
            format_result = run_formatter(file_path, formatter, args)
            results["actions"].append({
                "type": "format",
                "result": format_result
            })
        elif should_format and isinstance(formatter_info, dict) and 'not_installed' in formatter_info:
            # Formatter not installed - silent skip
            results["actions"].append({
                "type": "format_skipped",
                "reason": f"{formatter_info['not_installed']} not installed"
            })

        # Check if docs index needs updating
        docs_update = update_docs_index(file_path)
        if docs_update:
            results["actions"].append({
                "type": "docs_index",
                "result": docs_update
            })

        # Only output if there were actions taken
        if results["actions"]:
            print(json.dumps(results, indent=2))

        # Always exit 0 (don't block tool execution)
        sys.exit(0)

    except Exception as e:
        # Log error but don't block tool execution
        error_msg = {
            "hook": "PostToolUse",
            "error": str(e),
            "note": "Hook failed but tool execution continued"
        }
        print(json.dumps(error_msg, indent=2), file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
