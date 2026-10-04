---
type: overview
title: Project plan
description: Vision, principles, current state and roadmap themes for this project. Status of individual work lives on GitHub Issues, not here.
updated: 2026-10-02
version: 3.0.0-dev
---

# <Project name> — project plan

<!-- CUSTOMIZE: /setup fills this file from your answers. Keep it under 60 lines; it loads every session. -->

## Vision

<!-- CUSTOMIZE: ≤3 sentences. Who is this for, what problem does it solve, what does "done" look like in a year? -->
A lean, observable harness for Claude Code: an orchestrator that delegates to sub-agents, tracks work in GitHub Issues, and keeps what it learns in a linted wiki — for building software *and* for the research, documents and decisions around it.

## Principles

<!-- CUSTOMIZE: ≤7. Each one states what it forbids. Run `grilling` on these when you are ready; the three below are the template's. -->
1. **Reduce** — minimise what loads into context; forbids dumping every doc at session start.
2. **Offload** — delegate reads, research and drafting to sub-agents; forbids the main thread doing retrieval.
3. **Isolate** — contain side effects (worktrees, clean-context reviewers, hooks); forbids a writer reviewing its own work.

## Current state

<!-- CUSTOMIZE: one paragraph. What works today, what is in flight. Point at issues, don't restate them. -->
v3.0.1 in progress (branch `fix/v3.0.1-adoption-feedback`): the first adoption's feedback round. The security hook returns to the v2 guard model, project settings set no permission mode, and the `/setup`, test-runner and sub-agent-brief gaps the adopter hit are closed. Harness status is read from `gh issue list --label feature --state all`, not from this file.

## Roadmap

<!-- CUSTOMIZE: 3–5 phase themes. Each theme ends with the `feature` issues it contains (#N). No status here — GitHub owns it. -->
- **Phase 1 — foundation:** harness bootstrapped, first feature shipped end to end. <!-- #N #N -->
- **Phase 2 — <theme>:** <!-- #N -->
- **Phase 3 — <theme>:** <!-- #N -->

## Architecture

```
you ──/skill──> orchestrator (main thread) ──dispatch──> sub-agents (opus: judge · sonnet: build · haiku: fetch)
                     │                                        │
                 hooks (deny · salvage)                    files on disk + GitHub Issues (the hand-off medium)
                     │
                 docs/ wiki (what outlives a feature) · docs/decisions.md (why)
```

Full rationale: `docs/system/architecture.md`. How work flows: `docs/system/issue-flow.md`.

## Measurement

<!-- CUSTOMIZE: what would tell you the harness is paying off? e.g. issues closed per session, QA findings per build, time to first useful session for a new contributor. -->
