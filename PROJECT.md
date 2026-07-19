---
updated: 2026-07-19T00:00:00Z
version: 2.0.0
status: Active
---

# Project Starter — Project Plan

## Vision

<!-- CUSTOMIZE: Replace with your project's vision statement -->
A lean, observable, reusable starter template for AI agent orchestration. Fork and customize for any project.

## Current State

**Version:** 2.0.0
**Phase:** Ready to use

<!-- CUSTOMIZE: Track your active features here -->
### Active Features
- (Add your features as you build them)

### Capabilities
- 14 specialized agents (TDD subagents, QA reviewer, research, planning, agile coach, PRD simulator)
- 14 workflow commands (setup, explore, blueprint, build, qa, commit, etc.)
- 21 skills for learned patterns, content creation, and technical integration
- Agent memory system: structured per-agent memory files + evidence-gated learning loop (Agile Coach + Librarian)
- Explicit model-tier policy: Opus for high-stakes review, Sonnet for workhorse agents, Haiku for retrieval
- Four quality gates: symbol discovery, fidelity, QA review, readiness classification
- Observability (SQLite + JSON logs); schema prepared for v2.1 agent attribution — internal builds add nullable agent_id/parent_session_id columns, minimal public install keeps the v1 events schema (ETL in v2.1)
- Security hooks and SAST integration (Semgrep) with graceful degradation
- PRD Consistency Simulator: cold-reads specs before the build agent sees them
- Commit gate: hard-refuses BLOCKED/security findings; confirmation required for NEEDS_FIXES

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
- **Agents** (14): researcher, challenger, first-principles-thinker, specialist-creator, prompt-specialist, n8n-specialist, tech-product-lead, librarian, qa-reviewer, tdd-test-writer, tdd-implementer, tdd-refactorer, agile-coach, prd-consistency-sim
- **Commands** (14): setup, explore, blueprint, build, qa, commit, handover, prime, retro, logs, create-specialist, update-docs, debug, sync
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
