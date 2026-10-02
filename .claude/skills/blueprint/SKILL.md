---
name: blueprint
description: "Ground an approved feature spec in the real codebase, then cut it into tickets. Use on \"blueprint #N\", \"plan the build for #N\", \"is #N ready to build\", \"validate the spec against the code\", after /explore has produced a parent feature issue with an approved design note. Re-checks every path and library the spec names, interviews the developer, picks the test pyramid, then hands off to to-tickets."
type: skill
disable-model-invocation: true
argument-hint: "#N"
---

# Blueprint

States, labels and `gh` commands live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md). Test philosophy lives in the `test-strategy` skill. This skill is the grounding procedure.

## Context

Input: a parent `feature` issue whose design note the human approved (`/explore`). No parent or no approved note: stop and send the human to `/explore`. Output: a validated spec and sub-issues published under the parent. No files are written.

## Pattern

### Phase A: grounding (plan mode, no writes)

Enter plan mode. Read `gh issue view N --comments`.

1. **Codebase validation.** Glob/Grep every file, module, library and pattern the body names. Does each exist? Is anything already handling part of it (middleware, helpers, existing tests)? Greenfield: say so and skip mismatch analysis. A mismatch that blocks the whole approach goes to the human now, before the interview.
2. **Seams.** The spec introduces a new module, package or top-level file: run `codebase-design` (interface, seam, deletion test). Same-file edits skip this.
3. **Research (conditional).** Open questions the repo cannot answer: `researcher` (sonnet), facts-only brief, answer returned as text. Otherwise skip.
4. **Developer interview** via AskUserQuestion, at most 6 questions: error handling, data and migration, performance, security, rollback, existing tests that will break. **Skip any question the body already answers**; record "answered from spec: <q> - <a>" in the report.
5. **Test pyramid** per `test-strategy`. Backstop tests: at most 3 outcome-level tests for the feature, plus per-branch unit tests where logic branches. Not one test per AC line (that list rots). Name the validation depth (`unit | schema | integration | frontend | manual`).
6. **Cold read if the body changed.** Any edit since `/explore`'s sim run: `prd-consistency-sim` (opus) with `gh issue view N --json body` pasted in. `challenger` (opus) under the same conditions as `/explore` (3 or more OQs, integration or frontend depth, harness files), thorough pass.
7. **Gate.** Present: mismatches, research, interview answers, pyramid, file-change map (new / modified / deleted, path + purpose). Ask: **proceed / adjust / spike first.** Spike first: run the `spike` skill and fold the finding into the body, then re-gate. Nothing is posted before "proceed".

### Phase B: publish

8. **Codebase Validation Report** as an issue comment (`gh issue comment N --body-file <f>`), carrying the file-change map `to-tickets` cuts slices against.
9. **Amend the body only if the spec changed**, by one-line-diff discipline (issue-flow.md § Agent pickup protocol, step 7): pull body to a file, keep `.orig`, change, assert `diff` shows only the intended lines, then `gh issue edit N --body-file`. A change to an approved requirement also gets a `docs/decisions.md` line.
10. **Invoke `to-tickets`** on N. Hand it the validation depth and the pyramid. It shows the numbered breakdown as a vetoable alert, fact-checks, and publishes.

## Example

`/blueprint #12`. Glob finds `src/export/` exists but the body cites a `formatCsv` that does not (mismatch, flagged). Interview: 4 of 6 questions already answered in the body. Pyramid: 2 outcome tests, unit tests for the three format branches. Human picks "proceed". Report comment posted, one AC clarified in the body (diff: 1 line), `to-tickets` publishes a prefactor, two slices and the live-check ticket.

## Anti-patterns

- Posting or editing anything before the human says "proceed".
- Asking interview questions the spec answers.
- One test per AC line instead of backstop outcome tests.
- Trusting the body's paths without a Glob/Grep this turn.
- A silent body rewrite: amendments are one-line diffs, logged.
- Cutting tickets yourself instead of invoking `to-tickets`.
- Planning a wide mechanical refactor as one ticket (`to-tickets` sequences expand, migrate, contract).
- Writing a plan file: the sub-issues are the plan.
