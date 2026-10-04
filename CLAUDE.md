# Project Starter — operating contract

<!-- CUSTOMIZE: replace this line with one sentence on what this project is and for whom. -->
A Claude Code harness: an orchestrator main thread that delegates to sub-agents, tracks work in GitHub Issues, and keeps what it learns in a linted wiki. **Not all work is code** — documents, research and decisions follow the same discover → spec → build → prove arc. Everything else is a pointer; one home per fact.

## Governing documents

| Document | What it is for | Load |
|---|---|---|
| `PROJECT.md` | vision · principles · current state · roadmap themes (`#N` links) | every session |
| `docs/index.md` | wiki entry point (progressive disclosure) | entering an unfamiliar area |
| `docs/decisions.md` | append-only decision log, rejected options included | before re-opening a settled question |
| `docs/system/issue-flow.md` | how work lives in GitHub Issues: states, labels, pickup, close-out | before touching an issue |
| `docs/reference/claude-code.md` | official Claude Code doc links — **ask `claude-code-guide` before changing agents, hooks, settings or skill frontmatter** | before harness changes |

## Orchestrator contract

1. **Reduce · Offload · Isolate.** The main thread is the bottleneck: reads, greps, scoping and drafting go to sub-agents; pass pointers, not payloads; contain side effects.
2. **Sub-agent output is a claim, not a fact — and the brief decides whether the claim *can* be true.** Give an agent the live state it reasons about, or label its output unverified. Verify on disk before acting; a one-turn ack means the work was not done.
3. **State the independence tier with every multi-agent result.** Tier 1 prompt-only (agreement = framing coherence) · Tier 2 tool access (framing is yours, data is not) · Tier 3 independent inputs (agreement is evidence).
4. **Spawn unnamed for one-shot work; name an agent only to continue it**, and end a named brief with "SendMessage your report before stopping".
5. **Verify before disbelieving.** After compaction, "I have never seen this" is not "this did not happen": `/recover-session` finds the transcript before you call anything invented.
6. **Two human gates:** the human approves what to build (design note, then the ticket breakdown) and tests what was built (the PR); between them decide and report. **Ask first** for anything irreversible, pushed to the default branch, or outward-facing beyond the issue's own comments, branch and PR.

## The spine

Work lives in GitHub Issues; the issue is the spec (`docs/system/issue-flow.md`). `/explore` → `/blueprint` → `to-tickets` → `/build` (one sub-issue: `work-issue` + TDD with isolated sub-agents) → `/qa --issue N` → `/commit` (`Closes #N` on the commit in `direct` mode, on the PR in `pr` mode) → `/session-winddown`. A `BLOCKED SECURITY` verdict blocks `/commit` (step 0 reads the QA verdict comment on the issue). **Size in main-thread tokens, not hours:** `issue-flow.md` § Sizing.

## Workflow

- Integration mode: `pr` <!-- pr | direct — set by /setup. pr = branch per issue + PR carrying "Closes #N"; direct = commit to the default branch -->
- Agent signature on issues and comments: `> *Posted by the assistant.*` <!-- "" to disable -->
- Areas (labels): <!-- CUSTOMIZE: area:core, area:ops … -->

## Delegation & model policy

Opus by role, not "to be safe": plan and judge on Opus, implement on Sonnet, retrieve on Haiku. A role not listed runs on Sonnet. Agent frontmatter must match these tables (`tests/harness/test_model_tier_table.py`). Web research never runs on the main thread.

| Role | Model | Effort |
|---|---|---|
| Main thread (orchestrator) | as set | as set |
| Planning, design, review, judgement (challenger, first-principles-thinker, tech-product-lead, qa-reviewer, prd-consistency-sim) | opus | high |
| Implementation and default delegation (tdd-test-writer, tdd-implementer, tdd-refactorer, librarian, drafter, agile-coach, prompt-specialist, persona-creator) | sonnet | medium |
| Research (researcher) | sonnet | low |
| Pure volume: retrieval, lookups, bulk rewrites | haiku | low |

