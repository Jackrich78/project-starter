# Project Starter

Lean agent harness template for AI-assisted development. New project? Start with [docs/guides/getting-started.md](docs/guides/getting-started.md).

## Governing documents (orient here first)

<!-- CUSTOMIZE: /setup writes one row per doc it generates; /prime and the context-priming skill load them by tier. Keep it current when a governing doc is added. -->

| Document | What it's for | Load |
|---|---|---|
| `PROJECT.md` | current state + roadmap | orient (all modes) |
| `DECISIONS.md` | index + the *why* behind every call; superseded entries archived | index always; full entries on-demand |

## Quick Start

```bash
npm ci && npm test   # install and run all tests (works on a fresh clone)
```

## Agents

Specialists live in `.claude/agents/` (descriptions auto-load from frontmatter; index: `.claude/agents/README.md`). Which agent runs at which step: see Lifecycle.

## Commands

Lifecycle commands are in the Lifecycle table. Others: `/setup [docs path]` (one-time init) · `/prime [mode]` (load context) · `/qa [target]` (standalone review: file, directory, feature or sweep) · `/handover` · `/debug [issue]` · `/logs` · `/create-specialist [lib]` · `/update-docs` · `/sync [target]`. Details: `.claude/commands/`.

## Lifecycle

The feature path, from idea to merge. A GitHub issue follows Issue process instead.

| Step | Command | Who | Output |
|---|---|---|---|
| Spec | `/explore [topic]` (researcher, challenger, `prd-consistency-sim`) | agent + owner | `docs/features/FEAT-XXX_slug/prd.md` |
| Plan | `/blueprint FEAT-XXX` (challenger) | agent; owner approves | `plan.md`, test stubs |
| Build | `/build FEAT-XXX`: tdd-test-writer → tdd-implementer → tdd-refactorer → qa-reviewer | agent | code, tests, `handover.md`, QA verdict |
| Ship | `/commit`: QA gate, commit, push; PR optional | agent + owner | commit / PR |
| Merge | — | owner | |
| Learn | `/retro`: agile-coach → owner → librarian | all | Hard-won rules, `.claude/skills/` |

**Review depth.** Code → `qa-reviewer` invoked directly on `git diff origin/main...HEAD` (`/qa` has no branch target; with no target it sees only `HEAD~1`), plus one challenger critique. Docs and prompts (`CLAUDE.md`, agents, skills, commands) → a cold read by `prd-consistency-sim` (brief it with the changed files in place of a PRD), which follows the changed text with no context and reports where it would misread or hesitate. Mixed → both.

## Key Files

`docs/features/FEAT-XXX_slug/` per-feature prd, plan, handover · `docs/qa/` QA reports · `stacks/` deployment scaffolding (copy to root to use) · `.github/tests/` scaffold tests (extend or delete) · `test/` your tests (`unit/`, `integration/`, `e2e/`) · `.claude/logs/agent.db` session tracking (`/logs`).

## Principles

**Reduce** context, load on demand · **Offload** specialised work to sub-agents · **Isolate** side effects, fail gracefully.

## Development Standards (This Project)

- **TDD with isolation**: `/build` runs RED-GREEN-REFACTOR in separate sub-agents — the test writer sees only the PRD, the implementer only the tests, the refactorer tests + code.
- **QA gate**: security issues from `/build` or `/qa` block `/commit` until resolved.
- **Outcomes over outputs**: features solve user problems, not just ship code.
- **Spike before commit**: for an uncertain approach use the spike skill (it creates `spikes/`); extract learnings to `docs/`.

## Issue process

A label on the issue is its state; "the owner" is the human who runs the repo.

| State | Meaning | Who moves it |
|---|---|---|
| (no state label) | Not looked at yet | Agents leave it alone |
| `needs-plan` | The owner wants a plan | Agent posts a plan comment, swaps to `needs-info` |
| `needs-info` | The owner's turn | Owner answers, then relabels `needs-plan` for a new plan, or approves: adds `ready-for-agent`, removes `needs-info` |
| `ready-for-agent` | Newest plan approved | Agent builds it (below), swaps to `ready-for-human` |
| `ready-for-human` | A PR awaits review | Owner merges, or comments and relabels the issue `ready-for-agent` to send it back |

