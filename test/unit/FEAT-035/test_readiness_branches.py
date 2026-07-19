"""
AC-035-021, AC-035-022: Parse-level tests asserting that:
  1. The auto-harness-readiness SKILL.md documents all three readiness verdicts
     and that every caller branch table handles all three values.
  2. The /commit branch table distinguishes BLOCKED (refuse, no override)
     from NEEDS_FIXES (warn + override-with-confirmation).

These are documentation contract tests — they parse markdown and assert that
the required branches are present and correctly specified. They do not execute
the harness; they verify the harness contract is documented completely.
"""

from pathlib import Path
import re
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]

SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "auto-harness-readiness" / "SKILL.md"
COMMIT_PATH = REPO_ROOT / ".claude" / "commands" / "commit.md"
BUILD_PATH = REPO_ROOT / ".claude" / "commands" / "build.md"
RETRO_PATH = REPO_ROOT / ".claude" / "commands" / "retro.md"
QUALITY_GATES_PATH = REPO_ROOT / "docs" / "guides" / "quality-gates.md"
QA_REVIEWER_PATH = REPO_ROOT / ".claude" / "agents" / "qa-reviewer.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    assert path.exists(), f"Expected file not found: {path}"
    return path.read_text()


# ---------------------------------------------------------------------------
# AC-035-022: Readiness skill documents all three verdict values
# ---------------------------------------------------------------------------

class TestReadinessSkillVerdicts:
    """The SKILL.md must document ready, nearly-ready, and not-ready."""

    def test_skill_file_exists(self):
        assert SKILL_PATH.exists(), f"Readiness skill not found at {SKILL_PATH}"

    def test_all_three_readiness_values_present(self):
        text = read(SKILL_PATH)
        for verdict in ("READINESS: ready", "READINESS: nearly-ready", "READINESS: not-ready"):
            assert verdict in text, (
                f"Readiness skill missing verdict '{verdict}'. "
                "All three branches must be documented."
            )

    def test_ready_verdict_at_line_start(self):
        """READINESS: token must be documented as appearing at line start (grep-able)."""
        text = read(SKILL_PATH)
        # The skill should explain that READINESS: appears at start of line
        assert "start of a line" in text or "line start" in text, (
            "Skill must document that READINESS: appears at the start of a line "
            "so callers can grep for it."
        )

    def test_caller_contract_section_present(self):
        """Skill must document that all three branches must be handled."""
        text = read(SKILL_PATH)
        assert "Caller Contract" in text or "all three" in text.lower(), (
            "Readiness skill must include a caller contract stating all three "
            "branches must be handled."
        )

    def test_nearly_ready_produces_prompt_not_halt(self):
        """nearly-ready must prompt the user, not halt the build."""
        text = read(SKILL_PATH)
        # Find the Caller Contract or verdict table section — search from Caller Contract heading
        # to capture the action words that appear in context with nearly-ready
        caller_section_idx = text.find("Caller Contract")
        assert caller_section_idx != -1, "Caller Contract section not found in SKILL.md"
        caller_section = text[caller_section_idx: caller_section_idx + 1500]
        assert "nearly-ready" in caller_section, (
            "nearly-ready must appear in the Caller Contract section."
        )
        assert any(word in caller_section.lower() for word in ("confirm", "prompt", "proceed on")), (
            "nearly-ready branch must prompt the user and allow proceed on confirmation, "
            "not unconditionally halt. Context: " + caller_section[:400]
        )

    def test_not_ready_produces_halt(self):
        """not-ready must halt the build."""
        text = read(SKILL_PATH)
        caller_section_idx = text.find("Caller Contract")
        assert caller_section_idx != -1, "Caller Contract section not found in SKILL.md"
        caller_section = text[caller_section_idx: caller_section_idx + 1500]
        assert "not-ready" in caller_section, (
            "not-ready must appear in the Caller Contract section."
        )
        assert any(word in caller_section.lower() for word in ("halt", "do not proceed", "blocked", "stop")), (
            "not-ready branch must halt the build, not proceed. Context: " + caller_section[:400]
        )


