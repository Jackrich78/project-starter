"""Tests for scripts/prune_agent_memory.py — FEAT-035 Work Item 1 (AC-003, AC-004).

Critical regression: --dry-run MUST NOT modify any file (AC-003).
Covers:
- dry-run produces no file modification under any circumstances (AC-003 regression)
- --apply removes [PRUNE] entries, keeps [KEEP] entries (AC-004)
- --apply is idempotent (AC-004)
- Auto-eligible entries (>50 days + codified reason) are shown as [AUTO] in dry-run
  but are only written when --apply is passed
- Recent entries are never auto-applied
- Missing target file is skipped gracefully
- Empty manifest is a no-op
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "prune_agent_memory.py"

assert SCRIPT.exists(), f"Script not found: {SCRIPT}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _old_date(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")


def _setup(tmp_path: Path, memory_files: dict[str, str], manifest: str) -> tuple[Path, Path]:
    repo = tmp_path
    mem_dir = repo / "memory" / "agents"
    mem_dir.mkdir(parents=True, exist_ok=True)
    for name, content in memory_files.items():
        (mem_dir / f"{name}.md").write_text(content, encoding="utf-8")
    manifest_path = repo / "manifest.md"
    manifest_path.write_text(manifest, encoding="utf-8")
    return manifest_path, repo


def _run(manifest: Path, repo: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(manifest),
            "--memory-dir",
            str(repo / "memory" / "agents"),
            "--repo-root",
            str(repo),
            *extra,
        ],
        capture_output=True,
        text=True,
    )


def _memfile(entries: list[str]) -> str:
    body = "\n".join(entries) + "\n" if entries else "\n"
    return f"# Test Agent Memory\n\n## Patterns\n\n{body}\n## Incidents\n\n## Task Outcomes\n"


# ---------------------------------------------------------------------------
# AC-003: dry-run MUST NOT modify any file (regression)
# ---------------------------------------------------------------------------

class TestDryRunNoWrite:
    """AC-003: --dry-run (default) must never mutate any file."""

    def test_dry_run_default_writes_nothing(self, tmp_path: Path):
        """Default invocation (no flags) must not write any file."""
        entry = "- [2026-05-11] Test pattern — [FEAT-001, pass]\n  Source: agent.db:event_id=1."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Test pattern"
              Reason: Now codified
              Last updated: 2026-05-11
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        original_content = (repo / "memory" / "agents" / "librarian.md").read_text()

        r = _run(mp, repo)  # no --apply flag

        after_content = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert r.returncode == 0
        assert after_content == original_content, (
            "dry-run (default) must not write any file — content was modified"
        )
        assert "[DRY]" in r.stdout or "[AUTO]" in r.stdout
        assert "dry-run" in r.stdout

    def test_explicit_dry_run_flag_writes_nothing(self, tmp_path: Path):
        """Explicit --dry-run must not write any file."""
        entry = "- [2026-05-11] Pattern B — [FEAT-001, pass]\n  Source: commit:abcdefg."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Pattern B"
              Reason: Now codified
              Last updated: 2026-05-11
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        original = (repo / "memory" / "agents" / "librarian.md").read_text()

        _run(mp, repo, "--dry-run")

        after = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert after == original, "--dry-run must not modify any file"

    def test_auto_eligible_entry_not_written_without_apply(self, tmp_path: Path):
        """An auto-eligible entry (>50 days + codified) must NOT be written without --apply.

        This is the critical regression: the source had a bug where auto-eligible entries
        were written even during --dry-run. That bug is fixed: --apply is required.
        """
        old = _old_date(60)
        entry = f"- [{old}] Old codified pattern — [FEAT-001, pass]\n  Source: agent.db:event_id=99."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Old codified pattern"
              Reason: Now codified in librarian.md § 1
              Last updated: {old}
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        original = (repo / "memory" / "agents" / "librarian.md").read_text()

        # Run WITHOUT --apply — auto-eligible entry must be shown as [AUTO] but NOT written.
        r = _run(mp, repo)

        after = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert after == original, (
            "auto-eligible entry must NOT be written without --apply (dry-run regression)"
        )
        assert "[AUTO]" in r.stdout, "auto-eligible entry should be labelled [AUTO] in output"
        assert "dry-run" in r.stdout

    def test_dry_run_beats_apply_when_both_set(self, tmp_path: Path):
        """When both --dry-run and --apply are passed, --dry-run wins (no write)."""
        entry = "- [2026-05-11] Conflict test — [FEAT-001, pass]\n  Source: commit:1234567."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Conflict test"
              Reason: Codified
              Last updated: 2026-05-11
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        original = (repo / "memory" / "agents" / "librarian.md").read_text()

        _run(mp, repo, "--dry-run", "--apply")

        after = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert after == original, "--dry-run must win over --apply"


# ---------------------------------------------------------------------------
# AC-004: --apply removes [PRUNE] and keeps [KEEP] (AC-004)
# ---------------------------------------------------------------------------

class TestApply:
    def test_apply_removes_prune_tagged_entries(self, tmp_path: Path):
        recent_a = _old_date(10)
        recent_b = _old_date(9)
        entry_a = f"- [{recent_a}] Pattern A — [FEAT-001, pass]\n  Source: agent.db:event_id=1."
        entry_b = f"- [{recent_b}] Pattern B — [FEAT-002, pass]\n  Source: commit:abcdefg."
        mfile = _memfile([entry_a, "", entry_b])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Pattern A"
              Reason: Now codified
              Last updated: {recent_a}

            - [KEEP] Line 9: "Pattern B"
              Reason: Active issue
              Last updated: {recent_b}
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        r = _run(mp, repo, "--apply")
        assert r.returncode == 0
        out = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert "Pattern A" not in out
        assert "Pattern B" in out
        assert "Applied: 1" in r.stdout
        assert "Keep: 1" in r.stdout

    def test_apply_auto_eligible_when_apply_flag_set(self, tmp_path: Path):
        """Auto-eligible entries ARE applied when --apply is passed."""
        old = _old_date(60)
        entry = f"- [{old}] Old codified pattern — [FEAT-001, pass]\n  Source: agent.db:event_id=99."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Old codified pattern"
              Reason: Now codified in librarian.md § 1
              Last updated: {old}
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        r = _run(mp, repo, "--apply")
        assert r.returncode == 0
        out = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert "Old codified pattern" not in out
        assert "Auto-applied: 1" in r.stdout

    def test_recent_entry_not_auto_applied(self, tmp_path: Path):
        """Recent entry (< 50 days old) is not auto-applied even with codified reason."""
        recent = _old_date(10)
        entry = f"- [{recent}] Recent pattern — [FEAT-001, pass]\n  Source: agent.db:event_id=1."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Recent pattern"
              Reason: Now codified
              Last updated: {recent}
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        r = _run(mp, repo)  # no --apply
        assert r.returncode == 0
        out = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert "Recent pattern" in out  # NOT auto-pruned
        assert "[DRY]" in r.stdout

    def test_old_but_not_codified_reason_not_auto_eligible(self, tmp_path: Path):
        """Old entry without codification keyword is not auto-eligible."""
        old = _old_date(60)
        entry = f"- [{old}] Old active pattern — [FEAT-001, pass]\n  Source: agent.db:event_id=99."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ## Pruning Recommendations

            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "Old active"
              Reason: Possible removal; still observed
              Last updated: {old}
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)
        r = _run(mp, repo)
        assert r.returncode == 0
        out = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert "Old active pattern" in out  # NOT auto-pruned (non-codification reason)


# ---------------------------------------------------------------------------
# AC-004: idempotency
# ---------------------------------------------------------------------------

class TestIdempotency:
    def test_apply_is_idempotent(self, tmp_path: Path):
        """Re-running --apply on an already-pruned manifest is a no-op."""
        old = _old_date(60)
        entry = f"- [{old}] One-shot pattern — [FEAT-001, pass]\n  Source: agent.db:event_id=99."
        mfile = _memfile([entry])
        manifest = textwrap.dedent(f"""\
            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "One-shot pattern"
              Reason: Codified
              Last updated: {old}
            """)
        mp, repo = _setup(tmp_path, {"librarian": mfile}, manifest)

        # First run applies.
        r1 = _run(mp, repo, "--apply")
        assert r1.returncode == 0
        content_after_first = (repo / "memory" / "agents" / "librarian.md").read_text()

        # Second run is a no-op.
        r2 = _run(mp, repo, "--apply")
        assert r2.returncode == 0
        content_after_second = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert content_after_first == content_after_second, "second run must not modify the file"
        assert "not found" in r2.stdout.lower() or "already pruned" in r2.stdout.lower()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestSnippetCollision:
    """A non-unique snippet must not silently delete the wrong bullet (QA finding).

    Two bullets share the substring 'auth'. With memory file laid out by _memfile,
    bullet A is at line 5 and bullet B at line 8.
    """

    def _two_auth_bullets(self) -> str:
        entry_a = "- [2026-05-11] fix auth bug — [FEAT-001, pass]\n  Source: commit:abcdefg."
        entry_b = "- [2026-05-12] auth still flaky — [FEAT-002, fail]\n  Source: commit:1234567."
        return _memfile([entry_a, "", entry_b])

    def test_ambiguous_snippet_removes_nothing(self, tmp_path: Path):
        """Snippet 'auth' matches both bullets and the line hint resolves neither -> skip, no write."""
        manifest = textwrap.dedent("""\
            ### memory/agents/librarian.md

            - [PRUNE] Line 1: "auth"
              Reason: Now codified
              Last updated: 2026-05-11
            """)
        mp, repo = _setup(tmp_path, {"librarian": self._two_auth_bullets()}, manifest)
        original = (repo / "memory" / "agents" / "librarian.md").read_text()

        r = _run(mp, repo, "--apply")

        after = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert r.returncode == 0
        assert after == original, "ambiguous snippet must not delete any bullet"
        assert "fix auth bug" in after and "auth still flaky" in after
        assert "SKIP-AMBIGUOUS" in r.stdout
        assert "Ambiguous: 1" in r.stdout

    def test_line_hint_disambiguates_collision(self, tmp_path: Path):
        """Snippet 'auth' matches both, but Line 5 uniquely selects bullet A."""
        manifest = textwrap.dedent(f"""\
            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "auth"
              Reason: Now codified
              Last updated: {_old_date(10)}
            """)
        mp, repo = _setup(tmp_path, {"librarian": self._two_auth_bullets()}, manifest)

        r = _run(mp, repo, "--apply")

        after = (repo / "memory" / "agents" / "librarian.md").read_text()
        assert r.returncode == 0
        assert "fix auth bug" not in after, "the hinted bullet A should be removed"
        assert "auth still flaky" in after, "bullet B must be untouched"
        assert "Applied: 1" in r.stdout

    def test_dry_run_preview_echoes_actual_bullet(self, tmp_path: Path):
        """The preview must show the matched bullet text, not the manifest snippet."""
        manifest = textwrap.dedent("""\
            ### memory/agents/librarian.md

            - [PRUNE] Line 5: "fix auth"
              Reason: Now codified
              Last updated: 2026-05-11
            """)
        mp, repo = _setup(tmp_path, {"librarian": self._two_auth_bullets()}, manifest)

        r = _run(mp, repo)  # dry-run

        # The manifest snippet is "fix auth"; the actual bullet carries "[FEAT-001, pass]".
        # Echoing the real line (not the snippet) is what makes a collision visible.
        assert "[FEAT-001, pass]" in r.stdout
        assert (repo / "memory" / "agents" / "librarian.md").read_text(), "file still present, unmodified"


class TestEdgeCases:
    def test_missing_target_file_skipped(self, tmp_path: Path):
        manifest = textwrap.dedent("""\
            ## Recs

            ### memory/agents/nonexistent.md

            - [PRUNE] Line 5: "Anything"
              Reason: Codified
              Last updated: 2026-01-01
            """)
        mp, repo = _setup(tmp_path, {}, manifest)
        r = _run(mp, repo, "--apply")
        assert r.returncode == 0
        assert "not found" in r.stdout

    def test_empty_manifest_no_op(self, tmp_path: Path):
        manifest = "## Pruning Recommendations\n\n(no actionable items)\n"
        mp, repo = _setup(tmp_path, {"librarian": _memfile([])}, manifest)
        r = _run(mp, repo)
        assert r.returncode == 0
        assert "no actionable" in r.stderr or "Prune: 0" in r.stdout
