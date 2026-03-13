# Debug Report Template

Use this template for all debug reports. Copy frontmatter and sections exactly.

## Template Structure

```markdown
---
type: debug-report
date: YYYY-MM-DDTHH:MM:SSZ
bug-type: logic | integration | performance | test
severity: P0 | P1 | P2 | P3 | P4
scope: FEAT-XXX | system
status: fixed | monitoring | known-limitation
fixed-in: commit-sha (if fixed)
regression-test: path/to/test.ts (if added)
---

# Debug Report: [Issue Short Title]

**Date:** YYYY-MM-DD
**Reporter:** [Who reported]
**Assignee:** [Who investigated/fixed]
**Duration:** [Time from discovery to fix]

## Summary

### What Was Broken
[1-2 sentences: What functionality was not working correctly]

### What Was Fixed
[1-2 sentences: What changed to resolve the issue]

### Impact
- **Users Affected:** [Number/percentage or "All users" or "Edge case only"]
- **Features Affected:** [List affected features or "System-wide"]
- **Blast Radius:** [X files, Y functions, Z features]

## Timeline

| Time | Event |
|------|-------|
| YYYY-MM-DD HH:MM | Bug introduced (if known) |
| YYYY-MM-DD HH:MM | Bug discovered |
| YYYY-MM-DD HH:MM | Investigation started |
| YYYY-MM-DD HH:MM | Root cause identified |
| YYYY-MM-DD HH:MM | Fix implemented |
| YYYY-MM-DD HH:MM | Fix validated |
| YYYY-MM-DD HH:MM | Fix deployed (if applicable) |

## Investigation

### Reproduction Steps

1. [Step 1 to reproduce the bug]
2. [Step 2]
3. [Step 3]

**Expected Result:** [What should happen]
**Actual Result:** [What actually happened]

**Visual Evidence** (for UI bugs - include screenshots):
```markdown
![Bug - incorrect rendering](./screenshots/bug-before.png)
![Expected - correct rendering](./screenshots/expected.png)

