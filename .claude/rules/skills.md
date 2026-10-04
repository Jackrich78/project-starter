---
paths:
  - .claude/skills/**
---

# Skill conventions

Read `.claude/skills/writing-for-agents/SKILL.md` before authoring or editing a skill; build or evaluate with `skill-creator`. Confirm frontmatter semantics with `claude-code-guide` when unsure (`docs/reference/claude-code.md`).

- **`description` is the trigger surface, not a summary.** Name the problem and the phrasings that should fire it. A skill nothing loads is a skill that does not exist.
- **Frontmatter:** `name` (kebab-case = folder), `description`, `type: skill`; `disable-model-invocation: true` is reserved for skills only a human should start (setup, recover-session, prime, persona, prototype, audit-claude-md, writing-for-agents), while spine skills carry an `argument-hint` and a model-facing description so the orchestrator can invoke them; clean-context skills use `context: fork` + `agent: <name>`.
- **Body shape:** `## Context` (when, 1–2 sentences) · `## Pattern` (numbered steps) · `## Example` (one concrete run) · `## Anti-patterns` (what not to do, and why).
- **Point, never copy.** Operational facts live in `docs/system/<topic>.md`; the skill links to them. A copied procedure is the one that drifts.
- **Size cap 150 lines** (`tests/harness/test_size_caps.py`); detail goes to `references/` files the body names explicitly ("Read `references/x.md`").
- **One job per skill.** A skill that does two things fires on neither reliably.
- **Deterministic work goes in a script**, not in model carefulness (`scripts/` or the skill's own `scripts/`).
- **Attribution:** a skill adapted from someone else's work names the source and licence in its first lines (see `NOTICE`).
- **The ~3x rule:** prompted the same workflow three times → make it a skill rather than prompting it a fourth.
