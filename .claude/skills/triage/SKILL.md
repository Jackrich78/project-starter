---
name: triage
description: "Move issues out of needs-triage toward a state a human can act on; runs inside /session-winddown or whenever the queue has new items. Use on \"triage\", \"what needs me\", \"let's do some backlog items\", \"I have a new item, triage it\", \"move #N to ready\". Recommends and waits for the human's reply before changing any label."
type: skill
argument-hint: "[#N]"
---

Adapted from Matt Pocock's `triage` skill and its `AGENT-BRIEF.md`, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# Triage

States, labels and commands live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md). When unsure of a label or command, read that page; do not guess.

## Context

The human wants to work the backlog: a sweep ("triage", "what needs me"), a named item ("move X to ready"), or a new item to turn into a ticket. Before proposing a close, verify at the claimed boundary: the commit's diff must actually deliver the ACs; a commit that merely mentions an issue is not that issue shipping.

## Pattern

### Sweep

1. List the oldest 5 `needs-triage` issues: `gh issue list --state open --label needs-triage --json number,title,labels,createdAt --limit 100`, sort oldest first, take 5.
2. For each, read the issue and comments, then:
   - **Redundancy by concept:** search the repo for an existing implementation by what it does, not by the issue's wording. Exists means `wontfix` pointing at it, not `needs-info`.
   - **Prior rejection:** `grep REJECTED docs/decisions.md` for anything similar; a close match is `wontfix`, quoting the line.
3. **Verify the claim.** Bug: reproduce from the reporter's steps. Enhancement: check the described current state against today's repo. A brief built on a stale claim wastes the next session.
4. **Recommend,** numbered, one line each: priority, kind, target state, reason, whether the claim held. Fold a parent's sub-issues under it.
5. **Wait.** Apply nothing until the human answers by number ("1 ready, 3 drop: duplicate").
6. Apply exactly what they ruled with the commands in issue-flow.md. `ready-for-agent` needs a `Verified:` comment first (issue-flow.md § Verify gate). Prepend the agent signature from CLAUDE.md `## Workflow`.

### Named item

Confirm the label swap and any comment, then act. Skip redundancy checks; the human has decided.

### needs-info

Post and leave on `needs-info`:

```markdown
## Triage Notes

**What we've established so far:**
- point 1

**What we still need from you:**
- question 1
```

Questions are specific and answerable, never "please provide more info". The answer is recorded in the thread or body, not only in chat.

### New item

Fits one window: write it from `.github/ISSUE_TEMPLATE/ticket.md` and create it `needs-triage`. Bigger: not a triage job; run `grilling`, `/explore`, `/blueprint`, then `to-tickets`.

## Example

"triage": list the oldest 5, check each for redundancy and rejection, verify two claims, reply with 5 numbered recommendations. Human: "1 ready, 3 drop: dup of #9". Verify and label #1, close #3 as a duplicate of #9, leave the rest untouched.

## Anti-patterns

- Applying a label before the human replies.
- Briefing without verifying the claim against the repo.
- Promoting to `ready-for-agent` with no `Verified:` comment.
- Closing a question silently; record the answer first.
- Copying the states table or commands here instead of pointing at issue-flow.md.
