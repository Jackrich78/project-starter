# Project Starter

Lean agent harness template for AI-assisted development.

> **New project?** See [docs/guides/getting-started.md](docs/guides/getting-started.md) for setup instructions.

## Quick Start

```bash
# Run tests
npm test

# Start dev
npm run dev
```

## Agents

Specialists in `.claude/agents/` (descriptions auto-loaded from frontmatter).

**Command bindings:**
- `/build` → `tdd-test-writer` → `tdd-implementer` → `tdd-refactorer` → `qa-reviewer`
- `/qa` → `qa-reviewer`

Full index: `.claude/agents/README.md`

## Commands

- `/setup [docs path]` - One-time project initialization from template
- `/explore [topic]` - Discover and define features → PRD
- `/blueprint FEAT-XXX` - Technical grounding + implementation plan
- `/build FEAT-XXX` - TDD implementation with isolated subagents + QA
- `/qa [target]` - QA review (file, directory, feature, or sweep)
- `/commit` - Git workflow (checks QA gate first)
- `/handover` - Session recovery
- `/retro` - Extract learnings → skills
- `/logs` - Query observability database
- `/debug [issue]` - Systematic bug investigation
- `/create-specialist [lib]` - Create domain-expert sub-agent
- `/update-docs` - Update documentation index
- `/prime [mode]` - Load project context

## Key Files

- `PROJECT.md` - Project context and roadmap
- `docs/features/` - Feature documentation (README, prd, plan per feature)
- `docs/qa/` - QA review reports
- `stacks/` - Deployment scaffolding (copy to root when using a stack)
- `.claude/skills/` - Learned patterns
- `.claude/agents/tdd-*.md` - TDD subagents (test-writer, implementer, refactorer)
- `.claude/agents/qa-reviewer.md` - Security and quality reviewer
- `.claude/logs/agent.db` - Session tracking
- `.github/tests/` - Scaffold validation tests (extend or delete)
- `test/` - Your project tests (unit/, integration/, e2e/)

## Principles

1. **Reduce** - Minimize context, load on-demand
2. **Offload** - Use sub-agents for specialized work
3. **Isolate** - Contain side effects, fail gracefully

## Development Standards (This Project)

- **TDD with isolation**: `/build` runs RED-GREEN-REFACTOR with context-isolated subagents
- **QA gate**: Security issues from `/build` or `/qa` block `/commit` until resolved
- **Outcomes over outputs**: Features solve user problems, not just ship code
- **Spike before commit**: Use `spikes/` for uncertain approaches, extract learnings to `docs/`

## Context Rules

- **Web research**: Always use the Researcher agent (`subagent_type="researcher"`) for web searches. This preserves context in the main thread.
- **TDD subagents**: Test writer sees only PRD, implementer sees only tests, refactorer sees tests + implementation. This isolation prevents bias.
- **QA context**: The qa-reviewer reads handover.md, NOT the builder conversation. Clean context enables honest review.
