---
name: evaluate
description: "Score options against criteria and recommend one. Use on \"evaluate these options\", \"help me decide between\", \"score these against\", \"which should I pick\", \"run the war council on\", \"deep evaluate\". Quick mode is a scoring table; deep mode is a parallel panel of role-based sub-agents for high-stakes decisions. Pairs with grilling: grill to discover options, evaluate to rank them."
type: skill
---

# Evaluate

## Context

Known options, one decision. Two modes, one output shape. If the option set is unclear, run `grilling` first; it discovers options, this skill ranks them. Default to quick; deep only when the decision is irreversible, costly, or affects more than a month of work.

## Pattern

### Mode 1: Quick (default)

1. **Like-for-like.** Options must be the same kind of thing; reframe or ask if not. Asymmetric comparisons produce meaningless scores.
2. **Pick lenses with the human** (3-5), with a weight each. Suggested defaults, replace freely: Effort/energy to sustain, Value (benefit and time to first result), Learning, Risk (reversibility), Feasibility (can it ship with available resources). Score 1-5, state what 5 and 1 mean for each lens.
3. **Score with a reasoning chain.** One-line justification per score, tagged **EVIDENCE** (cites a source: the human's words, data, code) or **ESTIMATE** (your judgment, challengeable).
4. **Output:**
   ```
   **Verdict: <winner>** - <one line, citing the decisive lens>
   | Lens | Wt | Option A | Option B |
   | Value | 2x | 4 - "reason" [EVIDENCE] | 3 - "reason" [ESTIMATE] |
   **Weighted total:** A: X | B: X
   **Close calls:** <near ties>
   **What would flip it:** <one fact>
   **Assumptions to challenge:** <every ESTIMATE>
   ```

### Mode 2: Deep (War Council)

1. **Frame** back to the human: the decision, options, current leaning, what a wrong call costs. Wait for confirmation.
2. **Dispatch 5 sub-agents in parallel** (sonnet), each with the framing and one role. Each returns a structured verdict of about 200 words: position, confidence H/M/L, key risk.
   - **Economist**: unit economics, opportunity cost, hidden costs.
   - **Contrarian**: assumes the opposite is true; hunts the consensus trap.
   - **Customer**: the real user or buyer; willingness to pay; flags when none exists.
   - **Builder**: feasibility, complexity, build versus buy, the hard 20%.
   - **Domain expert**: chosen per decision (compliance, operator, staff engineer, editor, dealmaker); name the role and say why in the framing.
3. **Synthesize in the main thread; never delegate this.** The value is in reconciling disagreement. Table of member, position, confidence, risk; then where they agree (carries most weight), where they clash (where the real decision lives), a confidence-weighted recommendation, and what would flip it.
4. **Log the decision** in `docs/decisions.md` in the same turn the human decides: chosen option, the rejected options and why. Code preserves what was built, never what was tried.

## Example

"Evaluate Postgres versus SQLite for the job queue." Quick: lenses Feasibility 2x, Risk 2x, Value 1x; SQLite wins 4.1 to 3.4, flip fact "needs more than one writer host" tagged ESTIMATE. Human then says the choice is hard to undo: deep mode, 5 agents, Contrarian flags a second writer is planned, verdict flips to Postgres; decision logged with SQLite as the rejected option.

## Anti-patterns

- Running the council on a decision already made: wasted tokens.
- Five agents for a quick A-or-B: use Mode 1.
- Scoring without stated criteria: the numbers mean nothing.
- Equal weights when the human plainly cares about one lens.
- Averaging council scores: the disagreement is the signal, the mean hides it.
- Delegating the synthesis to a sub-agent.