# ---------------------------------------------------------------------------
# AC-035-021: /commit gate distinguishes BLOCKED from NEEDS_FIXES
# ---------------------------------------------------------------------------

class TestCommitBranchTable:
    """The /commit command must have separate handling for BLOCKED and NEEDS_FIXES."""

    def test_commit_file_exists(self):
        assert COMMIT_PATH.exists(), f"commit.md not found at {COMMIT_PATH}"

    def test_blocked_verdict_present(self):
        text = read(COMMIT_PATH)
        assert "BLOCKED" in text, "commit.md must document the BLOCKED verdict branch."

    def test_needs_fixes_verdict_present(self):
        text = read(COMMIT_PATH)
        assert "NEEDS_FIXES" in text, "commit.md must document the NEEDS_FIXES verdict branch."

    def test_approved_verdict_present(self):
        text = read(COMMIT_PATH)
        assert "APPROVED" in text, "commit.md must document the APPROVED verdict branch."

    def test_blocked_is_hard_refuse_no_override(self):
        """BLOCKED must be a hard refuse with no override option."""
        text = read(COMMIT_PATH)
        # Find the BLOCKED section
        blocked_idx = text.find("BLOCKED")
        assert blocked_idx != -1
        # Look in context around first BLOCKED mention for refuse/no override language
        context = text[blocked_idx: blocked_idx + 800]
        assert any(phrase in context.lower() for phrase in (
            "no override", "cannot proceed", "refuse", "refused", "blocked until"
        )), (
            "BLOCKED verdict must hard-refuse the commit with no override option. "
            f"Context around BLOCKED: {context[:400]}"
        )

    def test_needs_fixes_allows_override_with_confirmation(self):
        """NEEDS_FIXES must warn and allow override with explicit confirmation."""
        text = read(COMMIT_PATH)
        needs_fixes_idx = text.find("NEEDS_FIXES")
        assert needs_fixes_idx != -1
        # Look in a broader window since NEEDS_FIXES might appear multiple times
        context_start = max(0, needs_fixes_idx - 100)
        context = text[context_start: needs_fixes_idx + 1000]
        assert any(phrase in context.lower() for phrase in (
            "override", "explicit confirmation", "confirms override", "confirm"
        )), (
            "NEEDS_FIXES verdict must allow commit with explicit user override/confirmation. "
            f"Context: {context[:400]}"
        )

    def test_blocked_and_needs_fixes_are_distinct(self):
        """BLOCKED and NEEDS_FIXES must be handled in separate branches."""
        text = read(COMMIT_PATH)
        # Both must appear separately — not combined as "BLOCKED or NEEDS_FIXES → same action"
        blocked_count = text.count("BLOCKED")
        needs_fixes_count = text.count("NEEDS_FIXES")
        assert blocked_count >= 1, "BLOCKED must appear at least once"
        assert needs_fixes_count >= 1, "NEEDS_FIXES must appear at least once"
        # The old combined handling "If BLOCKED or NEEDS_FIXES:" must be gone
        assert "BLOCKED or NEEDS_FIXES" not in text, (
            "commit.md must NOT combine BLOCKED and NEEDS_FIXES into one branch. "
            "They require different handling: BLOCKED=refuse, NEEDS_FIXES=warn+override."
        )

    def test_branch_table_covers_four_cases(self):
        """Branch table must cover APPROVED, NEEDS_FIXES, BLOCKED, and no-report cases."""
        text = read(COMMIT_PATH)
        for verdict in ("APPROVED", "NEEDS_FIXES", "BLOCKED", "No report"):
            assert verdict in text, (
                f"commit.md branch table is missing case: '{verdict}'"
            )


# ---------------------------------------------------------------------------
# AC-035-022: /build command documents readiness three-branch handling
# ---------------------------------------------------------------------------

