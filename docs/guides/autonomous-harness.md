---
title: Autonomous Harness — Design Pattern & Roadmap
updated: 2026-06-19T00:00:00Z
status: v2.0 — narrative only; no script shipped
---

# Autonomous Harness — Design Pattern & Roadmap

This guide explains the opt-in autonomous-mode design pattern, the staged pipeline
contract, the cost model for offloading work to `claude -p`, and what is and is
not shipped in v2.0. It is a narrative reference — there is no script or automation
to configure here.

---

## The Default: Interactive Claude Code

Out of the box, this harness is fully interactive. You invoke slash commands
(`/explore`, `/blueprint`, `/build`, `/qa`, `/commit`) and Claude Code responds in
the conversation. You decide at every step whether to proceed, adjust scope, or
redirect. This is the right default for:

- Active feature work where requirements are still being shaped
- Unfamiliar codebases where you want to observe each agent's reasoning
- Features with significant architectural decisions or external-system coupling
- Any situation where the cost of a wrong autonomous decision exceeds the cost of
  a confirmation prompt

Interactive mode is not a training-wheels mode. It is the canonical mode. Autonomous
mode is an opt-in overlay for a specific narrow use-case: a feature that is
well-understood, well-scoped, PRD-locked, and whose entire build-validate-commit
cycle you are willing to review as a single PR rather than step by step.

---

## The Opt-In Gate: `AI_AUTOFLOW_ENABLED`

The autonomous-mode design pattern uses a single environment variable as the
entry gate:

```bash
AI_AUTOFLOW_ENABLED=1 ./auto.sh FEAT-XXX <slug>
```

When this variable is unset or empty, no autonomous pipeline runs. Slash commands
behave interactively. Sub-agents ask for confirmation before destructive or
irreversible actions. This is intentional: **an autonomous run must be an explicit,
affirmative act**, not a default that can fire accidentally.

The flag also serves as an in-process signal. When slash commands and sub-agents see
`AI_AUTOFLOW_ENABLED=1` in the environment, they adjust their behaviour:

- Ambiguous decisions that would normally prompt for input are resolved
  conservatively and recorded as `DECISION (AUTO_MODE): <choice> — <rationale>`
  in the stage output
- Findings that would normally ask "do you want to continue?" instead emit an
  `ESCALATION (AUTO_MODE): <reason>` signal and abort the run
- Manual-only checks in the validation section are skipped and logged as decisions
  deferred to PR review

The contract is: if you do not set `AI_AUTOFLOW_ENABLED=1`, none of this behaviour
activates. The harness is inert with respect to autonomous mode.

**v2.0 note:** The `AI_AUTOFLOW_ENABLED` flag, the `DECISION`/`ESCALATION` sentinel
format, and the slash-command branch contracts are described here for design
completeness. No script in this release sets or reads this variable. The design is
documented so that downstream users who build their own automation shell have a
stable, agreed-upon contract to implement against.

---

## The Staged Pipeline Contract

When an autonomous run is active, it must follow this ordered sequence. No stage
may be skipped and no stage may begin before the previous stage has exited cleanly.

```
discover → blueprint → build → validate → commit
```

Each stage has a defined entry contract, a defined exit contract, and a failure
mode that terminates the run and preserves the working directory for inspection.

### Stage contracts

**discover**
Entry: a locked PRD at `docs/features/FEAT-XXX_<slug>/prd.md`.
Work: runs any `discover_queries` declared in PRD frontmatter, verifying that
canonical names — database columns, environment variable names, configuration keys,
external API fields — match their live sources. Results are written to a
`discover-cache.yml` so downstream stages can read them without re-querying.
Exit: all queries returned expected results. Any non-zero exit aborts the run.
A PRD with no `discover_queries` field skips this stage cleanly.

