<!--
CANONICAL TEMPLATE for memory/agents/{name}.md files.
DO NOT EDIT this template — copy its structure to a new agent file.

Schema rules (enforced by scripts/validate_agent_memory.py):
- Exactly 3 H2 sections allowed: ## Patterns, ## Incidents, ## Task Outcomes.
- No other top-level (H1/H2) headings beyond the title H1 and these three H2s.
- Entries are markdown bullets starting with `- [YYYY-MM-DD] `.
- Every entry MUST end with a citation in one of these formats:
    agent.db:event_id=N         (N is an integer)
    commit:SHA                  (SHA is ≥7 hex chars)
    file.md:LINE                (file path + line number)
    qa:report#section           (path-relative qa report ref)
- Empty sections are allowed (validator passes).
- File line cap: ≤100 lines. Excess triggers pruning via scripts/prune_agent_memory.py.

Self-write rules:
- Each agent self-writes to its OWN file at end-of-feature only.
- Other agents do NOT read other agents' files. Only the Agile Coach reads cross-agent.
- Citation is mandatory. Entries without sources are rejected.
- 3 entries max per self-retro (pattern + incident + outcome).
-->

# {Agent Name} Agent Memory

> Sub-agent self-retro memory.
> Validate: `python scripts/validate_agent_memory.py --agent {name}`.
> Prune: see `scripts/prune_agent_memory.py`.

## Patterns

<!-- Append ONE pattern entry per self-retro IF you learned something durable. Format:
- [YYYY-MM-DD] {pattern title} — [FEAT-XXX, pass|fail]
  Brief insight (1–2 sentences). Source: agent.db:event_id=N OR commit:SHA OR file.md:LINE OR qa:report#section.
-->

## Incidents

<!-- Append ONE incident entry per self-retro IF something broke and you found a recovery path. Format:
- [YYYY-MM-DD] {incident title} — [FEAT-XXX]
  What broke. Recovery path. Prevent recurrence how. Source: …
-->

## Task Outcomes

<!-- Append ONE outcome entry per self-retro (always). Format:
- [YYYY-MM-DD] FEAT-XXX: pass|fail — one-line summary.
  Source: …
-->
