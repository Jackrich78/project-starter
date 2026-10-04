---
type: guide
title: First session
description: A scripted ten-minute first task on a real tiny item in your own repo, showing the full loop from prime to wind-down.
tags: [onboarding, workflow]
---

# First session (about 10 minutes)

Pick something genuinely small from your own repo: a typo, a missing test, a stale doc line. Real work proves the loop; a toy does not.

## 1. `/prime`
- **See:** branch, dirty count, last commits, roadmap themes, the frontier of `ready-for-agent` issues.
- **Proves:** context loads in a few lines, from the repo and GitHub, not from memory.

## 2. Pick or raise one `chore` ticket
Pick a frontier item, or raise one from the ticket template:
```bash
gh issue create --template ticket.md --title "chore: <small thing>" --label chore --label ready-for-agent
```
Put a `Tests:` line (AC id + test path) or, for non-code work, a `Proof:` line (the evidence that closes it) in the body.
- **See:** an issue number `#N`.
- **Proves:** the issue is the spec; no ticket line, no build.

## 3. `/build #N`
- **See:** the issue claimed with a "Working:" comment, a failing test first (RED), then minimal code (GREEN), then a clean-up pass. In `pr` mode, a branch `issue-N-slug`.
- **Proves:** isolated sub-agents each saw only what they needed; a test you saw fail is a test.

## 4. `/qa --issue N`
- **See:** a verdict comment on the issue: APPROVED, NEEDS_FIXES or BLOCKED. For a no-code ticket, a check against your `Proof:` line.
- **Proves:** an independent reviewer with clean context judged it, not the builder.

## 5. `/commit`
- **See:** the QA gate checked, a conventional message ending `Closes #N` (in `pr` mode, a PR you merge).
- **Proves:** a BLOCKED SECURITY verdict would have stopped here (`/commit` step 0).

## 6. Close-out comment
On the issue, four lines: `Shipped:` (SHA) · `Proof:` (fenced output, including the RED run) · `Not covered:` · `Learned:`.
- **See:** the issue closed with evidence attached.
- **Proves:** what shipped and what was learned survive the session.

## 7. `/session-winddown`
- **See:** tree clean and pushed, queue triaged, a `# Session Handover` comment on the issue.
- **Proves:** the next `/prime` starts exactly where this ended.

## What just happened

| Step | CLAUDE.md spine |
|---|---|
| `/prime`, ticket | Work lives in GitHub Issues; the issue is the spec |
| `/build` | Orchestrator delegates; TDD with isolated sub-agents; size in context windows |
| `/qa` | Sub-agent output is a claim; independent review on Opus |
| `/commit` | Ask first for irreversible steps; the security verdict gates it |
| Close-out | Learned facts go to the wiki or decision log in the turn they are made |
| `/session-winddown` | Reduce, Offload, Isolate: the next session loads a handover, not a transcript |

Next: raise a `feature` parent and `/explore #N`, see [../system/issue-flow.md](../system/issue-flow.md).
