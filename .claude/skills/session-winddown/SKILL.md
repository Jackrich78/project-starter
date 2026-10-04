---
name: session-winddown
description: "End a session cleanly, in the one order that works. Use on \"wrap up\", \"wind down\", \"call it a day\", \"stop here\", \"before I /clear\", \"hand over\", \"closing the laptop\", or at the end of any session that produced commits or closed issues. Orchestrates commit, close, retro, triage, handover; restates none of them."
type: skill
disable-model-invocation: true
argument-hint: "[session-start-sha]"
---

# Session wind-down

## Context

Each step reads the state the previous one produced, so the order is the value: a handover over a dirty tree or stale queue describes a repo nobody has. This skill orchestrates; procedures live in `commit`, `triage`, `handover`, and `docs/system/issue-flow.md`.

## Pattern

**Pre-flight** (one pass):
```bash
git status --short
git log --oneline @{u}..HEAD
git diff --name-only <session-start-sha>..HEAD
```
For every changed surface: does the page that documents it still tell the truth (its skill, the CLAUDE.md sentence that promises it, its `docs/system/` page)? Stale page -> fix it in step 1. All clean and nothing substantial -> say so in one line and stop.

1. **`/commit` everything**, pushed; `git status --short` empty.
2. **Close what shipped** per the Done rule in issue-flow. Ask what each issue's value was: if it was a question, the answer goes in the close-out `Learned:` line before closing. Needs a live check -> `ready-for-human`, not closed.
2b. **If commits landed:** dispatch `agile-coach` with the harvest pasted into the brief (it has no Bash): `git log --oneline <base>..HEAD`, the `Learned:` and `Proof:` lines of issues closed this session. Its block becomes the handover's "Process retro". Write accepted memory entries.
3. **`triage`**, so the handover's next steps read a current queue.
4. **`/handover`**, posted on the claimed or parent issue.
5. **Only then clear.** Irreversible: disk artifacts are the whole memory.

A commit message is a claim frozen at the moment it was written: re-check every status claim against current state.

## When NOT to run

- Short exchange: nothing to hand over.
- Work mid-flight: finish or park deliberately first.
- Another session is writing to the issues: confirm, or skip step 3 and say so.
- The human asked for one piece ("just the handover"): do that piece, mention what the rest would catch.

## Failure modes

- Dirty tree after step 1 -> stop; find the file (scratch to ignore, or an unnoticed edit).
- Push rejected -> resolve (fetch, rebase onto upstream, re-run gates) before continuing; unpushed work is invisible.
- No issue for the handover -> ask which; never invent.

## Example

"call it a day": pre-flight shows 2 unpushed commits changing `scripts/<script>.py`; `docs/system/<topic>.md` is stale -> fix, `/commit`, close #31 with `Learned:`, coach block, triage, handover, "safe to /clear".

## Anti-patterns

- Closing an issue only mentioned in a commit.
- Running steps 2-4 as one silent batch; queue changes need approval.
- Copying `/commit` or `/handover` procedure here; the copy drifts.
