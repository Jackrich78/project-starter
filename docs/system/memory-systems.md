---
type: domain-doc
title: "Memory systems: which memory is which"
description: "Where each kind of remembered thing lives in this template (auto-memory, per-agent memory, wiki, decision log, issues, salvage) and which to use for what."
tags: [memory, agents, wiki, routing]
---

# Memory systems: which memory is which

Six places hold things across sessions. Each has one job; picking the wrong one is how facts rot or leak.

| System | Lives in | Holds | Tracked in git? |
|---|---|---|---|
| Claude Code auto-memory | `~/.claude/projects/<slug>/memory/MEMORY.md` | Per-project incident learnings and confirmed preferences | No (outside the repo) |
| Per-agent memory | `.claude/agent-memory/<name>/MEMORY.md` | One agent's methods | Yes |
| The wiki | `docs/` | Durable facts about the system and how to work on it | Yes |
| The decision log | `docs/decisions.md` | Choices, with the rejected option | Yes |
| GitHub Issues | the issue tracker | Work state: spec, status, blockers, hand-off | Remote |
| Compaction salvage | `.claude/salvage/` | Structural extract of a transcript, written before compaction | No (gitignored, runtime) |

## Auto-memory

Claude Code's own memory. `MEMORY.md` is an index of one-line entries pointing at topic files; the index loads each session and is kept at 200 lines or fewer. It holds what the project taught this machine's sessions (an incident, a confirmed preference), not facts the repo should say. `/retro` prunes it: merge or drop entries until under the cap. It is outside the repo, so it never ships and nobody else sees it.

## Per-agent memory

`.claude/agent-memory/<name>/MEMORY.md`, tracked. **Methods only**: how to do the agent's job better, never findings, verdicts, quotes or drafts. Format: `- YYYY-MM-DD · <method> · source: <file:line|commit:sha|url>`; hard cap 150 lines; `scripts/validate_agent_memory.py` checks it (run by `/commit`).

Two write paths:

1. **Self-curating:** the TDD trio carries `memory: project` and edits its own file.
2. **Proposed:** every other agent reads its file via the first section of its prompt, ends its report with `## Proposed memory entries`, and the orchestrator writes the accepted lines.

Why `memory:` is restricted: the flag grants the agent unscoped Write and Edit. On an agent that ingests outside material (web search, fetched pages, pasted documents) that is a stored-prompt-injection path: hostile text becomes a persistent instruction. So only agents with no outside input get it, and `tests/harness/test_memory_flag_allowlist.py` enforces the list. Each agent reads only its own file; `agile-coach` is the one cross-reader and never writes.

## The wiki

`docs/`: system facts, guides, references. Linted by `scripts/wiki_lint.py`; routing rules in `docs/guides/knowledge-architecture.md`. Reach for it before reasoning from memory.

## Decision log

`docs/decisions.md`: one line per choice, in the turn it is made, rejected option included. Code shows what was built, never what was tried.

## GitHub Issues

The issue is the spec and the work queue (`docs/system/issue-flow.md`). Status, blockers and hand-off notes live on the issue, never on a wiki page or in a memory file.

## Salvage

`.claude/salvage/` is written by the `pre_compact` hook and re-injected after compaction or resume. Runtime state: gitignored, short-lived, never a source of truth.

## I need to write down...

| ...this | Put it in |
|---|---|
| How a part of this system works | `docs/system/<topic>.md` |
| Steps someone will follow | `docs/guides/<topic>.md` |
| Why we chose A over B | `docs/decisions.md` (one line, plus REJECTED) |
| A list of links or lookups | `docs/reference/` |
| A rule the agent must follow every session | `CLAUDE.md` or `.claude/rules/` |
| What I am doing this week | `docs/system/current-priorities.md` (short, dated) |
| What is blocked on whom, or what is next on a task | The GitHub issue |
| A technique an agent should reuse | Proposed entry for `.claude/agent-memory/<name>/MEMORY.md` |
| A trap this project taught this machine | Auto-memory |
| A confirmed personal preference | Auto-memory |
| A workflow I keep re-prompting (~3x) | A skill in `.claude/skills/` |