**blueprint**
Entry: a clean discover pass (or a PRD with no queries).
Work: runs `/blueprint FEAT-XXX` to produce `plan.md`. The plan must include a
`## Validation` section describing the runtime smoke checks. Any ambiguous decision
is recorded as a `DECISION` line; any unresolvable gap emits `ESCALATION` and aborts.
Exit: `plan.md` written, validation section present.

**build**
Entry: `plan.md` present.
Work: runs `/build FEAT-XXX` via the TDD red-green-refactor cycle. The internal QA
gate runs at the end. A `NEEDS_FIXES` result retries up to three times before
escalating. A `BLOCKED` (security) result aborts immediately — no retry, no override.
Exit: all tests pass on the net-new set; QA verdict is `APPROVED`.

**validate**
Entry: a passing build.
Work: runs `/validate FEAT-XXX`, which executes the `## Validation` checks authored
by blueprint. Each check must exit 0. Integration checks must include a read-back
probe — asserting that a write call returned success is not sufficient; the resulting
state must be confirmed to exist in the target system.
Exit: `VALIDATION_OK` emitted; no `VALIDATION_FAILURE:` lines in output.

**commit**
Entry: a clean validate pass.
Work: runs `/commit` on the feature branch. Refuses to commit to the main branch.
Pushes and opens a PR with a body that includes the autonomous decisions log, QA
status, and validation summary.
Exit: PR URL written to the run log.

### Failure handling

On any stage failure, the run aborts, the working directory is preserved, and a
cleanup script is written alongside the stage logs. The cleanup script contains the
exact commands to remove the working state when you are done inspecting it. It is
not auto-executed — that would destroy diagnostic state on transient failures.

---

## The `claude -p` Offload Narrative

`claude -p` (the `--print` / non-interactive mode of Claude Code) is how an
autonomous script drives Claude without a human in the conversation loop. Each
stage is a `claude -p` subprocess call with a slash command as the prompt. The
subprocess runs to completion, its stdout and stderr are captured to log files,
and the shell script greps for sentinel patterns (`DECISION`, `ESCALATION`,
`VALIDATION_OK`, `VALIDATION_FAILURE:`) to determine the outcome.

This design has three important properties:

**Composability.** Each stage is an independent process. The harness shell is a
coordinator, not a monolith. A stage can be retried, replaced, or skipped
independently. The shell does not need to understand what Claude did inside a
stage — only whether it succeeded.

**Turn-budget control.** Each `claude -p` invocation can be given a `--max-turns`
ceiling. The orchestrator shell enforces this ceiling; if Claude hits it without
emitting a success sentinel, the run is treated as a failure. This prevents runaway
sessions from consuming unbounded compute.

**Observability.** Because each stage writes to its own log file, a post-mortem can
replay exactly what Claude decided at each step, in what order, and why. The
`DECISION` lines form a structured audit trail that populates the PR body
automatically, so human reviewers know what autonomous choices were made without
reading raw logs.

### Rough cost model

These numbers are rough guidance for planning, not billing guarantees. Actual cost
depends on feature scope, model tier, and whether the CLI subscription or API keys
are in use.

| Stage | Model | Approximate turns | Approximate token range |
|-------|-------|------------------|------------------------|
| blueprint | sonnet | 20–50 | 30k–80k |
| build (per TDD cycle) | sonnet | ~3 per test stub | 5k–15k per stub |
| validate | sonnet | 10–20 | 15k–40k |
| commit | sonnet | 5–15 | 8k–20k |
| challenger (within blueprint) | opus | 5–10 | 10k–25k |
| qa-reviewer (within build) | opus | 5–10 | 10k–30k |

A feature with roughly 15 test stubs will consume approximately 50–80 turns in
the build stage alone. The 80-turn ceiling (the empirically-derived value from
production dogfooding) is the practical maximum for a well-scoped feature in a
single autonomous build pass.

