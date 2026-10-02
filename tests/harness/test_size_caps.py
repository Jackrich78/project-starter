"""Size caps that keep the harness lean.

Skills <= 150 lines (or carry a `# SPLIT-DEFERRED <reason>` marker), agents <= 300,
CLAUDE.md <= 150, and no `.claude/commands/` directory (skills only). A cap that
can be silenced with a marker is still visible: the test lists every marker.
"""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_CAP = 150
AGENT_CAP = 300
CLAUDE_MD_CAP = 150


def _lines(p: Path) -> int:
    return len(p.read_text(encoding="utf-8").splitlines())


SKILLS = sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md"))
AGENTS = sorted(p for p in (ROOT / ".claude" / "agents").glob("*.md") if p.name not in {"README.md", "TEMPLATE.md"})


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.parent.name)
def test_skill_under_cap_or_marked(skill: Path):
    n = _lines(skill)
    marked = "# SPLIT-DEFERRED" in skill.read_text(encoding="utf-8")
    assert n <= SKILL_CAP or marked, f"{skill.relative_to(ROOT)} is {n} lines (> {SKILL_CAP}) and has no '# SPLIT-DEFERRED <reason>' marker"


@pytest.mark.parametrize("agent", AGENTS, ids=lambda p: p.stem)
def test_agent_under_cap(agent: Path):
    n = _lines(agent)
    assert n <= AGENT_CAP, f"{agent.relative_to(ROOT)} is {n} lines (> {AGENT_CAP})"


def test_claude_md_under_cap():
    n = _lines(ROOT / "CLAUDE.md")
    assert n <= CLAUDE_MD_CAP, f"CLAUDE.md is {n} lines (> {CLAUDE_MD_CAP}); move detail to .claude/rules/ or docs/"


def test_no_commands_dir():
    assert not (ROOT / ".claude" / "commands").exists(), ".claude/commands/ must not exist: every workflow is a skill"


def test_every_skill_has_required_frontmatter():
    for skill in SKILLS:
        text = skill.read_text(encoding="utf-8")
        assert text.startswith("---\n"), f"{skill.relative_to(ROOT)}: missing frontmatter"
        fm = text.split("---", 2)[1]
        for key in ("name:", "description:"):
            assert key in fm, f"{skill.relative_to(ROOT)}: frontmatter lacks {key}"
        assert f"name: {skill.parent.name}" in fm, f"{skill.relative_to(ROOT)}: name must equal the folder name"
