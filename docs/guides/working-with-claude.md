---
type: guide
title: Working with Claude
description: How to steer a session - plan mode, when to delegate, how to brief a sub-agent, course-correcting, /clear discipline, and which of the four rule layers a new rule belongs in.
tags: [sessions, steering, delegation, rules]
---

# Working with Claude

Practical steering for a session on this harness. Setup is in `getting-started.md`; the operating contract is CLAUDE.md.

## Plan first when the cost of a wrong turn is high

Use plan mode (Shift+Tab to cycle) for anything that touches several files, an unfamiliar area, or a choice between approaches. Read, explore and agree the plan before any edit; skip it for a change you could describe in one sentence. For a feature, the plan is the parent issue's design note and `/blueprint`, not a chat message: it must survive the session. When a plan feels too convenient, ask for the strongest case against it (`grilling` skill, or the `challenger` agent) before approving.

## When to delegate

The main thread is the scarce resource. Delegate when work is:

- **bulky to read** (many files, logs, search results) and you need only the conclusion;
- **independent** of the next step (run several in parallel in one message);
- **better judged cold** (review, fact-check, QA: the author should not be the reviewer);
- **web research** (never on the main thread).

Do inline what is under half a context window and needs your live reasoning. The routing table is CLAUDE.md § Delegation & model policy; `claude-code-guide` answers how Claude Code itself behaves.

## Brief a sub-agent so its claim can be true

A sub-agent starts cold: it sees its own prompt and the brief, not your conversation.

1. **Give it the live state it reasons about** (the diff, the failing output, file paths), or label what it returns *unverified*. An agent briefed only with a description can only reason from priors.
2. **State the question and the done shape**: what to return, in what format, how long, and that it must end with `PASS`, `FAIL: <reason>` or `ESCALATION: <reason>`.
3. **Brief it to disprove, not to comply** when you want a check: "find what is wrong with this" beats "confirm this is right".
4. **Pass pointers, not payloads**: paths and line ranges, not pasted files.
5. **Spawn unnamed for one-shot work**; name an agent only to continue it, and end that brief with "SendMessage your report before stopping".

Then treat the result as a claim. State its independence tier: **Tier 1** prompt only (agreement means the framing is coherent), **Tier 2** it had tool access (the framing is yours, the data is not), **Tier 3** independent inputs (agreement is evidence). Verify on disk before acting. A one-turn acknowledgement means the work was not done.

## Course-correct early

- **Interrupt (Ctrl+C; Esc only clears the input)** the moment it heads the wrong way; a correction early costs one turn, late costs the rebuild. Double-Esc (or `/rewind`) restores an earlier point if it already went wrong.
- **Say what is wrong and what you want instead**, with the evidence ("that file does not exist: `ls` shows ..."). Corrections stick better with a reason.
- **Scope phrases work**: "only change what I asked", "do not guess; ask", "step by step" for a subtle bug, "take the contrarian view" before committing to a direction.
- **Two failed corrections on the same point: stop and restart** with a better prompt; a context full of dead ends degrades the next attempt.
- **After compaction**, "I have never seen this" is not "this did not happen": find the session with `/recover-session` before calling something invented.

## `/clear` discipline

One window, one task. `/clear` between unrelated tasks, and when a ticket is done; a ticket that needs a handover before it closes was mis-sized. `/clear` is not re-primed (`docs/system/hooks.md`), so start the next task by naming it, or run `/prime`. `/compact` is for continuing the *same* task; the salvage hook restores paths, commands and your recent words afterwards. Anything worth keeping beyond the window goes on the issue, in the wiki or in `docs/decisions.md` before you clear.

## Four layers of rules: where does a new rule go?

| Layer | File | Loads | Shared | Put here |
|---|---|---|---|---|
| Global | `~/.claude/CLAUDE.md` | every session, every project | no (yours) | personal style, safety rules you want everywhere |
| Project | `CLAUDE.md` | every session in the repo | yes (git) | the operating contract: rules that apply to all work here |
| Path-scoped | `.claude/rules/*.md` with `paths:` | when matching files are in play | yes (git) | conventions for one area (tests, hooks, docs) |
| Auto-memory | `~/.claude/projects/<project>/memory/` | every session, per project and machine | no | what Claude learned about you and the project |

| The rule is... | It goes in |
|---|---|
| true on every project you touch | global CLAUDE.md |
| true for everyone on this repo, always | project CLAUDE.md (keep it short: every line is paid every session) |
| true only when editing one kind of file | `.claude/rules/` with `paths:` |
| a workflow or procedure | a skill, not a rule |
| must hold regardless of the model | a hook or test (a rule that failed twice in prose becomes one) |
| a fact about the system | the wiki page for that fact, linked from where it is needed (`docs/guides/knowledge-architecture.md`) |
| a personal preference or correction | auto-memory |
| why an option was chosen or rejected | `docs/decisions.md` |
| a method an agent should reuse | that agent's memory file (`docs/system/memory-systems.md`) |

If a rule would have to be repeated in two layers, it is in the wrong place or one copy is a pointer.

## See also

- `docs/guides/agent-harness-patterns.md`: patterns behind the delegation rules.
- `docs/guides/claude-code-lesser-known.md`: loading and enforcement behaviours worth knowing.
- `docs/system/issue-flow.md`: how a session picks up and closes work.
