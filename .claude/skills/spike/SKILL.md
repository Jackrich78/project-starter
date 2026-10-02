---
name: spike
description: "Time-boxed technical investigation to reduce uncertainty before committing to an approach. Use on \"/spike <topic>\", \"does X work with Y\", \"we're not sure this is feasible\", \"prove this out first\", or when /blueprint finds confidence under 50% or several viable approaches. A spike is a sub-issue whose proof is the learning."
type: skill
disable-model-invocation: true
argument-hint: "[question]"
---

# Spike

## Context

A spike is temporary code that generates permanent knowledge. It answers one narrow question ("does X work with Y?") so the plan does not rest on a guess. It is a **sub-issue** of the work it unblocks; its `Proof:` is the learning, written as a comment on the parent. For a clickable logic demo use `prototype`; for a decision between known options use `evaluate`.

## Pattern

1. **Decide whether to spike.** Spike only if all hold: the question is narrow and testable; confidence is under 50%; a wrong guess means real rework; it fits within 8 hours. Do not spike if the answer is in the docs (read first), the question is too broad (split it), confidence is over 70% (just build), the pivot cost is low, or the goal is procrastination.
2. **Open the sub-issue.** `gh issue create --parent <P>` with the question, the time box (2-4h simple, 4-6h integration, 8h max), and the criteria: `Proof:` what result validates the approach, and what result means stop and pivot. Link it as blocking the parent work.
3. **Execute in `spikes/<topic>/`.** Write the minimum code that answers the question. Keep running notes (`references/findings-template.md`): finding, why it matters, gotchas noted the moment they appear. Stop when the box ends, finished or not.
4. **Extract the learning (required, whatever the outcome).** Post one comment on the parent issue:
   - **Validated:** the approach works, with the conditions ("works but requires X"); amend the parent's plan.
   - **Partial:** what is known and unknown; either proceed with qualified confidence, open a narrower follow-up spike, or pivot.
   - **Failed:** why it is infeasible and the alternative the spike suggests. This is success: you prevented wasted build time.
   A rejected approach also goes in `docs/decisions.md` as a `REJECTED` line with the reason.
5. **Close out.** Delete `spikes/<topic>/` (the code is throwaway; the comment is the artifact). If something is worth keeping, lift it into real code with tests in a normal ticket. Close the spike issue with `Proof:` linking the comment.

## Example

Parent #42 "move uploads to object storage". Spike #43: "Can the SDK stream a 2 GB file without buffering? Box 4h. Proof: peak RSS under 200 MB." Code in `spikes/stream-upload/`. Result at 3h: validated, needs multipart with 16 MB parts. Comment on #42 states that, plan amended, `spikes/stream-upload/` deleted, #43 closed.

## Anti-patterns

- A vague question ("explore storage"): the box has no end. Ask "does X do Y under Z".
- Documenting at the end: gotchas are forgotten; note as you go.
- Letting the code live on: spike code shipped to production skips tests and design.
- Overrunning the box: stop, record partial findings, then decide.
- Learning left in `spikes/`: only the issue comment survives deletion.
- Spiking what a docs page answers.
