# Debug Decision Trees

Complete decision trees for bug classification, severity assessment, scope determination, and agent coordination.

## Bug Type Classification Tree

Use this tree to classify bugs into one of four types:

```
Is this code that never worked (new feature failing)?
  YES → Not a bug - implementation issue
        → Use /build instead
  NO ↓

Does the code produce incorrect output for given input?
  YES ↓
    │
    ├─ Is the error in calculation, logic, or data transformation?
    │    YES → LOGIC BUG
    │    NO ↓
    │
    ├─ Is the error in UI rendering or user interaction?
    │    YES → UI BUG (classify as LOGIC BUG for routing)
    │    NO ↓
    │
    └─ Is the error in communication between services/APIs?
         YES → INTEGRATION FAILURE
         NO ↓

Does the code work but too slowly?
  YES ↓
    │
    ├─ Is response time or throughput degraded?
    │    YES → PERFORMANCE REGRESSION
    │    NO ↓
    │
    └─ Is memory usage or resource consumption excessive?
         YES → PERFORMANCE REGRESSION (memory)
         NO ↓

Does an automated test fail?
  YES ↓
    │
    ├─ Does the test fail consistently?
    │    YES ↓
    │    │
    │    ├─ Is the implementation wrong?
    │    │    YES → LOGIC BUG (test is correct)
    │    │    NO ↓
    │    │
    │    └─ Is the test wrong?
    │         YES → TEST FAILURE (test needs fixing)
    │         NO → Investigate further
    │
    └─ Does the test fail intermittently (flaky)?
         YES → TEST FAILURE (flaky test)
         NO → Investigate further

DEFAULT → LOGIC BUG (catch-all)
```

## Bug Type Descriptions

### LOGIC BUG

**Definition:** Code produces incorrect output due to flawed logic, calculation error, wrong conditional, or data transformation mistake.

**Examples:**
- Off-by-one error in loop
- Wrong comparison operator (`>` instead of `>=`)
- Incorrect formula in calculation
- Missing null/undefined check
- Wrong default value
- Inverted boolean logic

**Common Root Causes:**
- Misunderstood requirements
- Edge case not considered
- Copy-paste error
- Refactoring mistake

**Typical Fix:**
- Correct the logic
- Add unit test for the case
- Document edge case

#### UI Bug Investigation Checklist

When bug is classified as **LOGIC BUG (UI)**, use this checklist for investigation:

**1. Styling/CSS Issues:**
- [ ] Inspect computed styles in browser DevTools
- [ ] Check for CSS specificity conflicts (`!important`, inline styles)
- [ ] Verify correct CSS class names applied
- [ ] Check for Tailwind/utility class conflicts
- [ ] Test at different viewport sizes (responsive behavior)
- [ ] Check media query breakpoints

**2. React Component Issues:**
- [ ] Use React DevTools to inspect component props
- [ ] Check component state values
- [ ] Verify hooks dependencies (useEffect, useMemo, useCallback)
- [ ] Check for unnecessary re-renders (React Profiler)
- [ ] Verify conditional rendering logic
- [ ] Check event handler bindings

**3. Responsive/Layout Issues:**
- [ ] Test at standard breakpoints: 320px (mobile), 768px (tablet), 1024px (laptop), 1920px (desktop)
- [ ] Check viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] Verify flexible units (rem, %, vw, vh vs px)
- [ ] Check flexbox/grid container/item properties
- [ ] Test horizontal scrolling on mobile

**4. Visual Evidence Capture:**

**Manual approach** (works everywhere):
- Take screenshot of bug (browser DevTools: Cmd+Shift+P → "Capture screenshot")
- Take screenshot of expected behavior (design mockup or working version)
- Note browser version, OS, viewport size

**Automated approach** (if Playwright MCP available):
- Use Playwright to capture screenshots across browsers/viewports
- Screenshots saved to MCP output directory (check `mcp.output` for file paths)
- Use Playwright to extract computed styles programmatically

