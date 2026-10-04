---
type: reference
title: "tdd-implementer dispatch prompt (GREEN)"
description: "Prompt the orchestrator fills before dispatching tdd-implementer."
---

Dispatch with `subagent_type: tdd-implementer` after the RED run is saved to `red.txt`. Pass only the fields below: no issue number, ACs or plan.

```
Make these failing tests pass with the minimal implementation.

Failing tests: {test_paths}

Current failure output:
{test_output}

Do:
- Run the tests first and confirm they fail as shown. If the test files are
  missing on disk, stop with ESCALATION.
- Write the simplest code that passes; match neighbouring conventions.
- Never edit, skip or loosen a test. Report any test you think is wrong.
- Run the target tests, then the full suite. Paste both passing outputs.
- If you pass a test only by special-casing its input, say so.

Testing rules (path-scoped rules do not load in sub-agents, so they are restated here).
You judge the tests against these in "Test concerns"; you do not edit them:
- **Seen red:** you will run it before it counts.
- **Discriminating half:** assert the negative alongside the positive (the thing is logged *and* the ordinary case is not).
- **Stub at the boundary** the code crosses (fake binary on PATH, fake HTTP server), not deep inside with mocks that mirror the implementation.
- **Production types:** construct what the system under test receives in production, not a convenient dict.
- Time-dependent code: inject the clock. A skip names what it waits for.

Return the report in your agent format, ending PASS, FAIL or ESCALATION.
```

Gate after return: run `{test_paths}` then the full suite, save the output to `green.txt`. Red suite: re-invoke once with the failure, then stop and report.
