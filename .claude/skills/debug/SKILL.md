---
name: debug
description: Systematic bug investigation and resolution workflow. Use when bugs are found in existing code (logic errors, integration failures, performance regressions, test failures). Embodies senior engineer debugging approach with phase-based investigation, root cause analysis, fix implementation with tests, validation, and documentation.
---

# Debug Skill

Systematic bug investigation and resolution workflow for production and development issues. This skill embodies a senior software engineer's debugging approach: investigate systematically, understand root causes, fix with tests, validate thoroughly, and document learnings.

**Key principle:** Understand before fixing. Every bug fix includes a regression test and documentation update.

## When to Use

### Decision Tree: Debug vs Other Commands

```
Is this about existing code that's broken?
  NO → Use /build (new feature) or /blueprint (design work)
  YES ↓

Is this code that never worked (new feature failing)?
  YES → Use /build (implementation issue, not a bug)
  NO ↓

Is this investigating an approach (not fixing production code)?
  YES → Use /spike (time-boxed technical investigation)
  NO ↓

Is this about code quality without a specific failure?
  YES → Use /qa (quality review)
  NO ↓

→ USE /debug [description]
```

### Trigger Conditions

**Use /debug when:**
- Production code has a regression (worked before, broken now)
- Test failures in existing tests
- Performance degradation identified
- Integration failures after changes
- User-reported bugs
- QA findings that require investigation

**Don't use /debug when:**
- Building new features → `/build`
- Validating technical approach → `/spike`
- General quality review → `/qa`
- Understanding codebase → `/explore`

## Architecture: 6-Phase Workflow

