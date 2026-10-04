"""Labels in setup_labels.py <=> labels table in issue-flow.md (area:* excluded)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "github"))
import setup_labels  # noqa: E402


def doc_labels() -> set[str]:
    text = (ROOT / "docs/system/issue-flow.md").read_text()
    section = text.split("\n## Labels", 1)[1].split("\n## ", 1)[0]
    names = set()
    for line in section.splitlines():
        m = re.match(r"\|\s*`([^`]+)`\s*\|", line)
        if m:
            names.add(m.group(1))
    return {n for n in names if not n.startswith("area:")}


def script_labels() -> set[str]:
    return {n for n, _, _ in setup_labels.LABELS if not n.startswith("area:")}


def test_every_script_label_is_documented():
    assert script_labels() - doc_labels() == set()


def test_every_documented_label_is_in_script():
    assert doc_labels() - script_labels() == set()


def test_twelve_labels():
    assert len(script_labels()) == 12


def test_every_area_in_claude_md_is_produced_by_script():
    """Areas have one home: the `Areas (labels)` line in CLAUDE.md; the script reads it (no literal list)."""
    line = setup_labels.areas_line(ROOT / "CLAUDE.md")
    assert line is not None, "CLAUDE.md ## Workflow lacks the `- Areas (labels):` line"
    produced = {n for n, _, _ in setup_labels.area_labels(ROOT / "CLAUDE.md")}
    assert produced == set(setup_labels.parse_areas(line))
    assert all(n.startswith("area:") for n in produced)