| When you need… | Call | Model |
|---|---|---|
| external sources, library docs, prior art — memo returned, filed on the issue or as a wiki page (`docs/templates/research-memo.md`) | researcher | sonnet, effort low |
| a proposal checked before the human sees it, or any refute pass | challenger | opus |
| a problem reasoned from fundamentals, or a choice between options | first-principles-thinker | opus |
| a feature broken down and sequenced, or a roadmap proposed | tech-product-lead | opus |
| a cold read of a spec for gaps and silent assumptions | prd-consistency-sim | opus |
| QA on a build, or any security- or prod-relevant change | qa-reviewer | opus |
| a docs or wiki audit, cross-reference repair, surgical doc edits | librarian | sonnet |
| a document over one screen, or anything in the owner's voice | drafter (`MODE: internal` or `MODE: external-voice`) | sonnet |
| a process retro at wind-down | agile-coach | sonnet |
| a prompt generated or tightened | prompt-specialist | sonnet |
| a new persistent agent persona or library specialist | persona-creator | sonnet |
| how Claude Code itself behaves (hooks, frontmatter, settings) | claude-code-guide (built in) | as set |
| anything else | general-purpose | sonnet |

## Agent memory

Each agent keeps methods — never findings, verdicts or drafts — in `.claude/agent-memory/<name>/MEMORY.md`: one line per entry, `- YYYY-MM-DD · <method> · source: <file:line|commit:sha|url>`, hard cap 150 lines (`scripts/validate_agent_memory.py`, run by `/commit`). The TDD trio self-curates (`memory: project`). Every other agent reads its file via a line at the top of its prompt and ends its report with `## Proposed memory entries`; the orchestrator writes the accepted ones. Agents that ingest outside material (web, pasted text) never get the `memory:` flag. Mechanism: `docs/system/memory-systems.md`.

## Knowledge and decisions

- **The wiki is the context brain.** Reach for `docs/` before reasoning from memory; a fact you cannot cite to a page is a fact to go and check. A durable fact established in conversation lands on its page in that conversation. Routing: `docs/guides/knowledge-architecture.md`.
- **Log the decision in the turn it is made**, one line in `docs/decisions.md`, with the rejected option — code preserves what was built, never what was tried.
- **A wiki claim you observe to be false is fixed in that turn** — not noted, not queued, and not answered with a proposal for a new lint.
- No feature folders. Specs live on issues; what outlives the feature moves to the wiki at close-out.

## Security

- No credentials in code, logs or shell commands — the compaction salvage persists recent commands. **Never expand a secret into a printed position**, presence checks included: `[ -n "$TOKEN" ] && echo set`, never `${TOKEN:+yes}`.
- Assume every tracked file, commit message, branch name, issue and PR is world-readable: never copy names, paths or text from other projects into them.
- Read before write; Edit over Write; `git diff` after multi-section edits. Prefer deletion when adding and deleting both solve it.
- Deregister a hook in `settings.json` before deleting its file. A rule that failed twice in prose becomes a hook or a test.
- Every external action is observable; every change names its undo before it runs.

## Hard-won rules

1. **A test not in a CI lane does not exist.** Add the file to the workflow in the same commit; a local green in no lane enforces nothing.
2. **Optional runtimes never break the primary test command.** `npm test` degrades to a notice without Python; CI always runs the full suite.
3. **The memory read line goes at the top of the agent file.** Placed at the bottom, it was skipped every time.
4. **Find what exists before building.** An instruction that lives where nothing loads it never runs; a capability nobody points at gets rebuilt.

## Where things live

`.claude/agents/` sub-agent contracts (roster is harness-injected; `TEMPLATE.md` is the shape) · `.claude/skills/` every workflow, invoked as `/<name>` · `.claude/rules/` path-scoped conventions (testing, agents, skills, wiki, hooks) · `.claude/hooks/` enforcement (`.claude/hooks/README.md`) · `docs/system/` how the harness and the system work · `docs/guides/` practitioner how-tos · `tests/harness/` tests of the harness itself · `scripts/` validators and gates.

## Quick start

```bash
npm test                                   # harness tests (pytest when available)
gh issue list --label ready-for-agent      # the frontier
/setup                                     # first run: adapt the template, bootstrap GitHub
/prime                                     # every session: load context
```
