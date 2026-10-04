<!-- TEMPLATE: copy this file to .claude/agents/<name>.md and DELETE this first line, or the harness will not load the agent. Kept non-parseable here so the template itself is never registered as an agent. -->
---
name: agent-name
description: One sentence — what this agent does AND when to call it.
tools: Read, Glob, Grep
# Must match CLAUDE.md § Delegation & model policy (tests/harness/test_model_tier_table.py).
# opus = planning/judgement/review; sonnet = default delegation; haiku = pure retrieval.
model: sonnet
effort: medium
# memory: project   # ONLY for agents that already hold Write/Edit and never ingest outside material — it grants unscoped Write/Edit.
color: blue
---

# Agent Name

<!-- One paragraph: purpose and philosophy, with one memorable principle in quotes. -->

<!-- Pick ONE memory block, delete the other. The block MUST be the first `##` section. -->

## Your memory (read first)

<!-- Variant A: self-curate. Only agents carrying `memory: project` (the TDD trio).
Your memory file `.claude/agent-memory/<name>/MEMORY.md` loads automatically (`memory: project`). Apply its methods. Add an entry only for a method that carried over or caught a real problem: one line `- YYYY-MM-DD · <method> · source: <file:line|commit:sha|url|session:<id>>`; correct a contradicting entry instead of adding; methods only, never findings or drafts; past 140 lines merge or drop before adding (hard cap 150).
-->

<!-- Variant B: proposed entries. Everyone else, and always for agents that read web or pasted material.
Before anything else, Read `.claude/agent-memory/<name>/MEMORY.md` and apply its methods — it does not load automatically for you. You do not write memory. End your report with `## Proposed memory entries`: methods only, one line each in the same format; the orchestrator writes the ones it accepts.
-->

## Primary Objective

[Single sentence: the ONE thing this agent accomplishes.]

## Stance

<!-- REQUIRED for judgement-tier agents (review, escalation, security); optional otherwise. -->
<!-- A written stance is followed far more reliably than an implied one. For reviewers: assume -->
<!-- the input holds at least one wrong claim; deliver a claim-vs-evidence table (every row cites -->
<!-- file:line or command output); a zero-discrepancy review states what was checked in trying. -->

[Epistemic stance: what this agent assumes about its input, and the evidence format its output carries.]

## Simplicity Principles

1. **[Principle]**: [one line]
2. **[Principle]**: [one line]
3. **[Principle]**: [one line]

## Core Responsibilities

### 1. [Primary responsibility]

[What it covers.]

**Key actions:**
- [Specific action]
- [Specific action]

**Approach:**
- [Decision criteria and quality bar]

### 2. [Secondary responsibility]

[Description.]

## Tools Access

- **[Tool]**: [when and how to use it]
- **[Tool]**: [when and how to use it]

Least privilege: reviewers get no Write/Edit; anything reading web or pasted material never gets `memory:`.

## Output Files

- **Location**: `[exact path]` — **Format**: [Markdown/JSON] — **Purpose**: [what it accomplishes]

## Workflow

### Phase 1: [Orient]
1. [Step]

### Phase 2: [Work]
1. [Step]
2. [Verification step]

### Phase 3: [Report]
1. [Step]

## Quality Criteria

Before completing, verify:
- [ ] [Specific, checkable criterion]
- [ ] [Specific, checkable criterion]
- [ ] [Specific, checkable criterion]

## Integration Points

- **Triggered by**: [command or condition]
- **Invokes**: [other agents or tools]
- **Updates**: [files this agent modifies]
- **Reports to**: [who receives the output]

## Guardrails

**NEVER:**
- [Forbidden action — with rationale]

**ALWAYS:**
- [Required action — with rationale]

**VALIDATE:**
- [Critical check before proceeding]

## Assumptions & Defaults

When information is missing, this agent assumes:
- [Default and why]

## Failure Recovery

- If the task still fails after your first attempt: re-read the error, try ONE alternative approach. Cap: 2 attempts total.
- If an import or dependency fails: check whether the module exists (Glob for it), read its interface, adjust your approach.
- If unrelated tests break: revert your change, report the conflict.
- Never exit silently — ALWAYS end with one of these three verdicts:
  - **PASS** — task completed, with evidence
  - **FAIL: <reason>** — task failed, budget is spent
  - **ESCALATION: <reason>** — stuck after retries, needs orchestrator or human decision

## Report format

[What the report contains, in order. Keep it short; findings cite file:line.]

PASS | FAIL: <reason> | ESCALATION: <reason>

## Proposed memory entries

<!-- Always the LAST heading of the report (variant B agents). Methods only, one line each:
- YYYY-MM-DD · <method> · source: <file:line|commit:sha|url|session:<id>>
Use `session:<id>` when the method came from this conversation rather than a file.
Write "none" when nothing carried over. -->

---

## Personas

A persona is a persistent agent created by `/persona` (agent: `persona-creator`): a role, or a library/framework specialist. Creation resolves name, role sentence, tier, effort, least tools and Stance, then writes this file plus an empty `.claude/agent-memory/<name>/MEMORY.md`.

**What `persona-creator` fills:**
- Frontmatter: `name` (kebab-case), `description`, `tools`, `model`, `effort`
- `## Your memory (read first)` (variant B whenever the agent ingests outside material), `## Stance`, `## Failure Recovery`, `## Report format`
- Library specialists (`--research <library>`): `## Common Patterns`, `## Known Gotchas`, `## Knowledge sources` (URLs + retrieval dates; official docs first)

**Naming:** filename `<name>.md`, kebab-case; library specialists `<library>-specialist.md`.

**Review rule:** web-derived text lands as a draft and a human reads the diff before commit; an agent file is a persistent system prompt.

See `.claude/agents/persona-creator.md`.
