# Tests

| Directory | What lives here | Runner |
|---|---|---|
| `harness/` | Tests of the harness itself: model-tier table vs agent frontmatter, agent-memory format, hook deny patterns, settings wiring, wiki lint, size caps, dead paths. Shipped with the template; keep them. | `npm test` (pytest when available; CI always) |
| `unit/` · `component/` · `integration/` · `e2e/` | Your project's tests. Empty on clone. | your stack's runner — wire it into `npm test` or CI |

Conventions for writing tests are in `.claude/rules/testing.md` (loads automatically when you edit files under `tests/`).
