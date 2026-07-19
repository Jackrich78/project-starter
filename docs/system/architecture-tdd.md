# TDD Subagent Architecture

> Module of [architecture.md](architecture.md). Loaded by `/prime build`.

---

Each TDD phase runs in an isolated context window, preventing bias from leaking between phases.

## Phase Isolation

| Phase | Agent | Context Access | Gate |
|-------|-------|----------------|------|
| RED | tdd-test-writer | PRD only | Test MUST FAIL |
| GREEN | tdd-implementer | Test file only | Test MUST PASS |
| REFACTOR | tdd-refactorer | Test + implementation | Tests STAY GREEN |

## Why Context Isolation Matters

| Problem | Solution |
|---------|----------|
| Test writer sees implementation plans → tests verify implementation, not behavior | tdd-test-writer sees only PRD |
| Implementer sees PRD → over-engineers beyond what test requires | tdd-implementer sees only the test |
| Single context → "I know how this should work" bias | Each phase: fresh 200k context |

## TDD Flow

```
/build FEAT-XXX
    ↓
For each test stub from /blueprint:
    ↓
┌─────────────────────────────────┐
│ Task(tdd-test-writer)           │
│ Input: PRD acceptance criterion │
│ Output: Failing test            │
│ Gate: MUST FAIL                 │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ Task(tdd-implementer)           │
│ Input: Failing test only        │
│ Output: Minimal implementation  │
│ Gate: MUST PASS                 │
└─────────────────────────────────┘
    ↓
[Repeat for all test stubs]
    ↓
After all tests GREEN:
    ↓
┌─────────────────────────────────┐
│ Task(tdd-refactorer)            │
│ Input: Tests + implementation   │
│ Output: Improved code           │
│ Gate: Tests STAY GREEN          │
└─────────────────────────────────┘
```

---

## See Also

- [architecture.md](architecture.md) — Core system architecture
- [architecture-qa.md](architecture-qa.md) — QA integration, SAST, hooks
- [TDD Skill](../../.claude/skills/tdd-red-green-refactor/SKILL.md) — TDD orchestration