```
/debug [issue-description]
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 0: INTAKE & CLASSIFICATION                                │
│ → Parse issue description                                       │
│ → Classify bug type (logic/integration/performance/test)        │
│ → Assign severity (P0-P4)                                       │
│ → Determine scope (feature vs system)                           │
│ → Load context (feature docs or system docs)                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: INVESTIGATION & DIAGNOSIS                              │
│ → Reproduce issue locally                                       │
│ → Gather diagnostic data (logs, stack traces, state)            │
│ → Form hypothesis about cause                                   │
│ → Coordinate with researcher if unknown tech in stack           │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: ROOT CAUSE ANALYSIS                                    │
│ → Validate hypothesis with targeted tests                       │
│ → Identify exact failure point (file:line)                      │
│ → Map downstream implications                                   │
│ → Assess blast radius (what else affected?)                     │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: SOLUTION DESIGN                                        │
│ → Design fix approach                                           │
│ → Coordinate with challenger if complex/trade-offs              │
│ → Identify regression test requirements                         │
│ → Plan documentation updates                                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: IMPLEMENTATION                                         │
│ → Write failing regression test (RED)                           │
│ → Verify test fails with current code                           │
│ → Implement fix (GREEN)                                         │
│ → Verify fix passes test                                        │
│ → Run full test suite (no regressions)                          │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: VALIDATION                                             │
│ → Full test suite passes                                        │
│ → Manual smoke test                                             │
│ → Performance validation (if perf bug)                          │
│ → Security validation (coordinate with qa-reviewer if needed)   │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 6: DOCUMENTATION & HANDOVER                               │
│ → Create debug report                                           │
│ → Update feature docs (if user-facing change)                   │
│ → Update architecture docs (if design changed)                  │
│ → Prepare commit with regression test                           │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 0: Intake & Classification

**Goal:** Understand the bug and load the right context.

### Actions

1. **Parse Issue Description**
   - Extract: symptoms, expected behavior, actual behavior, context
   - Identify: files involved, error messages, reproduction steps

2. **Classify Bug Type** (see references/decision-trees.md for full tree)
   - **Logic Bug**: Incorrect calculation, wrong conditional, off-by-one
   - **Integration Failure**: API contract mismatch, service communication failure
   - **Performance Regression**: Increased latency, memory leak, N+1 queries
   - **Test Failure**: Flaky test, broken assertion, environment issue

   **Note:** UI/Frontend bugs (styling, component rendering, interactions) are classified as **LOGIC BUG** with sub-type annotation (e.g., "LOGIC BUG (UI - styling)"). This triggers the [UI Bug Investigation Checklist](references/decision-trees.md#ui-bug-investigation-checklist) for visual debugging steps.

3. **Assign Severity**
   - **P0 (Critical)**: Production down, data loss, security breach
   - **P1 (High)**: Major functionality broken, blocking users
   - **P2 (Medium)**: Feature partially broken, workaround exists
   - **P3 (Low)**: Minor issue, cosmetic, edge case
   - **P4 (Trivial)**: Nice-to-have, no user impact

4. **Determine Scope**
   - **Feature bug**: Related to specific FEAT-XXX → Load `docs/features/FEAT-XXX/`
   - **System bug**: Cross-cutting or infrastructure → Load `PROJECT.md`, `docs/system/`

5. **Load Context**
   ```bash
   # If feature bug:
   docs/features/FEAT-XXX/README.md
   docs/features/FEAT-XXX/prd.md
   docs/features/FEAT-XXX/plan.md

   # If system bug:
   PROJECT.md
   docs/system/architecture.md
   docs/system/connections.md
   ```

### Gate Criteria

- ✅ Bug type classified
- ✅ Severity assigned
- ✅ Scope determined (feature vs system)
- ✅ Context loaded
- ✅ Reproduction steps identified (or marked unknown)

## Phase 1: Investigation & Diagnosis

**Goal:** Reproduce the issue and form a hypothesis.

### Actions

1. **Reproduce Locally**
   - Follow reproduction steps from issue description
   - If steps missing: investigate from error message / stack trace
   - Document exact steps to trigger bug

2. **Gather Diagnostic Data**
   - Stack traces
   - Error messages
   - Application state at failure
   - Relevant logs
   - Environment variables (if applicable)

3. **Form Hypothesis**
   - What component/function is failing?
   - What changed recently? (check git log)
   - What input causes the failure?
   - What output is expected vs actual?

4. **Coordinate with Researcher** (if unknown technology)
   - If bug involves unfamiliar library/framework/API
   - If error message is cryptic and not well-documented

   ```
   Task(
     subagent_type="researcher",
     description="Research [library/error] for debug investigation",
     prompt="Research this error/technology to help debug:

     Issue: [bug description]
     Error: [error message]
     Context: [relevant code snippet]

     Find:
     1. Common causes of this error
     2. Debugging strategies
     3. Known issues in this library version

     Feature folder: docs/features/FEAT-XXX/ (or docs/debug/ if system)
     Create: research-debug-[topic]-[timestamp].md"
   )
   ```

### Gate Criteria

- ✅ Bug reproduced locally (or reproduction steps documented)
- ✅ Diagnostic data collected
- ✅ Hypothesis formed (even if unvalidated)
- ✅ Research completed if unknown tech involved

## Phase 2: Root Cause Analysis

**Goal:** Validate the hypothesis and identify the exact failure point.

### Actions

1. **Validate Hypothesis**
   - Write minimal test case that isolates the failure
   - Add debug logging around suspected code
   - Use debugger to step through execution

2. **Identify Exact Failure Point**
   - File path: `src/path/to/file.ts`
   - Line number: `123`
   - Function/method: `calculateDiscount()`
   - Exact condition: "Division by zero when cartItems.length === 0"

3. **Map Downstream Implications**
   - What other code calls this function?
   - What features depend on this behavior?
   - Are there similar bugs in related code?

4. **Assess Blast Radius**
   - How many users affected?
   - How many code paths affected?
   - Are there existing tests that should have caught this?

### Gate Criteria

- ✅ Hypothesis validated (root cause confirmed)
- ✅ Exact failure point identified (file:line)
- ✅ Downstream implications mapped
- ✅ Blast radius assessed

## Phase 3: Solution Design

**Goal:** Design the fix and plan implementation.

### Actions

1. **Design Fix Approach**
   - **Quick Fix**: Minimal change to resolve immediate issue
   - **Proper Fix**: Address root cause, may touch more code
   - **Refactor**: Fix reveals design flaw, requires restructuring

   Document trade-offs:
   - Quick fix now + proper fix later?
   - Or proper fix immediately?

2. **Coordinate with Challenger** (if complex or trade-offs exist)
   ```
   Task(
     subagent_type="challenger",
     description="Review fix approach for [bug]",
     prompt="Review this bug fix approach as a senior engineer.

     Bug: [description]
     Root Cause: [exact issue]
     Proposed Fix: [approach description]

     Alternatives considered:
     1. [Option 1]: [pros/cons]
     2. [Option 2]: [pros/cons]

     Focus on:
     1. Is this addressing root cause or symptom?
     2. Is this the simplest fix?
     3. Are there hidden implications?
     4. Is blast radius acceptable?

     @.claude/agents/challenger.md"
   )
   ```

3. **Identify Regression Test Requirements**
   - Use test-strategy skill to determine test level
   - What exactly should the regression test verify?
   - Should it be unit, integration, or e2e?

   ```
   Task(
     subagent_type="general-purpose",
     description="Determine test level for regression test",
     prompt="Determine the appropriate test pyramid level for this regression test.

     Bug: [description]
     Root Cause: [failure point]

     @.claude/skills/test-strategy/SKILL.md

     Return: Annotation (@test-approach: tdd|component-test|integration|e2e) and directory"
   )
   ```

4. **Plan Documentation Updates**
   - Feature README: Update if user-facing behavior changed
   - Handover: Add bug fix section
   - Plan: Update if architecture changed
   - Connections: Update if integration boundaries changed

### Gate Criteria

- ✅ Fix approach designed
- ✅ Challenger reviewed (if complex)
- ✅ Regression test requirements identified
- ✅ Documentation updates planned

## Phase 4: Implementation

**Goal:** Implement the fix with test-first approach.

### Actions

1. **Write Failing Regression Test (RED)**
   - Create test file in correct directory (from test-strategy)
   - Test should reproduce the bug
   - Verify test FAILS with current code
   - Test description should reference the bug: `"should [fix description] (fixes #XXX)"`

2. **Implement Fix (GREEN)**
   - Make minimal changes to pass the regression test
   - Follow existing code patterns
   - Add inline comments if fix is non-obvious

3. **Run Full Test Suite**
   - Verify regression test passes
   - Verify no other tests broken
   - If tests fail: investigate and fix

4. **Lint and Format**
   ```bash
   npm run lint
   npm run format
   # or equivalent for project
   ```

### Gate Criteria

- ✅ Regression test written and initially fails
- ✅ Fix implemented
- ✅ Regression test passes
- ✅ Full test suite passes
- ✅ Code is linted and formatted

## Phase 5: Validation

**Goal:** Ensure the fix works and doesn't introduce new issues.

### Actions

1. **Full Test Suite Validation**
   ```bash
   npm test
   # Verify: All tests passing
   ```

2. **Manual Smoke Test**
   - Follow original reproduction steps
   - Verify bug is fixed
   - Test edge cases related to the fix
   - Verify no obvious regressions in related features

3. **Performance Validation** (if performance bug)
   - Benchmark before/after
   - Verify performance meets acceptable threshold
   - Check for unintended performance impacts elsewhere

4. **Security Validation** (if P0/P1 or security-related)
   - Coordinate with qa-reviewer for security check

   ```
   Task(
     subagent_type="qa-reviewer",
     description="Security review of bug fix",
     prompt="Review this bug fix for security implications.

     Bug: [description]
     Severity: [P0/P1]
     Fix: [files changed]

     Context: Create minimal handover with:
     - What was fixed
     - Files changed
     - Security considerations

     @.claude/agents/qa-reviewer.md

     Focus OWASP review on changed code only."
   )
   ```

### Gate Criteria

- ✅ All tests passing
- ✅ Manual smoke test successful
- ✅ Performance acceptable (if perf bug)
- ✅ Security reviewed (if P0/P1 or security-related)
- ✅ No new issues introduced

## Phase 6: Documentation & Handover

**Goal:** Document the fix for future reference and prepare commit.

### Actions

1. **Create Debug Report**

   **Location:**
   - Feature bugs: `docs/features/FEAT-XXX/debug-[issue-slug]-YYYYMMDD.md`
   - System bugs: `docs/debug/[issue-slug]-YYYYMMDD.md`

   **Use template:** `.claude/skills/debug/references/debug-report-template.md`

   **Key sections:**
   - Summary: What was broken, what was fixed
   - Timeline: When bug introduced, when discovered, when fixed
   - Investigation: Diagnostic process
   - Root Cause: Exact failure point and why it happened
   - Solution: What was changed and why
   - Validation: How fix was verified
   - Prevention: What prevents similar bugs

2. **Update Feature Documentation** (if applicable)

   **For feature bugs:**
   - Update `docs/features/FEAT-XXX/README.md`:
     - Add debug report to "Related Documents"
     - Update manual test steps if behavior changed
   - Update `docs/features/FEAT-XXX/handover.md`:
     - Add "Bug Fixes" section with reference to debug report

   **For system bugs:**
   - Update `docs/debug/README.md` with link to new debug report
   - Update `docs/system/architecture.md` if architecture changed

3. **Update Architecture Docs** (if design changed)
   - `docs/system/connections.md`: Update integration boundaries
   - `docs/system/architecture.md`: Update component descriptions
   - Feature `plan.md`: Update if implementation approach changed

4. **Prepare Commit**
   - Stage changes (fix + test + docs)
   - Ready for `/commit` command
   - Commit message will reference debug report

### Gate Criteria

- ✅ Debug report created
- ✅ Feature/system docs updated
- ✅ Architecture docs updated (if changed)
- ✅ Changes staged for commit
- ✅ All documentation links valid

## Agent Coordination

The debug skill coordinates with other agents when specialized expertise is needed:

### Researcher Agent

**When:** Unknown technology, cryptic errors, library-specific issues

**Trigger conditions:**
- Stack trace involves unfamiliar library
- Error message not well-documented
- Bug involves third-party API behavior
- Need to understand library internals

**Example:**
```
Error: "Cannot read property 'apply' of undefined" in React hooks

