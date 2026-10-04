---
name: work-issue
description: "Claim and work one GitHub issue end to end: claim, re-verify, build, tick, close; the pickup protocol /build runs when a ticket is taken from the ready-for-agent frontier. Use on \"work on #N\", \"pick up the next ticket\", \"next\", \"what is next on the board\"."
type: skill
argument-hint: "[#N]"
---

Adapted from Matt Pocock's `implement` skill, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# Work Issue

States, labels, the frontier query and every command live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md) § Agent pickup protocol. This skill walks those steps in order and never restates them.

## Context

One ticket at a time, sized per issue-flow.md § Sizing. `ready-for-agent` is gate 1: after each hand-off take the next ready ticket, stopping where issue-flow.md § Agent pickup protocol says. Mode (`pr` | `direct`) comes from CLAUDE.md `## Workflow`.

## Pattern

1. **Choose.** Named issue, else the frontier query (issue-flow.md, pickup step 1): sibling of an in-progress parent first, then P0 to P2, oldest first.
2. **Claim before any other write:** assignee, then the "Working:" comment. In `pr` mode then `gh issue develop N --checkout --name issue-N-<slug>`.
3. **Read** the issue with `--comments`, not the list view.
4. **Re-verify `Current state`** against today's repo; if it changed, comment what changed before building.
5. **Build.** Code: `tdd-red-green-refactor` with isolated sub-agents. Non-code: produce the artifact the ticket's `Proof:` line names. Then `/qa --issue N`.
6. **Tick checkboxes one at a time** with the one-line diff assertion (issue-flow.md, pickup step 7). ACs tick only with evidence in hand.
7. **A task outgrows the ticket?** `gh issue create --parent N ...`, link it in a comment. Needing a handover to finish means the ticket was mis-sized.
8. **Blocked:** on information, `needs-info` plus an Ask block; on an issue, the native edge. Either way release the claim and take the next ticket; never push on a guess.
9. **Finish** via `/commit` (`Closes #N` per mode), post the close-out hand-off from `docs/templates/closeout-comment.md` (`direct` mode: confirm `CLOSED`). A live check goes to in review instead of closing. Last open sibling: run the parent close-out cascade.

Reading and writing on an issue: issue-flow.md § Talking to the human.

## Example

Human: "work on #14". Claim it, read it with comments, confirm the file it cites still has the bug, drive the fix through TDD, run `/qa --issue 14`, tick the one AC with the diff assertion, `/commit` with `Closes #14`, post the hand-off with test output as `Proof:`, take the next ticket.

## Anti-patterns

- Stopping to ask between the gates.
- Building before claiming: unclaimed work in flight is a collision.
- Briefing from the list view and missing comments that change the build.
- Trusting a ticket's file paths without re-checking them.
- Ticking a line before its evidence exists.
- Closing an issue that needs a live check, instead of in review.
- Copying the query or command table here instead of pointing at issue-flow.md.
