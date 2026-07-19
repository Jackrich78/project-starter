# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
