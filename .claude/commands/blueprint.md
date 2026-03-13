---
updated: 2026-02-19T00:00:00Z
description: Technical grounding and implementation blueprint — validates assumptions before creating plan
argument-hint: [FEAT-ID]
---

# Feature Blueprint

You are creating an implementation blueprint for: **$ARGUMENTS**

## Mission

Ground every plan in reality before committing to it. Phase A validates assumptions against the actual codebase and surfaces architectural unknowns. Phase B creates the plan only after those unknowns are resolved and the approach is approved.

## Philosophy

**Validate before you plan. Plan before you build.** The most expensive failure mode in AI-assisted development is a plan that looks correct on paper but breaks because a file doesn't exist, a library API differs, or existing middleware already handles what's being planned.

---

## Prerequisites

```
Required: docs/features/$ARGUMENTS/prd.md

If missing: Error — run /explore [topic] first to create a PRD
```

Phase A does not start until this check passes.

---

## Phase A: Technical Grounding

**No files are written in Phase A.** The goal is to surface what's real before committing to any approach.

---

### A1: Codebase Validation (agent self-check — no user questions needed)

Run Glob/Grep for every file, module, library, and pattern the PRD references. Answer these 4 questions:

1. **External libraries**: Do all referenced libraries exist in `package.json` / `requirements.txt` / `pyproject.toml`?
2. **Internal files/modules**: Do all referenced internal files/modules actually exist in the codebase?
3. **Existing patterns**: Are there established patterns for this type of operation the plan should follow?
4. **Existing coverage**: Does any existing middleware/auth/caching layer already handle parts of what's planned?

Document findings as a **Codebase Validation Report** in your response (inline — no separate file). Flag any mismatches.

**Graceful handling for greenfield/docs-only repos:**
If no `src/` or app code is found, note: "No existing codebase patterns found — this appears to be a greenfield or docs-only project. Proceeding with developer interview." Skip mismatch analysis, continue to A3.