Note: If using Playwright MCP, screenshots are automatically saved to mcp.output directory.
Reference the file paths from MCP output.
```

### Diagnostic Data

**Error Messages:**
```
[Stack trace or error messages]
```

**Environment:**
- OS: [Operating system]
- Browser: [Browser version if applicable]
- Node Version: [If applicable]
- Dependencies: [Relevant package versions]

**State at Failure:**
```
[Relevant application state, variables, database state]
```

### Hypothesis

**Initial Hypothesis:** [What we thought was wrong]

**Validation:** [How we tested the hypothesis]

**Result:** [Confirmed / Rejected / Refined]

## Root Cause Analysis

### Exact Failure Point

**File:** `src/path/to/file.ts`
**Line:** `123`
**Function:** `functionName()`
**Code:**
```typescript
// Problematic code
const result = doSomething(input); // Bug: [specific issue]
```

### Why It Failed

[Detailed explanation of the root cause. What condition triggered the failure? What assumption was wrong?]

### Why It Wasn't Caught

- [ ] No test existed for this case
- [ ] Test existed but was too lenient
- [ ] Test was flaky and ignored
- [ ] Error was silently swallowed
- [ ] Condition only occurs in production environment
- [ ] Other: [Explanation]

### When It Was Introduced

**Commit:** `abc1234` (if identified)
**PR:** #XXX (if applicable)
**Feature:** FEAT-XXX (if applicable)

**Context:** [Why was the change made that introduced the bug?]

## Downstream Implications

### What Else Was Affected

- [ ] Feature A: [How it was affected]
- [ ] Feature B: [How it was affected]
- [ ] API Contract: [What changed]
- [ ] Database: [Schema or data affected]
- [ ] Other: [Description]

### Similar Bugs Identified

- [ ] No similar issues found
- [ ] Similar pattern in [location]: [Description]
- [ ] Similar pattern in [location]: [Description]

## Solution

### Fix Approach

**Approach Chosen:** [Quick fix / Proper fix / Refactor]

**Why This Approach:**
[Rationale for the chosen approach]

**Alternatives Considered:**
1. [Alternative 1]: [Why not chosen]
2. [Alternative 2]: [Why not chosen]

### Code Changes

**Files Modified:**
- `src/path/to/file1.ts` - [What changed]
- `src/path/to/file2.ts` - [What changed]

**Key Changes:**
```diff
// Before
- const result = doSomething(input);
+ const result = doSomethingCorrectly(input);
// After
```

**Explanation:**
[Explain what changed and why it fixes the issue]

### Regression Test Added

**Test File:** `test/unit/FEAT-XXX/bug-fix.test.ts`
**Test Level:** unit | component | integration | e2e
**Annotation:** `@test-approach: tdd`

**Test Description:**
```typescript
describe('Bug #42: [short description]', () => {
  it('should [expected behavior that was broken]', () => {
    // Given: [precondition that triggers bug]
    // When: [action that caused failure]
    // Then: [expected correct behavior]
  });
});
```

**Test Validates:**
- [ ] Bug scenario is reproduced
- [ ] Fix prevents regression
- [ ] Edge cases are covered

## Validation

### Test Results

**Regression Test:**
- Before fix: ❌ FAIL (as expected)
- After fix: ✅ PASS

**Full Test Suite:**
- All tests: ✅ PASS
- New failures: None
- Flaky tests: None

### Manual Validation

**Smoke Test:**
1. [Manual test step 1] - ✅ PASS
2. [Manual test step 2] - ✅ PASS
3. [Manual test step 3] - ✅ PASS

**Edge Cases:**
- [ ] [Edge case 1]: Validated
- [ ] [Edge case 2]: Validated

### Performance Validation

(If applicable for performance bugs)

**Before Fix:**
- Response time: [X]ms
- Memory usage: [Y]MB
- Queries: [Z]

**After Fix:**
- Response time: [X]ms (improvement: [±X]%)
- Memory usage: [Y]MB (improvement: [±Y]%)
- Queries: [Z] (improvement: [±Z]%)

### Security Validation

(If applicable for P0/P1 or security-related fixes)

**QA Review:** [Link to qa-reviewer report if applicable]

**OWASP Checks:**
- [ ] No new vulnerabilities introduced
- [ ] Fix closes security gap
- [ ] No sensitive data exposed

## Prevention

### How to Prevent Similar Bugs

**Immediate Actions:**
- [ ] Add similar regression tests for related code
- [ ] Update code review checklist
- [ ] Add linting rule (if applicable)
- [ ] Update documentation

**Long-term Actions:**
- [ ] Refactor related code to prevent class of bugs
- [ ] Add architectural guardrails
- [ ] Improve monitoring/alerting
- [ ] Team training on [topic]

### What We Learned

**Technical Learnings:**
- [Key insight about the system]
- [Pattern to watch for in future]
- [Assumption that was wrong]

**Process Learnings:**
- [How we could catch this earlier]
- [What test was missing]
- [What documentation would have helped]

### Documentation Updates

**Updated Documents:**
- [ ] `docs/features/FEAT-XXX/README.md` - Added debug report link
- [ ] `docs/features/FEAT-XXX/handover.md` - Added bug fix section
- [ ] `docs/system/architecture.md` - Updated if design changed
- [ ] `docs/system/connections.md` - Updated if integration boundaries changed
- [ ] Other: [List]

## Related Links

- **PRD:** [link if feature bug]
- **Plan:** [link if feature bug]
- **Commit:** [link to fix commit]
- **Issue:** [link to issue tracker if applicable]
- **QA Report:** [link if qa-reviewer was involved]
- **Research:** [link if researcher was involved]

## Checklist

Before closing this debug report, verify:

- [ ] Root cause identified and documented
- [ ] Fix implemented and committed
- [ ] Regression test added (fails before, passes after)
- [ ] Full test suite passes
- [ ] Manual smoke test passes
- [ ] Documentation updated
- [ ] Similar patterns checked
- [ ] Prevention measures identified
- [ ] All links in report are valid
```

---

## Example: Filled Debug Report

```markdown
---
type: debug-report
date: 2026-02-12T14:30:00Z
bug-type: logic
severity: P2
scope: FEAT-012
status: fixed
fixed-in: a3f8c92
regression-test: test/unit/FEAT-012/discount-calculation.test.ts
---

# Debug Report: Discount Calculation Returns Incorrect Total

**Date:** 2026-02-12
**Reporter:** User via bug report
**Assignee:** Claude
**Duration:** 45 minutes

## Summary

### What Was Broken
The calculateTotal() function was returning incorrect totals when applying discounts to cart items. Users saw higher prices than expected at checkout.

### What Was Fixed
Fixed off-by-one error in discount calculation loop that was skipping the last item in the cart.

### Impact
- **Users Affected:** Approximately 15% (users with 3+ items in cart)
- **Features Affected:** FEAT-012 (Checkout), FEAT-008 (Cart Display)
- **Blast Radius:** 1 file, 1 function, 2 features

## Timeline

| Time | Event |
|------|-------|
| 2026-02-08 10:00 | Bug introduced in commit b2c4567 |
| 2026-02-11 15:30 | Bug discovered by user |
| 2026-02-12 14:00 | Investigation started |
| 2026-02-12 14:20 | Root cause identified |
| 2026-02-12 14:35 | Fix implemented |
| 2026-02-12 14:45 | Fix validated |

## Investigation

### Reproduction Steps

1. Add 3 items to cart
2. Apply a 10% discount code
3. Proceed to checkout
4. Observe total price

**Expected Result:** Total should be (item1 + item2 + item3) * 0.9
**Actual Result:** Total was (item1 + item2) * 0.9 (last item not discounted)

### Diagnostic Data

**Error Messages:**
No error messages - silent logic bug

**Environment:**
- OS: macOS 14
- Browser: Chrome 120
- Node Version: 20.10.0
- Dependencies: None relevant

**State at Failure:**
```typescript
cartItems = [
  { id: 1, price: 10.00 },
  { id: 2, price: 15.00 },
  { id: 3, price: 20.00 }
]
discount = 0.10

