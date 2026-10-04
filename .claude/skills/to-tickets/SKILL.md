---
name: to-tickets
description: "Break an approved plan or parent issue into sub-issues, each sized per issue-flow.md § Sizing; the spine step after /blueprint approval and before /build. Use on \"break this into tickets\", \"turn this plan into issues\", \"slice this feature\", \"to-tickets #N\". Shows a numbered breakdown the human can veto, then publishes."
type: skill
context: fork
argument-hint: "<parent #N>"
---

Adapted from Matt Pocock's `to-tickets` skill, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# To Tickets

States, labels and commands live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md). Ticket body shape is [`.github/ISSUE_TEMPLATE/ticket.md`](../../../.github/ISSUE_TEMPLATE/ticket.md). This skill is procedure only.

## Context

A feature has a parent issue with an approved design note and an approved `/blueprint`. The job: turn it into sub-issues an agent can pick up one at a time.

## Pattern

1. **Gather.** Read the parent body and comments (or the plan in conversation). Read `docs/decisions.md` for the area.
2. **Prefactor first.** Look for a change that makes the real change easy; if one exists it is ticket 1 and unblocks the rest.
3. **Draft 3-6 vertical slices.** Each is a narrow path through every layer it touches, demoable alone, sized per issue-flow.md § Sizing (at most 5 ACs), with blocking edges named. Each body follows `ticket.md` and carries a `Tests:` line (AC ids -> test paths) or, for non-code work, a `Proof:` line. Wide mechanical refactors go expand, migrate, contract instead.
4. **Alert the human.** Show a numbered breakdown (title, what it delivers end to end, what blocks it) before writing to GitHub. It is a vetoable alert, not a gate: say so, and proceed unless they reply with a change.
5. **Fact-check gate.** Every AC traces to a line in the parent body (no source = invented requirement or promoted open question: stop). Every file:line or "N hits" claim is grepped in this turn, never from an earlier read. Quoted spec clauses are diffed against the current spec. Then a `challenger` sample over up to 10 tickets must score 10/10; fix and re-check below that. Passing is the `Verified:` record (issue-flow.md § Verify gate).
6. **Publish blockers first,** in dependency order, so later tickets cite real numbers:
   `gh issue create --parent <P> --blocked-by <N> --label ready-for-agent,<kind>,<priority> --title "<t>" --body-file <f>`
   Never hand-link dependencies in a body. Prepend the agent signature from CLAUDE.md `## Workflow`.
7. **Last sub-issue:** a `ready-for-human` live check blocked by every slice, taken from the parent's Validation live-check line.

Do not edit or close the parent beyond what `--parent` links.

## Example

Approved blueprint for a three-window feature. Draft a prefactor plus 3 slices, show the numbered list; the human replies "merge 2 and 3". Redraft, map every AC to the parent body, challenger 10/10, publish the prefactor, then the merged slice blocked by it, then the last slice, then the live-check sub-issue blocked by all.

## Anti-patterns

- Treating the breakdown as a blocking approval instead of a vetoable alert.
- A ticket with no `Tests:` or `Proof:` line.
- A publish set with no trailing `ready-for-human` live check.
- ACs that do not trace to the parent body.
- Skipping the challenger sample, or publishing below 10/10.
- Hand-linking blockers in the body instead of `--parent` / `--blocked-by`.
- A horizontal slice (all schema, then all API) labelled vertical.
- Copying states, labels or commands here instead of pointing at issue-flow.md.
