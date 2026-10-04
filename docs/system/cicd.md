---
type: domain-doc
title: CI/CD
description: What validate.yml runs and why, the two-lane npm test degrade rule, the conftest guard, how to add project checks, and local workflow linting.
tags: [ci, github-actions, validation, testing]
updated: 2026-10-03
---

# CI/CD

Workflows live in `.github/workflows/`. A test or check that is in no workflow does not exist (`.claude/rules/testing.md`). This page mirrors the workflow files; when they disagree, the workflow is the fact and this page is fixed in the same turn.

## `validate.yml` (every push and PR, any branch)

`contents: read` only; concurrent runs on a ref cancel; 10-minute timeout per job. Actions are pinned by commit SHA. Two jobs.

### Job `validate`

Steps, in order; every one is blocking:

| Step | Why |
|---|---|
| Checkout (`fetch-depth: 0`, `persist-credentials: false`), Node 20, Python 3.12 | the two runtimes `npm test` and the hooks need; full history because `wiki_lint` derives staleness from git; repo scripts get no token. 3.12 matches `.python-version` when a project adds one |
| `pip install 'pytest>=8,<9' 'pyyaml>=6,<7'` | CI always has the optional runtime, so the harness suite runs here even when a local clone skips it |
| actionlint (`raven-actions/actionlint`) | a workflow syntax error is otherwise found only after pushing |
| `git ls-files "*.py" \| xargs python3 -m py_compile` | every tracked `.py` must compile: a hook that does not compile fails every session; catches syntax only |
| `python3 scripts/audit_claude_md.py --strict` | CLAUDE.md shape and size |
| `python3 scripts/wiki_lint.py --all` | wiki frontmatter, size caps, links, reserved files |
| `python3 -m pytest tests/harness -q` | the harness suite, run directly (not via `npm test`, which degrades to a notice without pytest and CI must not) |
| Project deps: `pip install 'uv>=0.11,<0.12' && uv sync --frozen` | `if: hashFiles('pyproject.toml') != ''`: skipped until the project has a `pyproject.toml` |
| Project tests: `uv run --frozen pytest tests/unit tests/integration -q` | same guard; the project lane on the locked environment, the same command `npm test -- project` runs locally |

### Job `cold-clone`

Simulates an adopter with no history, no `node_modules` and no Python deps: `git clone --depth 1` of the checked-out tree into `my-project`, then `npm test` and `node scripts/run_pytest_optional.mjs` (both must degrade to a NOTICE and exit 0 without pytest), `CLAUDE.md`, `PROJECT.md` and `.claude/skills/setup` present, and `bash scripts/github/check_gh.sh --quiet` is allowed to fail (no `gh` auth in CI).

## The `npm test` degrade rule (two lanes)

`npm test` runs `scripts/run_pytest_optional.mjs`, which has two lanes with one rule: a lane whose runtime or suite is missing prints one NOTICE and exits 0, so a Node-only cloner never sees red for a missing optional runtime. Pytest exit 5 (no tests collected) also counts as success.

| Lane | Command | Runs when | Otherwise |
|---|---|---|---|
| `harness` | `python3 -m pytest tests/harness -q` | `tests/harness/` exists and `python3 -m pytest --version` works | `NOTICE: pytest not found` (or `tests/harness not found`), exit 0 |
| `project` | `uv run --frozen pytest tests/unit tests/integration -q` (only the suite dirs that exist) | `pyproject.toml` and `.venv/` exist and `uv --version` works | `NOTICE: project tests skipped - add pyproject.toml and run uv sync once`, exit 0 |

- `npm test` runs harness then project and stops on a harness failure.
- `npm test -- harness [pytest args]` or `npm test -- project [pytest args]` runs one lane and passes the rest to pytest. `npm run test:project` is the project lane; `npm run test:py` is the harness suite under pytest directly.
- CI runs both lanes directly and never degrades, so the gates still bind there. Never turn the degrade into a failure, and never let a new optional runtime fail the primary command.

### The conftest guard

`Bash(npm test -- *)` is pre-approved in `.claude/settings.json`, so anything pytest collects runs without a permission prompt. `tests/conftest.py` is an autouse fixture for every test in every lane: it deletes each environment variable whose name ends in `KEY`, `TOKEN`, `SECRET` or `PASSWORD` and makes `socket.socket` and `socket.create_connection` raise. A collected test can never spend an API budget or call out. The guard is in-process only: a test that shells out starts a child with the parent environment and a working network, so tests must not subprocess anything that reads keys or opens a socket. Live checks are explicit script calls outside pytest, which prompt.

## Add a project check

For a Python project: add `pyproject.toml`, run `uv sync` once, put tests in `tests/unit` and `tests/integration`. Nothing else to wire: `npm test` picks the lane up locally and the two guarded steps in `validate.yml` run it in CI.

For another stack, replace the two guarded project steps in `validate.yml` with your runner (for example `npx tsc --noEmit` and `npm run test:unit`) and have `npm test` call the same command, so local and CI share one exit contract. Scope a step with `paths:` only if its backlog is zero: an advisory step that cannot fail is deleted, not tolerated.

## Validate workflows locally

```bash
actionlint .github/workflows/validate.yml   # syntax and expression errors
npm test                                    # both lanes, minus the installs
```

Pin third-party actions to a commit SHA, give every workflow a `permissions:` block, and never pipe an unpinned installer to a shell. The `ci-validation` skill carries the full pre-push checklist.
