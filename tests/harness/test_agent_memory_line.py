"""Every agent prompt names all four memory `source:` kinds the validator accepts.

`scripts/validate_agent_memory.py` accepts `file:line`, `commit:sha`, an
http(s) URL and `session:<id>`. An agent that only reads
`source: <file:line|commit:sha|url>` cannot cite a method learned in
conversation, so it either invents a file or drops the entry. The TEMPLATE
also has to say when `session:<id>` is the right kind.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
TEMPLATE = AGENTS_DIR / "TEMPLATE.md"
KINDS = ("file:line", "commit:sha", "url", "session:<id>")
SOURCE_SPEC = re.compile(r"source: <([^\n]*?)>>?")
SESSION_HINT = "Use `session:<id>` when the method came from this conversation rather than a file."


def _files_with_source_spec() -> list[Path]:
    return sorted(f for f in AGENTS_DIR.glob("*.md")
                  if f.name != "README.md" and "source: <" in f.read_text(encoding="utf-8"))


def _specs(path: Path) -> list[str]:
    return [m.group(0) for m in SOURCE_SPEC.finditer(path.read_text(encoding="utf-8"))]


def test_agents_carry_a_source_spec():
    files = _files_with_source_spec()
    assert TEMPLATE in files and len(files) > 3, [f.name for f in files]


@pytest.mark.parametrize("path", _files_with_source_spec(), ids=lambda p: p.stem)
def test_every_source_spec_names_all_four_kinds(path: Path):
    specs = _specs(path)
    assert specs, f"{path.name}: has 'source: <' but no parsable spec"
    for spec in specs:
        missing = [k for k in KINDS if k not in spec]
        assert not missing, f"{path.name}: {spec!r} lacks {missing}"


def test_template_explains_when_to_use_session_kind():
    assert SESSION_HINT in TEMPLATE.read_text(encoding="utf-8")
