---
type: guide
title: Agent harness patterns
description: Eight prompt-level principles for autonomous, token-efficient, self-healing multi-agent work - structural sequencing, file hand-offs, self-healing briefs, the ESCALATION sentinel, subscription-aware design, portability, forks over named agents, and asking what decision data changes.
tags: [agents, patterns, delegation, autonomy]
---

# Agent harness patterns

Principles for agent systems that are autonomous, token-efficient and self-healing. They are prompt-level patterns, not infrastructure: they work in any Claude Code project. Distilled from an audit of our own harness; each one fixed a real failure. Check adoption any time with `python3 scripts/adoption_check.py` (always fresh, no table to maintain).

## 1. Structural sequencing over live messaging

**Rule:** hand-offs are encoded in skills and prompt chains, not in live `SendMessage` links between running agents.
**Why:** a live link needs both agents alive in one session. It breaks when either dies, compacts, or runs elsewhere.
**Apply:** the skill defines the order; each agent is a pure function (inputs: file paths and context; outputs: files and a verdict); the orchestrator owns ordering and gates. `/build` chains test-writer, implementer, refactorer, QA this way, and no agent knows another exists. If you reach for `SendMessage` to chain agents, restructure as sequential dispatch.

## 2. File-based hand-offs

**Rule:** agents communicate through files on disk (and Issue comments); the orchestrator verifies a gate between steps, then passes paths to the next agent.
**Why:** files are durable and inspectable and survive restarts; messages vanish with their sender.
**Apply:** output is a file or a verdict; a gate is a command the orchestrator runs (tests, a grep for a sentinel, a `gh issue view`); the next brief carries paths, not payloads. In TDD the test-writer writes tests, the orchestrator confirms they fail, and only then dispatches the implementer.

## 3. Self-healing briefs

**Rule:** agents handle their own retries through prompt instructions, not a supervisor process.
**Why:** a watcher costs tokens and can die too; in-prompt recovery is free, portable and inside the agent's existing budget.
**Add to every agent** (`## Failure Recovery`):

```
- Two attempts maximum. After a failure, re-read the error and try ONE
  different approach.
- A missing import or dependency: check it exists, read its interface, adjust.
- Unrelated tests break: revert your change and report the conflict.
- Never exit silently: return PASS, FAIL: <reason> or ESCALATION: <reason>.
```

## 4. The ESCALATION sentinel

**Rule:** every agent ends with exactly one of `PASS` (with evidence), `FAIL: <reason>` (budget spent) or `ESCALATION: <reason>` (stuck, needs a decision).
**Why:** a silent failure is the most expensive kind: the orchestrator cannot tell done from dead from still running, and the human finds the gap hours later.
**Apply:** put it in each agent's guardrails; the orchestrator checks the last line and routes: PASS to the next step, FAIL logged and reported, ESCALATION surfaced to the human. A one-turn acknowledgement with no verdict means the work was not done.

## 5. Subscription-aware design

**Rule:** every running agent draws on a shared budget; prefer event-driven over polling, conditional output, and self-pacing.
**Apply:**
- Extend a hook that already fires instead of adding a poller.
- Speak only when something changed. A quiet tick should read state and stop; composing "still nothing" costs more than the check.
- Self-pace `/loop`: short after finishing a step, long while waiting on a human, stop when idle.
- Judgement on Opus, mechanical work on Sonnet or Haiku (CLAUDE.md § Delegation & model policy).
- Before adding a cron or loop, compute ticks per day x tokens per tick. If it is large, find an event-driven alternative or lengthen the interval. Recurring zero-token work belongs in a GitHub Actions cron (`docs/system/architecture.md` § Automation).

## 6. Portable across repos

**Rule:** the principles are prompt text and conventions; do not depend on this repo's scripts to follow them.
**Portable:** self-healing briefs, the ESCALATION sentinel, file hand-offs, sequencing in skills, budgeting discipline.
**Implementation-specific:** hook code, the Issue comment formats, the wiki layout. When adopting in another repo, copy the prompt patterns into its agent definitions and write your own enforcement; do not copy the scripts and assume the principles came with them.

## 7. Fork over named for one-shot work

**Rule:** for one-shot research, review or audit, spawn an unnamed agent or a fork. Name an agent only to continue it with `SendMessage`.
**Mechanics:** a *fork* clones the parent's context, runs in the background, and its result arrives as a completion notification. A *named agent* starts from only its prompt, stays addressable, and must be told to report; if it finishes without reporting it goes idle and you receive nothing. Forks are fire-and-forget; named agents are fire-and-manage.
**Why:** in our runs, named one-shot agents stalled with no report far more often than unnamed ones, and the failure is silent. End any named brief with "SendMessage your report before stopping". If one idles, nudge once, then read its transcript on disk: disk is ground truth.

## 8. Ask what decision this data changes

**Rule:** before building any monitor, dashboard or metric, write one sentence: "if this crosses X, I do Y."
**Why:** a metric with no defined response is a dashboard nobody reads by week three.
**Apply:** no Y means the number is informational: put it in a periodic audit, not a daily push. Keep budget and cost signals apart from forensic ("what happened") data; they share a source and nothing else.

## Related

- Contracts for agents: `.claude/rules/agents.md`; roster rules: `.claude/agents/README.md`.
- Test-and-verify side of the same ideas: `docs/system/testing-rules.md`.
- Why checks lie: `docs/guides/pruning-lessons.md`.
