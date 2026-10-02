"""docs/reference/claude-code.md must have been re-checked against the official docs recently.

The page holds only URLs, so it cannot be wrong in substance, but the harness
mechanisms it points at can change. `/harness-health` bumps the stamp.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs" / "reference" / "claude-code.md"
MAX_AGE_DAYS = 90


def _stamp() -> date:
    m = re.search(r"^last_checked:\s*(\d{4}-\d{2}-\d{2})", PAGE.read_text(encoding="utf-8"), re.M)
    assert m, "docs/reference/claude-code.md has no `last_checked: YYYY-MM-DD` in its frontmatter"
    return date.fromisoformat(m.group(1))


def test_reference_page_exists():
    assert PAGE.exists()


def test_reference_stamp_is_fresh():
    age = (date.today() - _stamp()).days
    assert age <= MAX_AGE_DAYS, (
        f"claude-code.md last_checked is {age} days old (> {MAX_AGE_DAYS}); run /harness-health and bump the stamp"
    )


def test_reference_rows_have_urls():
    text = PAGE.read_text(encoding="utf-8")
    rows = [l for l in text.splitlines() if l.startswith("| ") and "http" not in l and "Topic" not in l and "---" not in l]
    assert not rows, f"reference rows without a URL: {rows}"
