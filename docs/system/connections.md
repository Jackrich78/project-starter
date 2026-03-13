---
updated: 2026-03-09T00:00:00Z
---

# File Connections Map

**Updated:** 2026-03-09T00:00:00Z
**Purpose:** Visual reference of how project files interlink

---

## Context Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ENTRY POINTS                                    │
│                                                                              │
│     README.md ─────────────────┐                                            │
│     (user entry)               │                                            │
│                                ▼                                            │
│                           CLAUDE.md ◄──────── (loaded every session)        │
│                           (startup)                                         │
│                                │                                            │
│                                ▼                                            │
│                          PROJECT.md                                         │
│                         (on-demand)                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
┌─────────────────┐   ┌─────────────────────┐   ┌─────────────────┐
│  .claude/       │   │  docs/              │   │  docs/features/ │
│                 │   │                     │   │                 │
│ ┌─────────────┐ │   │ ┌─────────────────┐ │   │  FEAT-XXX/      │
│ │ agents/     │ │   │ │ system/         │ │   │  ├── README.md  │
│ │ ├─README.md │◄┼───┼─┤ ├─architecture  │ │   │  ├── prd.md     │
│ │ ├─TEMPLATE  │ │   │ │ ├─observability │ │   │  └── plan.md    │
│ │ ├─researcher│◄┼───┼─┤ ├─integrations  │ │   │                 │
│ │ ├─challenger│ │   │ │ └─connections   │ │   └─────────────────┘
│ │ ├─1st-princ │ │   │ └─────────────────┘ │            ▲
│ │ ├─specialist│ │   │                     │            │
│ │ ├─prompt-sp │ │   │ ┌─────────────────┐ │            │
│ │ ├─n8n-spec  │ │   │ │ templates/      │ │            │
│ │ ├─qa-review │ │   │ │ ├─prd-template  │─┼────────────┘
│ │ ├─librarian │ │   │ │ ├─plan-template │ │
│ │ ├─tdd-*     │ │   │ │ ├─readme-templ  │ │
│ │ └─tech-prod │ │   │ │ ├─research-tmpl │ │
│ └─────────────┘ │   │ │ └─qa-report-tmpl│ │
│ ┌─────────────┐ │   │ └─────────────────┘ │
│ │ commands/   │ │   │                     │
│ │ ├─explore ──┼─┼───┼─────────────────────┼─► creates PRD
│ │ ├─blueprint ┼─┼───┼─────────────────────┼─► creates plan.md
│ │ ├─build ────┼─┼───┼─────────────────────┼─► creates src/, test/, handover
│ │ ├─qa        │ │   │                     │
│ │ ├─commit    │ │   │                     │
│ │ ├─handover  │ │   │                     │
│ │ ├─prime     │ │   │                     │
│ │ ├─retro ────┼─┼───┼──► .claude/skills/  │
│ │ ├─logs      │ │   │                     │
│ │ ├─create-sp │ │   │                     │
│ │ ├─debug ────┼─┼───┼─────────────────────┼─► debug report + regression test
│ │ └─update-doc│ │   │                     │
│ └─────────────┘ │   │ ┌─────────────────┐ │
│                 │   │ │ README.md       │ │
│ ┌─────────────┐ │   │ │ (index)         │ │
│ │ hooks/      │ │   │ └─────────────────┘ │
│ │ ├─pre_tool  │ │   │                     │
│ │ ├─post_tool │ │   └─────────────────────┘
│ │ ├─pre_comp  │ │
│ │ ├─stop      │ │
│ │ └─send_evt  │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │ logs/       │ │
│ │ └─agent.db  │◄┼─── send_event.py writes here
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │ skills/     │◄┼─── /retro writes here
│ │ └─*.md      │ │
│ └─────────────┘ │
└─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              STACKS (ADDITIVE)                              │
│                                                                              │
│  stacks/                                                                     │
│  ├── README.md ─────────────── Usage + contribution guide                   │
│  └── cloudflare/                                                            │
│      ├── README.md ─────────── Setup instructions                           │
│      ├── .claude/agents/ ───── Stack-specific specialists                   │
│      ├── src/ ──────────────── Boilerplate code                             │
│      ├── wrangler.toml ─────── Platform config                              │
│      └── package.json ──────── Stack dependencies                           │
│                                                                              │
│  Usage: Copy desired stack files to root, then delete stacks/               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Hub Files

