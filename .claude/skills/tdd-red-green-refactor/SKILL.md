---
name: tdd-red-green-refactor
description: Orchestrates TDD with isolated subagents for RED-GREEN-REFACTOR cycle. Each phase runs in clean context for true context isolation. Use when implementing features with test stubs from /blueprint, or when task requires TDD approach.
updated: 2026-02-06T16:30:00Z
---

# TDD Red-Green-Refactor (Subagent Orchestration)

Orchestrate Test-Driven Development using specialized subagents for each phase. Each agent runs in a clean 200k context window, ensuring true isolation between test writing, implementation, and refactoring.

## When to Use

- Test stubs exist from `/blueprint` phase (files with `throw new Error('Not implemented')`)
- Feature has a clear specification (PRD/plan documents)
- Implementing new functionality that requires test coverage
- After planning phase creates test skeleton

**Anti-pattern:** Running all TDD phases in the same context (allows implementation knowledge to influence test writing)

### When NOT to Use TDD Subagents

Not everything goes through RED-GREEN-REFACTOR subagents. Use inline testing instead when:

- **UI components** → `@test-approach: component-test` — inline 6-step red-green in `/build`
- **Integration flows** → `@test-approach: integration` — inline red-green in `/build`
- **E2E user flows** → `@test-approach: e2e` — inline + browser MCP in `/build`
- **Exploratory prototypes** → manual testing only (no test stubs)

Only stubs annotated `@test-approach: tdd` (or with no annotation) are processed by this skill. See the [test-strategy skill](../test-strategy/SKILL.md) for the full decision tree.

## Architecture: Subagent Isolation

```
┌─────────────────────────────────────────────────────────────────┐
│ TDD ORCHESTRATION (this skill coordinates)                      │
│                                                                 │
│ For EACH test stub from /blueprint:                             │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 🔴 RED PHASE                                            │   │
│   │ → tdd-test-writer subagent                              │   │
│   │ → Clean 200k context window                             │   │
│   │ → Sees: PRD only (NO implementation plans)              │   │
│   │ → Task: Convert stub to real failing test               │   │
│   │ → Gate: Test MUST FAIL before continuing                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                          ↓                                      │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 🟢 GREEN PHASE                                          │   │
│   │ → tdd-implementer subagent                              │   │
│   │ → Clean 200k context window                             │   │
│   │ → Sees: Test file only (NO PRD, NO plan)                │   │
│   │ → Task: Write MINIMAL code to pass test                 │   │
│   │ → Gate: Test MUST PASS before continuing                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│ After ALL tests pass:                                           │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 🔵 REFACTOR PHASE                                       │   │
│   │ → tdd-refactorer subagent                               │   │
│   │ → Clean 200k context window                             │   │
│   │ → Sees: Test files + implementation files               │   │
│   │ → Task: Improve quality, maintain behavior              │   │
│   │ → Gate: Tests MUST STAY GREEN                           │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Why Subagent Isolation?

| Problem | Solution |
|---------|----------|
| Test writer sees implementation plans → tests verify implementation, not behavior | tdd-test-writer sees only PRD |
| Implementer sees PRD → over-engineers beyond what test requires | tdd-implementer sees only the test |
| Single context → "I know how this should work" bias | Each phase: fresh 200k context |

## Core Principle: SDD + TDD

**Specification-Driven Development (SDD):** Constantly validate against the feature spec

**Test-Driven Development (TDD):** Let tests drive implementation through RED-GREEN-REFACTOR

**Together:** Spec defines WHAT to build, tests define HOW to verify, TDD drives minimal implementation

## Orchestration Workflow

### Phase 0: Preparation (Main Agent)

**BEFORE invoking subagents:**

1. Read the feature PRD: `docs/features/FEAT-XXX/prd.md`
2. Read the implementation plan: `docs/features/FEAT-XXX/plan.md`
3. Locate test stubs created by `/blueprint`
4. Determine test order (dependency-based if needed)

```bash
# Find test stubs
grep -r "throw new Error" test/ --include="*.test.ts" --include="*.spec.ts"
grep -r "pytest.skip" tests/ --include="*.py"

