---
name: retro
description: "Turn what happened into durable process changes; runs inside /session-winddown, or after a feature closes. Use on \"retro\", \"what did we learn\", \"that was wrong, remember it\", \"always do X next time\". Modes: learn, feedback. Proposals need human approval before anything is edited."
type: skill
argument-hint: "[learn|feedback]"
---

# Retro

## Context

Default mode is `learn`. Home table: `.claude/rules/*`, `CLAUDE.md § Hard-won rules`, agent prompts, memory. Issue states and the `Learned:` line: `docs/system/issue-flow.md`. Evidence gate: no proposal without at least two converging sources or one objective record.

## Pattern

### learn (default)
1. Find the window: date of the last retro (`git log --grep` or `docs/log.md`), else 30 days.
2. `gh issue list --state closed --search "closed:>YYYY-MM-DD" --json number,title,comments`; harvest each `Learned:` line. Add `git log --oneline <base>..HEAD`.
3. Dispatch `agile-coach` (sonnet, read-only) with the harvest and range. It returns at most 5 numbered proposals with verbatim evidence.
4. Show them. The human approves by number (edits allowed). Nothing unapproved moves.
5. Dispatch `librarian` with the approved items; it applies by Edit only. Memory entries the coach proposed are written by you, after approval.
6. `git diff --stat`; a delta over 10% of a file stops the run. Then hand to `/commit`.

### feedback
A correction the human gave this session. Route it to the nearest file that is loaded at the moment it applies, and apply it:

| Kind | Home |
|---|---|
| Personal preference, all projects | `~/.claude/CLAUDE.md` |
| Project rule | `CLAUDE.md` |
| Rule for certain paths | `.claude/rules/<topic>.md` |
| One-off incident | auto-memory |
| An agent's method | proposed entry in `.claude/agent-memory/<agent>/MEMORY.md` (methods only) |

State the cause of the mistake ("what assumption was wrong"), not just the fix. A rule that failed twice in prose becomes a hook or test.

Always: if the auto-memory index (`MEMORY.md` under `~/.claude/projects/<project>/memory/`) exceeds 200 lines, merge or drop entries until under.

## Example

`/retro` after #41 closes. Harvest: `Learned: gh search lags writes by seconds` (#41) and a fix commit `fix: retry after label edit` -> two sources. Coach proposes "add a 5 s wait to `work-issue` pickup". Human: "1 yes". Librarian edits one line; diff is 2 lines.

## Anti-patterns

| Wrong | Why | Instead |
|---|---|---|
| Lessons as prose in a notes file | decays unread | route to a loaded file |
| Skip because nothing failed | cost and round-trip deltas still teach | run it, accept "No proposals" |
| Eight proposals at once | unranked proposals rot | cap 5, ranked |
| Librarian told to rewrite a file | silent meaning change | Edit only, surgical |
| Memory entry holding a finding or verdict | memory is methods only | one-line method with source |
| Re-opening a settled decision | recurring rounds | read `docs/decisions.md` first |