class TestBuildReadinessBranching:
    """The /build command must document all three readiness branches."""

    def test_build_file_exists(self):
        assert BUILD_PATH.exists(), f"build.md not found at {BUILD_PATH}"

    def test_build_references_readiness_skill(self):
        text = read(BUILD_PATH)
        assert "auto-harness-readiness" in text or "readiness" in text.lower(), (
            "build.md must reference the readiness gate."
        )

    def test_build_handles_ready_branch(self):
        text = read(BUILD_PATH)
        assert "ready" in text, "build.md must document the 'ready' readiness branch."

    def test_build_handles_nearly_ready_branch(self):
        text = read(BUILD_PATH)
        assert "nearly-ready" in text, (
            "build.md must document the 'nearly-ready' readiness branch."
        )

    def test_build_handles_not_ready_branch(self):
        text = read(BUILD_PATH)
        assert "not-ready" in text, (
            "build.md must document the 'not-ready' readiness branch."
        )

    def test_build_fidelity_gate_present(self):
        text = read(BUILD_PATH)
        assert "touches_external_api" in text or "fidelity" in text.lower(), (
            "build.md must reference the fidelity gate (touches_external_api)."
        )


# ---------------------------------------------------------------------------
# AC-035-022: /retro command documents readiness three-branch handling
# ---------------------------------------------------------------------------

class TestRetroReadinessBranching:
    """The /retro command must document all three readiness branches."""

    def test_retro_file_exists(self):
        assert RETRO_PATH.exists(), f"retro.md not found at {RETRO_PATH}"

    def test_retro_handles_ready_branch(self):
        text = read(RETRO_PATH)
        assert "READINESS: ready" in text or (
            "ready" in text and "readiness" in text.lower()
        ), "retro.md must document the 'ready' readiness branch."

    def test_retro_handles_nearly_ready_branch(self):
        text = read(RETRO_PATH)
        assert "nearly-ready" in text, (
            "retro.md must document the 'nearly-ready' readiness branch."
        )

    def test_retro_handles_not_ready_branch(self):
        text = read(RETRO_PATH)
        assert "not-ready" in text, (
            "retro.md must document the 'not-ready' readiness branch."
        )

    def test_retro_references_agile_coach_loop(self):
        text = read(RETRO_PATH)
        assert "Agile Coach" in text or "agile-coach" in text or "learning loop" in text.lower(), (
            "retro.md must reference the Agile Coach learning loop."
        )


# ---------------------------------------------------------------------------
# AC-035-020: QA reviewer documents three-value verdict set
# ---------------------------------------------------------------------------

class TestQAReviewerVerdictSet:
    """qa-reviewer.md must document exactly three verdict values."""

    def test_qa_reviewer_file_exists(self):
        assert QA_REVIEWER_PATH.exists(), f"qa-reviewer.md not found at {QA_REVIEWER_PATH}"

    def test_qa_reviewer_has_model_opus(self):
        text = read(QA_REVIEWER_PATH)
        assert "model: opus" in text, (
            "qa-reviewer.md frontmatter must include 'model: opus'."
        )

    def test_qa_reviewer_has_template_owned(self):
        text = read(QA_REVIEWER_PATH)
        assert "template-owned: true" in text, (
            "qa-reviewer.md frontmatter must include 'template-owned: true'."
        )

    def test_qa_reviewer_documents_approved_verdict(self):
        text = read(QA_REVIEWER_PATH)
        assert "APPROVED" in text, "qa-reviewer.md must document the APPROVED verdict."

    def test_qa_reviewer_documents_needs_fixes_verdict(self):
        text = read(QA_REVIEWER_PATH)
        assert "NEEDS_FIXES" in text, "qa-reviewer.md must document the NEEDS_FIXES verdict."

    def test_qa_reviewer_documents_blocked_verdict(self):
        text = read(QA_REVIEWER_PATH)
        assert "BLOCKED" in text, "qa-reviewer.md must document the BLOCKED verdict."

    def test_qa_reviewer_caller_contract_present(self):
        text = read(QA_REVIEWER_PATH)
        assert "Caller Contract" in text, (
            "qa-reviewer.md must include a 'Caller Contract' section."
        )

    def test_qa_reviewer_all_branches_must_be_handled(self):
        text = read(QA_REVIEWER_PATH)
        assert "all three branches" in text.lower() or "all three" in text.lower(), (
            "qa-reviewer.md must state that all three branches must be handled by the caller."
        )

    def test_qa_reviewer_reads_handover_not_conversation(self):
        text = read(QA_REVIEWER_PATH)
        assert "handover" in text.lower(), (
            "qa-reviewer.md must reference reading the handover document."
        )
        assert "not the builder" in text.lower() or "not the builder's" in text.lower() or \
               "not builder" in text.lower() or "NOT the builder" in text, (
            "qa-reviewer.md must explicitly state it reads the handover, not the builder's conversation."
        )


