#!/usr/bin/env python3
"""Single resolver for the project root, shared by the hooks."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def project_root() -> Path:
    """$CLAUDE_PROJECT_DIR, else `git rev-parse --show-toplevel`, else cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
        top = out.stdout.strip()
        if out.returncode == 0 and top:
            return Path(top)
    except Exception:
        pass
    return Path.cwd()

