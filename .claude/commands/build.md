---
updated: 2026-02-06T16:30:00Z
description: Implement feature using Test-Driven Development with isolated subagents and integrated QA
argument-hint: [FEAT-ID]
---

# Build: TDD Implementation with QA

Implementing: **$ARGUMENTS**

## Mission

Implement the feature using strict Test-Driven Development with context-isolated subagents, then validate through automated QA review. Each TDD phase runs in a clean context window, ensuring tests drive design without implementation bias.

## Philosophy

**Tests drive design.** Every line of code is written to make a failing test pass. Isolated contexts prevent the test writer from knowing implementation details, and the implementer from over-engineering beyond the test's requirements.

---

## Prerequisites

```
Required:
├── docs/features/$ARGUMENTS/plan.md (implementation approach)
├── docs/features/$ARGUMENTS/prd.md (acceptance criteria)
└── test/ (test stubs from /plan)

If missing: Run /blueprint $ARGUMENTS first
```

---

## Complete Workflow

```
/build $ARGUMENTS
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 0: DISCOVER & ROUTE                                       │
│ → Grep for @test-approach: annotations in all test stubs        │
│ → Classify into 4 groups: tdd, component-test, integration, e2e │
│ → Default no-annotation stubs to tdd                            │
└─────────────────────────────────────────────────────────────────┘
    ↓
    ├── tdd stubs ──────────→ Phases 1-3 (TDD subagents)
    ├── component-test stubs → Phase 3B (inline red-green)
    ├── integration stubs ──→ Phase 3B (inline red-green)
    └── e2e stubs ──────────→ Phase 3B (inline + MCP if available)
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASES 1-3: TDD ORCHESTRATION (@test-approach: tdd only)        │
│                                                                 │
│ For EACH tdd-annotated test stub:                               │
│   🔴 RED   → tdd-test-writer (clean context)                    │
│   🟢 GREEN → tdd-implementer (clean context)                    │
│                                                                 │
│ After ALL tdd tests pass:                                       │
│   🔵 REFACTOR → tdd-refactorer (clean context)                  │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3B: INLINE TESTING (component-test, integration, e2e)     │
│                                                                 │
│ For component-test + integration stubs:                         │
│   Inline 6-step red-green (no subagent isolation)               │
│                                                                 │
│ For e2e stubs:                                                  │
│   Inline + browser MCP if available (graceful degradation)      │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: GENERATE HANDOVER                                      │
│ → Auto-run /handover $ARGUMENTS internally                      │
│ → Creates docs/features/$ARGUMENTS/handover.md                  │
│ → Captures: what built, key files, decisions                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: QA REVIEW (enhanced 10-item TDD Compliance)            │
│ → Spawn qa-reviewer subagent (clean context)                    │
│ → Reads handover.md (NOT builder conversation)                  │
│ → Creates docs/qa/$ARGUMENTS-[scope]-YYYYMMDD.md                │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 6: QA ITERATION                                           │
│ If NEEDS_FIXES → fix issues → re-run QA (loop)                  │
│ If BLOCKED → escalate to human → re-run QA after decision       │
│ If APPROVED → ready for /commit                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Discover & Route

**Goal:** Classify test stubs by approach annotation and route to the correct execution flow.

1. Grep for `@test-approach:` annotations in all test stubs:
```bash
grep -r "@test-approach:" test/ --include="*.test.ts" --include="*.test.tsx" --include="*.spec.ts"
```

2. Classify stubs into groups:

| Annotation | Routing |
|-----------|---------|
| `@test-approach: tdd` | Phases 1-3 (TDD subagents) |
| `@test-approach: component-test` | Phase 3B (inline 6-step red-green) |
| `@test-approach: integration` | Phase 3B (inline red-green) |
| `@test-approach: e2e` | Phase 3B (inline + browser MCP if available) |
| No annotation | Default: Phases 1-3 (TDD subagents) |

3. Report the routing plan before proceeding:
```
Found N test stubs:
  - X stubs → TDD subagents (Phases 1-3)
  - Y stubs → Inline testing (Phase 3B)
