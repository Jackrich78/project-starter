---
name: architecture-review
description: "Multi-agent review of an architecture proposal before committing to it; fires during /explore or /blueprint when one agent's conclusion would become the thing built or reach the human as a decision. Use on \"challenge this plan\", \"stress-test this design\", \"review this architecture\", \"build vs buy\", \"get a second opinion\". Cheap decisions go to evaluate instead."
type: skill
---

# Architecture Review

## Context

A lone agent's answer looks complete whether or not it is; independent lenses and a refute round tell those apart. Use for proposals expensive to reverse: new execution model, build vs buy, keep vs replace, anything touching many issues. Cheap decisions do not need it (use `evaluate`).

## Pattern

1. **Pin the proposal** in one document: what is proposed and why, what it replaces, rough effort. Reviewers read this plus `PROJECT.md`, nothing else from the conversation.
2. **Review in parallel.** Launch all four in a single message, in the background, so no reviewer sees another's output:

   | Agent | Lens | Returns |
   |---|---|---|
   | `challenger` | What is wrong? | At most 5 findings rated VALID / RISKY / WRONG |
   | `qa-reviewer` | Is it safe? | Trust boundaries, credential scope, injection vectors; APPROVED / NEEDS_FIXES / BLOCKED |
   | `tech-product-lead` | Is it feasible? | Effort, dependencies, sequencing, sustainability for the team size |
   | `researcher` | Is it real? | Technical claims checked against docs, issues, community reports |
3. **Synthesize in the main thread.** Table of agreement versus disagreement; list plan-breaking findings (anything that changes the approach).
4. **Refute round.** Send each plan-breaking finding to a fresh agent with only that claim and the evidence, asking it to disprove it. Keep findings that survive; drop those that do not. Reviewer output is a claim, not a fact: spot-check cited files and docs yourself.
5. **Present** the recommendation with amendments for each surviving finding. When the human decides, log it in `docs/decisions.md` with the rejected alternatives; update the proposal; keep the review notes as the audit trail.

For a proposal spanning several layers, run rounds instead: (1) researcher plus an explorer map reality; present 3-5 forks and let the human lock them; (2) lead plans under the locks while challenger attacks the plan; present the disagreements. Rounds run sequentially, never in parallel, and stop at 3: if forks remain, the requirements are ambiguous, so return to `/explore`.

## Example

Proposal: replace the job queue with an in-process scheduler. Challenger: "no durability on crash" (WRONG as written). QA: BLOCKED, scheduler runs with the web tier's credentials. Lead: rewrite is 4x the effort of patching. Researcher: the cited library dropped async support. Refute round confirms the credential and library findings; amended plan keeps the queue and fixes the retry path. Decision logged, in-process scheduler recorded as rejected.

## Anti-patterns

- Skipping the challenger: confirmation bias is the main risk.
- Running agents sequentially or letting them read each other: the first framing wins.
- Skipping the researcher for "feature X exists" claims: verify against real docs.
- Treating reviewer findings as facts without the refute round.
- Running rounds in parallel or past three.
