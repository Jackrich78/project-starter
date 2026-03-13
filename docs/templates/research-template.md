---
id: research-[topic]
title: [Research Topic Title]
feature: FEAT-XXX
created: YYYY-MM-DD
research_type: [architecture|integration|performance|security|spike]
status: [in_progress|complete]
---

# Research: [Topic]

## Research Questions

[From PRD open questions or explicit research requests]

1. [Question 1]
2. [Question 2]
...

---

## Key Findings

### [Topic Area 1]

[Discoveries, patterns, technical details organized by topic, not by source]

### [Topic Area 2]

[Additional findings]

---

## Recommendations

[Clear, actionable guidance for planner with rationale]

**Primary Recommendation:** [Specific choice]

**Rationale:** [Why this is the best option given project constraints]

---

## Trade-offs

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| [Option A] | [Benefits] | [Drawbacks] | [Use when...] |
| [Option B] | [Benefits] | [Drawbacks] | [Use when...] |

---

## Resources

1. [Source Title](URL) - Retrieved via WebSearch, [Date]
2. [Source Title](URL) - Retrieved via WebSearch, [Date]

---

## Template Usage Notes

**When to use this template:**
- All research conducted via researcher agent
- Research for existing features (via /blueprint command)
- Research during feature exploration (via /explore command)
- Spike research for exploratory work

**Required sections:**
- Research Questions (what you're investigating)
- Key Findings (what you discovered)
- Recommendations (what you recommend based on findings)
- Resources (all sources cited with retrieval method)

**Optional sections:**
- Trade-offs (if comparing multiple options)

**Naming convention:**
- Format: `research-[topic]-[ISO-timestamp].md`
- Topic: Brief descriptor (e.g., `auth-patterns`, `database-design`, `spike-caching`)
- Timestamp: `YYYY-MM-DDTHH-MM-SSZ` (filesystem-safe ISO format)
- Example: `research-auth-patterns-2026-01-24T14-30-00Z.md`

**Location:**
- MUST be in feature folder: `docs/features/FEAT-XXX_[slug]/`
- NEVER in `/docs/` root or other locations

**Frontmatter fields:**
- `id`: Unique identifier matching filename
- `title`: Human-readable research title
- `feature`: Feature ID (FEAT-XXX) this research belongs to
- `created`: Date research was conducted (YYYY-MM-DD)
- `research_type`: Category (architecture, integration, performance, security, spike)
- `status`: Current status (in_progress, complete)