**5. Cross-Browser Testing:**
- [ ] Chrome (most common)
- [ ] Firefox (different rendering engine)
- [ ] Safari (WebKit, iOS important)
- [ ] Mobile browsers (Chrome Mobile, Safari iOS)

**Helpful Resources:**
- **Chrome DevTools**: https://developer.chrome.com/docs/devtools/
- **React DevTools**: https://react.dev/learn/react-developer-tools
- **CSS Debugging**: https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Debugging_CSS
- **Responsive Design**: https://web.dev/responsive-web-design-basics/
- **Tailwind CSS**: https://tailwindcss.com/docs/

**Test Routing** (via test-strategy skill):
- Styling bugs → `@test-approach: component-test` (render snapshot)
- Interaction bugs → `@test-approach: e2e` (user flow)
- Component logic bugs → `@test-approach: tdd` (unit test)
- Responsive bugs → `@test-approach: component-test` (multiple viewports)

### INTEGRATION FAILURE

**Definition:** Code fails when communicating with external service, API, database, or another component.

**Examples:**
- API returns unexpected status code
- Wrong HTTP method used
- Request payload format mismatch
- Authentication header missing
- Database connection timeout
- Service contract changed
- Wrong API endpoint

**Common Root Causes:**
- API contract changed without notice
- Environment configuration mismatch
- Authentication credentials expired
- Network connectivity issue
- Service versioning problem

**Typical Fix:**
- Update API call to match contract
- Fix authentication/authorization
- Add integration test
- Update service configuration
- Document integration contract

### PERFORMANCE REGRESSION

**Definition:** Code works correctly but performance has degraded (slower response time, higher resource usage).

**Examples:**
- N+1 query problem
- Missing database index
- Unoptimized loop
- Memory leak
- Excessive API calls
- Large payload without pagination
- Blocking I/O in critical path

**Common Root Causes:**
- Database query not optimized
- Caching removed or misconfigured
- Algorithm changed to less efficient one
- Data volume increased without optimization
- Resource pooling issue

**Typical Fix:**
- Add/optimize database index
- Implement caching
- Use more efficient algorithm
- Add pagination
- Optimize query (joins, projections)
- Add performance regression test with benchmark

### TEST FAILURE

**Definition:** Automated test fails, but the cause is test-related (flaky test, broken test, environment issue), not a logic bug in production code.

**Examples:**
- Test selector outdated after UI change
- Timing issue (race condition in test)
- Test data conflict
- Environment-specific failure
- Test depends on external state
- Assertion too strict
- Test order dependency

**Common Root Causes:**
- Test not isolated (shared state)
- Test uses brittle selectors
- Test has timing assumptions
- Test depends on specific data
- Mock/stub misconfigured

**Typical Fix:**
- Update test to match implementation
- Fix test isolation
- Add proper waits/retries
- Use stable selectors
- Mock external dependencies
- Document test requirements

## Severity Assessment Tree

Use this tree to assign priority level (P0-P4):

```
Is production down or data being lost?
  YES → P0 (CRITICAL)
  NO ↓

Is there a security vulnerability or data breach risk?
  YES → P0 (CRITICAL)
  NO ↓

Is core functionality completely broken for all users?
  YES → P1 (HIGH)
  NO ↓

Is core functionality broken for subset of users?
  YES ↓
    │
    ├─ Does it affect >50% of users?
    │    YES → P1 (HIGH)
    │    NO → P2 (MEDIUM)
    │
  NO ↓

Is there a workaround available?
  YES ↓
    │
    ├─ Is the workaround easy (< 1 minute)?
    │    YES → P3 (LOW)
    │    NO → P2 (MEDIUM)
    │
  NO → P2 (MEDIUM)

Is this cosmetic or edge case only?
  YES → P4 (TRIVIAL)
  NO → P3 (LOW)

DEFAULT → P3 (LOW)
```

## Severity Level Definitions

