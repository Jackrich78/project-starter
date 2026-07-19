---
name: decision-fork-panel
description: >-
  Run a structured, adversarial multi-agent round to resolve a significant,
  contested product/design/architecture decision — propose, panel of distinct
  perspectives, challenger, synthesize, log. Use when facing a genuine fork with
  multiple viable options and real stakes (a vertical, an architecture, a demo
  shape, a build-vs-borrow call), especially where a solo pass would miss
  failure modes or reproduce one perspective's blind spots. Do NOT use for
  choices with an obvious default, mechanical/convergent calls, or questions a
  single lookup answers — those are decided inline. When a decision feels weighty
  enough that you're tempted to deliberate at length solo, prefer running this
  round instead — it reaches a better-pressure-tested answer faster and cheaper
  than a bespoke agent round authored from scratch.
---

# Decision-fork panel — adversarial rounds without the per-round setup cost

A repeatable harness for the pattern that reliably produces good, defensible decisions: **frame → gate → panel → challenge → synthesize → log.** It exists so you run this at genuine forks without re-inventing the choreography (which perspectives, what context each gets, how to converge) every time — that setup cost is what makes ad-hoc rounds slow and token-heavy.

## When to run it (and when not to)

Run it for a **genuine fork**: multiple viable options, real stakes, and a solo pass would likely miss failure modes or bake in one lens's bias. Examples: which vertical/use-case, which architecture or protocol, demo shape, build-vs-borrow, a contested scope cut.

Do **not** run it for: choices with an obvious default (decide inline, mention it), mechanical/convergent work, or a fact one lookup settles. A panel for a non-fork is the classic waste — it burns tokens and wall-clock for a foregone conclusion.

## The procedure

1. **Frame the fork (inline, before spawning anything).** State: the decision, the 2–4 concrete options on a spectrum, the load-bearing constraints, the first-class tensions (e.g. "watchability vs. credibility"), and the goals/jobs it must serve. Naming constraints and tensions up front prevents the panel from circling. Write the shared **context pack** once: point agents at the project's governing-docs map (see `context-priming`) instead of re-listing files in every prompt — this is the biggest token saving across a multi-agent round.

2. **Front-load the gating checks — in parallel, before the panel invests.** Three checks kill or reshape more forks than the panel itself: **(a) competitive check** — does a named tool already ship this capability? (invalidates a differentiation thesis); **(b) load-bearing spike** — is the one mechanism the decision rests on actually validated? **(c) owner-utility gut-check** — put the one-line question "would the owner actually use this, personally, this month?" to the human *before* the panel runs. Three separate expensive rounds (mock refund agent, shopping-mandate agent, D-030 aftercare agent) each died to this test applied *after* the analysis; asked first, it costs one message. Run these first; a bad answer means there's no fork to panel.

3. **Spawn a small panel of DISTINCT perspectives, in parallel.** Each gets the same context pack + one non-overlapping lens, writes a short draft, returns a summary. A good default set:
   - **Architect / definer** — sharpens the options into concrete specs + a comparison table.
   - **Strategy / value** (McKinsey-style) — scores options against the goals/audience; finds where "I want both" helps vs. hurts.
   - **Feasibility / build-risk** — cost, time-box, kill-switches, what each option's hidden spikes are. Charge this lens with an **honest total-hour estimate including industrialization** (benchmarks, replication, hardening, write-up), not just the happy-path build — the founding round whose "25h" was really ~35h cost an entire extra hardening panel (D-032) to re-cost.
   - **Wildcard / chaos** (only when the *premise itself* is worth challenging) — argues the frame is wrong; generates genuinely different options. Run it "cold" (don't feed it the decision log) so it isn't anchored.
   Keep the panel small (2–4). Overlapping lenses are wasted agents.

4. **Challenge the leading synthesis** (a single high-capability skeptic). Prompt it to *attack*: steelman the rejected option, name where "protect what we've built" is sunk-cost bias, find the soft flank a sharp reviewer would hit. This step reverses more weak calls than the whole panel — the map-pin-was-a-gimmick catch is the archetype.

5. **Synthesize and decide.** Reconcile: what all lenses agree on, the one genuine fork the human must call, your recommendation with reasoning. Put the genuine fork(s) to the human; carry the clear calls as recommendations.

6. **Log it.** Write a `D-XXX` decision entry — context, options, choice, trade-off accepted, revisit trigger — and update the decision-log index. An unlogged decision gets re-litigated (the expensive failure mode this whole harness exists to avoid).

## Efficiency rules (the "faster" in this skill)

- **Shared context pack, not per-agent file lists.** Point every agent at the governing-docs map; don't re-list PROJECT/DECISIONS/etc. in each prompt.
- **Gate before you panel.** The competitive check + load-bearing spike are cheap and often collapse the fork — run them first, not after.
- **Cap panel size and de-duplicate lenses.** 2–4 distinct perspectives; if two agents would say the same thing, cut one.
- **Reserve the whole harness for genuine forks.** Convergent calls go inline. Most decisions are not forks.
- **Don't re-run a settled fork.** Read the decision log first; a logged `D-XXX` is settled unless its revisit clause fires.

## Anti-patterns

- Running a panel for a decision with an obvious default (waste).
- Redundant agents with overlapping lenses (pay N× for 1 perspective).
- Skipping the challenger because the synthesis "feels right" (that's exactly when it's least tested).
- Deciding, then not logging — guarantees a re-litigation round later.
- Feeding the wildcard/chaos agent the full decision log (anchors it; defeats the point of a cold outside read).

## Example (illustrative)

Fork: which demo "flavor" to build / whether to pivot to a different vertical. Ran architect + strategy + feasibility in parallel (shared context pack), then a cold chaos agent (several alternatives), then a high-capability challenger that killed a weak option and flagged sunk-cost bias in the synthesis. Synthesized → stayed on the current vertical, cut the weak option, logged the decision and its index entry. This skill keys off the governing-docs-map convention (see `context-priming`), so it works in any project that declares one.
