---
type: domain-doc
title: CI/CD
description: What validate.yml and the monthly harness-health workflow run and why, how to add project checks, the npm test degrade rule, and local workflow linting.
tags: [ci, github-actions, validation]
---

# CI/CD

Workflows live in `.github/workflows/`. A test or check that is in no workflow does not exist (`testing-rules.md` principle 7).

## `validate.yml` (every push and PR, any branch)

`contents: read` only; concurrent runs on a ref cancel; 10-minute timeout. Steps, in order:

| Step | Why |
|---|---|
| Checkout, Node 20, Python 3.11 | the two runtimes `npm test` and the hooks need |
| `pip install pytest pyyaml` | CI always has the optional runtime, so the full suite runs here even when a local clone skips it |
| actionlint (`raven-actions/actionlint`) | a workflow syntax error is otherwise found only after pushing |
| `py_compile` every `.py` under `.claude/hooks` and `scripts` | a hook that does not compile fails every session; catches syntax only |
| `npm test` | the harness suite: hook corpus, settings wiring, model-tier table, memory-flag allowlist, label list vs docs, leak gate |

The leak gate, coupling lint and wiki lint (`scripts/leak_gate.sh`, `scripts/coupling_lint.sh`, `scripts/wiki_lint.py --all`) are meant to run as blocking steps; check the workflow file for which are wired today rather than trusting this page, and add any that are missing in the commit that adds the script.

## `harness-health.yml` (monthly cron)

Deterministic checks, zero model tokens: the reference-doc stamp age (`docs/reference/claude-code.md` `last_checked`, tested at 90 days), agent contract checks (`scripts/adoption_check.py`, `scripts/validate_agent_memory.py --check-roster`) and the wiki lint. A cron is used instead of `/loop` (needs a live session) or `CronCreate` (expires after 7 days). The one part that needs a model, re-checking the Claude Code docs, is a SessionStart nudge from `session_prime.py` after 30 days: it asks you to run `/harness-health` and ask `claude-code-guide`.

## Add a project check

Add a step under the marked `CUSTOMIZE` comment in `validate.yml`:

```yaml
- run: npx tsc --noEmit
- run: ruff check .
```

Put project tests in `test/` (or `tests/`) and have `npm test` call them; do not add a second runner with a different exit contract. Scope a step with `paths:` only if its backlog is zero: an advisory step that cannot fail is deleted, not tolerated.

## The `npm test` degrade rule

`npm test` runs `scripts/run_pytest_optional.mjs`, which runs `tests/harness` when `python3 -m pytest` works and otherwise prints a NOTICE and exits 0, so a Node-only cloner never sees red for a missing optional runtime. Pytest exit 5 (no tests collected) also counts as success. CI installs pytest, so the gates still bind there. Never turn the degrade into a failure, and never let a new optional runtime fail the primary command.

## Validate workflows locally

```bash
actionlint .github/workflows/*.yml     # syntax and expression errors
npm test                               # what CI runs, minus the installs
```

Pin third-party actions to a major tag or SHA, give every workflow a `permissions:` block, and never pipe an unpinned installer to a shell. The `ci-validation` skill carries the full pre-push checklist.
