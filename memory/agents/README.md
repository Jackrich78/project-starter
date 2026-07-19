# Agent Memory

Per-agent self-retro memory files. Each agent writes to its own `{name}.md`
file at the end of a feature, recording patterns, incidents, and task outcomes
for the Agile Coach to cross-read and promote to `CLAUDE.md § Hard-won rules`.

## Opt-In Tracking Design

**By default, `memory/agents/*.md` files are gitignored** (except this README
and `TEMPLATE.md`). This means:

- Agent retros accumulate locally and persist in your working tree.
- They are NOT committed to git, so they never appear in the public repo.
- Downstream users who clone this template start with a clean slate.

**To opt in and track retros in git**, remove (or comment out) this line in
`.gitignore`:

```
memory/agents/*.md
```

Leave the `!README.md` and `!TEMPLATE.md` exceptions in place so the scaffold
remains visible to new cloners.

## Schema

See `TEMPLATE.md` for the full contract enforced by
`scripts/validate_agent_memory.py`.

| Rule | Detail |
|------|--------|
| File name | `memory/agents/{agent-name}.md` |
| H1 title | `# {Agent Name} Agent Memory` |
| H2 sections | Exactly 3: `## Patterns`, `## Incidents`, `## Task Outcomes` |
| Entry format | `- [YYYY-MM-DD] text (citation)` |
| Citation formats | `agent.db:event_id=N`, `commit:SHA`, `file.md:LINE`, `qa:report#section` |
| Max entries/feature | 3 (one per section) |
| Max file size | 100 lines (excess triggers pruning) |

## Tooling

```bash
# Validate all memory files
python scripts/validate_agent_memory.py

# Validate one agent
python scripts/validate_agent_memory.py --agent tdd-test-writer

# Preview a pruning manifest (no writes)
python scripts/prune_agent_memory.py docs/qa/pruning-manifest.md --dry-run

# Apply a pruning manifest
python scripts/prune_agent_memory.py docs/qa/pruning-manifest.md --apply
```

## Self-Write Rules

- Each agent self-writes to its OWN file at end-of-feature only.
- Other agents do NOT read other agents' files.
- Only the Agile Coach reads cross-agent memory.
- Citation is mandatory — entries without sources are rejected by the validator.
- Maximum 3 entries per self-retro (one pattern + one incident + one outcome).
