---
name: Feature
about: A parent issue that is the spec for several sub-issues
title: ""
labels: feature,needs-triage
---

<!-- The design note stays at one screen. Sub-issues are the plan. -->

## Design note
- **Question:** what are we deciding or building, and for whom?
- **In/out test:** a change is in scope when <test>; out when <test>.
- **Proposed shape:** the approach in a few lines.
- **Decisions needed:** choices the human must make before sub-issues are cut.
- **Open items:** unresolved questions (a question answerable by reading a file is not open).

## Requirements
- <what must be true, in plain terms>

## Acceptance criteria
- [ ] AC-001: Given <context>, when <action>, then <observable result>.
- [ ] AC-002: ...

## Outcome test
One observable check that answers "did this solve the user's problem?"

## Validation
- Unit: <what>
- Schema: <what>
- Integration: <what>
- Frontend: <what>
- Manual: <what>
- Live check: <what the human checks on the real surface; becomes the last sub-issue>

## Reversal
`git revert <sha>`; never a bare infrastructure command. Name any manual undo for effects outside git.

## Decisions
- Links to `docs/decisions.md` lines, rejected options included.

## Sub-issues
<!-- Native sub-issues only (`gh issue create --parent`); never hand-link here. -->
