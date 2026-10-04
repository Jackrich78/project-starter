---
type: reference
title: "tdd-test-writer dispatch prompt (RED)"
description: "Prompt the orchestrator fills before dispatching tdd-test-writer."
---

Fill the `{}` fields, dispatch with `subagent_type: tdd-test-writer`. It sees ACs and `Tests:` only: never paste the plan, the parent body or any implementation.

```
Convert the failing stubs into real failing tests for issue {issue}.

Acceptance criteria:
{ac_text}

Tests line (AC ids -> test paths): {ac_ids} -> {test_paths}

Do:
- Extend an existing test file before adding one; follow .claude/rules/testing.md.

Testing rules (path-scoped rules do not load in sub-agents, so they are restated here):
- **Seen red:** you will run it before it counts.
- **Discriminating half:** assert the negative alongside the positive (the thing is logged *and* the ordinary case is not).
- **Stub at the boundary** the code crosses (fake binary on PATH, fake HTTP server), not deep inside with mocks that mirror the implementation.
- **Production types:** construct what the system under test receives in production, not a convenient dict.
- Time-dependent code: inject the clock. A skip names what it waits for.

Also:
- Keep the AC id in each test name or comment.
- Assert the discriminating half (the negative beside the positive).
- Write bare scaffolding only so tests import; no real logic.
- Run the tests. Each must fail because behaviour is missing, not from a
  typo, bad import or broken fixture. Paste the real failing output.

Return the report in your agent format, ending PASS, FAIL or ESCALATION.
```

Gate after return: run `{test_paths}` yourself, save to `red.txt`, confirm each fails for the right reason. Keep `red.txt` for the close-out `Proof:`.
