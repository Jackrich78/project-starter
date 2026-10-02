---
paths:
  - tests/**
---

# Test conventions

Full rationale: `docs/system/testing-rules.md`. The rules:

- **Every test has been seen red.** Write it against a deliberately broken version first, or mutate the code once after writing; a test never observed failing is decoration.
- **Assert the discriminating half**, not only the positive case ("caution logged" *and* "ordinary not logged").
- **Stub at the boundary the code crosses** (a fake binary on PATH, a fake HTTP server), not deep inside with mocks that mirror the implementation.
- **Construct the type the system under test receives in production** (dataclass, Pydantic model, parsed JSON), never a convenient dict.
- **A test not in a CI lane does not exist.** Add the file to `.github/workflows/validate.yml` (or the runner `npm test` calls) in the same commit.
- **Look for existing tests first:** `grep -rl "<module>" tests/`. Extend before adding.
- **Pin surprising behaviour with a reason** in the test name or a comment; do not quietly change it.
- **A skip or marker names what it is waiting for.**
- **Time-dependent code gets time-independent tests** (inject the clock; offsets larger than any period).
- **Name the reader of an output before testing it.** If nobody reads it, test it last.
- **Backstop tests over exhaustive lists:** a few outcome-level tests plus per-branch unit tests, not one test per acceptance-criterion line.
