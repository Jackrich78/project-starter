# Contributing to Project Starter

The template develops itself with its own harness. Work is tracked in this repo's GitHub Issues; `docs/system/issue-flow.md` explains the labels and states.

## Getting started

```bash
git clone https://github.com/jackrich78/project-starter.git && cd project-starter
npm test                       # harness tests (pytest + pyyaml when available)
claude .                       # then /prime
```

Requirements: Claude Code, `gh` ≥ 2.96 (sub-issues), Node 18+, Python 3.9+ (optional locally, always in CI).

## Proposing a change

1. Look for an open issue first (`gh issue list --label ready-for-agent`); raise one with the ticket template if none fits. A design that touches CLAUDE.md, hooks or agents gets a `feature` parent issue with a design note before any code.
2. Branch `issue-N-<slug>` (`gh issue develop N --checkout`), build with `/build #N`, review with `/qa --issue N`, commit with `/commit` (it refuses on a `BLOCKED SECURITY` verdict and runs the validators).
3. Open a PR whose body carries `Closes #N`. CI runs `validate.yml`: actionlint, hook syntax, CLAUDE.md audit, wiki lint, leak gate, coupling lint, the harness tests and a cold-clone smoke job. All must be green.

## What a change must keep true

- **CLAUDE.md stays under 150 lines** (warn at 120). Detail goes to `.claude/rules/` or `docs/`.
- **Skills ≤ 150 lines, agents ≤ 300**, every skill with `name` = folder and a trigger-phrased `description` (`.claude/rules/skills.md`).
- **Agent frontmatter matches the CLAUDE.md model tables**; `memory:` only on the TDD trio (`.claude/rules/agents.md`).
- **Every wiki page has frontmatter with a `type`** and is listed in `docs/index.md` (`.claude/rules/wiki.md`).
- **A hook pattern change ships a corpus case** in `tests/harness/test_hooks.py`, seen red once (`.claude/rules/hooks.md`).
- **Decisions are logged** in `docs/decisions.md` in the same change, with the rejected option.
- **Nothing private, ever.** No real names, hosts, handles, client or product references, no secrets. Run `bash scripts/leak_gate.sh` and `bash scripts/coupling_lint.sh` before pushing; CI runs both.
- **Before changing anything the harness mechanism depends on** (agent frontmatter, hooks, settings, skill frontmatter), ask the built-in `claude-code-guide` and cite its answer in the commit body (`docs/reference/claude-code.md`).

## Attribution

Seven skills are adapted from Matt Pocock's skills (MIT); see `NOTICE`. Keep the attribution line in any derived skill.

## Licence

MIT. By contributing you agree your contribution is licensed the same way.
