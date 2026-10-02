---
name: persona
description: "Create a new persistent agent persona or library specialist. Use on \"add an agent for X\", \"create a specialist for <library>\", \"new persona\". Dispatches persona-creator; the human reviews the diff before anything is committed."
type: skill
disable-model-invocation: true
argument-hint: "<name> --role \"<one line>\" [--tier opus|sonnet|haiku] [--research <library>]"
---

# Persona

## Context

An agent file is a persistent system prompt, and web-derived text must never land in `.claude/agents/` unseen (`.claude/rules/agents.md`). `persona-creator` writes drafts only; the human approves.

## Pattern

1. Parse arguments. Missing `<name>` or `--role` -> ask. Tier default `sonnet`; tier and effort must match the CLAUDE.md model table.
2. Dispatch `persona-creator` with name, role, tier, and `--research <library>` when given. It creates `.claude/agents/<name>.md` from `TEMPLATE.md`, an empty `.claude/agent-memory/<name>/MEMORY.md`, and returns a proposed routing row.
3. Show the human `git diff` / `git status` for both files, in full. Stop for approval; apply requested edits.
4. After approval only: add the routing row to CLAUDE.md. No `memory:` frontmatter unless the agent is in the TDD trio.
5. Run `python3 scripts/adoption_check.py` and `npm test`. Failures -> fix or report; do not commit.
6. Hand to `/commit`.

## Example

`/persona stripe-expert --role "Stripe billing specialist" --research stripe` -> draft + empty memory, diff shown, human approves, routing row added, checks green.

## Anti-patterns

- Committing before the human read the diff.
- Granting `memory:` or Write tools to an agent that ingests web text.
- Adding the routing row before approval.