### P0 (CRITICAL)

**Response time:** Immediate (drop everything)

**Characteristics:**
- Production service completely down
- Data loss or corruption occurring
- Security breach or vulnerability being exploited
- Payment processing broken
- Critical compliance violation

**Example scenarios:**
- Database corrupting user data
- SQL injection vulnerability actively exploited
- Authentication completely broken (no one can log in)
- Payment gateway returning errors for all transactions

**Escalation:**
- Notify team immediately
- Coordinate with qa-reviewer for security validation
- Document incident timeline
- Prepare post-mortem

### P1 (HIGH)

**Response time:** Same day

**Characteristics:**
- Major functionality broken
- Large user impact (>50% affected)
- No reasonable workaround
- Revenue-generating feature broken
- Core user flow blocked

**Example scenarios:**
- Search functionality returns no results
- File upload fails for all users
- Dashboard shows incorrect data
- Critical API endpoint returns 500

**Escalation:**
- Prioritize above all non-P0 work
- Update stakeholders on ETA
- Consider hotfix deployment

### P2 (MEDIUM)

**Response time:** This week

**Characteristics:**
- Feature partially broken
- Workaround exists but not obvious
- Affects <50% of users
- Non-core functionality affected
- User can complete task with effort

**Example scenarios:**
- Export to CSV fails but export to JSON works
- Mobile layout broken but desktop works
- Error message confusing but user can proceed
- Slow performance but not timeout

**Escalation:**
- Fix in normal sprint work
- Document workaround for support team
- Consider backporting if fix is simple

### P3 (LOW)

**Response time:** Next sprint

**Characteristics:**
- Minor issue
- Easy workaround available
- Edge case only
- Cosmetic issue
- Low user impact

**Example scenarios:**
- Button alignment slightly off
- Tooltip text has typo
- Feature works but produces console warning
- Rare edge case fails

**Escalation:**
- Queue for normal prioritization
- May combine with other work in same area
- Consider fixing during refactoring

### P4 (TRIVIAL)

**Response time:** Backlog

**Characteristics:**
- Nice-to-have improvement
- No functional impact
- Ultra-rare edge case
- Cosmetic polish

**Example scenarios:**
- Color contrast could be slightly better
- Icon could be more intuitive
- Message could be more friendly
- Feature works but could be more elegant

**Escalation:**
- Backlog for low-priority work
- May never fix if higher priorities exist
- Good candidates for junior developer tasks

## Scope Determination Tree

Use this tree to determine if bug is feature-scoped or system-scoped:

```
Is the bug contained within a single feature?
  YES ↓
    │
    ├─ Does the feature have a FEAT-XXX identifier?
    │    YES → FEATURE BUG (scope: FEAT-XXX)
    │    NO ↓
    │
    └─ Can the bug be traced to feature code?
         YES → FEATURE BUG (identify FEAT-XXX)
         NO → SYSTEM BUG
  NO ↓

Does the bug affect multiple features?
  YES → SYSTEM BUG
  NO ↓

Is the bug in infrastructure or shared code?
  YES ↓
    │
    ├─ Is it in: auth, database, API layer, routing, config?
    │    YES → SYSTEM BUG
    │    NO ↓
    │
    └─ Is it in: utilities, helpers, shared components?
         YES → SYSTEM BUG
         NO → Investigate further

DEFAULT → SYSTEM BUG (when unclear, prefer system)
```

## Scope Type Context Loading

### FEATURE BUG (FEAT-XXX)

**Load these documents:**
```
docs/features/FEAT-XXX/README.md     # Feature overview
docs/features/FEAT-XXX/prd.md        # Requirements
docs/features/FEAT-XXX/plan.md       # Implementation approach
docs/features/FEAT-XXX/handover.md   # Current state (if exists)
```

**Understand:**
- What is the feature supposed to do?
- What are the acceptance criteria?
- What files implement this feature?
- What was the technical approach?

