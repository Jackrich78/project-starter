---
name: work-issue
description: "Claim and build one GitHub issue end to end: claim, re-verify, build, tick, close. Use on \"work on #N\", \"next\", \"pick up the next ticket\", \"build #N\". A standalone ticket or a feature's first sub-issue starts only on the human's word; later sub-issues of an approved parent start on standing permission."
type: skill
disable-model-invocation: true
argument-hint: "[#N]"
---

Adapted from Matt Pocock's `implement` skill, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# Work Issue

States, labels, the frontier query and every command live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md) § Agent pickup protocol. This skill walks those steps in order and never restates them.

## Context

One ticket, claimed and finished inside one fresh context window. A standalone ticket or a feature's first sub-issue starts only on "next" or "work on X". Approving a parent's design note is standing permission for its later sub-issues; stop at `needs-info` and at the live-check sub-issue. Mode (`pr` | `direct`) comes from CLAUDE.md `## Workflow`.

## Pattern

1. **Choose.** Named issue, else the frontier query (issue-flow.md, pickup step 1): sibling of an in-progress parent first, then P0 to P2, oldest first.
2. **Claim before any other write:** assignee, then the "Working:" comment. In `pr` mode then `gh issue develop N --checkout --name issue-N-<slug>`.
3. **Read** the issue with `--comments`, not the list view.
4. **Re-verify `Current state`** against today's repo; if it changed, comment what changed before building.
5. **Build.** Code: `tdd-red-green-refactor` with isolated sub-agents. Non-code: produce the artifact the ticket's `Proof:` line names. Then `/qa --issue N`.
6. **Tick checkboxes one at a time** with the one-line diff assertion (issue-flow.md, pickup step 7). ACs tick only with evidence in hand.
7. **A task outgrows the window?** `gh issue create --parent N ...`, replace the checklist line with the link. Needing a handover to finish means the ticket was mis-sized.
8. **Blocked:** on information, `needs-info` plus Triage Notes (see `triage`); on an issue, the native edge. Either way release the claim and stop; never push on a guess.
9. **Finish** via `/commit` (`Closes #N` per mode), confirm `CLOSED`, post the close-out from `docs/templates/closeout-comment.md`. A live check goes to in review instead of closing. Last open sibling: run the parent close-out cascade.

Prepend the agent signature from CLAUDE.md `## Workflow` to every issue and comment you post.

## Example

Human: "work on #14". Claim it, read it with comments, confirm the file it cites still has the bug, drive the fix through TDD, run `/qa --issue 14`, tick the one sub-task with the diff assertion, `/commit` with `Closes #14`, confirm it closed, post the close-out with test output as `Proof:`.

## Anti-patterns

- Starting a standalone ticket without the human's word.
- Building before claiming: unclaimed work in flight is a collision.
- Briefing from the list view and missing comments that change the build.
- Trusting a ticket's file paths without re-checking them.
- Ticking a line before its evidence exists.
- Closing an issue that needs a live check, instead of in review.
- Copying the query or command table here instead of pointing at issue-flow.md.
