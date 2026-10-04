---
name: handover
description: "Write the session handover as an issue comment so the next session starts cold and right; the last step of /session-winddown. Use on \"handover\", \"hand this over\", \"write up where we are\", \"I'm switching sessions\", or when /session-winddown reaches the handover step. Forward state only; re-checks every status claim against current state."
type: skill
context: fork
argument-hint: "[#N]"
---

# Handover

## Context

Runs forked: it inherits the session but keeps the main context clean. The handover is a comment on the claimed or parent issue (`docs/system/issue-flow.md`). It is forward state: open work, blockers, how to resume. Past actions belong in commits.

## Pattern

1. **Find the issue.** `$ARGUMENTS`, else the issue assigned to `@me` with a "Working:" comment, else `#N` in the branch name, else the parent of that issue. None -> ask which issue; never invent one, never write a file.
2. **Read the previous handover.** `gh issue view N --comments`; latest comment containing `# Session Handover`. Keep unresolved blockers and still-true decisions, drop resolved or superseded items, mark survivors `(from previous session)`. Keep its `Generated:` stamp and add `Updated:`.
3. **Re-check every status claim against current state**, not against commit messages or the old handover. A commit message is frozen at the moment it was written. Re-run the check, re-read the file, re-query the issue.
4. **Git state:** `git branch --show-current`, `git log --oneline -1`, `git status --short` (list dirty files).
5. **Draft** in this order, at most 1500 tokens:
   - `# Session Handover`, `*Generated: <date time>*`
   - **Blocker** on line 1 (or "no blockers: pick from the queue")
   - **Git state**
   - **Proved / not proved:** every green names its scope and what it does NOT cover. "Live-validated" only for behaviour seen on its real surface; anything waiting on a human or a deploy is "built, awaits <step>".
   - **Decisions and open questions**
   - **Next step:** one concrete command or action
   - **Process retro** (only when session-winddown supplies an `agile-coach` block)
6. **Post:** write to a temp file, then `gh issue comment N --body-file <file>`, signature on line 1 (issue-flow.md § Talking to the human). Confirm with the issue number and token estimate. Output no file path.

## Example

```
# Session Handover
*Generated: 2026-10-02 17:40*
**Blocker:** CI red on `issue-12-login`: `auth.test.js` timeout. Not reproduced locally.
**Git:** issue-12-login, 3a1f9c2 "feat(auth): add token refresh", dirty: none
**Proved:** unit tests pass (auth module only). Not proved: login flow in a browser.
**Next:** `gh run view --log-failed`, fix the timeout, push.
```

## Anti-patterns

| Wrong | Why | Instead |
|---|---|---|
| Chronological session log | the next session needs state, not history | forward state only |
| Copy "X not validated" from a commit message | the validation may have run after the commit | re-check now |
| Blocker buried mid-document | first line gets read | blocker on line 1 |
| Bare "tests pass" | a bounded green read as a general one | name the scope and the gap |
| No issue found, so invent one or write a file | untraceable state | ask which issue |
| State an incident's cause as fact | inference propagates for sessions | cite evidence or mark it inferred |
