# Project Starter

Lean agent harness template for AI-assisted development.

> **New project?** See [docs/guides/getting-started.md](docs/guides/getting-started.md) for setup instructions.

## Governing documents (orient here first)

<!-- CUSTOMIZE: /setup fills this in with the project's real governing docs. These carry the *what/why* — read the right ones before proposing or building; don't re-litigate a settled decision unless its revisit clause fires. The portable `context-priming` skill (`.claude/skills/context-priming/`) and `/prime` key off this table, so keep it current when a new governing doc is added. This repo picked "Full governance" via `/setup`: `PROJECT.md` and `DECISIONS.md` are real files here; `PRINCIPLES.md` and `docs/ARCHITECTURE.md` are left in the table as the template's example rows and are NOT present in this repo (see `.claude/commands/setup.md` §2.7 for how "Full governance" would generate them) — remove or fill them in if this repo later adopts them. -->

| Document | What it's for | Load |
|---|---|---|
| `PROJECT.md` | current state + roadmap | orient (all modes) |
| `PRINCIPLES.md` | operating principles — each states what it *forbids* | orient (all modes) |
| `DECISIONS.md` | index + the *why* behind every call; superseded entries archived | index always; full entries on-demand |
| `docs/ARCHITECTURE.md` | design rationale | on-demand (build/review) |

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
- **Step 5.5 (post-PRD, pre-blueprint):** After `/explore` produces a PRD, always run the `prd-consistency-sim` agent (cold read) before `/blueprint`. It surfaces spec gaps and ambiguous assumptions in a single sub-agent call — far cheaper than discovering them mid-build.
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
- `/sync [target]` - Sync template hooks/commands to downstream projects
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

## Model Defaults

Three tiers govern which model runs each agent. The goal: expensive models where judgment is irreplaceable, cheap models for retrieval.

| Tier | Model | When to use | Example agents |
|------|-------|-------------|----------------|
| Opus | `opus` | Orchestrator + high-stakes review: any agent whose output directly gates whether work ships | `challenger`, `qa-reviewer` |
| Sonnet | `sonnet` | Workhorse — ~95% of agents: planning, writing, coding, research synthesis | `librarian`, `specialist-creator`, `tech-product-lead`, `tdd-*`, `agile-coach` |
| Haiku | `haiku` | Scout / retrieval: fast lookups, symbol resolution, grep-and-return tasks with no judgment required | narrow retrieval specialists only |

**Override at the call site** with `model: <tier>` in agent frontmatter when a small project wants cheaper review (e.g. set `challenger` to `sonnet` for low-stakes internal tooling).

## Agent Learning Loop

The harness supports an evidence-gated learning loop so per-feature retros compound into lasting CLAUDE.md improvements.

**Flow:** Agile Coach proposes → human approves → Librarian applies.

1. **Agile Coach** (read-only) cross-reads agent memory files and `git log` after a feature ships, identifies patterns with ≥2 converging sources or objective evidence, and emits a structured proposal.
2. **Human reviews** the proposal and approves, rejects, or edits individual items.
3. **Librarian** applies approved items via `Edit` only — never `Write`. It reads the target file first, makes surgical line changes, then runs `git diff --stat` to confirm <10% line-count delta.

**Coach scope boundary** — proposals may target:
- `docs/system/`, `docs/guides/` (process documentation)
- `CLAUDE.md § Hard-won rules` (this file)
- `memory/agents/*.md` (agent memory files)
- Agent prompt files in `.claude/agents/`

**Out of scope for Coach proposals:** `src/` code, database schema, test fixtures, CI configuration.

## Hard-won rules

Rules extracted from feature retros via the Agile Coach → human approval → Librarian pipeline.

1. **Porting from a private repo: adversarial public-readiness pass required.** Acceptance criteria verify functional correctness; they do not catch confidential leakage (real names, private repo identifiers) or security properties of ported scripts (e.g. a `--dry-run` flag that still writes). Before any private-to-public port ships: (1) run a blocking grep gate for private identifiers — zero hits required; (2) audit every ported script's side-effect contract independently of its claimed flags; (3) treat the bar as "genuinely public-ready," not "passes the ACs." _(from this template's own development retros.)_

2. **Optional runtimes must never break the primary test command.** When adding tests in a non-primary language to a polyglot template (e.g. Python pytest in a Node.js template), the primary test runner (`npm test`) MUST degrade gracefully when the secondary runtime is absent — exit 0 with a notice, never a hard failure. Use a bridge script that detects runtime availability before delegating. CI runs the full suite; local cloners without the optional runtime are unaffected. _(from this template's own development retros.)_

3. **Sync manifests must be flag-derived, not hand-maintained.** When a pipeline propagates a subset of files to downstream targets, a hand-maintained list silently drifts when files are added. Instead: mark canonical files with a `template-owned: true` (or equivalent) frontmatter flag; enforce bidirectionally — every flagged file must appear in the manifest, and every manifest entry must resolve to an existing file. The flag travels with the file and survives renames; the validator is CI-gated. One-directional checks are insufficient. _(from this template's own development retros.)_

4. **Run the "does this already exist?" competitive check before building a differentiation thesis, not after.** A named competitor that already ships the capability can invalidate the thesis; discovering it mid-build is expensive. Check first, reword the claim before it ships. _(from a downstream project retro.)_

5. **Spike the single load-bearing technical unknown in parallel with planning, never only after it.** Identify the one mechanism the story cannot survive without and validate it early — an entire plan can rest on an unverified mechanism. _(from a downstream project retro.)_

6. **Don't re-litigate settled decisions — read the decision log and principles doc first.** A settled decision is settled unless new evidence trips its revisit clause; recurring re-openings cost repeated rounds. _(from a downstream project retro.)_

7. **Name load-bearing constraints and first-class tensions up front.** State the hard constraints and the core design tensions (e.g. "watchability vs. credibility") at the start of a design round, so they aren't discovered late as detours. _(from a downstream project retro.)_

8. **Every feature folder gets a `README.md` index from the start; mark drafts and separate them from canonical outputs.** A flat folder of many undated, unmarked files becomes unnavigable — a reviewer (or future session) can't tell canonical from draft from superseded. Convention: (a) each `docs/features/FEAT-XXX/` has a `README.md` mapping every file to a one-line purpose + status + where it was promoted; (b) discussion drafts carry a `DRAFT-` prefix and a `STATUS:` banner; (c) canonical outputs live at their promoted location (root/`docs/`) — the feature folder is the *working record*, not the source of truth; (d) keep the index current as files land (the Librarian / `/update-docs` owns this). _(from a downstream project retro.)_

9. **Confidentiality tooling must not leak what it protects.** Any file whose job is to enforce or document a confidentiality boundary (gate pattern lists, waiver files, rule provenance notes, comments in gate scripts) must itself be audited for the category of content it guards before first publish — enforcement artifacts are exactly where leaks hide, because they're the last thing anyone treats as "content." _(v2.0.0 release retro, 2026-07-19.)_

10. **Leak-detection gates must scan filenames and run case-insensitively from day one.** Both are default-off in naive grep gates and both are real leak vectors (a private name in a filename; a capitalized token slipping past a lowercase pattern). _(v2.0.0 release retro, 2026-07-19.)_
