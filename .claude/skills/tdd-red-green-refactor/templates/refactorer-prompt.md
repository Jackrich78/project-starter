---
type: reference
title: "tdd-refactorer dispatch prompt (REFACTOR)"
description: "Prompt the orchestrator fills before the single per-ticket refactor pass."
---

Dispatch with `subagent_type: tdd-refactorer` once, after every test is green and the GREEN state is committed locally.

```
Refactor the passing implementation without changing behaviour.

Test files: {test_paths}
Implementation files: {impl_paths}

Do:
- Run the full suite first. If it is not green, stop with FAIL: baseline.
- One small change at a time; run the suite after each; revert on red.
- Abstract only on the third repetition. Prefer deleting to adding.
- Do not edit tests (a mechanical rename that follows your own rename excepted,
  and say so). Do not change public signatures.
- "No refactoring needed" with one line on what you checked is a valid result.

Testing rules (path-scoped rules do not load in sub-agents, so they are restated here).
A mechanical rename in a test must keep it within these:
- **Seen red:** you will run it before it counts.
- **Discriminating half:** assert the negative alongside the positive (the thing is logged *and* the ordinary case is not).
- **Stub at the boundary** the code crosses (fake binary on PATH, fake HTTP server), not deep inside with mocks that mirror the implementation.
- **Production types:** construct what the system under test receives in production, not a convenient dict.
- Time-dependent code: inject the clock. A skip names what it waits for.

Return the report in your agent format, ending PASS, FAIL or ESCALATION.
```

Gate after return: run the full suite, confirm green. Commit-sized changes only; a red suite you cannot restore means `git restore -- <the implementation paths you touched>` back to the pre-refactor commit (never `git checkout -- .`: it discards every edit in the tree).
