# Test Strategy Examples

Concrete examples for each test approach level showing annotation, directory, pattern, and common mistakes.

## TDD Example: Backend Service

**Scenario:** User validation service that checks email format and uniqueness.

**Annotation:** `@test-approach: tdd`
**Directory:** `test/unit/FEAT-XXX/`
**Build routing:** RED-GREEN-REFACTOR subagents

```typescript
// @test-approach: tdd
// test/unit/FEAT-018/user-validation.test.ts

describe('FEAT-018: User Validation', () => {
  describe('AC-FEAT-018-001: Email format validation', () => {
    it('should reject email without @ symbol', () => {
      // Arrange
      const email = 'notanemail';

      // Act
      const result = validateEmail(email);

      // Assert
      expect(result.valid).toBe(false);
      expect(result.error).toContain('invalid format');
    });

    it('should accept standard email format', () => {
      const result = validateEmail('user@example.com');
      expect(result.valid).toBe(true);
    });
  });

  describe('AC-FEAT-018-002: Email uniqueness', () => {
    it('should reject duplicate email', async () => {
      // Arrange
      const store = createMockStore({ users: [{ email: 'taken@example.com' }] });

      // Act
      const result = await checkEmailUnique('taken@example.com', store);

      // Assert
      expect(result.unique).toBe(false);
    });
  });
});
```

**What NOT to do at this level:**
- Don't render a `<SignupForm>` — that's a component test
- Don't hit a real database — that's an integration test
- Don't navigate to `/signup` — that's an E2E test

---

## Component Test Example: React Form

**Scenario:** Login form with validation and submission feedback.

**Annotation:** `@test-approach: component-test`
**Directory:** `test/component/FEAT-XXX/`
**Build routing:** Inline 6-step red-green

```typescript
// @test-approach: component-test
// test/component/FEAT-018/LoginForm.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from '@/components/LoginForm';

describe('FEAT-018: Login Form', () => {
  describe('AC-FEAT-018-003: Form validation feedback', () => {
    it('should show error when email field is empty on submit', () => {
      // Render
      render(<LoginForm onSubmit={jest.fn()} />);

      // Interact
      fireEvent.click(screen.getByRole('button', { name: /log in/i }));

      // Assert
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });

    it('should disable submit button while loading', async () => {
      const slowSubmit = () => new Promise(resolve => setTimeout(resolve, 1000));
      render(<LoginForm onSubmit={slowSubmit} />);

      fireEvent.change(screen.getByLabelText(/email/i), {
        target: { value: 'user@example.com' },
      });
      fireEvent.change(screen.getByLabelText(/password/i), {
        target: { value: 'password123' },
      });
      fireEvent.click(screen.getByRole('button', { name: /log in/i }));

      expect(screen.getByRole('button', { name: /log in/i })).toBeDisabled();
    });
  });
});
```

**What NOT to do at this level:**
- Don't test email validation logic — that's a unit test
- Don't hit a real auth API — mock the `onSubmit` prop
- Don't test the full login-to-dashboard flow — that's E2E

---

## Integration Test Example: API with Database

**Scenario:** User creation API that persists to database and returns confirmation.

**Annotation:** `@test-approach: integration`
**Directory:** `test/integration/FEAT-XXX/`
**Build routing:** Inline red-green (same pattern as component-test)

```typescript
// @test-approach: integration
// test/integration/FEAT-018/user-api.test.ts

import request from 'supertest';
import { app } from '@/app';
import { createTestDb, cleanupTestDb } from '@/test-utils/db';

describe('FEAT-018: User API Integration', () => {
  let db: TestDatabase;

  beforeAll(async () => {
    db = await createTestDb();
  });

  afterAll(async () => {
    await cleanupTestDb(db);
  });

  describe('AC-FEAT-018-004: User creation persists to DB', () => {
    it('should create user and return 201 with user data', async () => {
      // Execute
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'Test User', email: 'test@example.com' });

      // Verify response
      expect(response.status).toBe(201);
      expect(response.body.user.email).toBe('test@example.com');

      // Verify persistence
      const rows = await db.query(
        'SELECT * FROM users WHERE email = $1',
        ['test@example.com']
      );
      expect(rows).toHaveLength(1);
    });
  });

  describe('AC-FEAT-018-005: Duplicate email returns 409', () => {
    it('should reject duplicate email with 409 Conflict', async () => {
      // Setup: create first user
      await request(app)
        .post('/api/users')
        .send({ name: 'First', email: 'dupe@example.com' });

      // Execute: attempt duplicate
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'Second', email: 'dupe@example.com' });

      // Verify
      expect(response.status).toBe(409);
    });
  });
});
```

**What NOT to do at this level:**
- Don't test email format validation in isolation — that's a unit test
- Don't render a signup form — that's a component test
- Don't navigate through signup → login → dashboard — that's E2E

---

## E2E Test Example: Multi-Page User Flow

**Scenario:** Complete signup-to-dashboard flow.

**Annotation:** `@test-approach: e2e`
**Directory:** `test/e2e/`
**Build routing:** Inline + browser MCP if available

The example below shows a Playwright-style pattern, but other browser tools (Stagehand, Vercel AI Browser) are equally valid. The key is testing the full user flow, not the specific tool.

```typescript
// @test-approach: e2e
// test/e2e/signup-flow.test.ts

describe('FEAT-018: Signup to Dashboard Flow', () => {
  describe('AC-FEAT-018-006: New user can sign up and reach dashboard', () => {
    it('should complete signup and redirect to dashboard', async () => {
      // Step 1: Navigate to signup
      await page.goto('/signup');

      // Step 2: Fill signup form
      await page.fill('[name="name"]', 'New User');
      await page.fill('[name="email"]', 'newuser@example.com');
      await page.fill('[name="password"]', 'SecurePass123!');
      await page.fill('[name="confirmPassword"]', 'SecurePass123!');

      // Step 3: Submit
      await page.click('button[type="submit"]');

      // Step 4: Verify redirect to dashboard
      await expect(page).toHaveURL('/dashboard');

      // Step 5: Verify welcome content
      await expect(page.getByText('Welcome, New User')).toBeVisible();
    });
  });

  describe('AC-FEAT-018-007: Signup with existing email shows error', () => {
    it('should show duplicate email error without leaving page', async () => {
      await page.goto('/signup');
      await page.fill('[name="email"]', 'existing@example.com');
      await page.fill('[name="password"]', 'AnyPass123!');
      await page.click('button[type="submit"]');

      await expect(page.getByText(/email already registered/i)).toBeVisible();
      await expect(page).toHaveURL('/signup');
    });
  });
});
```

**What NOT to do at this level:**
- Don't test every email format edge case — that's a unit test
- Don't test form rendering in isolation — that's a component test
- Don't test API response codes directly — that's an integration test
- Don't write E2E for every edge case — focus on critical happy paths
