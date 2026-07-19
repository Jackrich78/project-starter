---
updated: 2026-07-19T00:00:00Z
---

# Quality Gates

Four named checkpoints that run at specific moments in the build workflow. Each gate has a clear trigger, a pass/fail contract, and a documented example. Gates degrade gracefully when optional infrastructure is absent — a missing field or tool skips the gate cleanly rather than hard-blocking.

---

## Gate 1 — Discover

**When it runs:** At the start of `/blueprint`, before Phase A (fail-closed — see `.claude/commands/blueprint.md` § Discover Gate). Re-validated by the Readiness gate (Gate 4, criterion 5) before `/build` in case the PRD changed since blueprint ran.

**What it checks:**

Before writing code that references any external symbol — a database column, environment variable, API field, or config key — verify its real name against its live source. Do not trust the PRD prose or a schema diagram alone; verify the actual runtime artifact.

This gate is **stack-neutral**: the mechanism depends on your project. Any project with a live system to query should verify names before referencing them.

> **Postgres + Python example** (illustrative — substitute your stack's equivalent)
>
> - Verify a column name: `\d <table>` in psql, or `PRAGMA table_info(<table>)` in SQLite
> - Verify an env var is actually used: `grep -r "ENV_VAR_NAME" .` in the project root
> - Verify an API field: inspect a real response payload in `docs/features/FEAT-XXX/sample-payloads/`
>
> Other stacks: `rails db:schema:dump`, `terraform show`, `kubectl describe`, `aws cloudformation describe-stacks` — whatever exposes the live shape of the system.

**PRD frontmatter field (optional):**

```yaml
discover_queries:
  - label: "Verify events table columns"
    cmd: "python -c \"import sqlite3; c=sqlite3.connect('.claude/logs/agent.db'); print([r[1] for r in c.execute('PRAGMA table_info(events)')])\""
  - label: "Verify AGENT_DB_PATH is referenced in send_event.py"
    cmd: "grep -q 'AGENT_DB_PATH' .claude/hooks/send_event.py && echo OK"
```

The `discover_queries` field is **present only when the feature touches a live system**. A PRD with no `discover_queries` field skips the gate entirely without error.

**How to fail:**

- Any query in `discover_queries` exits non-zero → abort the run (fail-closed). The field name or value in the query output does not match what the PRD assumes → the PRD must be corrected before code is written.

**Concrete example:**

PRD says `events.session_id` but the live schema has `events.session_key`. The discover gate catches this before the implementer writes `WHERE session_id = ?` and ships a broken query.

---

## Gate 2 — Fidelity (opt-in)

**When it runs:** At the start of `/build`.

**Default behavior:** No-op. This gate is inactive unless the feature explicitly declares an external API surface.

**What it checks:**

When a feature interacts with an external API — a third-party service, a webhook payload, a live data source — tests must load from real captured payloads, not from payload shapes synthesized from PRD prose. PRD-synthesized payloads often miss fields, use wrong key names, or omit nesting that only real responses contain.

**Activation:**

The gate activates **only** when the PRD frontmatter contains:

```yaml
touches_external_api: true
```

If this flag is absent or `false`, the gate is a no-op and the build proceeds without any payload check.

**When active — warning + confirm (not hard-block):**

If `touches_external_api: true` AND no file matching `docs/features/FEAT-XXX/sample-payloads/*.json` exists:

```
FIDELITY WARNING
────────────────
No sample payloads found at docs/features/FEAT-XXX/sample-payloads/.
This feature declares an external API dependency (touches_external_api: true).

Tests that load from synthesized payloads risk passing locally and failing on
first contact with the real system.

Capture at least one real payload per external event type before proceeding.
See docs/guides/quality-gates.md § Gate 2 for capture instructions.

Proceed without payloads? (yes/no)
```

On user confirmation: proceed. On decline: stop and capture payloads first.

**When a payload file exists:** no warning is shown; tests load from `sample-payloads/`.

**How to fail:**

- `touches_external_api: true` in frontmatter AND no payload files AND user declines confirmation → build does not proceed.
- A payload file exists but tests synthesize from PRD prose instead of loading the file → flag in QA review (code quality issue, not a gate block).

**Capturing a real payload:**

Save the response from the live system as `docs/features/FEAT-XXX/sample-payloads/{system}-{event}.json` (kebab-case). Strip secrets. The structure is what matters, not the values. Common sources:

- REST API: capture a `curl` response with `--output`
- Webhooks: log one delivery from the provider's "Recent Deliveries" debug panel
- Database: `SELECT row_to_json(t) FROM table t LIMIT 1`

**Concrete example:**

A feature subscribes to a webhook event. The PRD documents the payload as `{ "type": "event", "data": { "user_id": "..." } }`. The real payload arrives as `{ "type": "event", "data": { "userId": "..." } }` — camelCase vs snake_case. Tests written against PRD prose pass; the handler crashes on first real delivery. Fidelity gate catches this if a real payload is captured.

---

## Gate 3 — QA Reviewer

**When it runs:** After `/build` completes (Phase 5 of the build workflow), and standalone via `/qa`.

**What it checks:**

An independent security and quality review. The reviewer operates with context isolation from the builder — it reads the handover document, not the builder conversation. This clean context enables unbiased assessment.

Review scope:
- OWASP Top 10 security analysis (SAST + LLM, ≥80% confidence threshold)
- Code quality (naming, complexity, duplication, error handling)
- TDD compliance (tests present, coverage, behavior-oriented names)
- Deployment verification (build evidence, smoke test)
- Scope consistency (handover vs PRD)

**Caller Contract — three-value verdict set:**

The QA reviewer emits exactly one of three verdicts in the report frontmatter:

```
status: APPROVED
status: NEEDS_FIXES
status: BLOCKED
```

All three branches **must** be handled by the caller. Partial handling (e.g., only handling `APPROVED` and `NEEDS_FIXES`) is a silent gap that allows security findings to pass through undetected.

| Verdict | Meaning | Caller action |
|---------|---------|---------------|
| `APPROVED` | All checks passed | Proceed to `/commit` |
| `NEEDS_FIXES` | Quality/coverage issues; no security blocker | Warn user; allow override with explicit confirmation |
| `BLOCKED` | Security finding or critical failure | Refuse `/commit`; no override; must resolve first |

**How to fail:**

- Any OWASP finding with ≥80% confidence → at minimum `NEEDS_FIXES`; if critical severity or hardcoded credentials → `BLOCKED`
- Tests failing → `BLOCKED`
- Deployment evidence absent → `NEEDS_FIXES`
- Scope changed without documentation → `NEEDS_FIXES`

**Concrete example:**

QA reviewer finds a hardcoded API key in `src/client.ts:12`. This is a `BLOCKED` verdict. `/commit` refuses the commit and instructs the author to move the key to an environment variable and re-run QA. No override option is offered for security findings.

---

## Gate 4 — Readiness

**When it runs:** Before `/build` begins (as a pre-build check); also surfaced during `/retro` when deciding whether to continue work on a feature.

**What it checks:**

Whether a feature has the prerequisites in place to run successfully through the build workflow. The readiness gate is a **manual check** — run it explicitly before dispatching `/build` on a feature where the prerequisite state is uncertain.

**Criteria checked:**

1. PRD exists at `docs/features/FEAT-XXX/prd.md` and contains acceptance criteria
2. `plan.md` exists at `docs/features/FEAT-XXX/plan.md`
3. Test stubs are present (at least one file in `test/`)
4. Working branch is clean (`git status` shows no untracked conflicting files)
5. If `discover_queries` are present in PRD frontmatter, they have been pre-validated (each exits 0 locally)

**Verdict format:**

The readiness skill emits exactly one verdict at the start of a line (grep-able):

```
READINESS: ready
READINESS: nearly-ready
READINESS: not-ready
```

**Three-branch handling (callers must handle all three):**

| Verdict | Definition | Caller action |
|---------|-----------|---------------|
| `READINESS: ready` | All criteria green | Proceed with `/build` |
| `READINESS: nearly-ready` | One or more warnings but no hard blockers | Prompt the user with the documented gap; proceed on confirmation |
| `READINESS: not-ready` | One or more hard-blocking criteria missing | Halt; do not proceed; display the blocking message |

Partial handling (e.g., only handling `ready`) is a silent gap — a `not-ready` feature would silently proceed into a broken build.

**How to fail (produce `not-ready`):**

- PRD does not exist or has no acceptance criteria
- `plan.md` does not exist
- `discover_queries` entries exit non-zero when pre-validated

**How to produce `nearly-ready`:**

- PRD and plan exist, ACs present, but test stubs are not yet created
- Branch has uncommitted changes but no conflicting state
- `discover_queries` have not been pre-validated but are present

**Concrete example:**

Feature FEAT-042 has a PRD and a plan, but no test stubs yet. Readiness emits `READINESS: nearly-ready` with the gap documented: "test stubs not yet created — run `/blueprint FEAT-042` to generate them." The build command prompts the user to confirm before proceeding, rather than silently starting a TDD cycle with no stubs.

---

## Summary Table

| Gate | Trigger | Default | Fail action |
|------|---------|---------|-------------|
| Discover | Start of `/blueprint` | No-op if `discover_queries` absent | Abort run (fail-closed) |
| Fidelity | Start of `/build` | No-op unless `touches_external_api: true` | Warn + require confirmation |
| QA Reviewer | After `/build` TDD completes | Always active | `BLOCKED` refuses commit; `NEEDS_FIXES` warns |
| Readiness | Before `/build`, during `/retro` | Manual check | `not-ready` halts; `nearly-ready` prompts |

All gates degrade gracefully: absent frontmatter fields skip the gate cleanly; missing optional tools (Semgrep) fall back to LLM-only review.
