---
updated: 2026-02-12T00:00:00Z
description: Systematic bug investigation and resolution workflow
argument-hint: [issue-description]
---

# Debug: Systematic Bug Investigation

Investigating: **$ARGUMENTS**

## Mission

Systematically investigate and resolve bugs in existing code through phase-based debugging: classify the issue, diagnose root cause, design and implement fix with regression test, validate thoroughly, and document learnings.

## Philosophy

**Understand before fixing.** Every bug is an opportunity to improve system resilience. Fix the root cause, not symptoms. Add regression tests. Document learnings to prevent recurrence.

---

## Prerequisites

```
Required: None (debug can operate on any codebase state)

Helpful:
├── docs/features/FEAT-XXX/ (if bug relates to specific feature)
├── PROJECT.md (for system understanding)
└── docs/system/ (for architecture context)
```

---

## Quick Start

```bash
# Debug a specific issue
/debug "calculateTotal returns wrong value for discounted items"

# Debug from test failure
/debug "LoginForm.test.tsx failing with 'email field not found'"

# Debug performance issue
/debug "Dashboard load time increased from 200ms to 3s"

# Debug integration failure
/debug "API returns 500 when calling /users endpoint"
```

---

## When to Use Debug vs Other Commands

**Use /debug when:**
- Existing code has a regression (worked before, broken now)
- Tests are failing unexpectedly
- Performance degradation identified
- Integration stopped working after changes
- User-reported bugs in production
- QA found blocking issues

**Don't use /debug when:**
- Building new features → Use `/build`
- Validating technical approaches → Use `/spike`
- General code quality review → Use `/qa`
- Planning implementation → Use `/blueprint`
- Understanding codebase → Use `/explore`

---

## Workflow

Invoke the debug skill to run the 6-phase systematic debugging process:

```
/debug $ARGUMENTS
    ↓
┌─────────────────────────────────────────┐
│ Phase 0: Intake & Classification        │
│ → Classify bug type                     │
│ → Assign severity (P0-P4)               │
│ → Determine scope                       │
│ → Load context                          │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Phase 1: Investigation & Diagnosis      │
│ → Reproduce issue                       │
│ → Gather diagnostics                    │
│ → Form hypothesis                       │
│ → Research if needed                    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Phase 2: Root Cause Analysis            │
│ → Validate hypothesis                   │
│ → Identify exact failure point          │
│ → Map downstream implications           │
│ → Assess blast radius                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Phase 3: Solution Design                │
│ → Design fix approach                   │
│ → Review with challenger if complex     │
│ → Identify test requirements            │
│ → Plan documentation updates            │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Phase 4: Implementation                 │
│ → Write failing regression test (RED)   │
│ → Implement fix (GREEN)                 │
│ → Run full test suite                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Phase 5: Validation                     │
│ → Full test suite validation            │
│ → Manual smoke test                     │
│ → Performance check (if applicable)     │
│ → Security review (if P0/P1)            │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Phase 6: Documentation & Handover       │
│ → Create debug report                   │
│ → Update feature/system docs            │
│ → Update architecture docs if changed   │
│ → Prepare commit                        │
└─────────────────────────────────────────┘
    ↓
Ready for /commit
```

---

## Execution

1. Read `.claude/skills/debug/SKILL.md` for detailed phase instructions
2. Execute the 6-phase debugging workflow defined there against: **$ARGUMENTS**
3. Coordinate with other agents as needed:
   - **researcher**: For unknown tech/libraries
   - **challenger**: For complex fix trade-offs
   - **qa-reviewer**: For security validation
   - **test-strategy**: For regression test routing
   - **librarian**: For documentation updates

---

## Output Artifacts

After debug completes:

### Debug Report

**Feature bugs:**
```
docs/features/FEAT-XXX/debug-[issue-slug]-YYYYMMDD.md
```

**System bugs:**
```
docs/debug/[issue-slug]-YYYYMMDD.md
```

Contains:
- Summary (what was broken, what was fixed)
- Timeline (introduction → discovery → resolution)
- Investigation process
- Root cause analysis
- Solution approach
- Validation results
- Prevention measures

### Regression Test

Placed in correct test directory based on test-strategy:
```
test/unit/FEAT-XXX/[bug-fix].test.ts        # Logic bugs
test/component/FEAT-XXX/[bug-fix].test.tsx  # UI component bugs
test/integration/FEAT-XXX/[bug-fix].test.ts # Integration bugs
test/e2e/[bug-fix].test.ts                  # User flow bugs
```

### Updated Documentation

- **Feature README**: Updated if user-facing behavior changed
- **Handover**: Bug fix section added with debug report link
- **Architecture docs**: Updated if design changed
- **Connections**: Updated if integration boundaries changed

---

## Success Criteria

Debug session succeeds when:

- ✅ Bug reproduced and root cause identified
- ✅ Fix implemented with minimal changes
- ✅ Regression test added (fails before fix, passes after)
- ✅ Full test suite passes (no new failures)
- ✅ Manual smoke test successful
- ✅ Debug report created
- ✅ Documentation updated
- ✅ Security validated (if P0/P1)
- ✅ Changes staged for /commit

