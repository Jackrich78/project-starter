---
updated: 2026-03-06T18:00:00Z
version: 1.0.0
status: Active
---

# Project Starter — Project Plan

## Vision

<!-- CUSTOMIZE: Replace with your project's vision statement -->
A lean, observable, reusable starter template for AI agent orchestration. Fork and customize for any project.

## Current State

**Version:** 1.0.0
**Phase:** Ready to use

<!-- CUSTOMIZE: Track your active features here -->
### Active Features
- (Add your features as you build them)

### Capabilities
- 12 specialized agents (including TDD subagents, QA reviewer, research, planning)
- 13 workflow commands (explore, blueprint, build, qa, commit, etc.)
- Skills system for learned patterns
- Observability (SQLite + JSON logs)
- Security hooks
- SAST integration (Semgrep) with graceful degradation

## Roadmap

<!-- CUSTOMIZE: Define your project milestones -->
- [ ] Set up project (fork, configure, run `/prime`)
- [ ] Define first feature (`/explore [topic]`)
- [ ] Create implementation plan (`/blueprint FEAT-001`)
- [ ] Build with TDD (`/build FEAT-001`)

## Architecture Overview

```
User → /command → Agent(s) → Skills → Documentation
                     ↓                    ↓
              Hooks (security, logging)   QA Review (SAST + LLM + semantic validation)
                     ↓                    ↓
              SQLite + JSON logs     docs/qa/ reports
```

### Core Components
- **Agents** (12): researcher, challenger, first-principles-thinker, specialist-creator, prompt-specialist, n8n-specialist, tech-product-lead, librarian, qa-reviewer, tdd-test-writer, tdd-implementer, tdd-refactorer
- **Commands** (12): explore, blueprint, build, qa, commit, handover, prime, retro, logs, create-specialist, update-docs, debug
- **Skills**: Extensible — add skills via `/retro` or manually in `.claude/skills/`
- **Hooks** (5): pre_tool_use (security), post_tool_use (logging), pre_compact (state), stop (suggestions), send_event (observability)

### CI/CD Structure

**Monorepo Pattern:**
- `.github/tests/` - Scaffold validation (isolated deps)
- `test/` - Project tests (your code)
- `stacks/[platform]/` - Self-contained with own tests

**Extending CI:**
- Edit `.github/workflows/validate.yml` (marked CUSTOMIZATION points)
- Use `ci-validation` skill before pushing
- See `.github/workflows/README.md` for guide

## Key Decisions

<!-- CUSTOMIZE: Document your architectural decisions here -->
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Context strategy | Dual files (CLAUDE.md + PROJECT.md) | Startup vs. deep context |
| Observability | SQLite + JSON | Structured queries + human readable |
| Feature docs | 3 files (README, prd, plan) | Minimal overhead |

## Documentation

- `docs/features/` - Per-feature documentation
- `docs/system/` - Architecture, connections, getting started
- `.claude/skills/` - Learned patterns
- `spikes/` - Temporary experimental code (deleted after learnings extracted)
