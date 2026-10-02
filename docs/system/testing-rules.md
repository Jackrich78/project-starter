---
type: domain-doc
title: Testing rules
description: Test-fidelity principles each paid for by a green suite that hid a bug, the validation-depth ladder, backstop tests, and what each TDD agent sees; read before writing or reviewing tests.
tags: [testing, tdd, validation, qa]
---

# Testing rules

Every rule here exists because a suite went green while the code was broken. Conventions in short form load when you edit under `tests/` (`.claude/rules/testing.md`); which pyramid level a test belongs to is in the `test-strategy` skill.

## Principles

1. **Every test has been seen red, and "seen" means a mutation, not a docstring.** Write it against a deliberately broken version, or mutate the code once after writing (flip the guard to `if False:`, run, restore). A red recorded in prose is indistinguishable from a test written green-first. This routinely catches tests that pass with the guard deleted because they exit through a different path.
2. **Assert the discriminating half.** "Caution commands are logged" is satisfied by a hook that logs everything; the pair "and ordinary commands log nothing" proves selection. Ask what else would make this assertion pass.
3. **Stub at the boundary the code crosses, not one layer in.** Mocking the function that would call a binary passes while the real script exits 127 with nothing on any stream. Put a fake binary on `PATH` or a fake server on a port. Construct the type the code receives in production (dataclass, parsed JSON payload), never a convenient dict; for an integration, commit a real captured payload before building, because a fixture and a spec that share one wrong assumption both pass.
4. **Pin surprising behaviour with the reason; do not quietly change it.** Changing what users see is a decision, not a test fix.
5. **A skip or marker names what it is waiting for.** A bare skip is an exemption that never expires. A marker with no consumer (no config that deselects on it) is documentation, not a gate.
6. **Blast radius beats coverage.** Rank by what a user loses if it breaks silently, not by file size. Name the reader of an output before testing it; if nobody reads it, test it last.
7. **A test not in a CI lane does not exist.** Add the file to `.github/workflows/validate.yml` (or the runner `npm test` calls) in the commit that creates it (`cicd.md`).
8. **Verify delivery, not just correctness.** A hook's output can be exactly right and reach nobody: a bare JSON blob on stdout from a PostToolUse or Stop hook goes to neither the model nor the user; only `hookSpecificOutput.additionalContext` or `systemMessage` does. Test that the reader receives it.

**Layer 0: test the wiring before the logic.** The manifest (`settings.json`, agent frontmatter, skill registration) decides whether anything executes. Every unit test of a hook passes with the hook unregistered. Parse the manifest as a document and walk it (`hooks.md`). Scope the claim to what the check catches: a syntax check under an older interpreter finds syntax, not runtime incompatibility, and a check that silently runs under a *newer* interpreter than production is a confident pass asserting nothing; skip loudly instead.

**Before writing any test:** (1) does coverage exist already (`grep -rl "<module>" tests/`)? (2) does it actually run in CI (`grep -n tests/ .github/workflows/*.yml`)? Turning on coverage you already own beats writing more. (3) who reads the output? **A pass you did not predict is a finding**: it means your model of the system was wrong. And **a count of affected tests is a measurement**; get it by running the change, not by reading code.

## Validation-depth ladder

Declare, per ticket, how deeply the work was proven at runtime; use the deepest level that matches its surface. The ticket's `Validation` section carries the evidence.

| Depth | When | Evidence required |
|---|---|---|
| `unit` | pure compute: parsers, formatters, no I/O | tests covering each AC pass; no previously passing test regressed |
| `schema` | migrations, DB-only change | unit tests, a second run of the migration (idempotent), a sample query showing the expected state |
| `integration` | touches an external surface (API, queue, third-party service) | unit tests, a call against a sandbox or fake at the real boundary, an assertion that the downstream effect landed (the call happened *and* the record exists) |
| `frontend` | anything visual | unit tests, a scripted user journey, screenshots of the AC scenario |
| `manual` | needs human judgement (tone, "does it feel right") | explicit `[MANUAL]` checks with paste-able commands; the live-check sub-issue asks a human pass/fail/skip per check |

A change touching a schema and an external surface is `integration`. Without browser automation, `frontend` falls back to `manual` with a paste-able command. A confident pass that never exercised the surface is worse than a visible `manual`.

## Backstop tests

Prefer a few outcome-level tests that prove each acceptance criterion end to end, plus per-branch unit tests where branches are risky, over one test per AC line. Every AC maps to at least one test; every test traces to an AC. The `Tests:` line on a ticket maps AC ids to test paths, so QA can check the mapping mechanically. Time-dependent code gets time-independent tests: inject the clock, and use offsets larger than any period.

## The TDD trio: what each sees

Isolation prevents "I know how this should work" bias; each phase runs in a fresh context (`.claude/skills/tdd-red-green-refactor/`). The orchestrator runs the tests between phases and holds the gate.

| Phase | Agent | Sees | Must not see | Gate |
|---|---|---|---|---|
| RED | `tdd-test-writer` | the ticket's ACs and `Tests:` line | the plan or any implementation | every new test fails, for the right reason |
| GREEN | `tdd-implementer` (clean context) | the failing tests and surrounding code | the spec, plan or issue | target tests pass and the whole suite stays green |
| REFACTOR | `tdd-refactorer` (clean context) | tests and implementation | -- | tests stay green |

The implementer never edits, skips or loosens a test; a test that looks wrong is reported. If it can pass only by special-casing an input, it says so, because the test is under-specified. Each agent ends with `PASS`, `FAIL: <reason>` or `ESCALATION: <reason>` (`docs/guides/agent-harness-patterns.md`). `qa-reviewer` then checks the work in a clean context, including whether the tests discriminate (principles 1-2).
