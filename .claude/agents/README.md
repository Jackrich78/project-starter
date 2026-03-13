---
updated: 2026-03-06T18:00:00Z
---

# Sub-Agent Index

Lists all sub-agents available in this project.

## Overview

This directory contains specialized sub-agents that provide focused expertise. Each agent has a single responsibility and well-defined integration points.

## Core Agents

### [Researcher](researcher.md)
**Status:** Active | **Color:** Orange
**Description:** Deep research specialist that investigates technical approaches using WebSearch to answer open questions from PRDs
**Triggers:** Invoked by `/explore` and `/blueprint` commands when research needed
**Outputs:** `docs/features/FEAT-XXX_[slug]/research-[topic]-[timestamp].md` (REQUIRED: must be in feature folder, single file per invocation)
**Tools:** Read, WebSearch, Task, Glob, Write
**Validation:** Enforces feature folder placement, offers skeleton feature creation if context missing

### [Challenger](challenger.md)
**Status:** Active | **Color:** Red
**Description:** Senior engineer that critically reviews proposals, iterating with agents on minor issues and escalating real decisions to the human
**Triggers:** Invoked by `/blueprint` command after architecture creation
**Outputs:** None (conversational feedback)
**Tools:** Read, Glob, Grep
**Key Features:**
- **Two-tier escalation**: Fixes minor issues via agent iteration, escalates trade-offs to human
- **Inline feedback**: No documents—feedback flows through conversation
- **Focused critique**: Max 3 issues per review

### [Specialist Creator](specialist-creator.md)
**Status:** Active | **Color:** Purple
**Description:** Creates comprehensive specialist sub-agents with research auto-population for libraries, frameworks, and technical domains
**Triggers:** `/create-specialist [library-name]` command
**Outputs:** `.claude/agents/[library-name]-specialist.md`
**Tools:** Read, Write, WebSearch

### [Prompt Specialist](prompt-specialist.md)
**Status:** Active | **Color:** Purple
**Description:** Multi-provider prompt engineer that generates and refines high-performance prompts for specific use cases
**Triggers:** Direct user request "generate/refine prompt for..."
**Outputs:** Optimized prompts (markdown)
**Tools:** Read, Write, WebSearch, Glob, Grep

### [N8N Specialist](n8n-specialist.md)
**Status:** Active | **Color:** Green
**Description:** Domain expert for N8N workflow implementation - transforms architecture specs into production-ready workflow JSON
**Triggers:** Direct invocation for N8N workflow design
**Outputs:** N8N workflow JSON
**Tools:** WebSearch, Read, Write

### [First Principles Thinker](first-principles-thinker.md)
**Status:** Active | **Color:** Purple
**Description:** Reasoning specialist that breaks down complex problems into fundamental truths and builds solutions from the ground up, avoiding analogy and convention traps
**Triggers:** Direct invocation for deep reasoning on complex or ambiguous problems
**Outputs:** Structured analysis with fundamental truths, assumptions challenged, and rebuilt conclusions
**Tools:** Read, WebSearch

### [Product-Engineering Lead Specialist](tech-product-lead.md)
**Status:** Active | **Color:** Blue
**Description:** Hybrid product strategist and tech lead who combines product thinking (Marty Cagan, Lean Startup) with technical architecture expertise (WBS, CPM, ADRs) to break down features, manage dependencies, and guide implementation ordering
**Triggers:** Direct invocation for feature breakdown, technical planning, PRD review, or strategy advice
**Outputs:** PRD improvements, implementation plans with WBS and dependencies, ADRs, feasibility assessments, critical path analysis
**Tools:** Read, Write, Glob, Grep
**Key Features:**
- **Product thinking**: MoSCoW prioritization, MVP scoping, success metrics, outcomes over output
- **Technical breakdown**: Work Breakdown Structure (WBS), dependency mapping, Critical Path Method (CPM)
- **Architecture decisions**: ADRs for significant decisions, technical feasibility assessment
- **Implementation planning**: Task sequencing, risk management, technical debt allocation (10-20%)
- **Hybrid leadership**: Combines Google's servant leadership with Amazon's data-driven decision-making