# Filter to TDD-only stubs (skip component-test, integration, e2e)
# Only @test-approach: tdd (or no annotation) are handled by this skill
grep -rL "@test-approach: component-test\|@test-approach: integration\|@test-approach: e2e" test/unit/ --include="*.test.ts" --include="*.spec.ts"
```

**Note:** Stubs annotated `@test-approach: component-test`, `integration`, or `e2e` are handled inline by `/build` Phase 3B, not by this skill.

### Phase 1: RED - Invoke Test Writer

For each test stub:

```
Task(
  subagent_type="tdd-test-writer",
  description="RED: Convert test stub to failing test",
  prompt="Convert the test stub at [test-file:stub] to a real failing test.

  Requirements from PRD:
  - [Acceptance Criterion from prd.md]
  - Given/When/Then: [specification]

  @.claude/agents/tdd-test-writer.md

  Gate: Return only after verifying test FAILS (not syntax error, actual failure)."
)
```

**Expected Return:**
- Test file path and line numbers modified
- Failure output showing test correctly fails
- Description of what behavior the test verifies

**Gate Validation:**
- ✅ Test runs without syntax errors
- ✅ Test FAILS (does not pass)
- ✅ Failure is meaningful (missing implementation, not import error)

### Phase 2: GREEN - Invoke Implementer

For each failing test:

```
Task(
  subagent_type="tdd-implementer",
  description="GREEN: Implement to pass test",
  prompt="Make this failing test pass with MINIMAL implementation.

  Failing test file: [test-file-path]
  Error: [failure output from RED phase]

  @.claude/agents/tdd-implementer.md

  Constraints:
  - Write the SIMPLEST code that passes
  - Do NOT read PRD or plan documents
  - Do NOT add untested features

  Gate: Return only after test PASSES."
)
```

**Expected Return:**
- Implementation file path and changes made
- Test success output
- Confirmation of minimal approach

**Gate Validation:**
- ✅ Test PASSES (green)
- ✅ No other tests broken (run full suite)
- ✅ Implementation is minimal

### Phase 3: REFACTOR - Invoke Refactorer (After All Green)

After all tests pass:

```
Task(
  subagent_type="tdd-refactorer",
  description="REFACTOR: Improve code quality",
  prompt="Refactor the implementation while keeping all tests green.

  Test files: [list of test files]
  Implementation files: [list of impl files]

  @.claude/agents/tdd-refactorer.md

  Instructions:
  - Make ONE small change at a time
  - Run tests after EACH change
  - UNDO immediately if tests fail
  - Report 'No refactoring needed' if code is clean

  Gate: All tests must remain GREEN."
)
```

**Expected Return:**
- "No refactoring needed" OR
- List of improvements made
- Final test results showing all pass

**Gate Validation:**
- ✅ All tests still pass
- ✅ No behavior changes
- ✅ Code is cleaner (or already clean)

## Handling Test Dependencies

Tests often have dependency order:

```
1. create_user() must work before...
2. update_user() which must work before...
3. delete_user()
```

**Strategy:**
1. Map test dependencies from plan.md
2. Invoke RED→GREEN for each test in topological order
3. Each test builds on previous GREEN tests
4. REFACTOR only after ALL tests pass

## Iteration Loop

```
For each test stub (in order):
    │
    ├─► RED (tdd-test-writer)
    │   └─► Gate: FAILS? → Continue
    │       └─► PASSES? → Error: Test stub doesn't test new behavior
    │
    └─► GREEN (tdd-implementer)
        └─► Gate: PASSES? → Next test
            └─► FAILS? → Debug, re-invoke implementer

After all tests:
    │
    └─► REFACTOR (tdd-refactorer)
        └─► Gate: All PASS? → Done
            └─► Any FAIL? → Undo, try different approach
