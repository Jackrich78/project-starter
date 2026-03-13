# Validation Criteria

Rules for the qa-reviewer to validate test pyramid level placement, detect anti-patterns, and verify AC coverage.

## Pyramid Level Rules

### Unit Tests (`test/unit/`)

**Should contain:**
- Logic and data transformations
- Utility functions
- Service methods
- Custom hooks (logic extraction)
- API handlers (request/response logic)
- State management (reducers, stores)

**Should NOT contain:**
- React component rendering (`render()`, `screen.getBy*`)
- User interaction simulation (`fireEvent`, `userEvent`)
- Database queries or connections
- HTTP requests to real endpoints
- Multi-page navigation

**Grep patterns for misplacement:**
```bash
# Unit tests that look like component tests
grep -r "render(" test/unit/ --include="*.test.tsx" --include="*.test.ts"
grep -r "screen\." test/unit/ --include="*.test.tsx" --include="*.test.ts"
grep -r "fireEvent\." test/unit/ --include="*.test.tsx" --include="*.test.ts"

# Unit tests that look like integration tests
grep -r "createTestDb\|testDatabase\|\.query(" test/unit/ --include="*.test.ts"
grep -r "request(app)" test/unit/ --include="*.test.ts"
```

### Component Tests (`test/component/`)

**Should contain:**
- Component rendering output
- User interaction (clicks, inputs, form submissions)
- Component state and props behavior
- Accessibility attributes
- Visual states (loading, error, empty)

**Should NOT contain:**
- Pure business logic (no component rendering)
- Database connections
- Real API calls (mock at the boundary)
- Multi-page navigation flows

**Grep patterns for misplacement:**
```bash
# Component tests with no rendering (probably a unit test)
grep -rL "render\|mount\|shallow" test/component/ --include="*.test.tsx" --include="*.test.ts"

# Component tests with DB access (probably integration)
grep -r "createTestDb\|\.query(" test/component/ --include="*.test.tsx"
```

### Integration Tests (`test/integration/`)

**Should contain:**
- API handler → database round-trips
- Middleware chains (auth → validation → handler)
- Multi-service communication
- External API integration (with mocks at boundary)
- Queue producer → consumer flows

**Should NOT contain:**
- Single-function logic (that's a unit test)
- Component rendering (that's a component test)
- Browser-based workflows (that's an E2E test)
- Tests of a single module in isolation

**Grep patterns for misplacement:**
```bash
# Integration tests that look like unit tests (no DB/API/service interaction)
grep -rL "request\|fetch\|query\|connect\|createTest" test/integration/ --include="*.test.ts"

# Integration tests that look like E2E (browser automation)
grep -r "page\.\|browser\.\|playwright" test/integration/ --include="*.test.ts"
```

### E2E Tests (`test/e2e/`)

**Should contain:**
- Complete user flows across pages
- Critical happy paths (signup → login → dashboard)
- Authentication flows end-to-end
- Multi-step form workflows
- Navigation and routing verification

**Should NOT contain:**
- Single-component rendering (that's a component test)
- API-only flows without browser (that's an integration test)
- Unit logic testing
- Tests for every edge case (E2E covers critical paths only)

**Grep patterns for misplacement:**
```bash
# E2E tests with no page navigation (probably integration)
grep -rL "page\.\|goto\|navigate\|browser" test/e2e/ --include="*.test.ts"
```

## Anti-Pattern Detection

### 1. Implementation Coupling

Tests that verify HOW code works rather than WHAT it does.

**Detection patterns:**
```bash
# Testing internal method calls
grep -r "\.mock\.\(calls\|instances\)" test/ --include="*.test.ts" --include="*.test.tsx" | head -20

# Testing private methods directly
grep -r "\._\|\.#\|private" test/ --include="*.test.ts" | head -20

# Overly specific mock setups (>5 mocks in one test)
# Manual review: check test files with many jest.mock() calls
```

**Rule:** If refactoring implementation (without changing behavior) breaks a test, that test is coupled to implementation.

### 2. Excessive Mocking

Tests where mocks outnumber real objects, obscuring what's actually tested.

**Detection patterns:**
```bash
# Files with many mock declarations
grep -c "jest\.mock\|vi\.mock\|mock\.\|Mock(" test/ -r --include="*.test.ts" --include="*.test.tsx" | sort -t: -k2 -rn | head -10

# Mocking the module under test (always wrong)
# Manual review: compare import paths in jest.mock() vs describe() subject
```

**Rule:** Mock only at system boundaries (external APIs, databases, file system). Internal modules should use real implementations.

### 3. Snapshot Abuse

Using snapshots as a substitute for meaningful assertions.

**Detection patterns:**
```bash
# Snapshot assertions
grep -r "toMatchSnapshot\|toMatchInlineSnapshot" test/ --include="*.test.ts" --include="*.test.tsx"

# Large snapshot files
find test/ -name "*.snap" -size +10k
```

**Rule:** Snapshots are acceptable for serializable output (API responses, config). Never use snapshots for component rendering — write explicit assertions instead.

## AC Coverage Verification

### Grep Pattern

```bash
# Find all AC references in tests
grep -r "AC-FEAT-XXX-" test/ --include="*.test.ts" --include="*.test.tsx" | sort

# Find all ACs defined in PRD
grep -r "AC-FEAT-XXX-" docs/features/FEAT-XXX/prd.md | sort
```

### Validation Process

1. Extract AC IDs from PRD: `AC-FEAT-XXX-001`, `AC-FEAT-XXX-002`, etc.
2. Extract AC IDs from test files
3. Compare: every PRD AC should have at least one corresponding test
4. Flag missing ACs as "Untested acceptance criterion"

### E2E Coverage Note

If PRD has user-flow ACs but no E2E tests exist:
- Check if browser MCP is configured
- If MCP available: flag as "E2E tests should be written"
- If MCP not available: flag as "E2E automated coverage: pending MCP setup" (Tier 1, not blocking)
