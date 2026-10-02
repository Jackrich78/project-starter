---
name: audit-claude-md
description: "Run the deterministic health check on CLAUDE.md and explain the findings. Use on \"audit CLAUDE.md\", \"is CLAUDE.md too long\", \"check for stale paths\", \"harness health\"."
type: skill
disable-model-invocation: true
---

# /audit-claude-md

## Context

CLAUDE.md is loaded every turn, so size and rot cost attention on every turn. The check is a script; this skill runs it and turns findings into edits.

## Pattern

1. Run `python3 scripts/audit_claude_md.py --strict` (add `--json` for machine output). Exit 1 means an alert, stale path or orphan rule.
2. Explain each finding and propose the fix; apply only what the human approves:
   - **Line count** (warn above 120, alert above 150): move domain rules into `.claude/rules/*.md` with `paths:` frontmatter, or delete lines that restate what the code or `--help` already shows.
   - **Soft language** ("consider", "might want to", "ideally"): rewrite as a hard rule or delete; a hedge is a rule nobody enforces.
   - **Stale path** (backticked path missing on disk): find where it moved and update, or remove the reference.
   - **Orphan scoped rule** (`paths:` glob matches zero files): fix the glob or delete the rule.
3. Re-run until clean. Detail on writing rules: `.claude/skills/writing-for-agents/SKILL.md`.

## Example

Output `STALE docs/old-guide.md`, `SOFT "ideally"` line 44, `WARN 131 lines`. Propose: repoint the path to `docs/guides/getting-started.md`, rewrite line 44 as "Always run `npm test` before commit", move the testing section to a `.claude/rules/<topic>.md` file. Re-run: exit 0.

## Anti-patterns

- Hand-counting lines or hunting paths instead of running the script.
- Fixing a warning by compressing prose instead of moving or deleting rules.
- Deleting a stale reference without checking whether the file merely moved.
