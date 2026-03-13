---
updated: 2026-02-06T00:00:00Z
description: Discover and define a feature through two-phase discovery
argument-hint: [feature topic]
---

# Feature Exploration

You are exploring a new feature: **$ARGUMENTS**

## Mission

Transform a vague feature idea into a structured Product Requirements Document (PRD) through deep discovery. Both product understanding AND technical understanding must be established before writing anything.

## Philosophy

**Ask first, write later.** The quality of the PRD depends entirely on the depth of the discovery conversation. Never rush to documentation.

---

## Workflow

### Step 1: Load Project Context

**Before asking ANY questions**, understand the project:

```
Read these files (if they exist):
├── PROJECT.md - Project goal, current state, roadmap
├── CLAUDE.md - Workflow rules, constraints
├── docs/system/architecture.md - System structure
└── docs/features/ - Scan existing feature folders
```

Extract:
- Project goal and vision
- Current tech stack and constraints
- Existing features and patterns
- What the project already has that might be relevant

This context informs your questions.

---

### Step 2: Product Discovery

Engage the user with questions about the WHAT and WHY. Ask these questions conversationally, adapting based on answers.

**Problem Space:**
1. "What specific problem triggers this feature?"
2. "Who experiences this problem? (role, context, how often)"
3. "What's the cost of NOT solving this problem?"

**Value & Success:**
4. "What value does solving this create for users? For the business?"
5. "How will we measure success? What does 'done' look like?"

**Scope:**
6. "What's explicitly IN scope for the first version?"
7. "What's explicitly OUT of scope? (What are we NOT building?)"

**User Stories:**
8. "Walk me through how a user would use this feature - what's the flow?"

Use `AskUserQuestion` tool for structured questions when useful, or converse naturally. Dig deeper on vague answers. Don't accept "it should just work" - get specifics.

---

### Step 3: Technical Discovery

Explore the HOW and constraints. Combine questions with research.

**Constraints:**
1. "Any technical constraints I should know about?"
2. "Dependencies or integrations required?"
3. "Performance, security, or compliance requirements?"

**Approach:**
4. "Do you have a preferred technical approach, or open to proposals?"
5. "Any existing code or patterns in this project we should leverage?"

**Research (if needed):**

If there are open technical questions you can't answer:

**VALIDATION (REQUIRED):**
- Feature folder MUST exist before invoking researcher
- If Step 4 (Generate Feature ID) not completed yet: Run Step 4 first to create feature folder
- Verify folder exists: `docs/features/FEAT-XXX_[slug]/`

**Invoke researcher:**
```
Task(
  subagent_type="researcher",
  description="Research [specific question] for FEAT-XXX",
  prompt="Research the following technical questions for FEAT-XXX:
  1. [Question 1]
  2. [Question 2]

  Context: [Brief context from discovery]

  REQUIRED OUTPUT LOCATION:
  docs/features/FEAT-XXX_[slug]/research-[topic]-[ISO-timestamp].md

  The feature folder MUST exist. If not found, FAIL immediately with error.

  Use ISO timestamp format: YYYY-MM-DDTHH-MM-SSZ"
)
```

**If research needed before full PRD:**
1. Create skeleton feature folder first (Step 4)
2. Add minimal prd.md with research questions
3. Invoke researcher with feature context
4. Complete PRD after reviewing research findings

---

### Step 4: Generate Feature ID

After discovery is complete:

1. Check `docs/features/` for existing FEAT-XXX folders
2. Assign the next sequential number
3. Create slug from feature name (lowercase, hyphens)
4. Create folder: `docs/features/FEAT-XXX_[slug]/`

Example: `docs/features/FEAT-010_user-authentication/`

---

### Step 5: Create PRD

Write `docs/features/FEAT-XXX_[slug]/prd.md` following `docs/templates/prd-template.md`.

Synthesize BOTH discovery phases into:

**From Product Discovery:**
- Problem Statement (clear, specific, ≤150 words)
- Goals & Success Criteria (measurable outcomes)
- User Stories (3-7 stories with Given/When/Then acceptance criteria)
- Scope & Non-Goals (explicit boundaries)

**From Technical Discovery:**
- Constraints & Assumptions (technical, business)
- Open Questions (anything still unresolved for /blueprint phase)

**Critical: Acceptance Criteria**

AC must be CLEAR and UNAMBIGUOUS. Each criterion:
- Uses Given/When/Then format
- Has a single testable condition
- Specifies exact expected behavior
- Can be verified as pass/fail

Bad: "Should work well"
Good: "Given a valid email, When submitted, Then user receives confirmation within 5 seconds"

---

### Step 5.5: PRD Self-Critique

**Before declaring the feature defined**, validate the PRD for implementability. This step catches issues that otherwise surface during `/plan` (costly rework).

**Quick self-check (always):**
1. **Agent overlap**: If PRD proposes a new agent, read `.claude/agents/README.md` and verify <50% overlap with existing agents. If >50%, enhance the existing agent instead.
2. **Concrete flows**: Every execution flow must have numbered steps. Flag any vague language ("simpler flow", "handles it appropriately", "lightweight process") and replace with specifics.
3. **Resolved decisions**: Every open question with a recommendation must be marked **DECIDED** or explicitly left **OPEN for /blueprint**. Ambiguous status wastes planning cycles.

**Challenger review (recommended for features that modify existing agents/commands):**

If the PRD proposes changes to existing agents, commands, or the workflow pipeline, invoke the challenger for a second opinion:

```
Task(
  subagent_type="challenger",
  description="Critique FEAT-XXX PRD",
  prompt="Review docs/features/FEAT-XXX_[slug]/prd.md for implementability.

  Also read .claude/agents/README.md for existing agent inventory.

  Focus on:
  1. Does any proposed new agent overlap >50% with existing agents?
  2. Are all execution flows concrete (numbered steps, not vague)?
  3. Are all open questions resolved or explicitly deferred?
  4. Is the scope realistic for one feature?

  Max 3 issues. Be direct."
)
```

If challenger finds issues, resolve them with the user before proceeding to Step 6.

---

### Step 6: Present Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FEATURE DEFINED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FEAT-XXX: [Feature Name]
📄 PRD: docs/features/FEAT-XXX_[slug]/prd.md

Problem: [1-2 sentence summary]
Scope: [Key inclusions]
Acceptance Criteria: [Count] defined
Open Questions: [Count] for planning phase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: /blueprint FEAT-XXX
```

---

## Success Criteria

Before completing exploration:

- ✅ Project context was read and understood
- ✅ Product discovery questions answered (problem, value, scope)
- ✅ Technical discovery questions answered (constraints, approach)
- ✅ Research conducted if open technical questions existed
- ✅ Feature ID assigned (FEAT-XXX)
- ✅ PRD created following template
- ✅ Acceptance criteria are CLEAR and TESTABLE
- ✅ Open questions documented for /blueprint phase
- ✅ Self-critique passed: no agent overlap, flows are concrete, decisions resolved
- ✅ Challenger review passed (if feature modifies existing agents/commands)
