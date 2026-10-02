---
name: debug
description: "Systematic bug investigation and fix. Use on \"this is broken\", \"it worked before\", \"find the root cause\", \"test is failing\", \"regression\", \"/debug <issue>\": logic errors, integration failures, performance regressions, test failures in existing code. Reproduce, find root cause, fix with a regression test, validate, record."
type: skill
argument-hint: "[issue description or #N]"
---

# Debug

## Context

Understand before fixing. Every fix ships with a regression test seen red, and the learning goes into the issue. Not for new features that never worked (use `/build`), approach questions (use `spike`), or general quality review (use `/qa`).

## Pattern

Each phase ends on its gate; do not start the next phase before it holds.

1. **Intake.** Parse symptom, expected versus actual behaviour, error text, repro steps. Read the issue if given (`gh issue view N`). Classify the bug (logic, integration, performance, test failure) and severity P0-P4; use the trees in `references/decision-trees.md`. UI bugs are logic bugs with the UI checklist there. Gate: type, severity, and repro steps (or "unknown") written down.
2. **Reproduce and diagnose.** Reproduce locally; gather stack trace, state, logs; check `git log` for what changed; form one hypothesis (which component, which input, expected versus actual). Unfamiliar library or cryptic error: dispatch `researcher`. Gate: the failure reproduces on demand.
3. **Root cause.** Test the hypothesis with a targeted probe, not a guess. Name the failure point as `file:line`, the blast radius (what else calls it), and why it was not caught. Gate: cause explained, not just located.
4. **Design the fix.** Prefer the root cause over the symptom. Several approaches or a blast radius over 5 files: ask `challenger`. Pick the test level with `test-strategy`. Gate: approach and test level chosen.
5. **Implement red-green.** Write the regression test, run it, see it fail for the right reason (RED). Implement the smallest fix (GREEN). Run the full suite. Gate: the new test passes, nothing else broke. A failure elsewhere means the fix is wrong or exposes a second bug; return to step 3, do not weaken the test.
6. **Validate.** Smoke the real path; for performance, re-measure; P0/P1 or anything touching auth, data handling or contracts: run `qa-reviewer`. Gate: verdict not BLOCKED.
7. **Record.** Post a close-out on the issue using `references/debug-report-template.md` (cause, fix, regression test, learned). Update any doc whose stated behaviour changed (`librarian` for cross-references). Then `/commit` with the test in the same commit.

Agent triggers in one line each: `researcher` unknown tech; `challenger` trade-offs or large blast radius; `qa-reviewer` P0/P1 or security; `librarian` doc drift.

## Example

"Discount applied twice on reorder." Intake: logic bug, P2, repro: place order, reorder. Diagnose: `calc_total` called from both `cart.py:41` and `checkout.py:88`. Root cause: reorder path re-applies the stored discounted price. RED: `test_reorder_discount_applied_once` fails with 90 != 81. Fix: apply discount only to list price. Suite green; close-out comment names the second caller as the reason it slipped through.

## Anti-patterns

- Fixing before reproducing: you cannot know it is fixed.
- Patching the symptom (a null check) while the cause stays.
- Skipping the regression test, or never seeing it fail.
- Weakening or deleting a test that fails after the fix.
- Over-engineering: a bug fix is not a refactor; file the refactor separately.
- Debugging against production data or state; reproduce locally.
- Burying the learning in chat instead of the issue.