**Debug report location:**
```
docs/features/FEAT-XXX/debug-[issue-slug]-YYYYMMDD.md
```

**Update after fix:**
- `README.md` → Add debug report to Related Documents
- `handover.md` → Add Bug Fixes section

### SYSTEM BUG

**Load these documents:**
```
PROJECT.md                           # Project overview
docs/system/architecture.md          # System architecture
docs/system/connections.md           # Component relationships
```

**Understand:**
- What is the system architecture?
- What are the integration boundaries?
- What shared code/infrastructure is involved?
- What features depend on this system code?

**Debug report location:**
```
docs/debug/[issue-slug]-YYYYMMDD.md
```

**Update after fix:**
- `docs/debug/README.md` → Add debug report link
- `docs/system/architecture.md` → Update if design changed
- `docs/system/connections.md` → Update if integration boundaries changed

## Agent Coordination Tree

Use this tree to determine when to invoke which agents:

```
Is the stack trace or error message from an unfamiliar library?
  YES → INVOKE RESEARCHER
        Topic: Library/framework in stack trace
        Output: research-debug-[library]-[timestamp].md
  NO ↓

Does the fix require significant trade-offs or refactoring?
  YES ↓
    │
    ├─ Are there multiple viable fix approaches?
    │    YES → INVOKE CHALLENGER
    │           Task: Review fix options and recommend
    │    NO ↓
    │
    ├─ Does the fix require touching >5 files?
    │    YES → INVOKE CHALLENGER
    │           Task: Validate blast radius acceptable
    │    NO ↓
    │
    └─ Is the fix a quick patch vs proper refactoring?
         YES → INVOKE CHALLENGER
               Task: Evaluate quick vs proper fix trade-off
         NO ↓

Is the bug P0 or P1 severity?
  YES ↓
    │
    └─ Does the fix touch security-sensitive code?
         YES → INVOKE QA-REVIEWER
               Task: Security validation of fix
         NO → INVOKE QA-REVIEWER (optional for P0)
              Task: Quality validation of critical fix
  NO ↓

Does the bug involve authentication, authorization, or data handling?
  YES → INVOKE QA-REVIEWER
        Task: Security review of fix
  NO ↓

Does the fix change API contracts or integration boundaries?
  YES ↓
    │
    ├─ INVOKE LIBRARIAN
    │    Task: Update all docs referencing changed API
    │
    └─ INVOKE QA-REVIEWER (optional)
         Task: Validate integration contract changes
  NO ↓

What test level should the regression test be?
  ALWAYS → USE TEST-STRATEGY
           Task: Determine test pyramid level
           Output: @test-approach annotation + directory
```

## Agent Coordination Examples

### Example 1: Unfamiliar Library Error

**Trigger:**
```
Error: "Cannot read property 'apply' of undefined" in React useEffect
Bug classification: Logic bug
Agent: Developer not familiar with React hooks lifecycle
```

**Decision:**
```
→ INVOKE RESEARCHER
  Description: "Research React hooks for debug investigation"
  Prompt: "Research React useEffect hook lifecycle and common errors.
          Error: 'Cannot read property apply of undefined'
          Context: useEffect with async function
          Find:
          1. Common causes of this error in useEffect
          2. Correct patterns for async in useEffect
          3. Debugging strategies"
  Output: docs/features/FEAT-XXX/research-debug-react-hooks-[timestamp].md
```

### Example 2: Multiple Fix Approaches

**Trigger:**
```
Bug: Race condition in async data loading
Severity: P1
Options:
  1. Add mutex (quick fix, adds complexity)
  2. Redesign data flow (proper fix, larger change)
```