### [Librarian](librarian.md)
**Status:** Active | **Color:** Teal
**Description:** Documentation consistency specialist who maintains the web of documents, enforces template compliance, updates cross-references, and validates completeness across 7+ document types
**Triggers:** Direct invocation for documentation audits or compliance checks
**Outputs:** Updated documents with compliance fixes, cross-reference updates, optional audit reports
**Tools:** Read, Write, Glob, Grep
**Key Features:**
- **Template validation**: Ensures all docs follow their templates (prd-template.md, plan-template.md, TEMPLATE.md)
- **Cross-reference maintenance**: Updates all references when files rename/move, verifies link integrity
- **Completeness checks**: Validates frontmatter, required sections, timestamp formats
- **Index maintenance**: Updates README.md files and hub docs (connections.md, CLAUDE.md)

## TDD Agents

Context-isolated agents for Test-Driven Development. Each phase runs in a clean 200k context window.

### [TDD Test Writer](tdd-test-writer.md)
**Status:** Active | **Color:** Red
**Description:** Writes failing tests for TDD RED phase. Converts test stubs to real failing tests with clean context isolation from implementation.
**Triggers:** Invoked by tdd-red-green-refactor skill during `/build`
**Outputs:** Updated test files with real assertions
**Tools:** Read, Glob, Grep, Write, Edit, Bash
**Key Features:**
- **Context isolation**: Sees only PRD requirements, NOT implementation plans
- **Gate enforcement**: Returns only after verifying test FAILS
- **Behavior focus**: Tests verify behavior, not implementation details

### [TDD Implementer](tdd-implementer.md)
**Status:** Active | **Color:** Green
**Description:** Implements minimal code to pass failing tests in TDD GREEN phase. Sees only the test—no PRD, plan, or prior discussion.
**Triggers:** Invoked by tdd-red-green-refactor skill after RED phase
**Outputs:** Implementation files with minimal code to pass tests
**Tools:** Read, Glob, Grep, Write, Edit, Bash
**Key Features:**
- **Context isolation**: Sees ONLY the failing test
- **Minimal implementation**: Writes simplest code that passes
- **Gate enforcement**: Returns only after test PASSES

### [TDD Refactorer](tdd-refactorer.md)
**Status:** Active | **Color:** Blue
**Description:** Improves code quality in TDD REFACTOR phase while keeping all tests passing. Sees test + implementation.
**Triggers:** Invoked by tdd-red-green-refactor skill after all tests pass
**Outputs:** Improved implementation files (or "No refactoring needed")
**Tools:** Read, Glob, Grep, Write, Edit, Bash
**Key Features:**
- **One change at a time**: Makes incremental improvements
- **Gate enforcement**: Tests must STAY GREEN after each change
- **Knows when to stop**: Reports "No refactoring needed" if code is clean

## QA Agents

