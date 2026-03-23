---
updated: 2026-03-08
---

# Commands Reference

13 commands ship with the harness, all part of the core workflow. Commands are defined in `.claude/commands/` and invoked by typing them in Claude Code.

---

## Setup

| Command | What it does | When to run |
|---------|-------------|-------------|
| `/setup [docs]` | One-time project initialization: interviews you about the project, generates CLAUDE.md, PROJECT.md, README.md, and architecture docs. Creates a feature roadmap with the Tech-Product Lead agent. Optionally sets up GitHub. | Once, immediately after cloning the template and before any other command. Pass paths to existing docs to pre-fill context. |

## Discovery

| Command | What it does | When to run |
|---------|-------------|-------------|
| `/explore [topic]` | Interviews you about the problem, researches the space, and produces a structured feature spec (PRD) with success criteria and scope. | When you have a vague idea but don't yet know what to build or what "done" looks like. |
| `/blueprint FEAT-XXX` | Translates the PRD into a verified technical plan: reads the actual codebase, validates assumptions, drafts implementation steps, and runs a Challenger review to catch gaps. | After `/explore` produces an approved PRD and before you start writing code. |

## Build

| Command | What it does | When to run |
|---------|-------------|-------------|
| `/build FEAT-XXX` | Implements the feature using Test-Driven Development with three isolated subagents: one writes failing tests, one writes minimal code to pass them, one refactors. A QA reviewer runs after. | When the blueprint plan is approved and you're ready to write code. |
| `/debug [issue]` | Runs a 6-phase investigation: classify the bug, find the root cause, implement a fix, write a regression test, verify, and document what was learned. Coordinates with QA and Challenger agents. | When something is broken and you need more than a quick look — for logic errors, integration failures, or hard-to-reproduce bugs. |

## Quality

| Command | What it does | When to run |
|---------|-------------|-------------|
| `/qa [target]` | Runs a two-layer quality review on any file, directory, or feature: first Semgrep SAST (15 rules, static analysis), then LLM analysis against the OWASP checklist. Outputs a report with APPROVED / NEEDS_FIXES / BLOCKED verdict. | After `/build`, or any time you want a security and quality check on existing code. |
| `/commit [message]` | Checks the QA gate, stages changes, formats the commit message to Conventional Commits standard, pushes, and waits for CI to pass before declaring done. | When your work is complete, tests pass, and you're ready to ship. |

## Session

| Command | What it does | When to run |
|---------|-------------|-------------|
| `/prime [mode] [FEAT-XXX]` | Loads the right context for your session: architecture docs, feature files, and handover. Mode shapes how Claude thinks — `think` for exploration, `build` for implementation, `review` for auditing. | At the start of every session, before any other command. |
| `/handover [FEAT-ID]` | Captures what you did, what decisions were made, and what's next — in a token-budgeted summary (under 1,500 tokens). The next session's `/prime` loads it automatically. | Before ending a session, or whenever you're about to hit the context limit. |
| `/retro [FEAT-XXX]` | Reviews completed work, extracts recurring patterns, and crystallizes them into reusable skills in `.claude/skills/`. The harness gets smarter after every feature. | After a feature ships, or when you notice a pattern worth preserving for future sessions. |
| `/logs [filter]` | Queries the SQLite audit trail to show what tools Claude used, in which session, and when. Filters: `recent`, `tools`, `sessions`, `count`. | When you want to audit Claude's activity, debug unexpected behavior, or review what happened in a previous session. |
| `/create-specialist [library]` | Generates a domain-expert sub-agent with specialized prompting for a specific library or API (e.g., Supabase, Stripe, OpenAI). The agent gets saved to `.claude/agents/` for future use. | When you're about to work with a library or service that needs deep expertise — create the specialist once, use it across features. |
| `/update-docs [scope]` | Validates that all cross-references in your documentation are accurate, updates the documentation index, and flags broken links or stale file references. | After making documentation changes, or periodically to keep the knowledge base consistent. |