→ Invoke researcher to understand React hooks lifecycle
→ Creates: research-debug-react-hooks-[timestamp].md
```

### Challenger Agent

**When:** Multiple fix approaches with trade-offs, complex fixes, refactoring required

**Trigger conditions:**
- Quick fix vs proper fix decision
- Fix requires significant refactoring
- Multiple viable approaches
- Blast radius > 5 files or > 2 features

**Example:**
```
Bug: Race condition in async data loading
Options:
  1. Add mutex (quick fix, adds complexity)
  2. Redesign data flow (proper fix, larger change)

→ Invoke challenger to evaluate trade-offs
→ Returns: Recommendation with reasoning
```

### QA Reviewer Agent

**When:** P0/P1 bugs, security-related fixes, critical path changes

**Trigger conditions:**
- Severity is P0 or P1
- Bug involves authentication, authorization, or data handling
- Fix touches security-sensitive code
- Fix changes API contracts

**Example:**
```
Bug: SQL injection in user search
Fix: Add parameterized queries

→ Invoke qa-reviewer for security validation
→ Creates: docs/qa/sql-injection-fix-YYYYMMDD.md
```

### Test Strategy Skill

**When:** Determining regression test level

**Always used** in Phase 3 to route regression test to correct pyramid level.

**Example:**
```
Bug: React component not rendering correct state
Root cause: useState hook misused

