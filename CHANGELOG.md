# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] - 2026-03-11

### Added
- 17-slide PPTX explainer deck (`docs/system/project-starter-explainer.pptx`)
- Diagram subfolder (`docs/system/diagrams/`) with 10 Excalidraw + PNG diagrams
- Two-remote sync workflow guide (`docs/system/two-remote-sync.md`)
- Generic brand guidelines starter (`/claude/skills/brand-guidelines/`)
- `CONTRIBUTING.md` for open source contributors

### Changed
- Renamed: "AI Workflow Starter" → "Project Starter" (repo, docs, package.json)
- Archon MCP removed from all public-facing files (researcher agent now WebSearch-only)
- Diagrams reorganised into `docs/system/diagrams/` subfolder
- PPTX build script uses relative paths (no hardcoded `/Users/builder/` paths)

### Removed
- Archon MCP integration docs and researcher.md conditional Archon branches
- Brand-specific skills (linkedin-*, sd-brand-guidelines) from public distribution

## [2.0.0] - 2026-01-24

### Added

- **Deep context system** - `docs/system/` with architecture, observability, integrations
- **Session recovery** - PreCompact hook saves state before context compaction
- **Security hooks** - PreToolUse blocks dangerous commands
- **Auto-formatting** - PostToolUse formats code after edits
- **Git suggestions** - Stop hook provides commit recommendations
- **Skills system** - `.claude/skills/` for learned patterns via `/retro`

### Changed

- **Agents reduced** - 5 focused agents (researcher, challenger, specialist-creator, prompt-specialist, n8n-specialist)
- **Commands streamlined** - 8 commands (explore, plan, build, commit, handover, prime, retro, status)
- **Feature docs simplified** - 3 files per feature (README, prd, plan) instead of 6
- **Context layers** - CLAUDE.md (~42 lines) + PROJECT.md + docs/system/ drill-down

### Removed

- Centralized AC.md (acceptance criteria now in feature plans)
- SOPs directory (replaced by skills)
- 6 documentation templates (kept 3: prd, plan, readme)
- Explorer, Planner, Documenter, Reviewer agents (consolidated)
- `/test` command (integrated into `/build`)

### Architecture

```
CLAUDE.md           → Startup (~42 lines)
PROJECT.md          → Roadmap, current state
docs/system/        → Deep technical reference
.claude/skills/     → Learned patterns
docs/features/      → Per-feature docs
```

## [1.0.0] - 2025-10-24

Initial release of Project Starter template.

- Phase 1: Planning & Documentation system
- 5 original sub-agents
- 6 slash commands
- PreCompact hook for session recovery
- Documentation templates and SOPs

---

**Note:** This changelog tracks major versions. Feature-specific changes are documented in `docs/features/FEAT-XXX/`.