**On `ready-for-agent`:** build test-first on an `issue-N-<slug>` branch, review per Review depth, commit, push, open a PR with `Closes #N`. Not `/commit` (it waits for the owner; use it only when the owner is present). A `BLOCKED` review verdict stops the push: treat the issue as stuck (Rules). Proof per Build loop; docs-only changes skip test-first.

**Plans.** A comment whose second line is exactly `**Plan vK**` (first line free), numbered up from v1. It opens with three lines — what changes for you, why it's worth it, scope — then files, proof, and numbered questions or "No questions". Approval counts only if `ready-for-agent` was added after the newest plan (check the issue timeline); otherwise the issue is stuck.

**Rules.**
- Only labels on the issue carry state, never comment text: the owner and agents may post from the same account.
- Only the owner adds `ready-for-agent` or removes `needs-info`. Agents never push to the base branch.
- One issue per run; the agent assigns itself when it starts. A stuck or failing agent pushes any work to its issue branch, comments the question or failure, swaps its state label for `needs-info`, and unassigns itself.

### Build loop

<!-- CUSTOMIZE: the values the build loop reads for this repo. -->
- **Test command:** `npm ci && npm test`
- **Base branch:** `main`
- **Proof of a change:** fenced test-command output in the PR
- **Tracker:** GitHub Issues on this repo

## Context Rules

- **Web research**: always through the `researcher` agent, never on the main thread.
- **QA context**: `qa-reviewer` reads `docs/features/FEAT-XXX/handover.md`, never the builder conversation.

## Model Defaults

Expensive models where judgement gates shipping, cheap ones for retrieval. Set per agent with `model:` in its frontmatter (e.g. `challenger` on `sonnet` for low-stakes projects).

| Tier | When | Agents (as on disk) |
|---|---|---|
| `opus` | review that gates whether work ships | challenger, qa-reviewer |
| `sonnet` | workhorse: planning, writing, coding | agile-coach, first-principles-thinker, librarian, n8n-specialist, prd-consistency-sim, prompt-specialist, specialist-creator, tdd-*, tech-product-lead |
| `haiku` | retrieval and lookups | researcher |

## Agent Learning Loop

Agile Coach (read-only) proposes patterns backed by ≥2 converging sources or one piece of objective evidence (commit, QA finding) → the owner approves each item → Librarian applies them with `Edit` only, never `Write`. Proposals may target `docs/system/`, `docs/guides/`, `CLAUDE.md § Hard-won rules`, `memory/agents/*.md` and `.claude/agents/`; never `src/`, database schema, test fixtures or CI.

## Hard-won rules

Extracted from retros via the Agent Learning Loop.

1. **Private-to-public ports need an adversarial public-readiness pass.** ACs don't catch leaked names or a `--dry-run` that still writes: run a blocking grep for private identifiers (zero hits), audit each ported script's side effects whatever its flags claim, and hold the bar at "public-ready", not "passes the ACs".
2. **Optional runtimes never break the primary test command.** `npm test` exits 0 with a notice when a secondary runtime (e.g. Python) is missing — a bridge script checks first; CI runs the full suite.
3. **Sync manifests are flag-derived, not hand-kept.** Mark canonical files `template-owned: true` in frontmatter and validate both ways in CI: every flagged file is in the manifest, every entry resolves to a file.
4. **Check "does this already exist?" before a differentiation thesis**, not mid-build; reword the claim before it ships.
5. **Spike the one load-bearing unknown in parallel with planning**, never only after it.
6. **Don't re-litigate settled decisions** — read the decision log first; reopen only when new evidence trips the revisit clause.
7. **Name hard constraints and core design tensions at the start of a design round**, so they don't surface late as detours.
8. **Every feature folder gets a `README.md` index from day one.** (a) `docs/features/FEAT-XXX/README.md` maps each file to purpose + status + where it was promoted; (b) drafts carry a `DRAFT-` prefix and a `STATUS:` banner; (c) canonical outputs live at their promoted location — the folder is the working record, not the source of truth; (d) keep the index current (Librarian / `/update-docs`).
9. **Confidentiality tooling must not leak what it protects.** Before first publish, audit gate pattern lists, waivers, provenance notes and gate-script comments for the content they guard.
10. **Leak gates scan filenames and match case-insensitively from day one.**
