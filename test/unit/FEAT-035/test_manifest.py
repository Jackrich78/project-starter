"""Tests for scripts/validate_manifest.py — FEAT-035 Work Item 7 (AC-027, AC-028).

Covers:
- validate_manifest.py passes on the real repo (all template-owned agents listed)
- Fails (exit 1) when a template-owned agent is dropped from the manifest
- Fails (exit 1) when the manifest lists a non-existent file
- Passes (exit 0) when an agent WITHOUT template-owned: true is absent from manifest
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "validate_manifest.py"
AGENTS_DIR = Path(__file__).resolve().parents[3] / ".claude" / "agents"


def run_validator(agents_dir: Path) -> subprocess.CompletedProcess:
    """Run validate_manifest.py against the given agents directory."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--agents-dir", str(agents_dir)],
        capture_output=True,
        text=True,
    )


class TestRealRepo:
    """validate_manifest.py must pass on the actual repository."""

    def test_passes_on_real_repo(self):
        """AC-028: bidirectional check passes on the live repo."""
        result = run_validator(AGENTS_DIR)
        assert result.returncode == 0, (
            f"validate_manifest.py failed on real repo:\n{result.stdout}\n{result.stderr}"
        )

    def test_output_mentions_ok(self):
        """Sanity: success output contains 'OK'."""
        result = run_validator(AGENTS_DIR)
        assert "OK" in result.stdout

    def test_manifest_has_version_header(self):
        """AC-030: .template-manifest must contain a template-version header."""
        manifest = AGENTS_DIR / ".template-manifest"
        assert manifest.exists(), ".template-manifest not found"
        content = manifest.read_text()
        assert "# template-version:" in content, (
            ".template-manifest is missing the '# template-version:' header"
        )

    def test_all_template_owned_agents_in_manifest(self):
        """AC-028: every agent with template-owned: true must be in .template-manifest."""
        manifest = AGENTS_DIR / ".template-manifest"
        manifest_entries = set()
        for line in manifest.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                manifest_entries.add(line)

        for md_file in sorted(AGENTS_DIR.glob("*.md")):
            if md_file.name in ("TEMPLATE.md", "README.md"):
                continue
            content = md_file.read_text()
            import re
            if re.search(r"^template-owned:\s*true\s*$", content, re.MULTILINE):
                assert md_file.name in manifest_entries, (
                    f"{md_file.name} has 'template-owned: true' but is not in .template-manifest"
                )

    def test_all_manifest_entries_exist(self):
        """AC-028: every .template-manifest entry must resolve to an existing file."""
        manifest = AGENTS_DIR / ".template-manifest"
        for line in manifest.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            target = AGENTS_DIR / line
            assert target.exists(), (
                f".template-manifest lists '{line}' but {target} does not exist"
            )


class TestFailureModes:
    """validate_manifest.py must exit 1 on specific violation types."""

    def _make_temp_agents_dir(self, tmp_path: Path) -> Path:
        """Copy the real agents dir to a temp location for mutation testing."""
        dest = tmp_path / "agents"
        shutil.copytree(AGENTS_DIR, dest)
        return dest

    def test_fails_when_flagged_agent_absent_from_manifest(self, tmp_path):
        """AC-028: a template-owned agent dropped from the manifest must fail.

        This exercises the 'silent non-propagation' case: someone adds a new
        core agent with template-owned: true but forgets to add it to the manifest.
        """
        agents_dir = self._make_temp_agents_dir(tmp_path)

        # Create a new template-owned agent not in the manifest
        orphan = agents_dir / "orphan-agent.md"
        orphan.write_text(textwrap.dedent("""\
            ---
            name: orphan-agent
            description: A test agent that is template-owned but not in the manifest.
            model: sonnet
            template-owned: true
            ---

            # Orphan Agent

            This agent exists to test that validate_manifest.py catches
            template-owned agents that are absent from .template-manifest.
        """))

        result = run_validator(agents_dir)
        assert result.returncode == 1, (
            "Expected exit 1 when a template-owned agent is absent from the manifest, "
            f"but got {result.returncode}.\nOutput:\n{result.stdout}"
        )
        assert "FLAGGED BUT NOT LISTED" in result.stdout, (
            f"Expected 'FLAGGED BUT NOT LISTED' in output.\nGot:\n{result.stdout}"
        )
        assert "orphan-agent.md" in result.stdout

    def test_fails_when_manifest_lists_missing_file(self, tmp_path):
        """AC-028: a manifest entry whose file does not exist must fail."""
        agents_dir = self._make_temp_agents_dir(tmp_path)

        # Add a ghost entry to the manifest
        manifest_path = agents_dir / ".template-manifest"
        existing = manifest_path.read_text()
        manifest_path.write_text(existing + "ghost-agent-that-does-not-exist.md\n")

        result = run_validator(agents_dir)
        assert result.returncode == 1, (
            "Expected exit 1 when manifest lists a non-existent file, "
            f"but got {result.returncode}.\nOutput:\n{result.stdout}"
        )
        assert "LISTED BUT MISSING" in result.stdout, (
            f"Expected 'LISTED BUT MISSING' in output.\nGot:\n{result.stdout}"
        )
        assert "ghost-agent-that-does-not-exist.md" in result.stdout

    def test_passes_when_non_template_agent_absent_from_manifest(self, tmp_path):
        """Non-template agents (no template-owned: true) may be absent — that is correct."""
        agents_dir = self._make_temp_agents_dir(tmp_path)

        # Create a user-created specialist without the flag — should not cause failure
        user_agent = agents_dir / "my-custom-specialist.md"
        user_agent.write_text(textwrap.dedent("""\
            ---
            name: my-custom-specialist
            description: A user-created specialist agent without template-owned flag.
            model: sonnet
            ---

            # My Custom Specialist

            This agent is created by the user and should not appear in the manifest.
        """))

        result = run_validator(agents_dir)
        assert result.returncode == 0, (
            "Expected exit 0 for a user agent without template-owned: true, "
            f"but got {result.returncode}.\nOutput:\n{result.stdout}"
        )

    def test_fails_when_manifest_missing_version_header(self, tmp_path):
        """The manifest must carry a # template-version: header."""
        agents_dir = self._make_temp_agents_dir(tmp_path)

        # Rewrite manifest stripping the version header
        manifest_path = agents_dir / ".template-manifest"
        lines = [
            line for line in manifest_path.read_text().splitlines()
            if "template-version:" not in line
        ]
        manifest_path.write_text("\n".join(lines) + "\n")

        result = run_validator(agents_dir)
        assert result.returncode == 1, (
            "Expected exit 1 when manifest lacks version header, "
            f"but got {result.returncode}.\nOutput:\n{result.stdout}"
        )
        assert "MANIFEST MISSING VERSION" in result.stdout

    def test_both_directions_fail_independently(self, tmp_path):
        """Both failure modes (flagged-unlisted AND listed-missing) can coexist."""
        agents_dir = self._make_temp_agents_dir(tmp_path)

        # Add a ghost entry to manifest
        manifest_path = agents_dir / ".template-manifest"
        manifest_path.write_text(manifest_path.read_text() + "ghost.md\n")

        # Also create a flagged-but-unlisted agent
        (agents_dir / "orphan2.md").write_text(
            "---\nname: orphan2\nmodel: sonnet\ntemplate-owned: true\n---\n# Orphan2\n"
        )

        result = run_validator(agents_dir)
        assert result.returncode == 1
        assert "FLAGGED BUT NOT LISTED" in result.stdout
        assert "LISTED BUT MISSING" in result.stdout