**Critical mismatch escalation:** If a mismatch would block the entire planned approach (e.g., a required library doesn't exist, a referenced module is gone), flag it as Tier 2 before A3 and surface to the user via AskUserQuestion.

---

### A2: External Research (conditional)

Invoke the researcher agent when ANY of:
- PRD references an external library/package not already in the project
- PRD references an API/endpoint with no existing implementation
- PRD proposes a pattern not seen in the codebase

```
Task(
  subagent_type="researcher",
  description="Research technical questions for $ARGUMENTS",
  prompt="Research these open questions from the PRD:
  1. [Question from PRD]
  2. [Question from PRD]

  Context: [Feature summary]

  REQUIRED OUTPUT LOCATION:
  docs/features/$ARGUMENTS/research-[topic]-[ISO-timestamp].md

  The feature folder exists and has been validated.
  Create research file with ISO timestamp format: YYYY-MM-DDTHH-MM-SSZ
  Include: findings, recommendations with rationale, trade-offs.
  Cap: 2,000 tokens per source query."
)
```

Wait for research to complete before proceeding to A3.

**Skip A2** if PRD only touches existing, well-understood patterns already verified in A1.

---

### A3: Developer Interview (6 questions via AskUserQuestion)

After presenting A1 findings, ask the following 6 questions grouped into 2–3 AskUserQuestion calls:

**Call 1 (architecture/data):**
- Q5: What's the error handling strategy — how do edge cases propagate through the system?
- Q6: Are there database schema changes? If yes, what's the migration + rollback strategy?

**Call 2 (risk/security):**
- Q7: Are there performance implications? (N+1 queries, unbounded loops, memory pressure)
- Q8: Are there security implications? (auth bypass risks, injection points, data exposure)

**Call 3 (ops/safety):**
- Q9: What's the rollback plan if this feature causes issues in production?
- Q10: Are there existing tests that will break? Have we planned for updating them?

Note: Questions 1–4 were answered by the agent in A1. Questions 5–10 surface architectural and operational assumptions that can't be read from the codebase.

---

### A4: Test Pyramid + Docs Scope (agent self-check — no user input)

Before presenting for approval:
- Define test pyramid from PRD ACs: unit X / integration Y / e2e Z counts
- Identify E2E scenario descriptions
- List any `docs/` files that will need updates as a result of this feature

---

### A5: Approval Gate

Present a structured summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL GROUNDING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Codebase validation: [X mismatches / clean]
External research: [conducted / skipped]
Interview answers: [summarized key points]
Test pyramid: Unit: X, Integration: Y, E2E: Z
Docs updates needed: [list or "none"]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use AskUserQuestion with 3 options:
- "Proceed to Phase B (create plan.md + test stubs)"
- "Adjust technical approach first" → discuss, then re-present A5
- "Run a spike first" → user redirects to /spike command; /blueprint resumes after

**→ No files written until "Proceed to Phase B" selected.**

---

## Phase B: Implementation Plan

Phase B begins only after A5 approval.

---

### B1: Additional Research (if needed)

If open PRD questions remain after A2, invoke researcher agent for remaining questions before writing plan.md.

---

### B2: Write `plan.md`

Write `docs/features/$ARGUMENTS/plan.md` following `docs/templates/plan-template.md`.

Phase A findings (codebase validation report, A3 interview answers) go into the `## Research References` section of plan.md. No separate Phase A artifact file.

**Technical Approach:**
- Overview (1-2 paragraphs)
- Key Decisions table (Decision | Choice | Rationale)

**File Changes:**
- New files to create (with purpose)
- Existing files to modify (what changes)
- Files to delete (why)

**Implementation Phases with WBS:**
- Phase 1: Foundation (setup, dependencies)
- Phase 2: Core Implementation (main functionality)
- Phase 3: Integration & Testing (wire together, verify)

The plan.md template includes a Tasks/WBS section — use it for this feature.

**Test Strategy:**
- What to test (not just "write tests")
- Unit test coverage areas
- Integration test scenarios
- E2E validation approach (from A4 pyramid)

**Dependencies & Risks:**
- External dependencies
- Internal dependencies
- Risks with mitigations

---

### B3: Challenger Review (CRITICAL)

Invoke the challenger agent to review the plan:

```
Task(
  subagent_type="challenger",
  description="Review blueprint for $ARGUMENTS",
  prompt="Review this implementation plan as a senior engineer.

  Read: docs/features/$ARGUMENTS/plan.md
  PRD: docs/features/$ARGUMENTS/prd.md

  Focus on:
  1. Is this the simplest approach?
  2. Are we building custom when off-the-shelf exists?
  3. Is scope matched to requirements?
  4. Are acceptance criteria clear and testable?
  5. Is the WBS task sizing reasonable?

  Return feedback with tier classification:
  - Tier 1: Issues I should fix (iterate without human)
  - Tier 2: Trade-offs requiring human decision

  @.claude/agents/challenger.md"
)
```

**Handle Challenger Feedback:**

**Tier 1 Issues (auto-iterate, NO human intervention):**
- Unnecessary complexity → Simplify the approach
- Missing obvious alternative → Add it to options considered
- Scope creep → Remove from scope
- Vague acceptance criteria → Rewrite with specifics

→ Update plan.md based on feedback. Continue to next step.

**Tier 2 Issues (escalate to human):**
- Simplicity vs. flexibility trade-offs
- Build vs. buy decisions
- Scope decisions affecting timeline
- Risk tolerance choices

→ Use AskUserQuestion to present options. Incorporate answer into plan.

---

### B4: Write Test Stubs with Approach Routing

Based on acceptance criteria from the PRD, create test stubs with the correct test approach annotation. Use the [test-strategy skill](../skills/test-strategy/SKILL.md) decision tree to choose the right level.

**Approach Selection:**

| Functionality | Annotation | Directory |
|---------------|-----------|-----------|
| Backend logic, pure functions, utilities, API handlers, hooks | `@test-approach: tdd` | `test/unit/FEAT-XXX/` |
| UI components, rendering, user interaction | `@test-approach: component-test` | `test/component/FEAT-XXX/` |
| API-to-DB flows, middleware chains, multi-service | `@test-approach: integration` | `test/integration/FEAT-XXX/` |
| Complete user flows across pages, auth flows | `@test-approach: e2e` | `test/e2e/` |
| **Default (if unclear)** | `@test-approach: tdd` | `test/unit/FEAT-XXX/` |

**Unit Test Stub (TDD):**

```typescript
// @test-approach: tdd
// test/unit/FEAT-XXX/[feature-name].test.ts

describe('FEAT-XXX: [Feature Name]', () => {
  describe('AC-FEAT-XXX-001: [Criterion Name]', () => {
    it('should [expected behavior from Given/When/Then]', () => {
      // TODO: Implement test
      // Given: [precondition]
      // When: [action]
      // Then: [expected result]
      throw new Error('Test not implemented');
    });
  });
});
```

**Component Test Stub:**

```typescript
// @test-approach: component-test
// test/component/FEAT-XXX/[ComponentName].test.tsx

describe('FEAT-XXX: [Component Name]', () => {
  describe('AC-FEAT-XXX-002: [Criterion Name]', () => {
    it('should [render/interaction behavior]', () => {
      // TODO: Implement test
      // Render: [component with props]
      // Interact: [user action]
      // Assert: [expected DOM state]
      throw new Error('Test not implemented');
    });
  });
});
```

**Integration Test Stub:**

```typescript
// @test-approach: integration
// test/integration/FEAT-XXX/[flow-name].test.ts

describe('FEAT-XXX: [Flow Name]', () => {
  describe('AC-FEAT-XXX-003: [Criterion Name]', () => {
    it('should [end-to-end data flow behavior]', async () => {
      // TODO: Implement test
      // Setup: [test database/services]
      // Execute: [API call or flow]
      // Verify: [response + persistence]
      // Teardown: [cleanup]
      throw new Error('Test not implemented');
    });
  });
});
```

**E2E Test Stub:**

```typescript
// @test-approach: e2e
// test/e2e/[flow-name].test.ts

describe('FEAT-XXX: [User Flow Name]', () => {
  describe('AC-FEAT-XXX-004: [Criterion Name]', () => {
    it('should [complete user flow]', async () => {
      // TODO: Implement test
      // Step 1: [navigate to page]
      // Step 2: [user action]
      // Step 3: [verify outcome]
      throw new Error('Test not implemented');
    });
  });
});
```

**Create test stubs for:**
- Each acceptance criterion (AC-FEAT-XXX-###)
- Each user story's key behavior
- Edge cases identified in PRD
- Place each stub in the correct directory based on its annotation

Test stubs should FAIL when run (throw Error). The /build command routes them by annotation.

---

### B5: Create or Update README

Write or update `docs/features/$ARGUMENTS/README.md` following `docs/templates/readme-template.md`.

**Status Section:**
```markdown
## Status

| Field | Value |
|-------|-------|
| Phase | Planning / Building / Complete |
| Last Updated | YYYY-MM-DDTHH:MM:SSZ |
| PRD | [prd.md](./prd.md) |
| Plan | [plan.md](./plan.md) |
```

Include **Manual Test Steps** — numbered steps a human can follow to verify the feature works.

---

### B6: Present Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLUEPRINT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FEATURE: $ARGUMENTS
📄 Plan: docs/features/$ARGUMENTS/plan.md
📖 README: docs/features/$ARGUMENTS/README.md
🧪 Test Stubs: test/unit/$ARGUMENTS/

Technical Approach: [Brief summary]
Files to Change: [X] new, [Y] modified
Implementation Phases: [Count]
Test Stubs Created: [Count] matching ACs

Phase A Summary:
  Codebase validation: [X mismatches / clean]
  Research: [conducted / skipped]
  Interview: [key architectural decisions captured]

Challenger Review: [Passed / Iterated on Tier 1 / Human decided Tier 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: /build $ARGUMENTS
```

---

## Success Criteria

Before completing blueprint:

- ✅ PRD was read and understood
- ✅ Phase A completed: codebase validated, research conducted if needed, interview answered
- ✅ A5 approval gate passed (user selected "Proceed to Phase B")
- ✅ No files written before A5 approval
- ✅ Plan created with clear technical approach and WBS
- ✅ Phase A findings captured in plan.md Research References
- ✅ Challenger reviewed the plan
- ✅ Tier 1 issues auto-fixed (no human needed)
- ✅ Tier 2 issues escalated to human (if any)
- ✅ TDD test stubs created (actual files, not just list)
- ✅ README created with manual test steps for humans
- ✅ All acceptance criteria are testable
- ✅ Ready for /build phase
