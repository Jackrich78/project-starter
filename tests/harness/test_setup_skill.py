"""/setup and the hygiene it depends on (v3.0.1 adoption feedback).

Covers: the skill's markers are achievable (no "first line", no "0 to update"),
every skill directory is tracked (an ignore rule hid `.claude/skills/build/` in
v3.0.0), area labels have one home (the `Areas (labels)` line in CLAUDE.md),
and the session primer notices the current-priorities placeholder.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".claude" / "skills" / "setup" / "SKILL.md"
LABELS_PY = ROOT / "scripts" / "github" / "setup_labels.py"
HOOKS = ROOT / ".claude" / "hooks"

sys.path.insert(0, str(ROOT / "scripts" / "github"))
sys.path.insert(0, str(HOOKS))
import setup_labels  # noqa: E402
import session_prime  # noqa: E402

PLACEHOLDER = "(issue links, one line each)"
SKILL_DIRS = sorted(p.parent for p in (ROOT / ".claude" / "skills").glob("*/SKILL.md"))


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


# --- 1. every skill on disk is tracked --------------------------------------

@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: p.name)
def test_skill_dir_is_tracked_and_not_ignored(skill_dir: Path):
    rel = str(skill_dir.relative_to(ROOT))
    assert _git("ls-files", rel).stdout.strip(), f"{rel} has no tracked files: run `git add {rel}/SKILL.md`"
    # check-ignore exits 1 when nothing is ignored
    assert _git("check-ignore", "-q", rel).returncode == 1, f"{rel} is matched by a .gitignore rule"


# --- 7/8. the skill text -------------------------------------------------------

def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _step(n: int) -> str:
    text = _skill()
    start = text.index(f"\n{n}. **")
    nxt = text.find(f"\n{n + 1}. **", start + 1)
    return text[start:nxt if nxt != -1 else None]


def test_skill_markers_are_achievable():
    text = _skill()
    assert "first line" not in text, "step 3 marker: CLAUDE.md:3 is a CUSTOMIZE comment, not the first line"
    assert "0 to update" not in text, "existing labels count as `update` by design; only `0 to create` can pass"
    assert "0 to create" in text
    assert "--grep=" in text, "step 7 marker must search git log, not HEAD's subject"
    assert "shows no diff" not in text


def test_step3_fills_areas_and_identity():
    s3 = _step(3)
    assert "area" in s3.lower()
    assert "Areas (labels)" in s3
    assert "current-priorities.md" in s3
    assert "version: 0.1.0" in s3


def test_step5_stub_labels_and_scratch_path():
    s5 = _step(5)
    assert "--label enhancement --label P2" in s5
    assert "plan mode" in s5


def test_step7_stages_by_path_without_a_leak_gate():
    s7 = _step(7)
    assert "Stage by explicit path" in s7 and "never `git add -A`" in s7
    assert "leak_gate" not in s7 and "pii-patterns" not in s7


def test_smoke_checklist_and_antipatterns():
    text = _skill()
    assert "git ls-files .claude/skills/build/SKILL.md" in text
    assert "founding-commit marker against HEAD" in text
    assert len(text.splitlines()) <= 150


# --- 4. area labels have one home --------------------------------------------

def test_no_hardcoded_area_label_list():
    src = LABELS_PY.read_text(encoding="utf-8")
    assert not re.search(r"^AREA_LABELS\b[^=\n]*=\s*\[", src, re.M), "areas come from CLAUDE.md, not a literal list"
    assert callable(getattr(setup_labels, "parse_areas", None))


@pytest.mark.parametrize("line, expected", [
    ("- Areas (labels): <!-- CUSTOMIZE: area:core, area:ops … -->", []),
    ("- Areas (labels): area:core, area:ops", ["area:core", "area:ops"]),
    ("- Areas (labels):  area:core ,area:ops   area:core", ["area:core", "area:ops"]),
])
def test_parse_areas(line, expected):
    assert setup_labels.parse_areas(line) == expected


def test_issue_flow_points_at_claude_md_for_areas():
    text = (ROOT / "docs/system/issue-flow.md").read_text(encoding="utf-8")
    assert "AREA_LABELS" not in text
    assert "Areas (labels)" in text


# --- 5. session primer notices the placeholder --------------------------------

def _tmp_root(tmp_path: Path, body: str) -> Path:
    pri = tmp_path / "docs" / "system" / "current-priorities.md"
    pri.parent.mkdir(parents=True)
    pri.write_text("---\nupdated: 2099-01-01\n---\n\n# Current priorities\n\n" + body, encoding="utf-8")
    return tmp_path


def test_primer_prints_notice_while_placeholder_present(tmp_path):
    root = _tmp_root(tmp_path, f"- **In flight this week:** {PLACEHOLDER}\n- **Next:** (x)\n")
    parts = session_prime.collect_parts(root)
    assert parts == [session_prime.PLACEHOLDER_NOTICE]
    assert "/setup step 3" in parts[0]
    assert PLACEHOLDER not in parts[0]


def test_primer_injects_body_once_filled(tmp_path):
    root = _tmp_root(tmp_path, "- **In flight this week:** #12 founding commit\n- **Next:** /explore #1\n")
    parts = session_prime.collect_parts(root)
    assert len(parts) == 1
    assert "#12 founding commit" in parts[0]
    assert "placeholder" not in parts[0]


def test_shipped_priorities_file_is_the_detection_marker():
    text = (ROOT / "docs/system/current-priorities.md").read_text(encoding="utf-8")
    assert PLACEHOLDER in text or "/setup step 3" in text, "either the placeholder (template) or a filled file"


# --- 2/3. hygiene scripts -------------------------------------------------------
