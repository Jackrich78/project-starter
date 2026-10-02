"""Agent frontmatter `model`/`effort` must agree with CLAUDE.md.

CLAUDE.md § "Delegation & model policy" is the single source of truth. Its two
pipe tables are parsed structurally and checked against `.claude/agents/*.md`
frontmatter. Nothing is hard-coded here: no agent names, no row counts.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
NON_AGENT_FILES = {"TEMPLATE.md", "README.md"}
SECTION = "Delegation & model policy"

# Routing rows that name something other than a `.claude/agents/*.md` file.
NO_FILE_CALLS = {"claude-code-guide", "general-purpose"}
DEFAULT_MODEL = "sonnet"
ROLE_HEADER = ["Role", "Model", "Effort"]
ROUTE_HEADER = ["When you need…", "Call", "Model"]


def _section() -> str:
    text = CLAUDE_MD.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(SECTION)}.*?\n(.*?)(?=^## |\Z)", text, re.DOTALL | re.MULTILINE)
    assert m, f"CLAUDE.md has no '## {SECTION}' section"
    return m.group(1)


def _split(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _tables(block: str) -> list[list[list[str]]]:
    """Every pipe table in block as [header, *rows] (separator dropped)."""
    tables, cur = [], []
    for line in block.splitlines() + [""]:
        if line.strip().startswith("|"):
            cur.append(line)
        elif cur:
            tables.append([_split(l) for l in cur if not re.match(r"^\|?[\s:|-]+\|?$", l.strip())])
            cur = []
    return tables


def _table(header: list[str]) -> list[list[str]]:
    for t in _tables(_section()):
        if t[0] == header:
            return t[1:]
    pytest.fail(f"CLAUDE.md § {SECTION} has no table with header {header}")


def _plain(cell: str) -> str:
    return cell.replace("**", "").replace("`", "").strip()


def _frontmatter(path: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.DOTALL)
    assert m, f"{path.name}: no frontmatter block"
    data = yaml.safe_load(m.group(1))
    assert isinstance(data, dict), f"{path.name}: frontmatter is not a mapping"
    return data


def _agent_files() -> list[Path]:
    return sorted(f for f in AGENTS_DIR.glob("*.md") if f.name not in NON_AGENT_FILES)


def _role_expectations() -> tuple[dict[str, tuple[str, str | None]], list[tuple[str, str | None]]]:
    """(named agent -> (model, effort), skipped rows). Skips 'as set'/'built in' rows."""
    named: dict[str, tuple[str, str | None]] = {}
    for role, model, effort in _table(ROLE_HEADER):
        model, effort = _plain(model).lower(), _plain(effort).lower()
        if model in {"as set", "built in"}:
            continue
        eff = effort if effort not in {"", "as set", "built in"} else None
        for group in re.findall(r"\(([^)]*)\)", role):
            for name in (n.strip() for n in group.split(",")):
                if re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
                    named[name] = (model, eff)
    return named, []


def _routing_calls() -> list[tuple[str, str]]:
    """(agent name, model cell) per routing row, qualifiers stripped."""
    out = []
    for _need, call, model in _table(ROUTE_HEADER):
        call = re.sub(r"\([^)]*\)", "", _plain(call)).strip()
        out.append((call, _plain(model).lower()))
    return out


def test_tables_parse_and_are_nonempty():
    named, _ = _role_expectations()
    assert named, "role table names no agents in parentheses"
    assert _routing_calls(), "routing table has no rows"


def test_agents_exist_to_check():
    assert _agent_files(), "no agent files found"


@pytest.mark.parametrize("path", _agent_files(), ids=lambda p: p.stem)
def test_agent_model_and_effort_match_role_table(path: Path):
    named, _ = _role_expectations()
    fm = _frontmatter(path)
    name = fm.get("name", path.stem)
    expected_model, expected_effort = named.get(path.stem, (DEFAULT_MODEL, None))
    where = "role table" if path.stem in named else f"default (unlisted -> {DEFAULT_MODEL})"
    assert fm.get("model") == expected_model, (
        f"{path.name}: model {fm.get('model')!r}, CLAUDE.md {where} says {expected_model!r}"
    )
    if expected_effort is not None:
        assert str(fm.get("effort")) == expected_effort, (
            f"{path.name}: effort {fm.get('effort')!r}, role table says {expected_effort!r}"
        )
    assert name == path.stem, f"{path.name}: frontmatter name {name!r} != filename stem"


def test_role_table_names_only_existing_agents():
    named, _ = _role_expectations()
    existing = {f.stem for f in _agent_files()}
    ghosts = sorted(set(named) - existing)
    assert not ghosts, f"role table names agents with no file: {ghosts}"


@pytest.mark.parametrize("call,model", _routing_calls(), ids=lambda v: str(v)[:30])
def test_routing_call_resolves_to_agent_file(call: str, model: str):
    if call in NO_FILE_CALLS or "built in" in call:
        pytest.skip(f"{call}: built-in agent, no file")
    base = call.split()[0] if call.split() else call
    path = AGENTS_DIR / f"{base}.md"
    assert path.is_file(), f"routing table calls {base!r} but {path} does not exist"
    model_word = re.split(r"[ ,]", model)[0]
    if model_word and model_word != "as":
        assert _frontmatter(path).get("model") == model_word, (
            f"{path.name}: routing table says {model_word!r}, frontmatter says "
            f"{_frontmatter(path).get('model')!r}"
        )
    m = re.search(r"effort (\w+)", model)
    if m:
        assert str(_frontmatter(path).get("effort")) == m.group(1), (
            f"{path.name}: routing table effort {m.group(1)!r}, frontmatter "
            f"{_frontmatter(path).get('effort')!r}"
        )
