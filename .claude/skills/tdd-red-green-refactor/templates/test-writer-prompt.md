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
- Keep the AC id in each test name or comment.
- Assert the discriminating half (the negative beside the positive).
- Write bare scaffolding only so tests import; no real logic.
- Run the tests. Each must fail because behaviour is missing, not from a
  typo, bad import or broken fixture. Paste the real failing output.

Return the report in your agent format, ending PASS, FAIL or ESCALATION.
```

Gate after return: run `{test_paths}` yourself, save to `red.txt`, confirm each fails for the right reason. Keep `red.txt` for the close-out `Proof:`.
