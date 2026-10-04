---
type: guide
title: Getting started
description: Clone the template, run /setup, and know what you have afterwards; includes the partial-adoption path.
tags: [onboarding, setup]
---

# Getting started

## Requirements

- Claude Code (current release).
- `gh` 2.96 or newer, authenticated (`gh auth status`). Sub-issues and blocked-by edges fail silently on older versions; `scripts/github/check_gh.sh` checks.
- Node 18+ for `npm test`.
- Python 3.9+ is **required**: every hook, including the security gate, runs with `python3`; without it enforcement is silently off. `pytest` + `pyyaml` are optional: they add the harness tests. Without them `npm test` prints a notice and exits 0; CI always runs the full suite.

## Steps

1. Clone (this is a template, not a package; there is nothing to `npm install`):
   ```bash
   git clone https://github.com/jackrich78/project-starter.git my-project && cd my-project
   ```
2. `claude .`
3. `/setup`. It asks at most six questions (name and one-liner, the problem and for whom, the first things to build, integration mode `pr | direct`, repo visibility, area labels), then:
   - fills CLAUDE.md and PROJECT.md;
   - renames the template remote to `upstream`, creates your GitHub repo, labels and issue templates;
   - has `tech-product-lead` propose a roadmap (at most 8 features, 3 phases) and creates stub `feature` issues from the list you approve;
   - makes the founding commit, pushes and watches CI.
   Preview with `/setup --dry-run`; rerun any time, finished steps print `ok`.
4. Check the smoke list `/setup` prints (tests, gh, labels, wiki lint, CI all pass).
5. Start with [first-session.md](first-session.md).

## What you get

An orchestrator main thread that delegates to sub-agents; GitHub Issues as the spec and the queue; per-agent memory; a linted wiki under `docs/`; a model policy enforced by a test; a small security hook. CLAUDE.md is the operating contract and the first thing to read.

Principles are not set during `/setup`. When ready, run the `grilling` skill on PROJECT.md; the three template principles stand until then.

## Partial adoption

Not ready for the whole harness? Take only `.claude/rules/` + `.claude/hooks/` + `settings.json` into an existing repo. You get path-scoped conventions and the deny/salvage hooks with no workflow change. Add skills and agents later, one at a time, as you hit the need.

## Troubleshooting

- `check_gh.sh` fails: upgrade `gh` or run `gh auth login`.
- `npm test` skips Python tests: install Python 3.9+ to run them locally.
- Wiki lint warnings: `python scripts/wiki_lint.py --all` names the page and rule.

## Next

[first-session.md](first-session.md) · wiki entry point: [../index.md](../index.md) · operating contract: [../../CLAUDE.md](../../CLAUDE.md)
