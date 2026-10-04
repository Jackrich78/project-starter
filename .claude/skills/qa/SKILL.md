---
name: qa
description: "Clean-context QA review of a build: security, standards and spec, one verdict; the spine step after /build and before /commit. Use on \"run QA on #N\", \"/qa --issue N\", \"review this\", \"QA the build\", \"is #N ready to commit\", \"sweep the repo for security issues\". Forks into qa-reviewer so the reviewer never sees the builder conversation."
type: skill
context: fork
agent: qa-reviewer
argument-hint: "[--issue N | <path> | --sweep]"
---

# QA

Verdict marker, states and `gh` facts live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md) § QA verdict marker. Your agent definition holds the ladders, severities, stance and report format; this skill only sets the target and the hand-off. Target: `$ARGUMENTS`.

## Context

Runs after `/build` and before `/commit`, or any time on a path or the whole tree. You are forked: you have no builder context and must not seek it.

## Pattern

1. **Parse the target.** `--issue N` (issue mode), a file or directory path, or `--sweep` / empty (whole tree: SAST plus Grep patterns, Spec ladder N/A).
2. **`--issue N`: gather, read-only.**
   - `gh issue view N --comments` (ACs, `Tests:`, `Proof:`, close-out). A sub-issue's ACs may live in its parent body: read the parent too.
   - The diff: `git diff <base>...HEAD` on the issue branch, else the commits mentioning `#N` (`git log -E --grep "#N([^0-9]|$)"`), plus uncommitted work (`git diff HEAD`).
   - The test files named on the `Tests:` line.
   - **No code files in the diff** (docs, research, decision): review against the ticket's `Proof:` rubric with a challenger-style stance: is each claim sourced, does the artifact answer the AC, did it overreach. Mark each claim holds / does not hold with evidence.
3. **Path or sweep mode:** read the named scope; spec inferred from `git log` if a `#N` appears, else N/A (never a block).
4. **Review** per your agent definition, three independent ladders, claim-vs-evidence table, exactly one verdict.
5. **Report format.** In `--issue` mode the FIRST line is exactly `<!-- QA-VERDICT: APPROVED|NEEDS_FIXES|BLOCKED|BLOCKED SECURITY -->` (one value). Non-issue modes: return the report inline, no first-line marker, no report file under `docs`.

## Post (`--issue` mode)

Post the report yourself: `gh issue comment N --body-file -` with a quoted heredoc, marker line first, then the agent signature (issue-flow.md § Talking to the human). Return only the marker line and the comment URL. No other `gh` write, no `git push`.

The orchestrator acts on the verdict, all four branches:

- `APPROVED`: proceed to `/commit`.
- `NEEDS_FIXES`: fix Tier 1 items and re-run; the human may override with explicit confirmation.
- `BLOCKED`: tests fail or review incomplete; stop.
- `BLOCKED SECURITY`: stop, no override. Surface to the human with numbered options (the comment's Tier 2 section), one reversible decision each.

## Example

`/qa --issue 31`. Fork reads the issue and the 40-line diff, Semgrep not installed (noted), tests 41/41. Spec ladder: AC-002 covered by `test_expiry.py::rejects_expired_token`, the negative half untested: Standards HIGH, so `NEEDS_FIXES`. The fork posts the report, returns the marker and URL; the orchestrator fixes the test, re-runs.

## Anti-patterns

- Reading the builder conversation or a handover to "understand intent".
- Any `gh` write but the one verdict comment, or `git push`, from the fork.
- Treating `BLOCKED SECURITY` like `NEEDS_FIXES`.
- Approving with a skipped security step, or deleting a SAST finding.
- A marker anywhere but line 1, or more than one verdict value.
- Writing a report file under `docs/` instead of the issue comment.
- Reviewing a docs-only diff against code ladders instead of the `Proof:` rubric.