If a feature exceeds this ceiling, it is a signal that the scope is too large for
a single autonomous run. Break it into smaller, sequentially-ordered features, each
of which can be autonomously built in budget. The `auto-harness-readiness` skill
(see `.claude/skills/auto-harness-readiness/SKILL.md`) provides a pre-dispatch gate
that estimates whether a feature fits the turn budget before you commit to a run.

**On billing:** when using a Claude Code subscription rather than direct API keys,
`claude -p` reports an informational API-equivalent cost figure but the actual
charge is the subscription rate. Verify your billing configuration before running
autonomous builds at scale. If the harness ever switches to direct API billing,
re-verify the cost model — per-run costs change materially.

---

## Why `auto.sh` Is Not Shipped in v2.0

The autonomous script (`auto.sh`) is **not included in this release**. This is
intentional, not an oversight.

The reference implementation in the project that this harness was derived from
accumulated tight coupling to a specific infrastructure stack over roughly a dozen
features of iterative development. Concretely, it assumed:

- A specific Python version and package manager
- A specific database stack and schema layout
- A specific set of external service integrations for notifications and observability
- A particular directory layout for memory, logs, and worktrees that is hardcoded
  in several places via absolute path construction rather than relative-to-repo logic
- Platform-specific tool availability (specific CLI tools resolved at preflight that
  may not be present on a different developer's machine)

Porting this script to a generic OSS template requires more than stripping the
stack-specific references. It requires:

1. Replacing all hardcoded paths with `$(dirname "$0")`-relative logic
2. Making the dependency list explicit and providing graceful degradation when
   optional tools are absent
3. Replacing all stack-specific observability writes with a generic event log
4. Making the validation layer pluggable so it works for any project type, not just
   the specific one the script was designed for
5. Establishing a principled cleanup model that works across different working
   directory layouts

This is a non-trivial effort that deserves its own scoped feature rather than a
rushed port that would ship with hidden coupling. Shipping a half-decoupled script
would be worse than shipping no script: users would clone it, find that it fails on
their stack, and either patch it ad hoc or file issues against assumptions that
were never documented.

**v2.1 plan:** The generalization work is scoped and will ship in v2.1. When it
lands, the script will be a first-class part of the template, documented with
stack-substitution guidance and tested against a minimal generic project rather
than a specific private stack. The design documented in this guide — the
`AI_AUTOFLOW_ENABLED` flag, the staged pipeline contract, the sentinel format —
will be the stable interface that the v2.1 script implements.

---

## How This Guide Reaches You

This guide reaches downstream users via **re-clone or `/setup`**, not via
`sync-downstream.sh`.

The sync pipeline (see `docs/guides/sync-guide.md`) covers hooks, the
manifest-controlled core agents, and the settings reference file. It deliberately
does not sync `docs/guides/` in v2.0. The rationale: adding a third synced surface
widens the diff-review gate and increases the clobber surface for a category of
file (reference guides) that is read rarely and often locally annotated by users.

If you cloned this template before v2.0 and want the new guides, the cleanest path
is to re-clone into a fresh directory and copy the specific guide files you want.
If your project was set up via `/setup`, re-running `/setup` from an updated
template clone will offer the updated guides.

---

## Summary

| Topic | Position |
|-------|----------|
| Default mode | Interactive Claude Code — slash commands, confirmation prompts, step-by-step |
| Autonomous mode | Opt-in via `AI_AUTOFLOW_ENABLED=1`; explicit env flag required |
| Pipeline contract | `discover → blueprint → build → validate → commit`; no stage may be skipped |
| Script shipped in v2.0 | None — design is documented; implementation deferred to v2.1 |
| Reason for deferral | Source script is stack-coupled; generalization requires its own scoped effort |
| How this guide propagates | Re-clone or `/setup`; NOT via `sync-downstream.sh` |
| Cost model | Rough guidance: ~50–80 turns for a 15-stub feature at the sonnet tier |
| Billing | Verify CLI-subscription vs API-key billing before running at scale |
