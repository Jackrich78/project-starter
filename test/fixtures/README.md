# Test Fixtures

Routing-proof fixtures that demonstrate the `@test-approach` annotation convention and directory placement rules.

## Purpose

These fixture files are **not real tests**. They exist to:
1. Prove that annotation grep patterns work correctly
2. Serve as templates for real test stubs created by `/plan`
3. Document the expected format for each test approach

## Fixture Files

| File | Annotation | Proves |
|------|-----------|--------|
| `sample-service.test.ts` | `@test-approach: tdd` | TDD routing to subagents |
| `sample-component.test.tsx` | `@test-approach: component-test` | Inline routing to Phase 3B |

## Extending for Real Projects

When you start building features:
1. `/plan` creates real test stubs with annotations in the correct directories
2. `/build` Phase 0 greps for `@test-approach:` to route stubs
3. These fixtures remain as reference — delete them if they cause noise in test runs

## Verifying Routing

```bash
# Should find both fixture annotations
grep -r "@test-approach:" test/fixtures/

# Should show tdd + component-test
grep -r "@test-approach:" test/fixtures/ | grep -oP "(?<=@test-approach: )\S+"
```

## See Also

- [Test Strategy Skill](../../.claude/skills/test-strategy/SKILL.md) — Full routing map
