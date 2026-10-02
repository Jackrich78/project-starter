"""README.md and PROJECT.md must not carry component counts.

"14 agents", "21 skills" and the like drift the week after they are written. The
roster is derived from the filesystem; prose links to it instead of counting it.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COUNT_RE = re.compile(r"\b\d+\s+(?:specialized\s+|workflow\s+|built-in\s+)?(agents?|skills?|commands?|hooks?|rules?)\b", re.IGNORECASE)


@pytest.mark.parametrize("name", ["README.md", "PROJECT.md"])
def test_no_component_counts(name: str):
    text = (ROOT / name).read_text(encoding="utf-8")
    hits = [m.group(0) for m in COUNT_RE.finditer(text)]
    assert not hits, f"{name} states component counts that will drift: {hits}"
