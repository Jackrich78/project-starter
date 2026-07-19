# Re-founding checklist

Use this when a project pivots or re-founds itself — a new direction that supersedes the current `PROJECT.md`/vision/architecture, not an incremental feature. It is deliberately a **checklist**, not a skill: re-foundings are rare (once per project, typically), so the setup cost of an executable skill isn't justified until the pattern repeats. If you find yourself running this more than once or twice on the same project, that's the signal to promote it to a skill instead.

The steps below are ordered to avoid the rework that an unordered pivot tends to cause — mainly, doing reference-sweeps and consistency passes late instead of in the founding round itself.

1. **Gate first:** run an owner-utility gut-check ("would the owner actually use this, personally, this month?") and a competitive check on the new direction *before* any decision-panel round invests time. A bad answer here means there's no fork to panel — see the `decision-fork-panel` skill's gating step.
2. Create an **archive branch** checkpointing the old project's HEAD before any pivot commits land, so the prior state stays recoverable.
3. Log the **founding decision** (new decision-log entry) with explicit supersession linkage — state which prior decision(s) and roadmap it supersedes.
4. **Rewrite `PROJECT.md`** for the new direction — fresh, not appended. Appending old context to new direction produces a document that serves neither.
5. Stamp **SUPERSEDED banners** (a couple of lines, pointing at the founding decision) on every doc that no longer applies (vision, one-pager, architecture, etc.). Docs that survive the pivot get a short **applicability note** instead of a full rewrite (e.g. an operating-principles doc that still holds).
6. Create the new **feature folder with its `README.md` index in the same commit** as the founding brief — don't defer the index to a later pass.
7. **Rewrite the risk register** for the new direction; the old one becomes heritage on the archive branch.
8. **Move the old feature folder to an archive location (e.g. `docs/features/archive/`) in the founding round itself** — not a later round — and rewrite all inbound references to it in the same pass. Doing this late means a second, dedicated reference-sweep commit.
9. Re-stamp every **governing-docs-map row** (load tier + heritage status) so `/prime` and the `context-priming` skill load the right things post-pivot.
10. Run a **documentation consistency gate before the founding commit lands** — checklist-driven: every superseded doc carries a banner pointing at the superseding decision; every governing-map row's load-tier is restamped; every moved/renamed file's inbound references are rewritten; every feature folder's README index is current. Use a clean-context reviewer (e.g. the Librarian agent) for this pass, not the orchestrator that just did the rewriting.
11. Write a **fresh handover** for the new project state.
12. Update memory/index files (project-direction memory, docs indexes) to reflect the new state.
