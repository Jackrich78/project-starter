# Decisions

Index of significant decisions. Full entries below; superseded entries move to
`docs/decisions/archive.md` (created at first supersession).

| ID | Title | Status |
|---|---|---|
| D-001 | Three-tier repo pipeline: keep two repos, batched tagged releases, /prime-surfaced port briefs | Active |
| D-002 | No deep-research skill yet: harden the single `researcher` agent instead | Active |

---

## D-001 — Three-tier repo pipeline

- **Date:** 2026-07-19
- **Status:** Active
- **Context:** Three tiers (public `project-starter` ← internal `ai-workflow-starter` ← working projects) with three flows, each showing friction: public lagged 3.5 months behind internal; an upstream porting brief sat unexecuted 2 days; skills had no propagation path. Decision round run per `pipeline-brief-2026-07-19` (from a downstream project) using fresh evidence from shipping v2.0.0 the same day. Prior thinking located and treated as incumbent (FEAT-030 PRD, two-remote-sync.md rationale).
- **Options:** (a) keep both internal tiers + lightweight release ritual; (b) collapse internal repo into a private branch/fork of the public repo; (c) keep both with squashed changelog-fronted public drops.
- **Choice:**
  - **Q1 — keep two repos** (a/c hybrid; reaffirms FEAT-030). The branch model (b) was already considered and rejected (`two-remote-sync.md` git-archive rationale); v2.0.0 evidence strengthened the rejection: `.github/public-overrides/` files (public keeps v1 send_event.py etc.) would become permanent recurring merge conflicts under branches, and a public-remoted repo carrying full private history reintroduces the structural history-leak risk `git archive` eliminates.
  - **Q2 — batched releases**: CHANGELOG entry + `git tag vX.Y.Z` (both repos) + single-commit snapshot force-push via `two-remote-sync.md` with the blocking `public_release_gate.sh`. Exercised by v2.0.0 (public commit `8e6dca9`).
  - **Q3 — port briefs surface via /prime in the source project**: briefs stay where authored (`docs/system/port-to-template-*.md`) with `status: pending|executed` frontmatter; the template-owned `/prime` (propagated by `/sync`) globs the *current project's own* briefs and surfaces pending ones at session start — the reminder fires where the owner works daily, no cross-repo machinery.
  - **Q4 — deferred**: expanding the template-owned/flag-derived surface (curated skills list, CLAUDE.md rules block, fail-closed release allowlist) revisits after living with the v1 gate.
  - **Cleanup:** `docs/guides/upstream-workflow-contributions.md` and FEAT-023 retired — they documented a `v2`-branch/`npm run sync-workflow` process that was never built.
- **Trade-off accepted:** Two repos mean the release ritual stays a manual (scriptable) step rather than a `git merge`; the /prime reminder reaches a source project only after its next `/sync` (no retroactive coverage of un-synced projects).
- **Revisit if:** a release requires >30 min of mechanical work despite the ritual (→ revisit Q2 scripting and Q1); the blacklist gate produces another real near-miss (→ Q4 allowlist inversion); a third repo tier or second maintainer appears (→ Q1).

---

## D-002 — No deep-research skill yet

- **Date:** 2026-10-13
- **Status:** Active
- **Context:** Issue #9 audited research in this harness. The `researcher` agent could only search (no WebFetch), so its claims rested on search summaries. The audit asked whether a dedicated deep-research skill (a main-thread orchestrator that fans out researchers) should exist.
- **Choice:** No skill. Harden the single `researcher` agent instead (WebFetch, `effort: high`, think-first, fetch-before-cite, quote check, Could-not-confirm list) and put the follow-up rule in CLAUDE.md Context Rules. Callers (`/explore`, `/blueprint`, spike, debug) already orchestrate their own researchers, so a skill would have one caller; CLAUDE.md says abstract only on the 3rd repetition.
- **Trade-off accepted:** No built-in fan-out across many parallel researchers for broad questions; callers dispatch them by hand.
- **Revisit if:** a re-run of the #9 before/after task leaves a wrong or unsupported claim in Key Findings, or makes no WebFetch calls (→ try `model: sonnet` on the researcher before adding a skill). A misquoted snippet whose claim is still right and backed by another verbatim quote doesn't count; re-run its false-premise question whenever the researcher's model changes; a third caller starts hand-rolling the same fan-out.
