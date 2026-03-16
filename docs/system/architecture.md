# System Architecture

**Updated:** 2026-03-06
**Purpose:** Deep technical reference for the agent harness

---

## Overview

This is a lean agent harness for AI-assisted development. It orchestrates specialized agents through slash commands, with hooks for security, logging, and session recovery.

### Core Principles

1. **Reduce** - Minimize context, load on-demand
2. **Offload** - Use sub-agents for specialized work
3. **Isolate** - Contain side effects, fail gracefully

### Context Layers

```
CLAUDE.md (~30 lines)       → Instant startup (every session)
PROJECT.md                  → Current state, roadmap (on-demand)
docs/system/architecture.md → Core reference (this file, on-demand)
  ├─ architecture-tdd.md    → TDD module (loaded by /prime build)
  └─ architecture-qa.md     → QA+Hooks module (loaded by /prime build, review)
.claude/skills/             → Executable patterns (when relevant)
docs/features/FEAT-XXX/     → Feature-specific detail
```

---

## Agent System

### Agent Structure

All agents follow the template in `.claude/agents/TEMPLATE.md`:

```yaml
---
name: agent-name
description: One-line purpose
tools: [Read, Write, Glob, ...]  # Minimal set needed
status: Active | Planned
color: blue | orange | red | purple | green
updated: YYYY-MM-DD
---
```

Key sections:
- **Primary Objective** - Single clear purpose
- **Workflow** - Step-by-step process
- **Quality Criteria** - Validation before completion
- **Guardrails** - What the agent must NOT do

### Available Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| **Researcher** | Deep research using WebSearch to answer open questions from PRDs | Read, WebSearch, Task, Glob, Write |
| **Challenger** | Critical review with two-tier escalation | Read, Glob, Grep |
| **First Principles Thinker** | Breaks down problems into fundamental truths | Read, WebSearch |
| **Specialist Creator** | Creates domain-expert sub-agents | Read, Write, WebSearch |
| **Prompt Specialist** | Generates optimized prompts | Read, Write, WebSearch, Glob, Grep |
| **Product-Engineering Lead** | Hybrid product strategist and tech lead | Read, Write, Glob, Grep |
| **N8N Specialist** | N8N workflow implementation | WebSearch, Read, Write |
| **Librarian** | Documentation consistency and cross-references | Read, Write, Glob, Grep |
| **QA Reviewer** | Security and quality review with SAST | Read, Glob, Grep, Bash |
| **TDD Test Writer** | Writes failing tests (RED phase) | Read, Write, Glob, Grep, Edit, Bash |
| **TDD Implementer** | Minimal code to pass tests (GREEN phase) | Read, Write, Glob, Grep, Edit, Bash |
| **TDD Refactorer** | Improves code quality (REFACTOR phase) | Read, Write, Glob, Grep, Edit, Bash |

### Agent Invocation

Agents are invoked via the Task tool:

```
Task(
  subagent_type="researcher",
  description="Research authentication patterns",
  prompt="Investigate OAuth vs JWT for [context]..."
)
```

For specialists created via `/create-specialist`:
```
Task(
  subagent_type="general-purpose",
  description="Get Supabase expertise",
  prompt="You are the Supabase Specialist. @.claude/agents/supabase-specialist.md [question]"
)
```

---

## Command System

### Command→Agent Mapping

| Command | Primary Agent | Purpose |
|---------|--------------|---------|
| `/setup` | Main + Product-Engineering Lead + Librarian + Challenger | Project initialization |
| `/explore` | Main + Researcher | Feature discovery → PRD |
| `/blueprint` | Main + Researcher + Challenger | Technical grounding + implementation plan |
| `/build` | Main | TDD implementation |
| `/debug` | Main + Researcher + Challenger + QA Reviewer | Bug investigation and resolution |
| `/commit` | Main | Git workflow |
| `/handover` | Main | Session recovery |
| `/prime` | Main | Load project context |
| `/retro` | Main | Extract learnings → skills |
| `/qa` | Main + QA Reviewer | Security and quality review |
| `/logs` | Main | Query observability database |
| `/create-specialist` | Main + Specialist Creator | Create domain-expert agent |
| `/update-docs` | Main | Update documentation index |

### Workflow Patterns

**New Project Flow:**
```
/setup [docs path]
    ↓
Main Agent → Interview + Doc Generation
    ↓
Product-Engineering Lead → Feature Roadmap
    ↓
Librarian + Challenger (opt-in) → Review
    ↓
Git & GitHub Setup
```

**Feature Development Flow:**
```
/explore [topic]
    ↓
Main Agent + Researcher → PRD
    ↓
/blueprint FEAT-XXX
    ↓
Main Agent + Researcher → Plan
    ↓
Challenger (inline) ──┬── Tier 1: Auto-fix → Continue
                      └── Tier 2: Ask user → Continue
    ↓
/build FEAT-XXX
    ↓
Main Agent → TDD Implementation (RED-GREEN-REFACTOR)
    ↓
/commit
```

---

## Orchestration Patterns

### Agent Handoffs

Context flows through explicit prompts, not shared state:

1. **Explore → Researcher:** PRD context passed in prompt
2. **Plan → Challenger:** Architecture passed for review
3. **Challenger → Human:** Tier 2 issues escalated with context

