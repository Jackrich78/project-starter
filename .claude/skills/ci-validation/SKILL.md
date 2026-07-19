---
name: ci-validation
description: Validates GitHub Actions workflow files locally before committing. Use when creating or modifying .github/workflows/*.yml files, before git commits including workflow changes, or when CI/CD configurations are updated. Prevents pushing syntax errors and config issues that would only be caught in GitHub Actions.
---

# CI Validation

Validate GitHub Actions workflows and CI configurations locally before pushing to catch errors in seconds instead of minutes.

## When to Use

- Creating or modifying `.github/workflows/*.yml` files
- Before committing workflow changes
- After updating CI scripts or configurations
- When adding new GitHub Actions steps

**Anti-pattern:** Push → Wait for GitHub Actions → See failure → Fix → Push again (wastes 5-10 minutes per cycle)

## Validation Steps

### 1. YAML Syntax & Workflow Validation

```bash
# Install actionlint if needed
which actionlint || brew install actionlint  # macOS
which actionlint || go install github.com/rhysd/actionlint/cmd/actionlint@latest

# Validate all workflows
actionlint .github/workflows/*.yml
```

**Catches:** YAML syntax errors, invalid actions, unknown versions, deprecated features, config issues

### 2. Simulate CI Commands Locally

Run every `run:` command from your workflow locally:

```bash
# If CI runs Python syntax checks
python3 -m py_compile .claude/hooks/*.py

# If CI runs shell scripts
./scripts/validate-template.sh

# If CI runs linting
npm run lint

# If CI runs type checking
npm run type-check
```

**Principle:** If it's in a workflow `run:` step, it should execute successfully on your machine first.

### 3. Run CI-Specific Tests

```bash
# Run tests that validate CI behavior
npm test -- .github/tests/

# Or pattern-match
npm test -- --grep "CI|workflow"
```

### 4. Environment Variable Check

```bash
# Extract env var references
grep -r "env\." .github/workflows/ | grep -oE '\$\{\{[^}]+\}\}'

# Verify documented in README or .env.example
```

### 5. Verify Workflow Triggers

```yaml
on:
  push:
    branches: [main]  # Intentional?
  pull_request:       # Needed?
  workflow_dispatch:  # Manual trigger?
```

## Pre-Commit Checklist

- [ ] `actionlint .github/workflows/*.yml` passes
- [ ] All workflow `run:` commands execute locally
- [ ] CI tests pass (`.github/tests/` if exists)
- [ ] Environment variables documented
- [ ] No hardcoded secrets
- [ ] Triggers match intent

## Example (from FEAT-010)

```bash
# 1. Validate
actionlint .github/workflows/*.yml

# 2. Simulate
python3 -m py_compile .claude/hooks/*.py
./scripts/validate-template.sh

# 3. Test
npm test -- .github/tests/validate-workflow.test.ts

# 4. Commit (only after all pass)
git commit -m "feat(ci): add workflow validation"
```

**Result:** Zero workflow failures in GitHub Actions.

## Common Catches

1. YAML indentation → actionlint
2. Invalid action versions (e.g., `@v99`) → actionlint
3. Missing scripts → local simulation fails
4. Python syntax errors → `py_compile`
5. Wrong file paths → local execution fails
6. Missing dependencies → test run fails

## Performance

- actionlint: < 1s
- Local simulation: < 30s
- CI tests: < 10s

**Total: 1-2 minutes** vs 5-10 minutes waiting for GitHub Actions failure

## Tools Required

- **actionlint** - Workflow validator
- **Local environment** - Tools CI uses (Python, Node.js, etc.)
- **Test runner** - npm/pytest/etc.
