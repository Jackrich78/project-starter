---
name: test-strategy
description: Guides test approach decisions across all pyramid levels. Use when deciding test approach during /blueprint, writing tests in tdd-test-writer, validating in qa-reviewer, or understanding testing philosophy.
---

# Test Strategy

Decide the right test approach for each piece of functionality, route test stubs to the correct directory, and ensure tests verify behavior at the appropriate pyramid level.

## When to Use

- During `/blueprint` to annotate test stubs with the correct approach
- During `/build` to route stubs to the right execution flow
- In `tdd-test-writer` to understand what belongs in unit tests
- In `qa-reviewer` to validate pyramid level placement
- When deciding between TDD subagents vs inline testing

## Decision Tree

For each piece of functionality, ask these questions in order:

```
Is this a complete user flow across pages?
  YES → e2e          → test/e2e/

Is this an API-to-DB round-trip, middleware chain, or multi-service flow?
  YES → integration   → test/integration/FEAT-XXX/

Is this a UI component with rendering or user interaction?
  YES → component-test → test/component/FEAT-XXX/

Is this backend logic, a pure function, utility, API handler, or hook?
  YES → tdd           → test/unit/FEAT-XXX/

Is this an exploratory prototype or spike?
  YES → manual testing only (no annotation, no stub)
```

**Default:** If unclear, use `tdd` (unit tests with TDD subagents).

## Annotation Convention

Every test stub gets a comment on the first line declaring its approach:

```typescript
// @test-approach: tdd | component-test | integration | e2e
```

The annotation determines both directory placement and build routing.

### Full Routing Map

```
Annotation              Directory                  /build Routing
─────────────────────   ───────────────────────    ──────────────────────────────
@test-approach: tdd     test/unit/FEAT-XXX/        RED-GREEN-REFACTOR subagents
@test-approach: component-test  test/component/FEAT-XXX/   Inline red-green (6-step)
@test-approach: integration     test/integration/FEAT-XXX/ Inline red-green (6-step)
@test-approach: e2e     test/e2e/                  Inline + MCP if available
(no annotation)         test/unit/FEAT-XXX/        Default: TDD subagents
```

## Directory Placement Rules

| Level | Directory | Contains |
|-------|-----------|----------|
| Unit | `test/unit/FEAT-XXX/` | Logic, data transformations, services, hooks, utilities |
| Component | `test/component/FEAT-XXX/` | UI rendering, user interaction, component state, accessibility |
| Integration | `test/integration/FEAT-XXX/` | API-to-DB flows, middleware chains, multi-service communication |
| E2E | `test/e2e/` | Complete user flows across pages, critical happy paths, auth flows |

## Component Testing: 6-Step Inline Workflow

Component tests run inline in the `/build` orchestrator (no subagent isolation needed). The test-code feedback loop is tight enough that isolation adds overhead without benefit.

**Steps:**

1. **Read** the component test stub and its acceptance criterion
2. **Write** the real test (render-interact-assert pattern)
3. **Run** the test — verify it FAILS (missing component)
4. **Implement** the minimal component to pass the test
5. **Run** the test — verify it PASSES
6. **Review** — check the component meets the AC, refactor if needed

**Pattern:**
```typescript
// @test-approach: component-test
// test/component/FEAT-XXX/LoginForm.test.tsx

describe('AC-FEAT-XXX-001: Login form validation', () => {
  it('should show error when email is empty', () => {
    // Render
    render(<LoginForm />);

    // Interact
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    // Assert
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  });
});
```

## Integration Testing Guidance

**When to use integration tests:**
- API handler → database round-trips
- Middleware chains (auth → validation → handler)
- Multi-service communication
- External API integration (with mocks at boundary)

**Integration tests are NOT:**
- Unit tests with extra setup (that's a unit test)
- E2E tests run without a browser (that's a misplaced E2E)

**Pattern:**
```typescript
// @test-approach: integration
// test/integration/FEAT-XXX/user-api.test.ts

describe('AC-FEAT-XXX-003: User creation API', () => {
  it('should persist user and return 201', async () => {
    // Setup
    const db = await createTestDb();

    // Execute
    const response = await request(app).post('/api/users').send({ name: 'Test' });

    // Verify
    expect(response.status).toBe(201);
    const user = await db.query('SELECT * FROM users WHERE name = $1', ['Test']);
    expect(user.rows).toHaveLength(1);

    // Teardown
    await db.cleanup();
  });
});
```

## E2E Testing with Browser MCP

E2E tests cover critical user flows across pages. The approach is **tool-agnostic** — multiple browser automation tools are valid:

| Tool | Notes |
|------|-------|
| Playwright MCP | Most mature, no credentials needed |
| Stagehand | AI-native, natural language + code |
| Vercel AI Browser | Vision-based, zero-maintenance |

**If browser MCP available:**
1. Use MCP tools for automated E2E execution
2. Tag findings with tool name in test output

**If browser MCP NOT available:**
1. Write E2E test stubs with documented steps
2. Generate manual test checklist from stubs
3. Note: "Requires browser MCP — see FEAT-020"
4. qa-reviewer flags as "E2E automated coverage: pending MCP setup"

**Pattern:**
```typescript
// @test-approach: e2e
// test/e2e/login-flow.test.ts

describe('AC-FEAT-XXX-005: Complete login flow', () => {
  it('should login and redirect to dashboard', async () => {
    // Step 1: Navigate to login page
    await page.goto('/login');

    // Step 2: Fill credentials
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'valid-password');

    // Step 3: Submit
    await page.click('button[type="submit"]');

    // Step 4: Verify redirect
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome')).toBeVisible();
  });
});
```

See FEAT-020 for browser MCP installation and configuration.

## Traceability

All test descriptions follow the AC traceability pattern:

```typescript
describe('AC-FEAT-XXX-###: [Criterion Name]', () => {
  // Tests for this acceptance criterion
});
```

This enables:
- Grep for coverage: `grep -r "AC-FEAT-XXX" test/`
- qa-reviewer validation: compare test ACs against PRD ACs
- Tracing failures back to requirements

## References

- [Validation Criteria](references/validation-criteria.md) — Pyramid level rules, anti-patterns, AC coverage patterns
- [Examples](references/examples.md) — Full examples for each approach level

## See Also

- [TDD Skill](../tdd-red-green-refactor/SKILL.md) — Orchestrates TDD subagents (unit tests only)
- [/blueprint Command](../../commands/blueprint.md) — Creates annotated test stubs
- [/build Command](../../commands/build.md) — Routes stubs by annotation
- [QA Reviewer](../../agents/qa-reviewer.md) — Validates pyramid placement
- [TDD Test Writer](../../agents/tdd-test-writer.md) — RED phase (unit tests only)