```

See [test-strategy skill](../skills/test-strategy/SKILL.md) for the full routing map and decision tree.

---

## Phase 1: RED - Write Failing Tests

**Goal:** Test stubs annotated `@test-approach: tdd` (or no annotation) become real tests that FAIL. Phases 1-3 apply to TDD stubs only.

Invoke the tdd-test-writer subagent for each test stub:

```
Task(
  subagent_type="tdd-test-writer",
  description="RED: Convert test stub to failing test",
  prompt="Convert the test stub for [acceptance criterion] to a real failing test.

  Requirements from PRD:
  - [AC-XXX description]
  - Given/When/Then: [specification]

  @.claude/agents/tdd-test-writer.md

  Gate: Return only after verifying test FAILS."
)
```

**Checkpoint:**
- ✅ All acceptance criteria have real tests
- ✅ All tests FAIL (proves test validity)
- ✅ Error messages describe what's missing

---

## Phase 2: GREEN - Minimal Implementation

**Goal:** Write the SIMPLEST code to pass tests.

Invoke the tdd-implementer subagent for each failing test:

```
Task(
  subagent_type="tdd-implementer",
  description="GREEN: Implement to pass test",
  prompt="Make this failing test pass with MINIMAL implementation.

  Failing test: [test-file-path]
  Error: [failure output]

  @.claude/agents/tdd-implementer.md

  Gate: Return only after test PASSES."
)
```

**Checkpoint:**
- ✅ All tests PASS
- ✅ No existing tests broken
- ✅ Implementation is minimal (no gold-plating)

---

## Phase 3: REFACTOR - Improve Quality

**Goal:** Clean up without breaking tests.

Invoke the tdd-refactorer subagent after all tests pass:

```
Task(
  subagent_type="tdd-refactorer",
  description="REFACTOR: Improve code quality",
  prompt="Refactor the implementation while keeping all tests green.

  Test files: [list]
  Implementation files: [list]

  @.claude/agents/tdd-refactorer.md

  Gate: All tests must remain GREEN."
)
```

**Checkpoint:**
- ✅ Tests still PASS
- ✅ Code is cleaner than before
- ✅ No new functionality added

---

## Phase 3B: Inline Testing (component-test, integration, e2e)

**Goal:** Handle non-TDD test stubs using inline red-green without subagent isolation.

### Component Test + Integration Stubs (Inline 6-Step Red-Green)

For each stub annotated `@test-approach: component-test` or `@test-approach: integration`:

1. **Read** the test stub and its acceptance criterion from the PRD
2. **Write** the real test (replace `throw new Error` with real assertions)
3. **Run** the test — verify it FAILS (missing implementation)
4. **Implement** the minimal code to pass the test
5. **Run** the test — verify it PASSES
6. **Review** — check the implementation meets the AC, refactor if needed

No subagent isolation is needed — the test-code feedback loop is tight enough that isolation adds overhead without benefit.

### E2E Stubs (Inline + Browser MCP)

For each stub annotated `@test-approach: e2e`:

1. **Check** if browser MCP tools are available (Playwright MCP, Stagehand, Vercel AI Browser, etc.)
2. **If MCP available:**
   - Write E2E test using MCP tools
   - Run to verify the test executes the full user flow
   - Tag findings with tool name in test output
3. **If MCP NOT available:**
   - Write E2E test stubs with documented steps
   - Generate manual test checklist from stubs
   - Note in handover: "E2E automated coverage pending — requires browser MCP (see FEAT-020)"
   - qa-reviewer will flag as Tier 1 (non-blocking)

**Checkpoint:**
- All component-test and integration tests PASS
- E2E tests PASS (with MCP) or have manual checklists (without MCP)

---

## Phase 4: Generate Handover

**Goal:** Capture build context for QA review.

After TDD completes, automatically generate handover:

```bash
# Equivalent to running /handover $ARGUMENTS
# Creates: docs/features/$ARGUMENTS/handover.md
```

The handover captures:
- Current state and what was built
- Key files modified
- Decisions made during implementation
- Git state

**This handover is the artifact for QA** - the reviewer reads this, NOT the builder conversation.

---

## Phase 5: QA Review

**Goal:** Independent security and quality review.

Spawn the qa-reviewer subagent with clean context:

```
Task(
  subagent_type="qa-reviewer",
  description="QA: Review implementation",
  prompt="Review the implementation of $ARGUMENTS.

  Context: docs/features/$ARGUMENTS/handover.md
  PRD: docs/features/$ARGUMENTS/prd.md

  @.claude/agents/qa-reviewer.md

  Perform:
  1. OWASP security review (≥80% confidence only)
  2. Code quality review
  3. TDD compliance validation
  4. Create report in docs/qa/$ARGUMENTS-[scope]-YYYYMMDD.md"
)
```

**QA Report Status:**
- **APPROVED**: All checks passed → ready for /commit
- **NEEDS_FIXES**: Issues found → proceed to Phase 6
- **BLOCKED**: Critical security issues → escalate to human

---

## Phase 6: QA Iteration

**Goal:** Resolve QA findings before commit.

### If NEEDS_FIXES:

1. Review the qa-report in `docs/qa/`
2. Address each issue (Tier 1 fixes)
   - For simple fixes (typos, obvious errors): Fix directly
   - For blocking QA issues requiring investigation: Consider `/debug [issue-description]` for systematic debugging
3. Re-run tests to verify fixes don't break anything
4. Re-run QA:

```
Task(
  subagent_type="qa-reviewer",
  description="QA: Re-review after fixes",
  prompt="Re-review $ARGUMENTS after fixes.
  Previous report: docs/qa/$ARGUMENTS-[previous].md
  @.claude/agents/qa-reviewer.md"
)
```

5. Loop until APPROVED

### If BLOCKED:

1. QA has escalated Tier 2 issues to human via AskUserQuestion
2. Present the security finding to the user
3. User decides: Block commit | Accept risk | Mark as false positive
4. Apply user's decision
5. Re-run QA to confirm resolution

### If APPROVED:

Ready for /commit. QA gate is satisfied.

---

## Wrap Up

After all phases complete:

1. Run full test suite one more time
2. Run linter if available (`npm run lint`, `ruff check`)
3. Verify QA report shows APPROVED status
4. Present summary

---

## Summary Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUILD COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 FEATURE: $ARGUMENTS
🧪 Tests: [X] passing, [Y] total
📁 Files: [A] created, [B] modified
📊 Coverage: [XX]%

TDD Cycle:
  🔴 RED: [X] tests written, all failed ✓
  🟢 GREEN: [X] tests passing ✓
  🔵 REFACTOR: Code cleaned ✓

QA Review:
  📄 Report: docs/qa/$ARGUMENTS-[scope]-YYYYMMDD.md
  ✅ Status: APPROVED
  🔒 Security: No critical issues
  📝 Quality: [X] suggestions noted

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: /commit
```

