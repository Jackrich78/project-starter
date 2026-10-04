# docs/ log

Append-only, newest first. ISO date heading, then a bold verb (**Creation**, **Update**, **Deprecation**) per line.

## 2026-10-05

- **Update** — `guides/getting-started.md` gains § Upgrading (never edit a shipped file; the upgrade runs as one `chore` issue); `/setup` now keeps the page instead of offering to delete it.

## 2026-10-04

- **Update** — v3.0.1 strip-back: `system/hooks.md` rewritten for the v2.0.1 guard plus five rules; leak gate, coupling lint, harness-health, recall and claim-check references removed across `system/`, `guides/` and `index.md`.
- **Deprecation** — `system/observability.md` (observability removed, issue #1).
- **Update** — `system/cicd.md` rewritten to match the workflows (two-lane `npm test`, project tests behind `pyproject.toml`, `cold-clone` job); `system/current-priorities.md` and `system/issue-flow.md` comments point at the single home for area labels; `reference/claude-code.md` notes that path-scoped rules do not load in sub-agents.

## 2026-10-02

- **Update** — security pass: deny hook hardened against obfuscated forms, pre-approved execution vectors removed from the allow list, `scripts/recall.py` added, `leak_gate.sh --history`, redactor covers `sk-` keys; `tests/component/` convention made real.
- **Creation** — `system/{architecture,hooks,observability,testing-rules,cicd,memory-systems,current-priorities}.md`, `guides/{knowledge-architecture,agent-harness-patterns,pruning-lessons,working-with-claude}.md`; `scripts/wiki_lint.py` enforces the schema in CI.
- **Deprecation** — `docs/README.md`, `system/{architecture-qa,architecture-tdd,cicd-workflow}.md`, `.claude/commands/` (every workflow is now a skill).
- **Creation** — `system/issue-flow.md`, `templates/closeout-comment.md`, `templates/research-memo.md`, `guides/getting-started.md`, `guides/first-session.md`; issue templates and label bootstrap under `.github/` and `scripts/github/`.
- **Creation** — wiki bundle established for v3.0: `index.md`, `log.md`, `decisions.md` (moved from the repo root), `reference/claude-code.md`.
- **Deprecation** — `docs/features/`, `docs/qa/`, PRD/plan templates, sync guides, stacks: removed (decisions D1, D2, D4).
