"""Tests for scripts/validate_agent_memory.py — FEAT-035 Work Item 1 (AC-001, AC-002).

Covers:
- Empty template passes (AC-002)
- All four citation formats pass (AC-002)
- Schema violations exit 1: forbidden H2, missing citation, bad date, missing H1, duplicate H2
- >100-line file warns but does not exit 1 (AC-002)
- --agent filter narrows scope
- fixtures/bad_memory.md is rejected by the validator
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "validate_agent_memory.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

assert SCRIPT.exists(), f"Script not found: {SCRIPT}"


def _write(memory_dir: Path, name: str, content: str) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = memory_dir / f"{name}.md"
    path.write_text(content, encoding="utf-8")
    return path


def _run(memory_dir: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--memory-dir", str(memory_dir), *args],
        capture_output=True,
        text=True,
    )


EMPTY_TEMPLATE = textwrap.dedent("""\
    <!-- schema comment -->

    # Example Agent Memory

    > Self-retro file.

    ## Patterns

    ## Incidents

    ## Task Outcomes
    """)


# ---------------------------------------------------------------------------
# Empty template
# ---------------------------------------------------------------------------

class TestEmptyTemplate:
    def test_empty_template_passes(self, tmp_path: Path):
        _write(tmp_path, "example-agent", EMPTY_TEMPLATE)
        r = _run(tmp_path)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "OK" in r.stdout

    def test_multiple_empty_templates_pass(self, tmp_path: Path):
        for name in ("tdd-test-writer", "tdd-implementer", "qa-reviewer"):
            _write(tmp_path, name, EMPTY_TEMPLATE.replace("Example Agent", name))
        r = _run(tmp_path)
        assert r.returncode == 0
        assert "3 memory file(s)" in r.stdout

    def test_readme_and_template_excluded_from_scan(self, tmp_path: Path):
        """README.md and TEMPLATE.md must not be treated as agent memory files."""
        _write(tmp_path, "example-agent", EMPTY_TEMPLATE)
        # Write README.md and TEMPLATE.md with invalid schema — validator must skip them.
        (tmp_path / "README.md").write_text("no headings at all", encoding="utf-8")
        (tmp_path / "TEMPLATE.md").write_text("## Patterns\nno h1", encoding="utf-8")
        r = _run(tmp_path)
        assert r.returncode == 0, r.stdout + r.stderr
        # Only the one real agent file should be reported.
        assert "1 memory file(s)" in r.stdout


# ---------------------------------------------------------------------------
# Valid entries — all four citation formats (AC-002)
# ---------------------------------------------------------------------------

class TestValidEntries:
    def test_entry_with_agent_db_citation(self, tmp_path: Path):
        content = EMPTY_TEMPLATE.replace(
            "## Patterns\n",
            "## Patterns\n- [2026-05-12] Test pattern — [FEAT-001, pass]\n  Insight here. Source: agent.db:event_id=2847.\n",
        )
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 0, r.stdout

    def test_entry_with_commit_sha(self, tmp_path: Path):
        content = EMPTY_TEMPLATE.replace(
            "## Incidents\n",
            "## Incidents\n- [2026-05-12] Broke X — [FEAT-001]\n  Detail. Source: commit:3a7f2cd.\n",
        )
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 0

    def test_entry_with_file_line_citation(self, tmp_path: Path):
        content = EMPTY_TEMPLATE.replace(
            "## Task Outcomes\n",
            "## Task Outcomes\n- [2026-05-12] FEAT-001: pass — done.\n  Source: docs/qa/feat-001-qa.md:42.\n",
        )
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 0

    def test_entry_with_qa_report_citation(self, tmp_path: Path):
        content = EMPTY_TEMPLATE.replace(
            "## Patterns\n",
            "## Patterns\n- [2026-05-12] Pattern — [FEAT-001, pass]\n  Detail. Source: qa:docs/qa/feat-001.md#findings.\n",
        )
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 0


# ---------------------------------------------------------------------------
# Schema violations — exit 1 (AC-002)
# ---------------------------------------------------------------------------

class TestFailures:
    def test_forbidden_h2_section_fails(self, tmp_path: Path):
        content = EMPTY_TEMPLATE + "\n## Random Other Section\n"
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 1
        assert "forbidden H2" in r.stdout

    def test_entry_without_citation_fails(self, tmp_path: Path):
        content = EMPTY_TEMPLATE.replace(
            "## Patterns\n",
            "## Patterns\n- [2026-05-12] Pattern without source — [FEAT-001, pass]\n  Just prose, no citation here.\n",
        )
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 1
        assert "missing citation" in r.stdout

    def test_entry_with_wrong_date_format_fails(self, tmp_path: Path):
        content = EMPTY_TEMPLATE.replace(
            "## Patterns\n",
            "## Patterns\n- [May 12 2026] Bad date — [FEAT-001, pass]\n  Source: agent.db:event_id=1.\n",
        )
        _write(tmp_path, "example-agent", content)
        r = _run(tmp_path)
        assert r.returncode == 1
        assert "must start with" in r.stdout

    def test_missing_h1_fails(self, tmp_path: Path):
        content = "## Patterns\n\n## Incidents\n\n## Task Outcomes\n"
        _write(tmp_path, "x", content)
        r = _run(tmp_path)
        assert r.returncode == 1
        assert "exactly 1 H1" in r.stdout

    def test_duplicate_h2_fails(self, tmp_path: Path):
        content = "# X\n\n## Patterns\n\n## Patterns\n\n## Incidents\n\n## Task Outcomes\n"
        _write(tmp_path, "x", content)
        r = _run(tmp_path)
        assert r.returncode == 1
        assert "duplicate H2" in r.stdout

    def test_bad_memory_fixture_is_rejected(self, tmp_path: Path):
        """fixtures/bad_memory.md must fail validation (AC-002 regression fixture)."""
        import shutil
        shutil.copy(FIXTURES_DIR / "bad_memory.md", tmp_path / "bad-agent.md")
        r = _run(tmp_path)
        assert r.returncode == 1, f"Expected exit 1 for bad_memory.md, got {r.returncode}:\n{r.stdout}"


# ---------------------------------------------------------------------------
# Line-cap warning (AC-002 — warns, does not fail)
# ---------------------------------------------------------------------------

class TestLineCap:
    def test_overcap_file_warns_not_fails(self, tmp_path: Path):
        # Build a >100-line file with otherwise valid content.
        body = "# X\n\n## Patterns\n\n## Incidents\n\n## Task Outcomes\n\n"
        padding = "\n".join(["<!-- pad -->"] * 110)
        _write(tmp_path, "x", body + padding + "\n")
        r = _run(tmp_path)
        assert r.returncode == 0, r.stdout + r.stderr  # warnings only, not error
        assert "WARN" in r.stdout


# ---------------------------------------------------------------------------
# CLI behaviour
# ---------------------------------------------------------------------------

class TestCLI:
    def test_agent_filter(self, tmp_path: Path):
        _write(tmp_path, "good-agent", EMPTY_TEMPLATE)
        # This file would fail if scanned — filter must prevent it.
        (tmp_path / "bad-agent.md").write_text("garbage no headings", encoding="utf-8")
        r = _run(tmp_path, "--agent", "good-agent")
        assert r.returncode == 0
        assert "1 memory file" in r.stdout

    def test_agent_filter_missing(self, tmp_path: Path):
        _write(tmp_path, "good-agent", EMPTY_TEMPLATE)
        r = _run(tmp_path, "--agent", "nonexistent")
        assert r.returncode == 2

    def test_empty_dir_returns_ok(self, tmp_path: Path):
        """A memory dir with no *.md agent files (only .gitkeep) should pass cleanly."""
        (tmp_path / ".gitkeep").touch()
        r = _run(tmp_path)
        assert r.returncode == 0
        assert "0 memory file(s)" in r.stdout