Files with the most connections (high centrality):

| File | Incoming | Outgoing | Role |
|------|----------|----------|------|
| `CLAUDE.md` | 6 | 0 | Startup context (no @-refs) |
| `docs/system/architecture.md` | 4 | 4 | Core technical reference (+ 2 modules) |
| `.claude/agents/README.md` | 3 | 12 | Agent index |
| `PROJECT.md` | 4 | 0 | State/roadmap |
| `README.md` | 2 | 10+ | External entry |
| `docs/qa/` | N | 0 | QA report storage (referenced by build.md, qa.md, qa-reviewer.md) |

---

## Command → Agent Flow

```
/explore ──────► researcher (optional)
                     │
                     ▼
                 (optional) challenger (Step 5.5 PRD self-critique)
                     │
                     ▼
/blueprint ─────► researcher (optional) + challenger (required)
                     │
                     ├──► consults: test-strategy skill (4-value routing)
                     └──► annotates test stubs with @test-approach: tdd|component-test|integration|e2e
                              │
                              ▼
                 (ready for /build)
                     │
                     ▼
/build ─────────► Phase 0: Discover & route by annotation
                     │
                     ├──► @test-approach: tdd ──────► Phases 1-3 (TDD ORCHESTRATION)
                     │                                  │
                     │                                  ├──► tdd-test-writer (RED)
                     │                                  │         │
                     │                                  │         ▼
                     │                                  ├──► tdd-implementer (GREEN)
                     │                                  │         │
                     │                                  │         ▼ (repeat for each test)
                     │                                  │
                     │                                  └──► tdd-refactorer (REFACTOR, after all pass)
                     │
                     └──► @test-approach: component-test|integration|e2e ──► Phase 3B (inline testing)
                              │
                              ▼
                     handover generated (Phase 4)
                              │
                              ▼
                     qa-reviewer (Phase 5: SAST + LLM sandwich + semantic validation)
                              │
                              ├──► SAST scan (Semgrep with graceful degradation)
                              ├──► LLM review (OWASP checklist, confidence ≥80%)
                              └──► TDD Compliance (#1-#7 standard + #8-#10 semantic validation)
                                    │
                                    ├──► #8: AC Coverage (grep for AC references)
                                    ├──► #9: Pyramid Level Placement (validate directory)
                                    └──► #10: Anti-patterns (detect quality issues)
                              │
                              ▼
                     docs/qa/FEAT-XXX-*.md (Phase 6)
                              │
                              ▼
/commit ────────► (checks QA gate first)

/qa ───────────► qa-reviewer (SAST + LLM sandwich + semantic validation)
                     │
                     ├──► SAST scan (Semgrep with graceful degradation)
                     ├──► LLM review (OWASP checklist, confidence ≥80%)
                     └──► TDD Compliance (#1-#7 standard + #8-#10 semantic validation)
                     │
                     ▼
                 docs/qa/[target]-*.md

/create-specialist ──► specialist-creator
/retro ────────────► (main agent) ──► .claude/skills/
    │
    └─ feedback ──► librarian (for doc operations)
/prime ────────────► mode-aware: reads architecture.md + modules per mode
/logs ─────────────► queries .claude/logs/agent.db (events table)
/handover ─────────► writes docs/features/FEAT-XXX/handover.md
/debug ────────────► researcher + challenger + qa-reviewer (systematic bug investigation)
/update-docs ──────► (main agent) ──► updates doc index + cross-references
```

---

## Context Loading Order

When Claude starts a session:

```
1. CLAUDE.md             (~30 lines, always loaded)
2. /prime [mode]         → mode-aware loading:
   - bare:   git state + feature list only
   - think:  architecture.md + PROJECT.md
   - build:  architecture.md + architecture-tdd.md + architecture-qa.md + feature files
   - review: architecture.md + architecture-qa.md + feature files (optional)
   - create: architecture.md + PROJECT.md
3. docs/features/*       (when working on specific feature)
4. .claude/skills/*      (when relevant pattern exists)
```

