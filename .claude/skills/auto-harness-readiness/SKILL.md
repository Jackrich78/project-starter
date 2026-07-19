---
name: auto-harness-readiness
description: Manual pre-build readiness gate. Checks whether a feature has the prerequisites in place to run successfully through the /build workflow. Use when the user asks "is FEAT-XXX ready to build?", "ready to start the build?", "can we build this now?", or signals they are about to dispatch /build on a feature. Also use before /retro when deciding whether continued work on a feature is warranted. Emits exactly one of three verdicts — READINESS: ready / nearly-ready / not-ready — at the start of a line so callers can grep for it. Do NOT trigger for mid-build inspection (check test output instead) or feature scoping (use /explore or /blueprint).
---

# Auto-Harness Readiness Skill

Manual pre-build gate. Checks whether a feature satisfies the prerequisites for a successful `/build` run. Returns a grep-able verdict and a concrete gap list. Never auto-dispatches; never writes files.

## When to use

- Before `/build FEAT-XXX` when prerequisite state is uncertain
- After `/blueprint` to confirm plan and stubs are in place before building
- During `/retro` when deciding whether to continue work on a feature or declare it blocked

## Do not use for

- Mid-build inspection (check test runner output)
- Feature scoping or discovery (use `/explore` or `/blueprint`)
- Structure drift analysis (use `/retro analyze`)

---

## Pattern

### Step 1 — Read feature context

Read these in parallel (skip gracefully if absent):

- `docs/features/FEAT-XXX/prd.md` — acceptance criteria, open questions, `discover_queries` frontmatter
- `docs/features/FEAT-XXX/plan.md` — implementation approach and validation section
- `test/` — presence of test stubs for this feature
- Current `git status` — branch cleanliness

### Step 2 — Score against five criteria

For each criterion: ✅ pass / ⚠️ warning / ❌ blocker, with a one-line evidence note.

**Criterion 1 — PRD exists and has acceptance criteria**

- ✅ `docs/features/FEAT-XXX/prd.md` exists and contains at least one `AC-` item
- ⚠️ PRD exists but has unresolved open questions marked `OPEN —`
- ❌ PRD does not exist, or exists with no acceptance criteria

**Criterion 2 — Plan exists**

- ✅ `docs/features/FEAT-XXX/plan.md` exists with a defined implementation approach
- ⚠️ Plan exists but has no validation or test strategy section
- ❌ `plan.md` does not exist

**Criterion 3 — Test stubs are present**

- ✅ At least one test file for this feature exists under `test/`
- ⚠️ No test stubs yet, but plan indicates `/blueprint` generates them
- ❌ No stubs and no indication of how they will be created

**Criterion 4 — Working branch is clean**

- ✅ `git status` shows a clean working tree (or uncommitted changes are clearly in-scope)
- ⚠️ Uncommitted changes present but no conflicting state
- ❌ Merge conflicts or detached HEAD state

**Criterion 5 — `discover_queries` pre-validated (when present)**

- ✅ No `discover_queries` in PRD frontmatter (gate skips cleanly)
- ✅ `discover_queries` present and each `cmd` exits 0 when run locally
- ⚠️ `discover_queries` present but not yet pre-validated
- ❌ `discover_queries` present and one or more `cmd` exits non-zero

### Step 3 — Emit verdict

After scoring all five criteria, emit the verdict at the start of a line:

```
READINESS: ready
```
```
READINESS: nearly-ready
```
```
READINESS: not-ready
```

**Verdict definitions:**

| Verdict | Condition | Caller action |
|---------|-----------|---------------|
| `READINESS: ready` | All criteria ✅ | Proceed with `/build` |
| `READINESS: nearly-ready` | One or more ⚠️ warnings, no ❌ blockers | Prompt user with gap list; proceed on confirmation |
| `READINESS: not-ready` | One or more ❌ blockers | Halt; do not proceed; show blocking message |

The `READINESS:` token must appear at the start of a line (no leading whitespace). Prose before the verdict line is allowed; prose after is not — exit immediately after emitting the verdict.

---

## Caller Contract

Every caller that invokes this skill MUST handle all three verdict branches. Partial handling (e.g., only branching on `ready`) is a silent gap — a `not-ready` feature would silently proceed into a broken build.

**`/build` command handling:**

```
READINESS: ready        → proceed with Phase 0 (Discover & Route)
READINESS: nearly-ready → prompt: "Gap: [gap]. Proceed anyway? (yes/no)"
                          on yes: proceed; on no: halt
READINESS: not-ready    → halt with message: "Build blocked: [blocker]. Resolve before /build."
```

**`/retro` handling:**

```
READINESS: ready        → note feature is build-ready; include in next-steps
READINESS: nearly-ready → surface gap to user; suggest /blueprint to close it
READINESS: not-ready    → flag as blocked; do not include in build candidates
```

---

## Output format

```
Readiness Check — FEAT-XXX

Criterion 1 PRD + ACs:      ✅ prd.md exists, 12 ACs found
Criterion 2 Plan:           ✅ plan.md exists with validation section
Criterion 3 Test stubs:     ⚠️ no stubs yet (blueprint will generate)
Criterion 4 Branch clean:   ✅ working tree clean
Criterion 5 discover_queries: ✅ no discover_queries (gate skips)

READINESS: nearly-ready
Gap: test stubs not yet created. Run /blueprint FEAT-XXX to generate them, then re-check readiness.
```

---

## Anti-patterns

- Do not proceed with `/build` when verdict is `not-ready` — even if the user requests it. The gap will surface as a broken build rather than a pre-flight warning.
- Do not treat `nearly-ready` as equivalent to `ready`. Surface the gap explicitly so the user can decide whether to close it first.
- Do not emit `READINESS:` mid-prose or with leading whitespace — callers grep for it at line start.

---

## See also

- `docs/guides/quality-gates.md` — full quality gate documentation (Gate 4: Readiness)
- `.claude/commands/build.md` — readiness three-branch handling in the build workflow
- `.claude/commands/retro.md` — readiness branching in the retrospective workflow
- `.claude/commands/blueprint.md` — generates plan.md and test stubs (closes nearly-ready gaps)
