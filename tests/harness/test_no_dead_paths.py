"""Every backticked relative path named in the governing files must exist.

A path that CLAUDE.md, a rule file, the wiki index or the README promises and the
repo does not have is the most confident kind of wrong a cold session can read.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    ROOT / "CLAUDE.md",
    ROOT / "README.md",
    ROOT / "docs" / "index.md",
    *sorted((ROOT / ".claude" / "rules").glob("*.md")),
    *sorted((ROOT / "docs" / "system").glob("*.md")),
    *sorted((ROOT / "docs" / "guides").glob("*.md")),
    *sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")),
]
# Backticked paths that start with a known top-level directory or dotdir.
PATH_RE = re.compile(r"`((?:docs|scripts|tests|\.claude|\.github)/[^`\s<>{}*|]+)[^`]*`")
# Markdown links in docs/index.md: [text](relative/path.md)
LINK_RE = re.compile(r"\]\(((?!https?://)[^)#]+\.md)\)")


def _refs(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    refs = set()
    for m in PATH_RE.finditer(text):
        ref = m.group(1).rstrip(".,;:)")
        ref = ref.split(":")[0]  # strip :line / :symbol suffixes
        if "<" in ref:
            continue
        if ref.startswith(".claude/qa/") or ref.startswith(".claude/salvage/") or ref.startswith(".claude/logs/"):
            continue  # runtime files, gitignored by design
        if ref == ".claude/CLAUDE.md":
            continue  # documented alternative location, not a file this repo ships
        refs.add(ref)
    return refs


def _ignored(ref: str) -> bool:
    """A path the repo deliberately does not ship (e.g. the private patterns file)."""
    import subprocess
    r = subprocess.run(["git", "check-ignore", "-q", ref], cwd=ROOT, capture_output=True)
    return r.returncode == 0


@pytest.mark.parametrize("file", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_backticked_paths_exist(file: Path):
    missing = sorted(r for r in _refs(file) if not (ROOT / r).exists() and not _ignored(r))
    assert not missing, f"{file.relative_to(ROOT)} names paths that do not exist: {missing}"


def test_docs_index_links_resolve():
    index = ROOT / "docs" / "index.md"
    missing = []
    for m in LINK_RE.finditer(index.read_text(encoding="utf-8")):
        target = (index.parent / m.group(1)).resolve()
        if not target.exists():
            missing.append(m.group(1))
    assert not missing, f"docs/index.md links to missing pages: {missing}"
