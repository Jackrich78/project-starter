---
name: context-priming
description: >-
  Efficiently load a project's governing context at session start (or when
  onboarding to an unfamiliar repo) using a tiered, mode-aware convention —
  instead of dumping every doc into context or guessing. Use at session start,
  when the user runs a prime/onboard command, when picking up an unfamiliar
  codebase, or before proposing/building on a project whose decisions and
  principles you haven't loaded. Portable across any project that declares a
  "Governing documents" map in its CLAUDE.md. Do NOT use for deep feature work
  once already oriented (load feature files directly instead).
---

# Context priming — load a project's what/why efficiently

The goal at session start is not to read everything (context bloat, cost) and not to read nothing (drift, re-litigating settled calls). It is to load the **orientation tier** — the small set of documents that carry the project's *what and why* — and to know where the rest lives for on-demand loading. This skill is convention-driven: it reads whatever governing-docs map the host project declares, so the same procedure works across projects.

## The convention (what a project must declare)

A project adopting this puts a **"Governing documents" map** in its `CLAUDE.md` (auto-loaded every session, so it also reaches sub-agent contexts). Each row maps a document to its purpose and a **load tier**:

- **`always`** — load its index/summary every prime (e.g. `PROJECT.md` state; a decision-log *index*, never the full log).
- **`orient`** — load in full when the session's mode calls for it (e.g. vision + principles for planning; architecture for building).
- **`on-demand`** — do *not* load at prime; load only when a specific task needs it (full decision entries, archives, deep research, feature folders).

A typical map: `PROJECT.md` (state), `PRODUCT-VISION.md` (north star), `PRINCIPLES.md` (operating principles — what each forbids), `DECISIONS.md` (index always, entries on-demand), `docs/ARCHITECTURE.md` (design rationale), a one-pager/pitch (on-demand). Adapt names to the project.

## Modes (mindset + scope)

Priming takes a **mode** that shapes both what loads and how to think:

- **`think`** — explore, question assumptions, weigh alternatives. Load vision + principles + architecture + decision index.
- **`build`** — make it work; minimal, tests-first. Load principles + architecture + decision index + the target feature's files.
- **`review`** — be suspicious; hunt for what's wrong. Load principles + decision index + QA/test conventions.
- **`create`** — audience, narrative, clarity. Load vision + one-pager + principles.
- **`bare`** — no mode: git state + a feature listing only. Stop.

## Procedure

1. **Capture git state:** current branch, `git status --short`, last ~3 commits. (Cheap orientation for every mode.)
2. **Load the orientation tier for the mode**, per the project's governing-docs map. Load *indexes/summaries* for `always` docs (never a full decision log); load `orient` docs in full only where the mode calls for them.
3. **If a feature/task ID is given:** load that feature's folder (README/PRD/plan first pages, handover if present) — scope, not everything.
4. **Note, don't load, the `on-demand` tier** — know it exists so you can fetch it when a specific decision, archive, or research doc becomes relevant.
5. **Respect settled decisions:** a logged decision is settled unless its own revisit clause fires. Don't re-open it from a cold read; check the log first.
6. **Summarize in 3–5 lines** (branch/status, mode + framing, feature if any, anything notable). Do **not** dump file contents back to the user — the files are in context, that's the point.

## Principles this encodes

- **Reduce** — minimize what's in context; load on demand. A decision-log *index* beats the full log; an orientation tier beats "read everything."
- **Orient before act** — load the what/why before proposing or building, so work builds on settled ground instead of re-deriving or contradicting it.
- **The map is the source of truth** — when in doubt about what to load, follow the project's governing-docs map rather than guessing paths.

## Adopting this in a new project (copy-to-template)

1. Copy this skill folder into the project's `.claude/skills/`.
2. Add a **"Governing documents"** table to the project's `CLAUDE.md` (document · purpose · load tier), listing that project's real docs.
3. Point the project's session-start command (e.g. `/prime`) at the orient tier per mode, or invoke this skill. Keep the decision log as an **index + archive** so its index is cheap to load `always` while superseded detail stays out of the default context.
4. Keep the map current: when a new governing doc is added, add a row — otherwise priming silently misses it.
