---
name: test-strategy
description: "Decide the test approach and pyramid level for a piece of behaviour. Use when annotating test stubs in /blueprint, routing them in /build, writing tests, or judging whether a test sits at the right level: \"what kind of test is this\", \"unit or integration\", \"do we need e2e\"."
type: skill
---

# Test Strategy

## Context

Pick the cheapest level that proves the behaviour, route each stub to its directory, and keep tests at the right pyramid level. Operational test rules (seen red, discriminating assertion, boundary stubs, CI lane): `docs/system/testing-rules.md`.

## Pattern

1. **Walk the tree in order** for each behaviour; first YES wins, default is `tdd`:
   - complete user flow across pages: `e2e` -> `tests/e2e/`
   - API-to-DB round-trip, middleware chain, multi-service flow: `integration` -> `tests/integration/<area>/`
   - UI component rendering or interaction: `component-test` -> `tests/component/<area>/`
   - logic, pure function, utility, handler, hook: `tdd` -> `tests/unit/<area>/`
   - exploratory prototype or spike: manual only, no stub
2. **Annotate** the stub's first line: `// @test-approach: tdd | component-test | integration | e2e`. It sets directory and build routing: `tdd` goes to the TDD sub-agents (`tdd-red-green-refactor`); `component-test` and `integration` run inline red-green (read stub, write real test, see it fail, implement, see it pass, review); `e2e` runs inline with a browser tool if available, else write the steps as a manual checklist and let `qa-reviewer` flag "E2E automated coverage: pending".
3. **Name tests by acceptance criterion**: `describe('AC-3: <criterion>')`, where the AC numbers come from the issue body. This makes coverage greppable: `grep -rhoE "AC-[0-9]+" tests/ | sort -u`.
4. **Apply the backstop rule.** Write a few outcome-level tests that pin the behaviour end to end, plus per-branch unit tests where branching logic lives. Do not write one test per acceptance-criterion line; an exhaustive list of near-duplicates buys no extra confidence and breaks on every refactor.
5. **Watch the boundaries.** Integration is not a unit test with extra setup, and not an e2e without a browser. Mock at the boundary the code crosses, not at its own internals.

Read `references/examples.md` for a full example per level and `references/validation-criteria.md` for pyramid rules, anti-patterns and AC coverage checks.

## Example

Behaviour: "creating a user returns 201 and persists." Tree: API-to-DB round-trip, so `integration`, file `tests/integration/<area>/user-api.test.ts`, first line `// @test-approach: integration`, `describe('AC-2: User creation API')`. Also a unit test for the email-format branch (`tdd`), not a unit test per AC bullet.

## Anti-patterns

- Defaulting everything to e2e: slow, flaky, and it localises nothing.
- One test per AC line instead of backstop plus branch tests.
- Mocking the module under test, so the test mirrors the implementation.
- Skipping the annotation: the stub falls to the default and routes wrongly.
- Asserting on private state or mock call counts rather than observable outcomes.