→ Use test-strategy to determine level
→ Result: @test-approach: component-test
→ Directory: test/component/FEAT-XXX/
```

### Librarian Agent

**When:** Documentation inconsistency found, architecture changed, cross-references broken

**Trigger conditions:**
- Fix changes API signatures (need to update docs)
- Multiple docs reference changed behavior
- Architecture diagram needs updating

**Example:**
```
Bug fix changes authentication flow

→ Invoke librarian to update all auth references
→ Updates: docs/system/architecture.md, FEAT-015/README.md, etc.
```

## Output Artifacts

### Debug Reports

**Feature Bugs:**
```
docs/features/FEAT-XXX/debug-[issue-slug]-YYYYMMDD.md
```

**System Bugs:**
```
docs/debug/[issue-slug]-YYYYMMDD.md
```

**Structure:** See `.claude/skills/debug/references/debug-report-template.md`

### Updated Documentation

**Feature README:**
- Related Documents section: Link to debug report
- Manual Test Steps: Updated if behavior changed

**Handover:**
- Bug Fixes section: Reference to debug report and changes

**Architecture Docs:**
- Updated if design/integration boundaries changed

### Regression Test

**Location determined by test-strategy:**
- Unit: `test/unit/FEAT-XXX/[bug-fix].test.ts`
- Component: `test/component/FEAT-XXX/[bug-fix].test.tsx`
- Integration: `test/integration/FEAT-XXX/[bug-fix].test.ts`
- E2E: `test/e2e/[bug-fix].test.ts`

**Test naming convention:**
```typescript
// Regression test for bug #42
describe('Bug #42: [short description]', () => {
  it('should [expected behavior that was broken]', () => {
    // Test reproduces the bug scenario
    // Verifies fix prevents regression
  });
});
```

## Success Metrics

Debug session succeeds if:

| Metric | Good | Bad |
|--------|------|-----|
| **Time to Root Cause** | < 30 minutes | > 2 hours |
| **Test Coverage** | Regression test added | Fix without test |
| **Blast Radius** | Fix is minimal | Fix touches unrelated code |
| **Documentation** | Debug report + docs updated | No documentation |
| **Recurrence** | Bug doesn't return | Same bug appears again |

## Integration with Workflow

```
User reports bug
    ↓