---

## Summary Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEBUG COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 BUG: $ARGUMENTS
📊 Classification: [Type] | [Severity] | [Scope]

Investigation:
  🔍 Root Cause: [file:line] - [description]
  📈 Blast Radius: [X] files, [Y] features affected

Fix:
  ✅ Regression test: [test-file]
  📝 Changes: [X] files modified
  🧪 Tests: All passing

Documentation:
  📄 Debug report: [path-to-report]
  📚 Docs updated: [list of updated docs]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: /commit
```

---

## Integration Points

### From /build

If tests fail during implementation:
```
/build FEAT-XXX
    ↓
Test failure: "Unexpected error in validation"
    ↓
/debug "Test failure: validation error in user signup"
    ↓
[debug workflow]
    ↓
Fix + regression test
    ↓
Resume /build
```

### From /qa

QA findings trigger debug:
```
/qa FEAT-XXX
    ↓
QA report: "NEEDS_FIXES - SQL injection in search"
    ↓
/debug "SQL injection vulnerability in user search"
    ↓
[debug workflow with qa-reviewer validation]
    ↓
Fix approved
    ↓
/commit
```

### To /commit

Debug prepares for commit:
```
/debug [issue]
    ↓
[phases 0-6 complete]
    ↓
All gates passed
    ↓
/commit
    ↓
Commit includes:
  - Fix
  - Regression test
  - Debug report reference
```

---

## Examples

### Example 1: Logic Bug
```bash
/debug "calculateTotal function returns wrong value for discounted items"

# Workflow:
# Phase 0: Classify as logic bug, P2, feature FEAT-012
# Phase 1: Reproduce with test data, form hypothesis about discount calculation
# Phase 2: Root cause: off-by-one error in discount loop
# Phase 3: Design minimal fix
# Phase 4: Write regression test, implement fix
# Phase 5: Validate with test suite + manual test
# Phase 6: Create debug report, update docs
```

### Example 2: Integration Failure
```bash
/debug "API returns 500 when calling /users endpoint after auth changes"

# Workflow:
# Phase 0: Classify as integration bug, P1, system-wide
# Phase 1: Reproduce via API call, check logs, form hypothesis about auth middleware
# Phase 2: Root cause: auth middleware expects JWT format change
# Phase 3: Design fix with challenger (multiple options)
# Phase 4: Implement fix, add integration test
# Phase 5: Validate with full test suite, manual API test
# Phase 6: Create debug report, update architecture docs
```

### Example 3: Performance Regression
```bash
/debug "Dashboard load time increased from 200ms to 3s after FEAT-022"

# Workflow:
# Phase 0: Classify as performance bug, P2, feature FEAT-022
# Phase 1: Profile with dev tools, identify slow query
# Phase 2: Root cause: N+1 query introduced in recent change
# Phase 3: Design fix (add join or caching)
# Phase 4: Implement fix, add performance regression test
# Phase 5: Benchmark before/after, validate improvement
# Phase 6: Create debug report, document performance patterns
```

### Example 4: Test Failure
```bash
/debug "LoginForm.test.tsx failing with 'email field not found'"

# Workflow:
# Phase 0: Classify as test failure, P3, feature FEAT-015
# Phase 1: Run test locally, inspect component rendering
# Phase 2: Root cause: selector changed but test not updated
# Phase 3: Design fix (update test selector)
# Phase 4: Fix test, verify passes
# Phase 5: Run full test suite
# Phase 6: Create debug report, note test maintenance pattern
```

### Example 5: UI/Frontend Bug
```bash
/debug "Submit button misaligned on mobile - overlaps with text input"

# Workflow:
# Phase 0: Classify as logic bug (UI - styling), P3, feature FEAT-018
# Phase 1: Reproduce on mobile viewport, inspect element
#          - Use browser DevTools or Playwright to capture screenshots
#          - Check computed styles: margin-top: -20px causing overlap
#          - Screenshots saved to mcp.output if using Playwright
# Phase 2: Root cause: Tailwind class 'mt--5' should be 'mt-5'
# Phase 3: Design fix (correct CSS class)
# Phase 4: Update Button.tsx, add component test with mobile viewport
# Phase 5: Visual verification at 320px, 768px, 1920px viewports
#          Manual smoke test on actual mobile device
# Phase 6: Create debug report with before/after screenshots
#          Update component documentation

# Note: Uses UI Bug Investigation Checklist from decision-trees.md
# Test routed to: test/component/FEAT-018/Button.test.tsx (component-test)
```

---

## See Also

- [Debug Skill](.claude/skills/debug/SKILL.md) - Complete debugging workflow
- [Test Strategy Skill](.claude/skills/test-strategy/SKILL.md) - Regression test routing
- [/build Command](build.md) - Feature implementation with TDD
- [/qa Command](qa.md) - Quality and security review
- [QA Reviewer Agent](../agents/qa-reviewer.md) - Security validation
- [Challenger Agent](../agents/challenger.md) - Fix approach review
- [Researcher Agent](../agents/researcher.md) - Technical investigation