### [QA Reviewer](qa-reviewer.md)
**Status:** Active | **Color:** Red
**Description:** Security and quality reviewer with clean context. Runs Semgrep SAST (when available) then LLM analysis using sandwich method. Reads handover for context, performs OWASP security checks, validates TDD compliance, and escalates issues with two-tier model.
**Triggers:** Invoked by `/build` (automatic) or `/qa` (manual)
**Outputs:** `docs/qa/[scope]-YYYYMMDD.md` (via orchestrator)
**Tools:** Read, Glob, Grep, Bash (NO Write—review only)
**Key Features:**
- **SAST integration**: Semgrep static analysis with graceful degradation (sandwich method)
- **Context isolation**: Reads handover, NOT builder conversation
- **OWASP checklist**: Systematic security review with confidence scoring (≥80%)
- **Finding attribution**: Every finding tagged `[SAST]` or `[LLM]` with source
- **Two-tier escalation**: Tier 1 in report, Tier 2 escalates to human via AskUserQuestion
- **TDD validation**: Verifies test coverage and quality (10-item checklist including semantic validation)
- **Semantic validation**: AC coverage (#8), pyramid level placement (#9), anti-pattern detection (#10)

## Specialist Sub-Agents

**Dynamic domain experts** created via `/create-specialist` command.

### How to Create Specialists

```bash
/create-specialist Supabase           # Library-specific
/create-specialist PydanticAI narrow  # Explicit narrow scope
/create-specialist Database broad     # Category-wide
```

### Naming Convention

- **Filename:** `[library-name]-specialist.md` (kebab-case)
- **Examples:**
  - Supabase → `supabase-specialist.md`
  - PydanticAI → `pydantic-ai-specialist.md`
  - Next.js → `nextjs-specialist.md`

### How Specialists Are Used

Specialists are invoked as **subordinates** by other agents:

```
Task(
  subagent_type="general-purpose",
  description="Get [Library] expertise",
  prompt="You are the [Library] Specialist. [question]
  @.claude/agents/[library]-specialist.md"
)
```

## Agent Templates

### [TEMPLATE.md](TEMPLATE.md)
**Purpose:** Structural scaffold for all sub-agent definitions
**Sections:**
- YAML frontmatter (name, description, tools, status, color)
- Primary Objective
- Simplicity Principles
- Core Responsibilities
- Tools Access
- Output Files
- Workflow
- Quality Criteria
- Integration Points
- Guardrails

## Agent Design Principles

1. **Single Responsibility:** Each agent has ONE clear purpose
2. **Stateless Design:** Agents don't maintain session state
3. **Template Compliance:** All agents follow TEMPLATE.md structure
4. **Tool Minimalism:** Only essential tools in frontmatter
5. **Quality Gates:** Validation before completion
6. **Graceful Degradation:** Work without optional dependencies

## Workflow Orchestration

```
User Request
    ↓
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
Test Stubs Created
    ↓
/build FEAT-XXX
    ↓
┌─────────────────────────────────────┐
│ TDD ORCHESTRATION (isolated)        │
│                                     │
│ For each test stub:                 │
│   🔴 tdd-test-writer → FAILS        │
│   🟢 tdd-implementer → PASSES       │
│                                     │
│ After all pass:                     │
│   🔵 tdd-refactorer → CLEAN         │
└─────────────────────────────────────┘
    ↓
Handover Generated
    ↓
┌─────────────────────────────────────┐
│ QA REVIEW                           │
│ → qa-reviewer (clean context)       │
│ → Creates docs/qa/FEAT-XXX-*.md     │
│                                     │
│ APPROVED → /commit                  │
│ NEEDS_FIXES → iterate or /debug     │
│ BLOCKED → escalate to human         │
└─────────────────────────────────────┘
    ↓
/commit (with QA gate)

Bug Discovered (Production or Development):
    ↓
/debug [issue-description]
    ↓
┌─────────────────────────────────────┐
│ DEBUG WORKFLOW                      │
│ → Phase 0: Classify & load context  │
│ → Phase 1: Investigate & diagnose   │
│ → Phase 2: Root cause analysis      │
│ → Phase 3: Solution design          │
│ → Phase 4: Implement with test      │
│ → Phase 5: Validate fix             │
│ → Phase 6: Document & prepare       │
│                                     │
│ Coordinates with:                   │
│ → researcher (unknown tech)         │
│ → challenger (complex fixes)        │
│ → qa-reviewer (security validation) │
│ → test-strategy (test routing)      │
└─────────────────────────────────────┘
    ↓
Debug Report + Regression Test
    ↓
/commit
```

## Tool Access by Agent

| Agent | Read | Write | Glob | Grep | Bash | WebSearch | Task |
|-------|------|-------|------|------|------|-----------|------|
| Researcher | ✅ | ✅ | ✅ | - | - | ✅ | ✅ |
| Challenger | ✅ | - | ✅ | ✅ | - | - | - |
| First Principles Thinker | ✅ | - | - | - | - | ✅ | - |
| Specialist Creator | ✅ | ✅ | - | - | - | ✅ | - |
| Prompt Specialist | ✅ | ✅ | ✅ | ✅ | - | ✅ | ✅ |
| N8N Specialist | ✅ | ✅ | - | - | - | ✅ | - |
| Product-Engineering Lead | ✅ | ✅ | ✅ | ✅ | - | - | - |
| Librarian | ✅ | ✅ | ✅ | ✅ | - | - | - |
| **TDD Test Writer** | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| **TDD Implementer** | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| **TDD Refactorer** | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| **QA Reviewer** | ✅ | - | ✅ | ✅ | ✅ | - | - |

## Related Documentation

- [CLAUDE.md](../../CLAUDE.md) - Main project instructions
- [PROJECT.md](../../PROJECT.md) - Project context and roadmap
- [Slash Commands](../commands/) - Workflow command definitions
- [Test Strategy Skill](../skills/test-strategy/SKILL.md) - Decision tree for test pyramid levels

---

**Note:** This index should be updated when adding/removing sub-agents.