Expected total: 45.00 * 0.9 = 40.50
Actual total: 25.00 * 0.9 = 22.50 (item3 missing)
```

### Hypothesis

**Initial Hypothesis:** Loop was not iterating over all items due to off-by-one error

**Validation:** Added console.log to track loop iterations - confirmed loop stopped at index 1 (should go to index 2)

**Result:** Confirmed - loop condition was `i < items.length - 1` instead of `i < items.length`

## Root Cause Analysis

### Exact Failure Point

**File:** `src/features/checkout/calculateTotal.ts`
**Line:** `23`
**Function:** `calculateTotal()`
**Code:**
```typescript
// Problematic code (line 23)
for (let i = 0; i < items.length - 1; i++) {
  subtotal += items[i].price;
}
```

### Why It Failed

The loop condition `i < items.length - 1` caused the loop to stop one iteration early. For an array of 3 items (indices 0, 1, 2), the loop only processed indices 0 and 1, skipping the last item at index 2.

This is a classic off-by-one error where the developer likely confused the condition for "iterate up to but not including" with "iterate through all items."

### Why It Wasn't Caught

- [x] No test existed for this case
- [ ] Test existed but was too lenient
- [ ] Test was flaky and ignored
- [ ] Error was silently swallowed
- [ ] Condition only occurs in production environment

The original implementation only had a test for 2 items in cart, which coincidentally passed because the condition worked correctly for 2 items (loop runs for i=0 only, which is correct since i < 2-1 = i < 1 is false after first iteration).

### When It Was Introduced

**Commit:** `b2c4567`
**PR:** #42
**Feature:** FEAT-012

**Context:** Initial implementation of discount calculation. Developer copied loop pattern from another function that intentionally used `length - 1` for a different purpose (processing pairs).

## Downstream Implications

### What Else Was Affected

- [x] Feature FEAT-008 (Cart Display): Shows incorrect subtotal preview
- [ ] Feature B: Not affected
- [ ] API Contract: No changes
- [ ] Database: No changes
- [ ] Other: None

### Similar Bugs Identified

- [x] Similar pattern in `src/features/cart/calculateSubtotal.ts:45` - Fixed proactively
- [ ] No other instances found after code search

## Solution

### Fix Approach

**Approach Chosen:** Quick fix (correct loop condition)

**Why This Approach:**
Simple logic error with obvious fix. No architectural changes needed. Low risk.

**Alternatives Considered:**
1. Use Array.reduce() instead of loop - Overkill for this simple fix, can refactor later
2. Rewrite entire calculation function - Unnecessary, loop pattern is fine when correct

### Code Changes

**Files Modified:**
- `src/features/checkout/calculateTotal.ts` - Fixed loop condition
- `src/features/cart/calculateSubtotal.ts` - Fixed similar pattern proactively

**Key Changes:**
```diff
// src/features/checkout/calculateTotal.ts:23
- for (let i = 0; i < items.length - 1; i++) {
+ for (let i = 0; i < items.length; i++) {
    subtotal += items[i].price;
  }
```

**Explanation:**
Changed loop condition from `i < items.length - 1` to `i < items.length` to correctly iterate over all items including the last one.

### Regression Test Added

**Test File:** `test/unit/FEAT-012/discount-calculation.test.ts`
**Test Level:** unit
**Annotation:** `@test-approach: tdd`

**Test Description:**
```typescript
describe('Bug #42: Discount calculation skips last item', () => {
  it('should apply discount to all items including last one', () => {
    // Given: Cart with 3 items and 10% discount
    const items = [
      { id: 1, price: 10.00 },
      { id: 2, price: 15.00 },
      { id: 3, price: 20.00 }
    ];
    const discount = 0.10;

    // When: Calculate total with discount
    const total = calculateTotal(items, discount);

    // Then: All items should be included in discounted total
    expect(total).toBe(40.50); // (10 + 15 + 20) * 0.9
  });
});
```

**Test Validates:**
- [x] Bug scenario is reproduced (3+ items with discount)
- [x] Fix prevents regression
- [x] Edge cases are covered (added test for 1 item, 2 items, 5 items)

## Validation

### Test Results

**Regression Test:**
- Before fix: ❌ FAIL (expected 40.50, got 22.50)
- After fix: ✅ PASS

**Full Test Suite:**
- All tests: ✅ PASS (28/28)
- New failures: None
- Flaky tests: None

### Manual Validation

**Smoke Test:**
1. Add 3 items to cart, apply discount - ✅ PASS (correct total)
2. Add 1 item to cart, apply discount - ✅ PASS (correct total)
3. Add 5 items to cart, apply discount - ✅ PASS (correct total)

**Edge Cases:**
- [x] Empty cart: Validated (returns 0)
- [x] No discount: Validated (returns subtotal)
- [x] 100% discount: Validated (returns 0)

### Performance Validation

Not applicable (not a performance bug)

### Security Validation

Not applicable (P2, no security implications)

## Prevention

### How to Prevent Similar Bugs

**Immediate Actions:**
- [x] Added regression tests for 1, 2, 3, 5 items
- [x] Searched codebase for similar loop patterns (found and fixed 1)
- [x] Added note in code review checklist: "Check loop bounds for off-by-one errors"
- [ ] Update linting rule (not applicable for this pattern)

**Long-term Actions:**
- [ ] Consider using Array.reduce() in refactoring to avoid manual loops
- [ ] Add code review focus on array iteration patterns
- [ ] Team training: Common off-by-one error patterns (next sprint)

### What We Learned

**Technical Learnings:**
- Off-by-one errors are easy to miss in code review
- Tests with only 2 items masked the bug (need 3+ to trigger)
- Loop patterns copied from other code may have different requirements

**Process Learnings:**
- Test multiple array sizes (1, 2, 3, many) not just one case
- Code review should question every `-1` or `+1` in conditions
- Proactively search for similar patterns when bug found

### Documentation Updates

**Updated Documents:**
- [x] `docs/features/FEAT-012/README.md` - Added debug report link
- [x] `docs/features/FEAT-012/handover.md` - Added bug fix section
- [ ] `docs/system/architecture.md` - Not applicable
- [ ] `docs/system/connections.md` - Not applicable

## Related Links

- **PRD:** docs/features/FEAT-012/prd.md
- **Plan:** docs/features/FEAT-012/plan.md
- **Commit:** a3f8c92
- **Issue:** N/A
- **QA Report:** N/A
- **Research:** N/A

## Checklist

Before closing this debug report, verify:

- [x] Root cause identified and documented
- [x] Fix implemented and committed
- [x] Regression test added (fails before, passes after)
- [x] Full test suite passes
- [x] Manual smoke test passes
- [x] Documentation updated
- [x] Similar patterns checked
- [x] Prevention measures identified
- [x] All links in report are valid
```

---

## Template Usage Notes

### Frontmatter Fields

- **type**: Always `debug-report`
- **date**: ISO 8601 timestamp when report created
- **bug-type**: `logic | integration | performance | test` (from decision tree)
- **severity**: `P0 | P1 | P2 | P3 | P4` (from decision tree)
- **scope**: `FEAT-XXX` or `system` (from decision tree)
- **status**: `fixed` (most common) | `monitoring` (fix deployed, watching) | `known-limitation` (won't fix)
- **fixed-in**: Git commit SHA where fix was merged
- **regression-test**: Relative path to regression test file

### Section Guidelines

**Summary**: Keep concise (1-2 sentences per subsection). Reader should understand the bug in 30 seconds.

**Timeline**: Use actual timestamps if available, or best estimates. Include key milestones only.

**Investigation**: Focus on the diagnostic process. Show how you narrowed down the issue.

**Root Cause Analysis**: Be specific. "File:line" precision. Explain *why* it failed, not just *what* failed.

**Solution**: Explain trade-offs. If you chose quick fix over proper fix, document why and note technical debt.

**Validation**: Prove the fix works. Include test results, manual validation, and any specific checks.

**Prevention**: Most important section for long-term value. How do we avoid this bug class in the future?

### When to Use Each Section

**Required sections** (always fill out):
- Summary
- Investigation
- Root Cause Analysis
- Solution
- Validation
- Prevention
- Checklist

**Optional sections** (use when applicable):
- Timeline (helpful for P0/P1, skip for trivial bugs)
- Downstream Implications (required if >1 feature affected)
- Performance Validation (required for performance bugs only)
- Security Validation (required for P0/P1 or security-related)

### Report Locations

**Feature bugs:**
```
docs/features/FEAT-XXX/debug-[issue-slug]-YYYYMMDD.md
```

**System bugs:**
```
docs/debug/[issue-slug]-YYYYMMDD.md
```

Use descriptive slug: `discount-calculation-off-by-one-20260212` not `bug-1`

---

## See Also

- [Debug Skill](../SKILL.md) - Main debugging workflow
- [Decision Trees](decision-trees.md) - Bug classification and severity