```

## Success Criteria

After completing TDD cycle:

- [ ] All test stubs converted to real tests
- [ ] All tests pass (GREEN)
- [ ] Code is refactored and clean
- [ ] Each phase ran in isolated context
- [ ] No spec requirements missed
- [ ] Test coverage matches acceptance criteria

## Context Isolation Table

| Phase | Agent | Sees | Does NOT See |
|-------|-------|------|--------------|
| RED | tdd-test-writer | PRD, acceptance criteria, test stubs | Plan, implementation details, prior discussion |
| GREEN | tdd-implementer | Test file, failure output | PRD, plan, how it "should" work |
| REFACTOR | tdd-refactorer | Test files, implementation files | PRD, plan (behavior locked by tests) |

## Anti-Patterns to Avoid

### 1. Running All Phases in Main Context
```
❌ Main agent writes test, implementation, refactors
```
**Why it fails:** No context isolation, tests influenced by implementation knowledge

### 2. Passing Implementation Knowledge to Test Writer
```
❌ Task prompt: "Write tests for the validation function that uses regex"
```
**Why it fails:** Test writer now knows implementation approach

### 3. Passing PRD to Implementer
```
❌ Task prompt: "Implement to pass test. PRD says it should also handle X"
```
**Why it fails:** Implementer adds features beyond what test requires

### 4. Skipping Gates
```
❌ Continue to GREEN even though test already passes
```
**Why it fails:** Test doesn't verify new behavior

## Integration with Workflow

```
/blueprint FEAT-XXX
    ↓
Creates test stubs + plan.md
    ↓
/build FEAT-XXX
    ↓
THIS SKILL: tdd-red-green-refactor (orchestration)
    │
    ├── For each test stub:
    │   ├── Task(tdd-test-writer) → RED
    │   └── Task(tdd-implementer) → GREEN
    │
    └── After all pass:
        └── Task(tdd-refactorer) → REFACTOR
    ↓
Verify all tests pass
    ↓
Generate handover
    ↓
QA review (qa-reviewer)
    ↓
/commit
```

## Performance Metrics

**Per test stub:**
- RED phase: 1-2 minutes (subagent writes test)
- GREEN phase: 2-5 minutes (subagent implements)
- Total: ~5-7 minutes per acceptance criterion

**REFACTOR phase:**
- 2-10 minutes (depends on code complexity)

**Quality gains:**
- 95%+ test coverage (natural outcome)
- True behavior-driven tests (context isolation)
- Minimal implementations (no gold-plating)
- Clean code (refactor phase)

## Troubleshooting

### Test Writer Returns "Already Passing"
- Test stub doesn't test new behavior
- Check if stub was properly marked
- May need to adjust stub or skip if already implemented

### Implementer Can't Pass Test
- Test may have invalid assertion
- Check test expectations match realistic implementation
- May need to adjust test (rare—prefer fixing implementation)

### Refactorer Keeps Failing Tests
- Changes are modifying behavior
- Undo to last GREEN state
- Make smaller, more atomic changes

### Subagent Times Out
- Reduce scope (fewer tests per invocation)
- Split complex tests into multiple stubs
- Increase timeout if test suite is slow

## See Also

- [Test Strategy Skill](../test-strategy/SKILL.md) - Decision tree for all pyramid levels
- [TDD Test Writer Agent](.claude/agents/tdd-test-writer.md) - RED phase
- [TDD Implementer Agent](.claude/agents/tdd-implementer.md) - GREEN phase
- [TDD Refactorer Agent](.claude/agents/tdd-refactorer.md) - REFACTOR phase
- [/blueprint command](.claude/commands/blueprint.md) - Creates test stubs
- [/build command](.claude/commands/build.md) - Invokes this skill
- Kent Beck - "Test-Driven Development: By Example"
- Martin Fowler - "Refactoring"
