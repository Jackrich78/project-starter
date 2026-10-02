---
name: grilling
description: "Stress-test a plan, decision or idea by structured interview before acting on it. Use on \"grill me\", \"stress-test this\", \"poke holes in this plan\", \"interview me about this\", \"help me decide\". Maps a design tree and asks the open frontier in numbered rounds with recommended answers."
type: skill
---

Adapted from Matt Pocock's `grilling` skill, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# Grilling

## Context

A plan or idea is about to be acted on and nobody has pushed on it yet. Interview the human until you share one understanding. Map it as a **design tree**: every decision branches into the decisions that hang off it. Each question is exactly one reversible decision with a one-line trade-off, never a bundle under one number.

## Pattern

1. **Work the tree in rounds.** The **frontier** is every decision whose prerequisites are settled: questions you can ask now without guessing at unheard answers. Ask the whole frontier in one round, numbered, each with your recommended answer. Wait for answers before the next round.
2. **Format each question:**
   ```
   ❓ **Q1** - **<title>**: <body, options if any>

   ➡️ <your recommended answer>
   ```
3. **Recompute the frontier** after each round. A question that depends on one still open belongs to a later round.
4. **Facts are your job, decisions are theirs.** Look facts up (files, docs, tools; a sub-agent if broad) instead of asking. Check `docs/decisions.md` for a prior ruling first; cite it and move on rather than re-asking. Questions downstream of a running lookup wait; ask the rest now.
5. **Close** when the frontier is empty: every branch visited, nothing silently assumed. Do not act until the human confirms shared understanding.
6. **Log the outcome** in `docs/decisions.md` in the same turn when it was a choice between options: the decision, the option rejected, the reason. Prose that never reaches the log is unrecoverable later.

## Example

Human: "grill me on moving sessions to Redis."
Round 1 (frontier, no dependencies): Q1 scope: all sessions or only the admin ones? Q2 downtime budget during cutover? Q3 does anything else read the session table? (fact: you grep for it, so not asked). Recommended answers attached.
Round 2 after answers: Q4 dual-write window length (depends on Q2). Q5 rollback trigger.
Close: "Shared understanding: admin-only, 5 min budget, dual-write 1 day. Confirm?" Then append the decision and the rejected all-sessions option to `docs/decisions.md`.

## Anti-patterns

- Asking a question you could look up: it spends the human's attention on your job.
- Bundling two decisions under one number: the answer cannot be "yes to the first".
- Asking a dependent question in the same round as its prerequisite: you are guessing the earlier answer.
- Acting before confirmation, or logging the decision a turn later.
