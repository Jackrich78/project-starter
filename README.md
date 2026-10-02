[![CI](https://github.com/jackrich78/project-starter/actions/workflows/validate.yml/badge.svg)](https://github.com/jackrich78/project-starter/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# Project Starter

A Claude Code harness you clone into a project. An orchestrator main thread delegates to specialist sub-agents, tracks work in GitHub Issues, and keeps what it learns in a linted wiki, so sessions compound instead of restarting. Not all work is code: documents, research and decisions follow the same discover, spec, build, prove arc.

## What you get

- **Orchestrator + sub-agents:** planning and review on Opus, building on Sonnet, retrieval on Haiku.
- **GitHub Issues as the spec:** the issue is the plan, the queue and the close-out record.
- **Per-agent memory:** methods (never findings) kept in `.claude/agent-memory/`, capped and validated.
- **A linted wiki:** `docs/` with an index, a decision log and CI-enforced structure.
- **Model policy with a CI test:** agent frontmatter must match the table in CLAUDE.md.
- **Security hooks + leak gate:** deny hook, least-privilege settings, a gate that scans for private identifiers.

## What this is not

- Not a skill pack. It integrates Matt Pocock's skills (see `NOTICE`) and adds the harness around them.
- Not an all-in-one toolkit. It is small on purpose; add what you need.
- Not a replacement for Claude Code's own `/code-review`, `/security-review` or plan mode. It uses them.

## Quick start

```bash
git clone https://github.com/jackrich78/project-starter.git my-project && cd my-project
claude .
/setup          # asks <= 6 questions, bootstraps GitHub
/prime          # every session
```

## Lifecycle

| Phase | How |
|---|---|
| Bootstrap | `/setup` |
| Vision | `grilling` on PROJECT.md |
| Roadmap in GitHub | stub `feature` issues from `/setup`, later `/explore --roadmap` |
| Discovery | `/explore #N` |
| Design | `/blueprint #N` |
| Tickets | `to-tickets` |
| Build loop | `/build #N` then `/qa --issue N` |
| Ship | `/commit` (`Closes #N`), close-out comment |
| Learn | `/session-winddown`, `/retro` |

Non-code work follows the same path; its tickets carry a `Proof:` line where code tickets carry `Tests:`.

## Partial adoption

Take only `.claude/rules/` + `.claude/hooks/` + `settings.json`. See [getting started](docs/guides/getting-started.md).

## Requirements

Claude Code; `gh` 2.96+ authenticated; Node 18+ for `npm test`; Python 3.9+ optional (harness tests).

## Security stance

The default allow list is read-only; observability is opt-in; `scripts/leak_gate.sh` blocks private identifiers before they ship. Details in `docs/system/`.

## Learn more

- [Getting started](docs/guides/getting-started.md)
- [First session](docs/guides/first-session.md)
- [Docs index](docs/index.md)

## Licence

MIT, see [LICENSE](LICENSE), except `.claude/skills/skill-creator/` (Anthropic, Apache-2.0). Third-party attributions: `NOTICE`.
