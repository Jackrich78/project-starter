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

Return the report in your agent format, ending PASS, FAIL or ESCALATION.
```

Gate after return: run the full suite, confirm green. Commit-sized changes only; a red suite you cannot restore means `git restore -- <the implementation paths you touched>` back to the pre-refactor commit (never `git checkout -- .`: it discards every edit in the tree and the security hook blocks it).
