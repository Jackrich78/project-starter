# Component Tests

UI component tests using render-interact-assert pattern.

## When to Use

Place tests here when they verify:
- Component rendering output
- User interaction (clicks, inputs, form submissions)
- Component state and props behavior
- Accessibility attributes
- Visual states (loading, error, empty)

## Annotation

```typescript
// @test-approach: component-test
```

## Pattern

```typescript
describe('AC-FEAT-XXX-###: [Criterion]', () => {
  it('should [behavior]', () => {
    render(<Component />);
    fireEvent.click(screen.getByRole('button'));
    expect(screen.getByText('result')).toBeInTheDocument();
  });
});
```

## Build Routing

Component test stubs are handled by `/build` Phase 3B (inline 6-step red-green), NOT by TDD subagents.

## See Also

- [Test Strategy Skill](../../.claude/skills/test-strategy/SKILL.md) — Full decision tree
- [Examples](../../.claude/skills/test-strategy/references/examples.md) — Component test example
