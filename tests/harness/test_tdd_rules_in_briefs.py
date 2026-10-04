"""Path-scoped `.claude/rules/*.md` load in the main thread only.

A sub-agent sees none of them, so every TDD agent prompt and every TDD dispatch
template must restate the five testing rules verbatim. `tdd-test-writer.md` is
the source copy; the other five files are checked against it, and the reference
page records the mechanism.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS = REPO_ROOT / ".claude" / "agents"
TEMPLATES = REPO_ROOT / ".claude" / "skills" / "tdd-red-green-refactor" / "templates"
SOURCE = AGENTS / "tdd-test-writer.md"
RESTATED_IN = [
    AGENTS / "tdd-implementer.md",
    AGENTS / "tdd-refactorer.md",
    TEMPLATES / "test-writer-prompt.md",
    TEMPLATES / "implementer-prompt.md",
    TEMPLATES / "refactorer-prompt.md",
]
HEADING = "Testing rules (path-scoped rules do not load in sub-agents, so they are restated here)"
REFERENCE = REPO_ROOT / "docs" / "reference" / "claude-code.md"
REFERENCE_SENTENCE = "a sub-agent sees none of them, so a brief must restate what it needs"


def _bullets(path: Path) -> list[str]:
    """The five rule bullets, stripped of indentation and list marker."""
    text = path.read_text(encoding="utf-8")
    start = text.index("**Seen red:**")
    end = text.index("A skip names what it waits for.", start) + len("A skip names what it waits for.")
    block = text[text.rfind("\n", 0, start) + 1:end]
    return [re.sub(r"^\s*-\s*", "", ln).strip() for ln in block.splitlines() if ln.strip()]


def test_source_copy_has_five_rules():
    bullets = _bullets(SOURCE)
    assert len(bullets) == 5, bullets
    assert bullets[1].startswith("**Discriminating half:**")


@pytest.mark.parametrize("path", RESTATED_IN, ids=lambda p: p.name)
def test_discriminating_half_bullet_present(path: Path):
    discriminating = _bullets(SOURCE)[1]
    assert discriminating in path.read_text(encoding="utf-8"), (
        f"{path.relative_to(REPO_ROOT)} lacks the test-writer's bullet: {discriminating}"
    )


@pytest.mark.parametrize("path", RESTATED_IN, ids=lambda p: p.name)
def test_all_five_rules_restated_verbatim(path: Path):
    text = path.read_text(encoding="utf-8")
    missing = [b for b in _bullets(SOURCE) if b not in text]
    assert not missing, f"{path.relative_to(REPO_ROOT)} is missing: {missing}"


@pytest.mark.parametrize("path", RESTATED_IN, ids=lambda p: p.name)
def test_restated_under_the_explaining_heading(path: Path):
    assert HEADING in path.read_text(encoding="utf-8"), f"{path.relative_to(REPO_ROOT)} lacks: {HEADING}"


def test_reference_page_states_rules_do_not_load_in_subagents():
    assert REFERENCE_SENTENCE in REFERENCE.read_text(encoding="utf-8")
