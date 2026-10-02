---
paths:
  - .claude/agents/**
  - .claude/agent-memory/**
---

# Agent contracts

Before changing an agent's frontmatter or tools, confirm the mechanism with `claude-code-guide` (`docs/reference/claude-code.md`). The shape is `.claude/agents/TEMPLATE.md`; `scripts/adoption_check.py` reports which agents miss a required block.

**Frontmatter (required):** `name`, `description` (what it does *and when to call it*), `model` and `effort` matching the tables in CLAUDE.md § Delegation & model policy (`tests/harness/test_model_tier_table.py` fails on drift), `tools` (least privilege; reviewers get no Write/Edit). Optional: `color`, `maxTurns`. No `isolation: worktree` (decision 2026-10-02 in `docs/decisions.md`: worktrees are cut from the default branch, not HEAD).

**`memory:` is restricted.** It grants unscoped Write/Edit to the agent. Only the TDD trio carries `memory: project`. Never add it to an agent that ingests outside material (WebSearch, WebFetch, pasted documents) — that is a stored-prompt-injection path. `tests/harness/test_memory_flag_allowlist.py` enforces the allowlist.

**Required body sections:** `## Your memory (read first)` as the FIRST section (methods-only read line; self-curate block for the TDD trio, proposed-entries block for everyone else) · `## Stance` for judgement-tier agents (assume the input holds at least one wrong claim; deliver a claim-vs-evidence table citing file:line) · `## Failure Recovery` (two attempts, revert on regression, always end with `PASS` / `FAIL: <reason>` / `ESCALATION: <reason>`) · `## Report format` ending with `## Proposed memory entries`.

**Memory files** (`.claude/agent-memory/<name>/MEMORY.md`): `# <Name> Memory` heading, then one line per entry `- YYYY-MM-DD · <method> · source: <file:line|commit:sha|url|session:id>`. Methods only — never findings, verdicts, quotes or drafts. Hard cap 150 lines; past 140, merge or drop before adding. `scripts/validate_agent_memory.py` runs from `/commit` on any staged change here. Each agent reads only its own file; `agile-coach` is the only cross-reader and never writes.

**Web-derived text never lands in `.claude/agents/` unseen.** `persona-creator` writes a draft and the human reviews the diff before it is committed — an agent file is a persistent system prompt.