# ---------------------------------------------------------------------------
# AC-035-016: quality-gates.md documents all four gates
# ---------------------------------------------------------------------------

class TestQualityGatesDocument:
    """quality-gates.md must have four named sections with required content."""

    def test_quality_gates_file_exists(self):
        assert QUALITY_GATES_PATH.exists(), (
            f"quality-gates.md not found at {QUALITY_GATES_PATH}"
        )

    def test_discover_gate_present(self):
        text = read(QUALITY_GATES_PATH)
        assert "Discover" in text, "quality-gates.md must have a Discover gate section."

    def test_fidelity_gate_present(self):
        text = read(QUALITY_GATES_PATH)
        assert "Fidelity" in text, "quality-gates.md must have a Fidelity gate section."

    def test_qa_reviewer_gate_present(self):
        text = read(QUALITY_GATES_PATH)
        assert "QA Reviewer" in text or "QA Review" in text, (
            "quality-gates.md must have a QA Reviewer gate section."
        )

    def test_readiness_gate_present(self):
        text = read(QUALITY_GATES_PATH)
        assert "Readiness" in text, "quality-gates.md must have a Readiness gate section."

    def test_discover_is_stack_neutral(self):
        text = read(QUALITY_GATES_PATH)
        # Must not assume Postgres is the only stack
        # Should mention it as an example, not a global assumption
        assert "example" in text.lower() or "substitute" in text.lower(), (
            "Discover gate must be stack-neutral and present Postgres as an example, "
            "not a global assumption."
        )
        assert "Postgres" in text or "postgres" in text.lower(), (
            "Discover gate must include a labeled Postgres example."
        )

    def test_fidelity_is_opt_in(self):
        text = read(QUALITY_GATES_PATH)
        assert "touches_external_api" in text, (
            "Fidelity gate must reference the 'touches_external_api' opt-in flag."
        )
        assert "no-op" in text.lower() or "default" in text.lower(), (
            "Fidelity gate must document that it is a no-op by default."
        )

    def test_fidelity_is_warn_not_hard_block(self):
        text = read(QUALITY_GATES_PATH)
        # Find the fidelity section
        fidelity_idx = text.find("Fidelity")
        context = text[fidelity_idx: fidelity_idx + 2000]
        assert "warn" in context.lower() or "confirmation" in context.lower(), (
            "Fidelity gate must warn and require confirmation, not hard-block."
        )
        assert "NOT hard-block" in context or "does not hard-block" in context.lower() or \
               "does NOT hard-block" in context or "not hard-block" in context.lower(), (
            "Fidelity gate must explicitly state it does NOT hard-block."
        )

    def test_readiness_three_branches_documented(self):
        text = read(QUALITY_GATES_PATH)
        for verdict in ("ready", "nearly-ready", "not-ready"):
            assert verdict in text, (
                f"quality-gates.md Readiness section missing verdict '{verdict}'."
            )

    def test_qa_reviewer_three_verdicts_documented(self):
        text = read(QUALITY_GATES_PATH)
        for verdict in ("APPROVED", "NEEDS_FIXES", "BLOCKED"):
            assert verdict in text, (
                f"quality-gates.md QA Reviewer section missing verdict '{verdict}'."
            )
