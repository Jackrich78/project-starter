---
type: reference
title: Skills — authoring conventions
description: How a skill is written here (frontmatter, trigger-phrased description, body shape, size cap, attribution). Holds no inventory — the harness injects the roster from the files themselves.
---

# Skills

A skill is executable knowledge: a workflow the session loads on demand instead of re-deriving it. One folder per skill, `SKILL.md` plus optional `references/`, `templates/` or `scripts/`. Invoke as `/<name>`.

## There is no list on this page, deliberately

The harness reads `name` and `description` from every `.claude/skills/*/SKILL.md` at session start. That listing cannot drift. To see what exists: `ls .claude/skills/`. A hand-maintained inventory lived here once and was 27 entries behind the directory when it was deleted.

## Frontmatter

| Key | Required | Notes |
|---|---|---|
| `name` | yes | kebab-case, equal to the folder name (`tests/harness/test_size_caps.py` checks) |
| `description` | yes | **the trigger surface**: the problem and the phrasings that should fire it, not a summary |
| `type` | yes | `skill` (wiki lint enforces the taxonomy) |
| `disable-model-invocation` | for skills only a human should start | `true` means only `/<name>` runs it; spine skills omit it so the orchestrator can invoke them (`.claude/rules/skills.md`) |
| `argument-hint` | when it takes arguments | shown in the slash-command picker |
| `context: fork` + `agent:` | for clean-context work | the body becomes that agent's brief |

## Body

`## Context` (when, 1–2 sentences) · `## Pattern` (numbered steps) · `## Example` (one concrete run) · `## Anti-patterns` (what not to do, and why). Cap 150 lines; detail goes to `references/` files the body names explicitly. Operational facts live in `docs/system/<topic>.md` — point, never copy.

## Creating and changing skills

Read `writing-for-agents` first, build or evaluate with `skill-creator`, extract one from a session that just worked with `/retro`. The ~3× rule: prompted the same workflow three times, make it a skill. Adapted skills carry their source and licence in the first lines (see `NOTICE`). Rules load automatically when you edit here: `.claude/rules/skills.md`.
