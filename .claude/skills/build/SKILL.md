---
name: build
description: "Build exactly one GitHub sub-issue end to end with TDD, review and QA; the spine step after to-tickets, ending in /qa --issue N and /commit. Use on \"build #N\", \"implement #N\", \"work the next ticket\", \"/build\". Claims the issue, writes failing tests per acceptance criterion, implements, refactors. Escalates to /blueprint when there is no parent issue."
type: skill
argument-hint: "[#N]"
---

# Build

States, labels, claim protocol, modes and the close-out shape live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md). The loop mechanics live in `tdd-red-green-refactor`. This skill is the sequence and its gates.

## Context

One `ready-for-agent` ticket at a time, sized per issue-flow.md § Sizing; `ready-for-agent` is gate 1, so no fresh "next" is needed. Loop and stops: issue-flow.md § Agent pickup protocol.

## Pattern

1. **Preflight.** `scripts/github/check_gh.sh` passes; `.claude/agents/{tdd-test-writer,tdd-implementer,tdd-refactorer,qa-reviewer}.md` and the three templates under `.claude/skills/tdd-red-green-refactor/templates/` exist; read the integration mode from CLAUDE.md `## Workflow`. Anything missing: stop and report which.
2. **Pick and claim** through `work-issue` (named issue, else frontier). **Claim before any other write.** No parent issue behind a sub-issue, or nothing to claim: escalate to `/blueprint`, never improvise a plan.
3. **`pr` mode:** create the branch with `gh issue develop N --checkout --name issue-N-<slug>` (issue-flow.md § Integration modes). `direct` mode: stay put.
4. **Stubs.** Read the `Tests:` line (AC ids -> test paths). For each AC id create one failing stub at its path (`fail("RED stub: AC-00X")` in the project's runner), AC id in the test name. No `Tests:` line: not ready, pickup step 8 (non-code work has a `Proof:` line: build that artifact, skip to step 6).
5. **Run `tdd-red-green-refactor`** on the stubs. Gates it enforces: RED proven before GREEN; suite green after REFACTOR. Keep the RED output for the close-out `Proof:`.
6. **`/simplify`** (native) on the changed code; rerun the suite. Then **`/security-review`** (native); fix findings, rerun the suite.
7. **`/qa --issue N`.** The fork posts its own verdict and returns the marker and URL.
   - `APPROVED`: step 8.
   - `NEEDS_FIXES`: fix, rerun the suite, re-run `/qa --issue N`. At most **3** iterations, then stop and report what was tried.
   - `BLOCKED` or `BLOCKED SECURITY`: stop. Surface to the human with numbered options; never self-approve.
8. **`/commit`** (`Closes #N` or `Refs #N` per mode). `/commit` runs `/code-review --fix` (at most 2 passes) in `pr` mode. Then the `work-issue` finish steps: post the close-out hand-off (`Proof:` includes the RED output), parent cascade if last sibling.

Then take the next ready ticket (issue-flow.md, Standing permission).

## Example

`/build #31` ("reject expired tokens", `Tests: AC-002 -> tests/auth/test_expiry.py`). Preflight green, claimed, branch `issue-31-expired-tokens`. One stub generated; test-writer returns RED output; implementer GREEN; refactorer "No refactoring needed". `/simplify` trims one helper, `/security-review` clean. QA returns NEEDS_FIXES (negative case untested); fix, re-QA, APPROVED. `/commit`, PR opened, hand-off posted, next ticket.

## Anti-patterns

- Implementing before RED is proven, or accepting a test that was never seen failing.
- Showing the implementer the spec or plan; it sees failing tests only.
- Picking a parent issue, or stopping to ask between the gates.
- Looping QA past 3 iterations, or treating `BLOCKED SECURITY` like `NEEDS_FIXES`.
- Improvising scope when the ticket is thin: comment, `needs-info`, next ticket (work-issue step 8).
- Skipping `/simplify` and `/security-review` so opus QA spends its run on trivia.
- Restating claim or close-out commands here instead of pointing at issue-flow.md.
