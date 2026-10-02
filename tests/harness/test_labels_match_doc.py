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
