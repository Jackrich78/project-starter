# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.2] - 2026-10-04

### Added

- Two human gates (approve what to build, test what was built) with a same-session loop between them; token-based ticket sizing (main-thread tokens, not hours).
- pr mode commits, pushes and opens the PR without asking; README carries the opt-in snippet.
- Gate-2 hand-off to the human: How to test and Decided.
- Issue protocol section in `issue-flow.md`: one Ask block, signature on line 1.
- `human_input.py` surfaces human replies (incl. a second assistant's signature variant) in `/prime`, triage and wind-down.
- `/retro` harness mode; redacted `scripts/recall.py` transcript reader.
- Ticket template: Interface line; test-writer sees Interface.

### Changed

- QA fork posts its own verdict; human-only checks never block; recommend-one questions are asked yes/no.
- Sub-agent reports capped at 300 words; human reports ~5 lines.
- Hook: secret-file reader rule widened.

### Removed

- Fallback `qa-reviewer-prompt`; ticket template Sub-tasks section; hook `eval(` rule.

### Fixed

- Hook README matches the rule table.

## [3.0.1] - 2026-10-04

Back to the v2.0.1 balance. v3.0.0's enforcement layer cost more autonomy than it bought.

### Changed

- **Security hook** is v2.0.1's flat rule table again (156 lines, was 788), Bash-only, deny by JSON `permissionDecision`, plus five rules for risks seen in real sessions: `.env` reads, grep/rg of `.env` values, bare environment dumps, echo of secret-named variables, trailing force-push flags. Fixes v2's `rm -rf /private/tmp` and `| shasum` false positives; masks URL credentials and token-shaped runs in the block log. Capped at 170 lines by a test.
- **`settings.json`** sets no `permissions.defaultMode` (the owner's mode governs); the deny list keeps secret stores, Claude Code private state and irreversible remote actions only.
- **QA gate** is prose in `/commit` step 0, reading the verdict comment on the issue; no verdict file, no hook.
- **Spine skills are agent-invocable**: 15 workflow skills drop `disable-model-invocation`, so the agent runs build → QA → commit → wind-down without the human typing each step; 7 human-start skills keep it (#2).
- **Adoption fixes:** two-lane `npm test` (harness and project), `/setup` markers that can actually be met, `.claude/skills/build/` no longer gitignored, testing rules restated in the TDD briefs.

### Removed

- Leak gate (`scripts/leak_gate.sh`, waivers, pattern example), `scripts/coupling_lint.sh`, `scripts/adoption_check.py`, `scripts/recall.py`.
- Monthly `harness-health` workflow, its skill, the reference stamp and the session-start nudge.
- Opt-in observability: `send_event.py`, `agent.db`, `/logs`, `docs/system/observability.md` (issue #1).
- The `subagent_claim_check` hook (the rule stays in CLAUDE.md).

## [3.0.0] - 2026-10-02

Third iteration of the harness: an assistant harness that can also build code. Ported as mechanisms, never content, from the maintainer's private harness after a pre-write privacy and security audit.

### Changed

- **CLAUDE.md** is a 100-line operating contract (orchestrator contract, issue-based spine, two CI-parsed model tables, memory and decision rules, five hard-won rules). Path-scoped conventions moved to `.claude/rules/{testing,agents,skills,wiki,hooks}.md`.
- **Work lives in GitHub Issues.** The issue is the spec; a parent `feature` issue carries the design note, acceptance criteria, outcome test, validation and reversal; sub-issues are the plan. `docs/system/issue-flow.md` is the one home for states, labels, pickup protocol and the close-out comment. Integration mode `pr` (default) or `direct`, set in CLAUDE.md `## Workflow`.
- **Skills only.** Every workflow is `.claude/skills/<name>/SKILL.md`, invoked as `/<name>`; `.claude/commands/` is gone. Commands shrank from 300–700 lines each to skills under 150.
- **Agents** rewritten to one contract: memory block first, Stance on judgement agents, Failure Recovery with PASS / FAIL / ESCALATION, report ending in proposed memory entries. Opus by role (plan, judge), Sonnet to build and draft, Haiku for volume; `tests/harness/test_model_tier_table.py` fails on drift. `specialist-creator` became `persona-creator`; `drafter` added; `n8n-specialist` removed.
- **Per-agent memory** at `.claude/agent-memory/<agent>/MEMORY.md`: one-line methods, 150-line cap, validator run by `/commit`; `memory: project` only on the TDD trio. Replaces `memory/agents/`.
- **Wiki over `docs/`**: frontmatter `type` on every page, reserved `index.md`/`log.md`, 300-line cap, decay tiers, `scripts/wiki_lint.py` in CI, semantic `wiki-lint` skill. Decision log moved to `docs/decisions.md` (one line per decision, rejected option mandatory).
- **Security baseline**: `settings.json` rewritten with a read-only allow list and `defaultMode: default`; `pre_tool_use.py` blocks the exfiltration, credential-read, secret-expansion and destructive forms a security audit found bypassable, plus a QA gate that blocks commit/push on `BLOCKED SECURITY`; observability is opt-in and redacted; `scripts/leak_gate.sh` scans content, filenames, OOXML and `.gitignore` text case-insensitively; `scripts/coupling_lint.sh` catches private-product leftovers.
- **Security audit round 3** (independent clean-session audit before release): the deny hook now resolves wrapper prefixes, catches shells and interpreters fed from stdin/here-strings/heredocs, `php`/`lua`/`osascript`, shell functions and brace groups, `xargs` readers fed by directory listings, exec-capable `git config` keys, abbreviated push flags, history-rewriting git verbs, `rm -rf .git`, shell writes to hook/settings/leak-gate files, reads of Claude Code home state and the transcript directory, recursive grep over home, `npm` config flags that execute, `gh --jq env`, and the empty-argument tokenizer split. Edits of harness files through the Edit tool return `permissionDecision: ask`. `settings.json`: `npm test *` became `npm test -- *`; new deny entries for npm config flags, `git config remote.*|alias.*|core.*`, and `~/.claude` state files. `send_event.redact` covers key names with prefixes/suffixes, `-p`/`-u`/`--token` CLI forms, `Authorization: Basic|Token`, cookies, URL tokens and a dozen more vendor prefixes; `pre_compact` redacts before truncating and writes the salvage `0600`; `scripts/recall.py` redacts every printed line. `leak_gate.sh --history` also scans author, committer, message and added-file-name lines, binary diffs and merges; waiver output no longer prints pattern text; an invalid pattern fails the gate. Workflows pin every action by commit SHA, drop `persist-credentials`, pin pip ranges and run pytest directly. `to-tickets` is no longer model-invocable; `agile-coach` loses Bash; `/commit` accepts issue-comment verdicts only from owner/member/collaborator; `/setup` stages by path behind the leak gate; `setup_labels.py` targets this checkout's origin. NOTICE records the Apache-2.0 skill-creator and the two further Pocock adaptations.
- **Session continuity**: zero-LLM compaction salvage and re-prime, session priming with a staleness banner, a sub-agent claim-check reminder, `scripts/recall.py`.
- **Harness self-maintenance**: `docs/reference/claude-code.md` (official doc pointers with a `last_checked` stamp and a 90-day test), a rule to consult `claude-code-guide` before harness changes, `/harness-health`, a monthly zero-token GitHub Actions check.

### Added

- Skills adapted from Matt Pocock's skills (MIT, see `NOTICE`): grilling, codebase-design, writing-for-agents, prototype, triage, to-tickets, work-issue. Also: session-winddown, recover-session, git-housekeeping, evaluate, architecture-review, audit-claude-md, harness-health, persona, handover (issue comment), logs.
- `/setup` as a 7-step idempotent bootstrap: fills CLAUDE.md/PROJECT.md, wires GitHub (repo, labels, issue templates), turns the roadmap into stub `feature` issues, founding commit and smoke checklist.
- `docs/guides/first-session.md`: a scripted ten-minute first task; cold-clone smoke job in CI.
- Harness tests under `tests/harness/` (deny-hook corpus, settings wiring, hook runtime, leak gate, tier table, memory, size caps, dead paths, README counts, reference stamp).

### Removed

- `stacks/` (Cloudflare), `docs/features/`, `docs/qa/`, PRD/plan/readme/qa templates, `memory/agents/`, the private middle-tier sync pipeline (`/sync`, `sync-downstream.sh`, manifest, `public-exclude.txt`, two-remote guides), `.github/tests/`, `test/`, eleven vendored document skills (docx, pdf, pptx, excalidraw, mcp-builder, slack, diagram, icon, md-to-doc, brand-guidelines, youtube), `auto-harness-readiness`, `context-priming`, `decision-fork-panel`, `template-sync`, the always-on event store, markdownlint in CI.

## [2.0.1] - 2026-07-19

### Added

- `DECISIONS.md` — decision log seeded with D-001 (repo-pipeline conventions: two-repo topology, batched tagged releases, `/prime`-surfaced port briefs).
- `/prime` surfaces pending `docs/system/port-to-template-*.md` briefs at session start (`status: pending|executed` frontmatter convention).
- `scripts/check_doc_counts.sh` — warns when hand-written agent/command/skill counts drift from the real directories; wired into the release workflow.
- Hard-won rules 9 (confidentiality tooling must not leak what it protects) and 10 (leak gates scan filenames, case-insensitively).

### Removed

- `docs/guides/upstream-workflow-contributions.md` — described a `v2`-branch / `npm run sync-workflow` contribution process that was never built. See `CONTRIBUTING.md` for the real path.

### Fixed

- Sync documentation (`template-sync` skill, `/sync` command, sync-guide) corrected to match actual `sync-downstream.sh` behavior (manifest-controlled agent sync, `settings.template.json` reference copy).
- Documentation indexes: previously unlisted guides added to `docs/README.md` and `connections.md`; `/sync` added to architecture command table and getting-started.

## [2.0.0] - 2026-07-19

### Added

- **Governing-docs map** — `CLAUDE.md` gains a "Governing documents (orient here first)" table (doc → purpose → load tier); `/prime` loads it per mode so sessions orient on the project's *what/why*, not just harness structure. `/setup` populates it from the docs it actually generates.
- **`context-priming` skill** — tiered, mode-aware loading of a project's governing docs at session start; convention-driven and portable to any repo declaring the map.
- **`decision-fork-panel` skill** — structured adversarial decision round (frame → gate → panel → challenger → synthesize → log), including an owner-utility gut-check gate and honest total-hour costing.
- **Opt-in governance scaffolding in `/setup`** — a single "light / full governance?" question; full generates `DECISIONS.md` (index + tombstones + stub D-000), a `PRINCIPLES.md` skeleton (each principle states what it forbids), and a conditional `docs/RISK-REGISTER.md`. Light stays exactly as before.
- **Librarian pre-commit consistency gate** — `/setup`'s multi-doc rewrite now runs a blocking Librarian checklist (cross-refs, governing-map tiers, feature-folder indexes) before the founding commit; Challenger review stays opt-in.
- **Feature-folder README convention** — every `docs/features/FEAT-XXX/` carries a File Index (file → purpose → status) from creation; drafts use `DRAFT-` prefix + `STATUS:` banner.
- **`docs/guides/refounding-checklist.md`** — 12-step checklist for project pivots/re-foundings (deliberately a checklist, not a skill).
- **Public release gate** — `scripts/public_release_gate.sh`: blocking PII/personal-content sweep over the release export tree (content patterns + file-type rules + visible waivers, no bypass flag), wired into the release workflow.
- **Hard-won rules 4–8** — competitive-check-before-thesis, spike-the-load-bearing-unknown, don't-re-litigate-settled-decisions, name-constraints-up-front, feature-folder-README-index.

- **Agent memory scaffold** — `memory/agents/` directory with `.gitkeep`, `README.md`, and `TEMPLATE.md`. Memory files (except README and TEMPLATE) are gitignored by default; users opt into tracking by removing the ignore line. Contract: three required sections (`## Patterns`, `## Incidents`, `## Task Outcomes`), citation-backed bullets, ≤100 lines per file.
- **`scripts/validate_agent_memory.py`** — schema validator; exits 1 on missing sections, malformed bullet dates, or missing citations; warns at >100 lines.
- **`scripts/prune_agent_memory.py`** — applies Agile Coach pruning manifests; dry-run by default; `--apply` to write.
- **Agile Coach agent** (`agile-coach.md`) — deterministic, read-only meta-optimizer. Reads build artifacts (commits, handover, QA, agent memory) and proposes hard-won rules, prompt tightenings, and memory pruning. Cites every claim verbatim. Falls back gracefully when `agent.db` is absent (tags `[no-observability]`).
- **PRD Consistency Simulator agent** (`prd-consistency-sim.md`) — cold-context read-only agent. Reads a PRD once and reports what it would build and every assumption it makes where the spec is silent or ambiguous. Always run after `/explore` produces a PRD and before `/blueprint` begins. Caps output at 10 assumptions + 3 risk flags.
- **`docs/guides/quality-gates.md`** — documents all four quality gates: Discover (stack-neutral symbol verification), Fidelity (opt-in sample payload enforcement), QA Reviewer (SAST + OWASP + three-value verdict), and Readiness classification (ready / nearly-ready / not-ready).
- **`docs/guides/autonomous-harness.md`** — documents the autonomous opt-in design pattern and `claude -p` offload narrative. No script ships in v2.0; pattern is documented for v2.1.
- **Observability schema prepared for v2.1 agent attribution** — internal builds add nullable `agent_id TEXT` and `parent_session_id TEXT` columns to the `events` table (backward-compatible, idempotent); the minimal public install keeps the v1 events schema. ETL and `/logs agents` view deferred to v2.1.
- **`scripts/validate_manifest.py`** — bidirectional guard: every agent with `template-owned: true` must appear in `.template-manifest`; every manifest entry must resolve to an existing file.
- **`.claude/agents/.template-manifest`** — manifest listing core harness agents for `sync-downstream.sh`.
- **`.claude/settings.template.json`** — reference settings file for downstream sync (does not overwrite `settings.json`).

### Changed

- **Model-tier policy** — `## Model Defaults` table added to `CLAUDE.md`: Opus (challenger, qa-reviewer), Sonnet (workhorse agents), Haiku (retrieval). Five agents (`challenger`, `qa-reviewer`, `librarian`, `specialist-creator`, `tech-product-lead`) now carry `model:` frontmatter.
- **Agent TEMPLATE.md** — `model:` field added; `template-owned: true` flag added.
- **Librarian agent** — `Write` tool removed; Edit-only contract enforced. Read-before-Edit required; post-edit `git diff --stat` verification required; >10% line-count delta flagged as suspect.
- **`specialist-creator` agent** — always emits `model: sonnet` (or `haiku` for explicit retrieval roles) in generated agent frontmatter; `model:` field is never absent from output.
- **`qa-reviewer` agent** — `model: opus`; verdict set documented as exactly three values: `APPROVED`, `NEEDS_FIXES`, `BLOCKED`; all three branches must be handled by the caller.
- **`/commit` gate** — hard-refuses `BLOCKED` or security-finding verdicts (no override); `NEEDS_FIXES` requires explicit user confirmation before proceeding.
- **`/explore` workflow** — Step 5.5 added: always run `prd-consistency-sim` after PRD is produced and before `/blueprint` begins.
- **`/build` and `/retro`** — document all three readiness branches from `auto-harness-readiness` skill: `ready` proceeds, `nearly-ready` prompts user, `not-ready` halts.
- **`auto-harness-readiness` skill** — rewritten as a stack-neutral manual pre-`/build` gate (was a dormant autonomous port).
- **`send_event.py`** — `os.makedirs` guard before connect; `AGENT_DB_PATH` env override respected; `ensure_events_table()` reconciled to match `init_db.py` schema exactly.
- **`sync-downstream.sh`** — extended to sync manifest-controlled agents and `settings.template.json`; `docs/guides/` excluded from sync (reach via re-clone or `/setup`).
- **Agent and skills counts** — 14 agents (up from 12), 21 skills (up from 18), 14 commands (unchanged from v1's 14).
- **Version** — bumped to 2.0.0 in `PROJECT.md`, `package.json`, and `CHANGELOG.md`.

### Fixed

- `prune_agent_memory.py` dry-run regression: no file writes occur unless `--apply` is passed explicitly.
- `ALTER TABLE` idempotency: per-column `PRAGMA table_info` guard prevents duplicate-column errors on re-run.
- `send_event.py` silent failure: missing parent directory no longer causes uncaught exceptions.

## [1.0.0] - 2026-03-13

Initial public release.

### Included

- 12 specialized agents (TDD, QA, research, planning, and more)
- 12 workflow commands (`/explore`, `/blueprint`, `/build`, `/qa`, `/commit`, etc.)
- Skills system for learned patterns via `/retro`
- Observability with SQLite + JSON logs
- Security hooks and SAST integration (Semgrep)
- Generic brand guidelines starter skill
- Cloudflare deployment stack
- Architecture diagrams and explainer deck

---

**Note:** This changelog tracks major versions. Feature-specific changes are documented in `docs/features/FEAT-XXX/`.