Each agent gets fresh context window. Pass only what's needed.

### Offloading Decisions

**Spawn sub-agent when:**
- Task requires specialized expertise (research, review)
- Task is isolated and can run independently
- You need parallel execution

**Work inline when:**
- Task is simple and contextual
- You already have the information needed
- Spawning would add latency without benefit

### Two-Tier Escalation (Challenger)

**Tier 1 (Auto-fix):** Minor issues the agent can resolve
- Typos, formatting, missing details
- Agent iterates without human involvement

**Tier 2 (Escalate):** Real decisions requiring human input
- Architectural trade-offs
- Scope changes
- Risk assessments

Max 3 issues per review to avoid overwhelm.

---

## Context Management

### Retrieval Hierarchy

When gathering information:

1. **Local files first** - Read existing code/docs
2. **WebSearch** - Current web information
3. **Ask user** - Last resort for missing context

### Compaction Guidelines

When context approaches limits:

1. **PreCompact hook fires** - Saves session state automatically
2. **State preserved:**
   - Feature being worked on
   - Recent file changes
   - Suggested next action
3. **Recovery flow:**
   - Read `.claude/session-state.json`
   - Load relevant feature docs
   - Continue from saved state

### What to Preserve

- Current feature ID and status
- Key decisions made
- Blocking issues
- File paths modified

### What NOT to Preserve

- Full file contents (re-read when needed)
- Exploration dead-ends
- Verbose research results

---

## Guardrails

### Blocked Command Patterns

Defined in `pre_tool_use.py`:

```python
BLOCKED_PATTERNS = [
    r'rm\s+-rf\s+/',      # Root deletion
    r'sudo\s+rm',         # Privileged deletion
    r'curl.*\|\s*bash',   # Code injection
    r'>\s*/etc/',         # System file writes
    # ... see hook for full list
]
```

### Validation Rules

Quality gates before completion:

1. **PRD validation:** All required sections present
2. **Plan validation:** Architecture decisions documented
3. **Code validation:** Tests pass, no lint errors
4. **Commit validation:** Conventional format, no secrets

### Fail-Open Principle

Hooks exit 0 on errors to avoid blocking legitimate work:
- Log the error
- Allow the operation
- Don't fail silently on expected operations

---

## File Conventions

### Naming

- Agents: `.claude/agents/[name].md` (kebab-case)
- Commands: `.claude/commands/[name].md` (kebab-case)
- Specialists: `.claude/agents/[library]-specialist.md`
- Features: `docs/features/FEAT-XXX_[description]/`
- Stacks: `stacks/[platform]/` (e.g., `stacks/cloudflare/`)

### Required Files per Feature

1. `README.md` - Human-readable summary
2. `prd.md` - Product requirements
3. `plan.md` - Implementation plan

### Stack Structure

Each stack in `stacks/[platform]/` contains:
1. `README.md` - Setup instructions
2. `.claude/agents/` - Platform-specific specialist agents
3. Config files - Platform configuration (e.g., `wrangler.toml`)
4. `src/` - Boilerplate code (optional)

**Usage:** Copy stack files to project root, then delete `stacks/` directory. See [stacks/README.md](../../stacks/README.md#design-rationale) for why this merge-to-root pattern was chosen.

### Spike Structure

Temporary exploratory code validating technical approaches:

```
spikes/spike-[topic]-[timestamp]/
├── FINDINGS.md              # Running notes (REQUIRED)
├── README.md                # Context & goals
└── [runnable code]          # POC to prove concept
```

**Note:** Timestamp can be `YYYYMMDD` or full ISO 8601 `YYYYMMDDTHHMMSSZ`

**Lifecycle:**
1. **Create:** Time-boxed validation (2-8 hours)
2. **Execute:** Minimal code to answer specific question
3. **Extract:** Create research doc in `docs/features/FEAT-XXX/research-spike-[topic]-[timestamp].md`
4. **Cleanup:** Delete spike directory after feature ships (research doc remains)

**See the [Spike Skill](../../.claude/skills/spike/SKILL.md) for complete process.**

---

## Topic Modules

Detailed architecture for specialized workflows. Loaded by `/prime` modes that need them.

- [architecture-tdd.md](architecture-tdd.md) — TDD subagent phases, isolation, flow (loaded by `build`)
- [architecture-qa.md](architecture-qa.md) — QA integration, SAST, hooks, escalation (loaded by `build`, `review`)

---

## See Also

- [getting-started.md](getting-started.md) - **Start here** - Using this template for new projects
- [architecture-tdd.md](architecture-tdd.md) - TDD subagent architecture
- [architecture-qa.md](architecture-qa.md) - QA integration & hooks
- [Test Strategy Skill](../../.claude/skills/test-strategy/SKILL.md) - Decision tree for all pyramid levels
- [Spike Skill](../../.claude/skills/spike/SKILL.md) - Technical validation spike process
- [observability.md](observability.md) - Logging, checkpoints, debugging
- [integrations.md](integrations.md) - MCPs, external tools
- [connections.md](connections.md) - File relationship map
- [PROJECT.md](../../PROJECT.md) - Current roadmap
- [CLAUDE.md](../../CLAUDE.md) - Startup context
