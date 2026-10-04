# docs/ — the wiki

Progressive-disclosure index. Read a section's one-line descriptions before opening a file. Routing authority for *where a new fact goes*: [`guides/knowledge-architecture.md`](guides/knowledge-architecture.md). Every page carries frontmatter with a `type`; `scripts/wiki_lint.py` enforces it.

## Start here

- [`../CLAUDE.md`](../CLAUDE.md) — the operating contract (loads every session).
- [`../PROJECT.md`](../PROJECT.md) — vision, principles, roadmap themes.
- [`decisions.md`](decisions.md) — append-only decision log, rejected options included.
- [`log.md`](log.md) — newest-first changelog of this wiki.

## System — how the harness works (`system/`)

- [`system/issue-flow.md`](system/issue-flow.md) — how work lives in GitHub Issues: states, labels, pickup protocol, close-out comment.
- [`system/architecture.md`](system/architecture.md) — design rationale: orchestrator, sub-agents, hooks, gates.
- [`system/memory-systems.md`](system/memory-systems.md) — which memory is which: auto-memory, per-agent memory, the wiki.
- [`system/hooks.md`](system/hooks.md) — what each hook enforces, its fail mode, and how to test a pattern change.
- [`system/testing-rules.md`](system/testing-rules.md) — test-fidelity rules the TDD agents and QA follow.
- [`system/cicd.md`](system/cicd.md) — what CI runs and how to extend it.
- [`system/current-priorities.md`](system/current-priorities.md) — injected at session start; keep it short and dated.

## Guides — practitioner how-tos (`guides/`)

- [`guides/getting-started.md`](guides/getting-started.md) — clone → `/setup` → first issue; upgrading.
- [`guides/first-session.md`](guides/first-session.md) — a scripted ten-minute first task that exercises the whole loop.
- [`guides/knowledge-architecture.md`](guides/knowledge-architecture.md) — the wiki schema: frontmatter, reserved names, decay tiers, ingest routing.
- [`guides/agent-harness-patterns.md`](guides/agent-harness-patterns.md) — self-healing briefs, ESCALATION sentinel, file hand-offs, forks over named agents.
- [`guides/working-with-claude.md`](guides/working-with-claude.md) — steering sessions, plan mode, when to delegate.
- [`guides/pruning-lessons.md`](guides/pruning-lessons.md) — how checks lie; read before any docs reorganisation.
- [`guides/claude-code-lesser-known.md`](guides/claude-code-lesser-known.md) — lesser-known Claude Code behaviours, with sources.

## Reference (`reference/`)

- [`reference/claude-code.md`](reference/claude-code.md) — official Claude Code doc links by topic.

## Templates (`templates/`)

- [`templates/closeout-comment.md`](templates/closeout-comment.md) — Shipped / Proof / Not covered / Learned.
- [`templates/research-memo.md`](templates/research-memo.md) — question, answer-first summary, sources, confidence, what would change the answer.

## Archive (`archive/`)

- [`archive/decisions-2026.md`](archive/decisions-2026.md) — superseded full decision entries.
