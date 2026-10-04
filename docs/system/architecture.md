---
type: domain-doc
title: Architecture
description: Design rationale of the harness - orchestrator and sub-agents, why Issues are the spec, why memory is methods-only, why model choice is by role, the three layers, the gates, what runs where, and what the template deliberately does not do.
tags: [architecture, design, rationale]
---

# Architecture

Why the harness is shaped the way it is. How-to lives in `docs/guides/`; per-mechanism contracts in `hooks.md`, `testing-rules.md`, `cicd.md`, `memory-systems.md`, `issue-flow.md`. Choices between options are logged with their rejected alternative in `docs/decisions.md`.

## Core idea: one orchestrator, many cold sub-agents

The main thread is the bottleneck: its context is the scarcest resource and everything it reads stays there. So it plans, decides, verifies and talks to the human; reads, searches, drafting and review go to sub-agents that start cold with only the brief they are given. Three principles follow (CLAUDE.md § Orchestrator contract):

- **Reduce**: pass pointers, not payloads; load docs on demand.
- **Offload**: one agent, one job; a reviewer that can write is not a reviewer.
- **Isolate**: contain side effects (clean-context sub-agents for implementers, read-only tools for reviewers).

Sub-agent output is a *claim*. The brief decides whether the claim can be true: an agent given no live state can only reason from priors. The orchestrator verifies on disk before acting and states the independence tier of any multi-agent result (prompt-only, tool access, independent inputs). Hand-offs between agents are files and Issue comments, never live messages (`docs/guides/agent-harness-patterns.md`).

## The three layers

| Layer | Mechanism | Used for | Why this layer |
|---|---|---|---|
| Enforcement | hooks, `permissions.deny`, CI | rules that must hold regardless of model reasoning (no exfil, no secrets in logs) | deterministic; the model cannot talk its way past it |
| Knowledge | skills, `.claude/rules/`, the wiki | how to do a workflow, conventions, facts | loaded on demand; costs nothing until relevant |
| Isolation | sub-agents, `context: fork` | clean-context work: TDD phases, QA, research | prevents a shared context from biasing the check |

Rule of thumb: a rule that failed twice in prose becomes a hook or a test. Knowledge never goes in a hook; enforcement never goes in a skill.

## Why the Issue is the spec

Specs live on GitHub Issues (`issue-flow.md`), not in feature folders in git. A spec where the work is tracked is read by teammates and agents alike; a README per feature was a second home for the same facts that only its author navigated. What outlives a feature moves to the wiki at close-out (the `Learned:` line), and the rejected options go to `docs/decisions.md`: code preserves what was built, never what was tried. Sizing is in context windows, not hours, because the window is what an agent actually runs out of.

## Why memory is methods-only and tracked

Per-agent memory (`.claude/agent-memory/<name>/MEMORY.md`) holds *methods* that carried over, never findings, verdicts or drafts: findings go stale, methods compound. It is tracked in git so changes are reviewable in PRs, and each file is one line per entry under a 150-line cap. The `memory:` frontmatter flag grants unscoped Write/Edit, so only the TDD trio has it; any agent that ingests outside material (web, pasted text) never gets it, because stored text that re-enters a prompt is a persistent injection path. Others propose entries in their report and the orchestrator writes the accepted ones. Mechanism: `memory-systems.md`.

## Why the model policy is by role, and tested

Opus plans and judges (output gates whether work ships), Sonnet builds and drafts, Haiku does pure volume. "Opus to be safe" is the failure mode: it spends the budget where judgement is not needed. The table lives in CLAUDE.md § Delegation & model policy and `tests/harness/test_model_tier_table.py` fails when an agent's frontmatter drifts from it, so the policy cannot rot silently. Web research never runs on the main thread.

## The gates

Each gate has an owner who is not the author of the thing gated.

| Gate | Where | Enforced by |
|---|---|---|
| Design note approved | parent issue, before sub-issues exist | human; `work-issue` stops at `needs-triage` |
| Fact-check 10/10 | `to-tickets`, before `ready-for-agent` | `challenger` samples 10 claims against the repo; below 10/10 fix and resample |
| RED before GREEN | `/build` | the orchestrator runs the tests between phases (`testing-rules.md`) |
| QA verdict | `qa-reviewer`, clean context | verdict marker on the issue; `BLOCKED SECURITY` makes `/commit` refuse (step 0) |

## Automation: what runs where

| Need | Mechanism | Why |
|---|---|---|
| Rule that must always hold | hook (`hooks.md`) | no session, no tokens, deterministic |
| React to something in a live session | `/loop` (dynamic, self-paced) | needs the session's context; stop it when done |
| Reminder to look at something | SessionStart nudge | cheapest possible: a sentence at the right moment |

Design rules for anything that runs repeatedly:

- **Event-driven over polling.** Extend a hook that already fires rather than adding a poller; a tick that finds nothing should cost almost nothing, and a tick that announces "nothing changed" costs more than the work.
- **Self-pace** `/loop` to the work: short after a step completes, long while waiting on a human, stop when idle.
- **`CronCreate` jobs expire after 7 days** and exist only while a session lives, so they are never the owner of recurring maintenance. Use an Actions cron.
- **Estimate before adding a loop:** ticks per day x tokens per tick. A large product means find an event-driven alternative or lengthen the interval.
- **A loop needs a verifiable, bounded done state** and a file as state (a checklist the loop ticks off), so it neither runs forever nor re-does finished work.

## What the template deliberately does not do

- **No feature folders.** The Issue is the spec; the wiki holds what lasts.
- **No telemetry.** A silent store of tool output is a liability for strangers.
- **No autonomous task loop.** Nothing picks up Issues unattended. A human says "next"; approving a design note grants standing permission for its sub-issues, and agents stop at `needs-info` and the live-check.
- **Soft gates over hard gates.** Only security is a hard stop (deny hook, `BLOCKED SECURITY`). Process gates are verdicts and reminders the orchestrator must act on and the human can overrule, because a hard gate that is wrong blocks real work and teaches people to bypass it.
- **No slash-command layer.** Skills carry every workflow; two files per workflow is two homes per fact.
- **No inventory pages.** Rosters and counts are generated or injected; a hand-maintained list drifts within weeks (`.claude/agents/README.md`).