---

## File Reference Details

### Root Files

**CLAUDE.md** (startup)
- References: `.claude/agents/README.md` (pointer only, no longer @-loaded)
- Referenced by: docs/README.md, agents/README.md, architecture.md

**PROJECT.md** (roadmap)
- References: None
- Referenced by: docs/README.md, agents/README.md, architecture.md

**README.md** (external entry)
- References: docs/guides/getting-started.md, docs/system/architecture.md, docs/guides/commands-reference.md, docs/guides/skills-reference.md, docs/system/observability.md, docs/system/cicd-workflow.md, docs/system/diagrams/*.png, .claude/agents/README.md, stacks/README.md, LICENSE
- Referenced by: (no internal doc links to root README.md; it is the public entry point)

### System Documentation

**docs/system/architecture.md** (core only — TDD/QA moved to modules)
- References: TEMPLATE.md, observability.md, integrations.md, PROJECT.md, CLAUDE.md, architecture-tdd.md, architecture-qa.md
- Referenced by: README.md, docs/README.md

**docs/system/architecture-tdd.md** (module)
- References: architecture.md, architecture-qa.md, TDD skill
- Referenced by: architecture.md

**docs/system/architecture-qa.md** (module)
- References: architecture.md, architecture-tdd.md, qa-reviewer.md, qa/README.md
- Referenced by: architecture.md

**docs/system/observability.md**
- References: architecture.md, integrations.md
- Referenced by: README.md, docs/README.md, architecture.md

**docs/system/integrations.md**
- References: architecture.md, observability.md
- Referenced by: docs/README.md, architecture.md, researcher.md

**docs/guides/project-starter-explainer.pptx** (teaching deck)
- What it is: 17-slide explainer presentation covering the Project Starter system — commands, agents, TDD pipeline, context isolation, skills, and session continuity. Intended for onboarding and sharing with new users.
- References: Concepts from architecture.md, commands-reference.md, skills-reference.md, README.md (narrative arc mirrors README structure)
- Referenced by: (none — public asset)
- Built by: docs/system/pptx-workspace/ (see below)

**docs/system/pptx-workspace/** (HTML source + build script)
- What it is: Source files for project-starter-explainer.pptx. Contains 17 HTML slide files (slide01.html – slide17.html) and a Node.js build script (build-pptx.cjs) that assembles them into the .pptx via the html2pptx pipeline.
- References: .claude/skills/pptx/ (html2pptx.cjs pipeline), project-starter-explainer.pptx (output)
- Referenced by: (none — build tooling)

**docs/system/cicd-workflow.md**
- References: architecture.md
- Referenced by: README.md

**docs/guides/commands-reference.md**
- References: (none)
- Referenced by: README.md, getting-started.md

**docs/guides/skills-reference.md**
- References: (none)
- Referenced by: README.md, getting-started.md

**docs/guides/working-with-claude.md**
- References: architecture.md, getting-started.md
- Referenced by: getting-started.md

**docs/guides/two-remote-sync.md**
- References: (none)
- Referenced by: (none — operational guide for maintainers)

### Agents

**agents/README.md** (index)
- References: All 12 agents, TEMPLATE.md, CLAUDE.md, PROJECT.md, commands/
- Referenced by: CLAUDE.md, README.md

**agents/researcher.md**
- References: specialist patterns, integrations.md
- Referenced by: agents/README.md, explore.md, blueprint.md

**agents/challenger.md**
- References: None
- Referenced by: agents/README.md, blueprint.md

**agents/qa-reviewer.md**
- References: qa-report-template.md, qa/README.md, build.md, qa.md, handover.md, test-strategy skill
- Referenced by: agents/README.md, architecture.md, build.md, qa.md
- Enhanced TDD Compliance: #8 AC Coverage, #9 Pyramid Level Placement, #10 Anti-patterns

### Commands

**commands/explore.md**
- Creates: docs/features/FEAT-XXX/prd.md
- Invokes: researcher agent

**commands/blueprint.md**
- Reads: prd.md, PROJECT.md, test-strategy skill
- Creates: plan.md with @test-approach annotations, README.md
- Invokes: researcher, challenger agents
- Uses: docs/templates/plan-template.md
- Test stubs annotated with: @test-approach: tdd|component-test|integration|e2e
- Stub placement by directory: test/unit/, test/component/, test/integration/, test/e2e/

**commands/build.md**
- Reads: plan.md, prd.md, test-strategy skill
- Creates/modifies: src/, test/, handover.md, docs/qa/FEAT-XXX-*.md
- Invokes: tdd-test-writer, tdd-implementer, tdd-refactorer, qa-reviewer
- Phases:
  - Phase 0: Discover & route by @test-approach annotation
  - Phases 1-3: TDD subagents (RED-GREEN-REFACTOR)
  - Phase 3B: Inline testing (component-test, integration, e2e)
  - Phase 4: Generate handover.md
  - Phase 5: QA review (SAST + LLM + semantic validation)
  - Phase 6: Create QA report

**commands/qa.md**
- Invokes: qa-reviewer agent
- Creates: docs/qa/[target]-*.md

**commands/retro.md**
- Reads: .claude/logs/sessions/
- Creates: .claude/skills/*.md

**commands/prime.md** (mode-aware)
- Reads: docs/system/architecture.md (all modes except bare), architecture-tdd.md (build), architecture-qa.md (build+review), PROJECT.md (think+create), docs/features/ (when FEAT-ID)

### Feature Documentation

**docs/features/FEAT-XXX/README.md**
- References: prd.md, plan.md, research-*.md, handover.md, system docs
- Referenced by: docs/README.md

**docs/features/FEAT-XXX/prd.md**
- References: None (content only)
- Referenced by: README.md, plan.md, commands

**docs/features/FEAT-XXX/plan.md**
- References: prd.md, research-*.md
- Referenced by: README.md, build.md

**docs/features/FEAT-XXX/research-[topic]-[timestamp].md**
- Created by: Researcher agent during /explore or /blueprint
- Naming: `research-[topic]-YYYY-MM-DDTHH-MM-SSZ.md`
- References: External sources (cited with URLs)
- Referenced by: plan.md, README.md

---

## Cross-Reference Patterns

### Feature Development Flow
```
User Request
    │
    ▼
/explore [topic]
    │
    ├──► reads: PROJECT.md, existing code
    ├──► invokes: researcher agent
    └──► creates: docs/features/FEAT-XXX/prd.md
    │
    ▼
/blueprint FEAT-XXX
    │
    ├──► reads: prd.md, PROJECT.md
    ├──► uses: docs/templates/plan-template.md
    ├──► invokes: researcher, challenger agents
    └──► creates: plan.md, README.md
    │
    ▼
/build FEAT-XXX
    │
    ├──► reads: plan.md, prd.md
    ├──► Phase 0: discovers test stubs with @test-approach annotation
    ├──► routes by annotation:
    │         ├──► tdd → Phases 1-3 (TDD subagents)
    │         └──► component-test|integration|e2e → Phase 3B (inline testing)
    ├──► Phases 1-3: TDD ORCHESTRATION (tdd-test-writer → tdd-implementer → tdd-refactorer)
    ├──► Phase 3B: inline testing for non-TDD approaches
    ├──► creates: src/, test/
    ├──► Phase 4: generates handover.md
    ├──► Phase 5: invokes qa-reviewer (SAST + LLM sandwich + semantic validation)
    └──► Phase 6: creates docs/qa/FEAT-XXX-*.md
    │
    ▼
/commit
    │
    └──► git workflow (checks QA gate)
```

### Agent Invocation Pattern
```
Main Agent (user-facing)
    │
    ├──► Task(researcher) ──► WebSearch
    │
    ├──► Task(challenger) ──► Review feedback
    │
    ├──► Task(first-principles-thinker) ──► Deep reasoning
    │
    ├──► Task(specialist-creator) ──► New agent file
    │
    ├──► Task(prompt-specialist) ──► Optimized prompts
    │
    ├──► Task(tech-product-lead) ──► Product + tech strategy
    │
    ├──► Task(qa-reviewer) ──► SAST scan + LLM review
    │
    ├──► Task(tdd-test-writer) ──► Failing tests (RED)
    │
    ├──► Task(tdd-implementer) ──► Minimal implementation (GREEN)
    │
    ├──► Task(tdd-refactorer) ──► Code quality (REFACTOR)
    │
    ├──► Task(librarian) ──► Documentation consistency
    │
    ├──► Skill(test-strategy) ──► Test approach routing
    │
    └──► Task([library]-specialist) ──► Domain expertise
```

---

## Statistics

| Category | Count |
|----------|-------|
| Root files | 4 |
| System docs | 7 (architecture, architecture-tdd, architecture-qa, cicd-workflow, connections, integrations, observability) |
| Guides | 9 (getting-started, working-with-claude, commands-reference, skills-reference, two-remote-sync, project-starter-explainer.pptx, mcp-configuration, upstream-workflow-contributions, creating-branded-presentations) |
| Agent definitions | 12 + TEMPLATE + README |
| Command definitions | 13 |
| Skills | 21 |
| Templates | 5 |

---

## Consistency Maintenance

### How /retro Maintains System Consistency

The `/retro feedback` mode uses Claude Code best practices to propagate changes across interconnected files:

#### Component Update Process

**1. Discovery Phase (Read-Only)**
```
User: /retro feedback agent X "rename to Y"
    │
    ▼
Read component file
    │
    ▼
Grep codebase for references (.claude/, docs/)
    │
    ▼
Build dependency graph:
- Direct: [text](X.md) links
- Indirect: Task(subagent_type="X")
- Documentation: handover mentions, index entries
```

**2. Update Phase (Atomic Edits)**
```
Dependency order:
1. File rename (bash mv)
2. Component file itself (Edit tool)
3. Index files (README.md)
4. Reference files (handovers, plans)
5. Cross-references (other agents, commands)
    │
    ▼
Each edit verified with Grep
```

**3. Verification Phase**
```
Grep for old references → should return 0 results
Validate markdown links → all resolve correctly
Check invocation paths → agent/command still accessible
    │
    ▼
Generate report showing files modified + verification status
```

#### Update Propagation Rules

**When an agent file changes:**
- Update `.claude/agents/README.md` (index entry, tool access table)
- Search `docs/features/*/handover.md` for mentions
- Search `.claude/commands/*.md` for invocation references
- Search other agent files for integration points
- Update `docs/system/connections.md` diagrams if workflow changes

**When a command file changes:**
- Check if listed in `CLAUDE.md` command reference
- Update `docs/system/connections.md` workflow diagrams
- Search agent files for command trigger references
- Update related template documentation

**When a template file changes:**
- Search command files for template usage
- Update `docs/system/architecture.md` if structure changes
- Check feature files for template compliance

#### Claude Code Best Practices Applied

1. **Tool Selection:**
   - Grep (not bash grep) for finding references
   - Glob (not bash find) for pattern matching
   - Read (not cat) for file reading
   - Edit (not sed) for atomic string replacement

2. **Workflow Pattern:**
   - Read → Grep → Plan → Edit → Verify
   - No assumptions - always discover references first
   - Atomic edits - one change per Edit call
   - Verify after each critical change

3. **Dependency Management:**
   - Update in topological order (dependencies first)
   - Never leave broken references during update
   - Validate all changes before completion

#### Consistency Checklist

Before completing a `/retro feedback` operation, verify:
- All references to old name updated
- Grep returns 0 results for old reference
- Markdown links resolve correctly
- Index files updated (README.md)
- Related documentation updated (handovers, plans)
- Frontmatter timestamps updated
- No broken agent/command invocation paths

---

## See Also

- [architecture.md](architecture.md) - System structure and patterns
- [observability.md](observability.md) - Logging and debugging
- [integrations.md](integrations.md) - External tools
- [getting-started.md](../guides/getting-started.md) - Setup instructions
- [.claude/commands/retro.md](../../.claude/commands/retro.md) - /retro command documentation
- [.claude/commands/build.md](../../.claude/commands/build.md) - /build TDD workflow
- [.claude/skills/test-strategy/SKILL.md](../../.claude/skills/test-strategy/SKILL.md) - Test approach routing
