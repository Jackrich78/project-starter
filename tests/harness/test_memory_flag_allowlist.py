"""`memory:` is a stored-prompt-injection path: it grants unscoped Write/Edit.

Only the TDD trio carries it. Agents that ingest outside material (WebSearch,
WebFetch, MCP tools) never do. Every agent opens with its memory block.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
NON_AGENT_FILES = {"TEMPLATE.md", "README.md"}
MEMORY_FLAG_ALLOWLIST = {"tdd-test-writer", "tdd-implementer", "tdd-refactorer"}
MEMORY_HEADING = "## Your memory (read first)"


def _agents() -> list[Path]:
    return sorted(f for f in AGENTS_DIR.glob("*.md") if f.name not in NON_AGENT_FILES)


def _split(path: Path) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", path.read_text(encoding="utf-8"), re.DOTALL)
    assert m, f"{path.name}: no frontmatter"
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def _tools(fm: dict) -> list[str]:
    t = fm.get("tools", [])
    if isinstance(t, str):
        t = t.split(",")
    return [x.strip() for x in t if str(x).strip()]


def _first_h2(body: str) -> str | None:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    in_fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("## "):
            return line.rstrip()
    return None


def test_agents_exist():
    assert _agents()


@pytest.mark.parametrize("path", _agents(), ids=lambda p: p.stem)
def test_memory_flag_only_on_allowlist(path: Path):
    fm, _ = _split(path)
    if "memory" in fm:
        assert path.stem in MEMORY_FLAG_ALLOWLIST, (
            f"{path.name} carries `memory:` but is not in {sorted(MEMORY_FLAG_ALLOWLIST)}"
        )


@pytest.mark.parametrize("path", _agents(), ids=lambda p: p.stem)
def test_ingesting_agents_have_no_memory_flag(path: Path):
    fm, _ = _split(path)
    ingest = [t for t in _tools(fm) if t in {"WebSearch", "WebFetch"} or t.startswith("mcp__")]
    if ingest:
        assert "memory" not in fm, f"{path.name} has {ingest} and `memory:` (stored-injection path)"


@pytest.mark.parametrize("path", _agents(), ids=lambda p: p.stem)
def test_first_heading_is_memory_block(path: Path):
    _, body = _split(path)
    assert _first_h2(body) == MEMORY_HEADING, (
        f"{path.name}: first `##` heading is {_first_h2(body)!r}, expected {MEMORY_HEADING!r}"
    )