---

## Success Criteria

Before completing build:

- ✅ All test stubs converted to real tests (RED)
- ✅ All tests pass (GREEN)
- ✅ Code is refactored and clean (REFACTOR)
- ✅ Handover generated
- ✅ QA review completed
- ✅ QA status is APPROVED
- ✅ No critical security issues
- ✅ Ready for /commit

---

## TDD Best Practices

These principles ensure TDD is effective:

**1. Isolated Contexts**
Each TDD phase runs in a clean subagent context. Test writer can't see implementation plans, implementer can't see PRD requirements beyond the test.

**2. Test Behavior, Not Implementation**
Test WHAT happens, not HOW it happens. Tests should survive refactoring.

**3. Red MUST Fail**
If a test passes before implementation, it's not testing the right thing.

**4. Green MUST Pass**
Don't move on until the test is green. Debugging gets harder with more failing tests.

**5. Never Refactor with Red**
If tests are failing, fix the code first. Refactoring while red hides bugs.

**6. Tests Are Documentation**
Write test names that describe behavior: `shouldRejectInvalidEmail` not `testEmail`.

**7. QA as Safety Net**
The qa-reviewer provides an independent check. If QA finds something, it's a real issue.

---

## See Also

- [Test Strategy Skill](../skills/test-strategy/SKILL.md) - Decision tree, routing map, all pyramid levels
- [TDD Skill](.claude/skills/tdd-red-green-refactor/SKILL.md) - Orchestration details
- [TDD Test Writer](.claude/agents/tdd-test-writer.md) - RED phase
- [TDD Implementer](.claude/agents/tdd-implementer.md) - GREEN phase
- [TDD Refactorer](.claude/agents/tdd-refactorer.md) - REFACTOR phase
- [QA Reviewer](.claude/agents/qa-reviewer.md) - Security + quality review
- [/qa command](.claude/commands/qa.md) - Standalone QA
- [/commit command](.claude/commands/commit.md) - QA gate enforcement