**Decision:**
```
→ INVOKE CHALLENGER
  Description: "Review fix approach for race condition bug"
  Prompt: "Review this bug fix approach as a senior engineer.

          Bug: Race condition in async data loading
          Root Cause: Multiple parallel fetches overwrite state

          Proposed Fixes:
          1. Add mutex lock
             - Pros: Quick (30 min), minimal code change
             - Cons: Adds complexity, doesn't fix root design issue

          2. Redesign data flow with request deduplication
             - Pros: Proper fix, improves overall architecture
             - Cons: 4-6 hours, touches multiple files

          Focus on:
          1. Quick vs proper fix trade-off for P1
          2. Is mutex acceptable short-term solution?
          3. Can we do quick fix now + refactor later?
          4. Hidden implications of each approach?"
```

### Example 3: Security-Sensitive Fix

**Trigger:**
```
Bug: SQL injection in user search
Severity: P0 (security vulnerability)
Fix: Change to parameterized queries
```

**Decision:**
```
→ INVOKE QA-REVIEWER
  Description: "Security review of SQL injection fix"
  Prompt: "Review this bug fix for security implications.

          Bug: SQL injection vulnerability in user search
          Severity: P0
          Fix: Replaced string concatenation with parameterized queries

          Files changed:
          - src/api/users/search.ts
          - test/integration/user-search.test.ts

          Context: Create minimal handover with:
          - What was fixed (SQL injection vector)
          - How fix works (parameterized queries)
          - Security considerations

          Focus OWASP review on:
          1. Is parameterization correct?
          2. Are all SQL injection vectors closed?
          3. Are there similar patterns elsewhere?
          4. Is input validation sufficient?"
```

### Example 4: Architecture Change

**Trigger:**
```
Bug fix changes authentication flow
Files affected: 7 files across 3 features
Integration boundaries changed
```

**Decision:**
```
→ INVOKE LIBRARIAN
  Description: "Update docs after auth flow change"
  Prompt: "Update all documentation referencing authentication flow.

          Change: Authentication moved from middleware to edge function
          Affected features: FEAT-012, FEAT-015, FEAT-018

          Update:
          1. docs/system/architecture.md (auth flow diagram)
          2. docs/system/connections.md (integration boundaries)
          3. All feature READMEs referencing auth
          4. Cross-references to auth implementation

          Validate:
          - All auth flow diagrams updated
          - All code examples updated
          - All links valid"
```

### Example 5: Regression Test Routing

**Trigger:**
```
Bug: React component not rendering correct state
Root cause: useState hook misused
Fix: Correct useState dependency array
```

**Decision:**
```
→ USE TEST-STRATEGY
  Description: "Determine regression test level"
  Prompt: "Determine the appropriate test pyramid level for this regression test.

          Bug: React component not rendering correct state
          Root Cause: useState dependency array missing value
          Fix location: src/components/UserProfile.tsx

          Decision needed:
          - Is this unit/component/integration/e2e test?
          - What directory should regression test go in?
          - What annotation should it have?

          @.claude/skills/test-strategy/SKILL.md"

  Expected Output:
  - Annotation: @test-approach: component-test
  - Directory: test/component/FEAT-XXX/UserProfile.test.tsx
  - Rationale: UI component rendering = component test
```

## Decision Tree Summary Table

| Decision | Tree | Output |
|----------|------|--------|
| Bug Type | Bug Type Classification | LOGIC / INTEGRATION / PERFORMANCE / TEST |
| Severity | Severity Assessment | P0 / P1 / P2 / P3 / P4 |
| Scope | Scope Determination | FEAT-XXX / SYSTEM |
| Researcher? | Agent Coordination | YES (unfamiliar tech) / NO |
| Challenger? | Agent Coordination | YES (complex/trade-offs) / NO |
| QA Reviewer? | Agent Coordination | YES (P0/P1/security) / NO |
| Librarian? | Agent Coordination | YES (arch change) / NO |
| Test Level | Agent Coordination | Always use test-strategy |

## See Also

- [Debug Skill](../SKILL.md) - Main debugging workflow
- [Debug Report Template](debug-report-template.md) - Report structure
- [Test Strategy Skill](../../test-strategy/SKILL.md) - Test level routing
