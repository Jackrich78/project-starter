---
name: tdd-red-green-refactor
description: "Run RED, GREEN, REFACTOR with three isolated sub-agents, each in a clean context, with a gate command between steps. Use when /build reaches the test stubs, on \"do this with TDD\", \"write the failing tests first\", \"red green refactor\". Fills the dispatch prompts in templates/ and keeps the RED output as proof."
type: skill
---

# TDD red-green-refactor

Called by `/build` after it generated one failing stub per AC id on the ticket's `Tests:` line. Test philosophy: `test-strategy` skill and `.claude/rules/testing.md`. Claim, close-out and QA mechanics: `docs/system/issue-flow.md`.

## Context

Isolation is the point: whoever writes the test must not know the code, whoever writes the code must not know the spec, so tests cannot be bent to fit an implementation. You, the orchestrator, are the only one holding all three views.

## Pattern

Hand-offs are files, never pasted summaries. Make a scratch dir outside the tree (`mktemp -d`); the RED run goes to `red.txt`, the GREEN run to `green.txt`.

1. **RED: `tdd-test-writer`.** Fill `templates/test-writer-prompt.md` (`{issue}`, `{ac_ids}`, `{ac_text}`, `{test_paths}`, `{interface}`). It sees the ACs, the `Tests:` paths and the `Interface:` line only, never the plan. Gate: run the named tests yourself and save the output to `red.txt`. Every test must **fail for the right reason** (missing behaviour, not a typo or bad import). A passing test is redundant or wrong: send it back.
2. **Mutation-seen-red.** A test never observed failing is not a test. The RED output is proof it was seen red; if a stub went green without implementation code, break the behaviour once and show it fail. `red.txt` goes into the close-out `Proof:`.
3. **Commit the RED tests** as a local commit (`test(#N): RED`) so the red state is a checkpoint you can return to.
4. **GREEN: `tdd-implementer`** (clean context: it is given the test paths and the RED output, nothing else). Fill `templates/implementer-prompt.md` with `{test_paths}` and `{test_output}` (content of `red.txt`) and nothing else: no issue number, no ACs, no plan. Gate: run the target tests, then the full suite. Save to `green.txt`. Tests it flags as wrong are reported to you, never edited by it. Red suite: re-invoke once with the failure, then stop.
5. **REFACTOR: `tdd-refactorer`** (clean context), once per ticket after all tests are green. Fill `templates/refactorer-prompt.md` with the tests and the implementation paths. Gate: full suite green. "No refactoring needed" is a valid result. Skip only when the diff is under about 50 lines and adds no abstraction; say so in the commit body.
6. **QA hand-off.** Not a TDD phase: `/build` runs `/qa --issue N`. The template `templates/qa-reviewer-prompt.md` is the fallback brief for dispatching `qa-reviewer` directly when `/qa` is unavailable.

Order multiple stubs by dependency: foundation tests first; one REFACTOR pass after all are green so cross-stub duplication is visible.

## Example

Ticket `Tests: AC-001, AC-002 -> tests/test_slug.py`. Two stubs exist. Writer returns two real tests, both red (`slugify` raises NotImplementedError); `red.txt` saved. RED commit. Implementer gets the test path plus `red.txt` text, returns a four-line function; merged, suite 41/41. Refactorer: "No refactoring needed". `/build` continues to `/simplify`.

## Anti-patterns

- Giving the implementer the issue, a spec snippet, or "it should also handle X".
- Letting the writer see the implementation, or the implementer edit a test.
- Skipping the RED gate because "the stub obviously fails": run it.
- Dispatching the implementer before the RED run is saved: without `red.txt` there is no proof the tests were ever red.
- One refactor pass per stub; assertions on call counts instead of behaviour.
- Summarising the RED output instead of saving the real one.