/debug [description]
    ↓
[6-phase debug workflow]
    ↓
Changes staged + Debug report created
    ↓
/commit
    ↓
Git commit with:
  - Fix
  - Regression test
  - Debug report reference
```

### With /build

If tests fail during `/build`:

```markdown
## If Tests Fail During Implementation

If tests fail unexpectedly during implementation:
- First check for typos or obvious errors
- If issue is unclear, use `/debug [description]` for systematic investigation
```

### With /qa

QA findings can trigger debug sessions:

```
/qa FEAT-XXX
    ↓
QA report shows: "Security issue in authentication"
    ↓
/debug "Authentication allows bypass via header manipulation"
    ↓
[debug workflow]
```

### With /commit

Debug workflow prepares for commit:

```
/debug [issue]
    ↓
[phases 0-6]
    ↓
All gates passed
    ↓
/commit
    ↓
Commit message includes:
  fix: [bug description]

  Root cause: [brief explanation]
  Regression test: [test file]
  Debug report: docs/features/FEAT-XXX/debug-[slug]-YYYYMMDD.md
```

## Anti-Patterns

### Debugging Without Understanding

```
❌ See error → Google → Copy/paste fix → Ship
```

**Why it fails:** No understanding of root cause, likely to recur

**Correct:**
```
✅ See error → Reproduce → Diagnose → Understand → Fix with test → Document
```

### Fixing Symptoms Instead of Root Cause

```
❌ "NullPointerException" → Add null check everywhere
```

**Why it fails:** Treats symptom, not disease

**Correct:**
```
✅ Trace why value is null → Fix data flow → Prevent null at source
```

### Skipping Regression Test

```
❌ Fix bug → Manual test → Ship → Bug returns next sprint
```

**Why it fails:** No automated safety net

**Correct:**
```
✅ Write failing test → Fix → Test passes → Bug can't return silently
```

### Over-Engineering the Fix

```
❌ Simple logic bug → Redesign entire module → 3 weeks later...
```

**Why it fails:** Perfect is enemy of good

**Correct:**
```
✅ Identify minimal fix → Validate with challenger → Implement → Note refactor as technical debt
```

### Debugging in Production

```
❌ Add debug logging to production → Deploy → Check logs → Remove logging
```

**Why it fails:** Risk, slow feedback loop

**Correct:**
```
✅ Reproduce locally → Debug locally → Fix → Validate → Deploy
```

## References

- [Decision Trees](references/decision-trees.md) - Bug classification, severity, scope, agent coordination
- [Debug Report Template](references/debug-report-template.md) - Complete report structure
- [Test Strategy Skill](../test-strategy/SKILL.md) - Regression test level routing

## See Also

- [/build Command](../../commands/build.md) - Suggests /debug on unexpected test failures
- [/qa Command](../../commands/qa.md) - Quality review can surface bugs
- [QA Reviewer Agent](../../agents/qa-reviewer.md) - Security validation for fixes
- [Challenger Agent](../../agents/challenger.md) - Fix approach validation
- [Researcher Agent](../../agents/researcher.md) - Technical investigation support
- [Test Strategy Skill](../test-strategy/SKILL.md) - Test level routing
