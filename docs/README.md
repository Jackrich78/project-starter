# Documentation Index

Project documentation organized by type.

---

## Directories

| Directory | Purpose |
|-----------|---------|
| `features/` | Per-feature documentation (README, prd, plan) |
| `guides/` | User-facing how-tos (setup, commands, skills, sync) |
| `system/` | Deep technical reference (architecture, connections, CI/CD, observability) |
| `templates/` | Document templates for commands |
| `research/` | Shared research findings |
| `../spikes/` | Temporary spike directories (at project root) |
| `../stacks/` | Deployment target scaffolding (Cloudflare, etc.) |

---

## Guides

User-facing how-tos for operating the harness:

- **[getting-started.md](guides/getting-started.md)** - Using this template for new projects
- **[working-with-claude.md](guides/working-with-claude.md)** - Configure project context and steer Claude in sessions
- **[commands-reference.md](guides/commands-reference.md)** - Full command reference with when-to-run context
- **[skills-reference.md](guides/skills-reference.md)** - All skills with descriptions
- **[two-remote-sync.md](guides/two-remote-sync.md)** - Syncing changes between private and public repos
- **[mcp-configuration.md](guides/mcp-configuration.md)** - MCP setup and on-demand activation
- **[upstream-workflow-contributions.md](guides/upstream-workflow-contributions.md)** - Contributing improvements back to the template

---

## System Documentation

Deep technical reference for the harness internals:

- **[architecture.md](system/architecture.md)** - Agent system, commands, hooks, orchestration patterns
- **[cicd-workflow.md](system/cicd-workflow.md)** - CI/CD pipeline, validation, troubleshooting
- **[observability.md](system/observability.md)** - Logging, session state, debugging
- **[integrations.md](system/integrations.md)** - MCPs, WebSearch, IDE tools
- **[connections.md](system/connections.md)** - File relationship map

---

## Templates

Used by `/explore` and `/blueprint` commands:

- **[prd-template.md](templates/prd-template.md)** - Product requirements
- **[plan-template.md](templates/plan-template.md)** - Implementation plan
- **[readme-template.md](templates/readme-template.md)** - Feature README
- **[qa-report-template.md](templates/qa-report-template.md)** - QA review reports
- **[research-template.md](templates/research-template.md)** - Research findings

---

## Features

Feature documentation lives in `features/FEAT-XXX_description/` directories.
Each feature has: README.md (summary), prd.md (requirements), plan.md (implementation).

Use `/explore [topic]` to start a new feature.

---

## Navigation

- [CLAUDE.md](../CLAUDE.md) - Startup context (commands, principles)
- [PROJECT.md](../PROJECT.md) - Current roadmap and state
- [CHANGELOG.md](../CHANGELOG.md) - Version history

---

*This index is manually maintained. Update when adding new features or system docs.*
