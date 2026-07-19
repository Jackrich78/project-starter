# Test Organization

## Directory Structure

| Directory | Purpose | Annotation | Build Routing |
|-----------|---------|-----------|---------------|
| `unit/` | Logic, services, utilities, hooks | `@test-approach: tdd` | TDD subagents (RED-GREEN-REFACTOR) |
| `component/` | UI rendering, interaction, state | `@test-approach: component-test` | Inline 6-step red-green |
| `integration/` | API-to-DB, middleware, multi-service | `@test-approach: integration` | Inline red-green |
| `e2e/` | Full user flows across pages | `@test-approach: e2e` | Inline + browser MCP |
| `fixtures/` | Routing-proof samples (not real tests) | — | Not executed |

## Annotation Convention

Every test stub gets a first-line comment declaring its approach:

```typescript
// @test-approach: tdd | component-test | integration | e2e
```

This annotation determines both directory placement and `/build` routing. Tests without an annotation default to `tdd`.

## Where Scaffold Tests Live

`.github/tests/` contains tests that validate the STARTER structure.
You don't need to touch those unless extending the scaffold itself.

## Running Tests

```bash
# All tests
npm test

# Specific suite
npm test -- test/unit/FEAT-XXX/

# By directory
npm test -- test/component/
npm test -- test/integration/
npm test -- test/e2e/
```

## TDD Workflow

Use `/build FEAT-XXX` command which:
1. **Phase 0** discovers and routes stubs by `@test-approach` annotation
2. **Phases 1-3** run TDD subagents for `tdd` stubs
3. **Phase 3B** runs inline testing for `component-test`, `integration`, and `e2e` stubs

See `.claude/skills/test-strategy/SKILL.md` for the full decision tree and routing map.
