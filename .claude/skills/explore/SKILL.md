---
name: explore
description: "Turn a vague idea, question or decision into the right artifact: one ticket, a parent feature issue with an approved design note, a decisions line or a wiki page; the first spine step, before /blueprint. Use on \"explore #N\", \"let's think through X\", \"should we build X or Y\", \"scope this feature\", \"plan the roadmap\", \"/explore --roadmap\". Gates on the human approving a design note before any acceptance criteria are written."
type: skill
argument-hint: "#N | <topic> | --roadmap"
---

# Explore

States, labels, sizing, templates and every `gh` command live in [`docs/system/issue-flow.md`](../../../docs/system/issue-flow.md). This skill is the discovery procedure and points there.

## Context

Something is not yet specified: an idea, a stub parent (`#N`), a question, a fork between options. Output is the smallest durable artifact that lets the next reader act. Next step after a parent: `/blueprint #N`.

## Pattern

1. **Enter plan mode.** The plan file is scratch for your own thinking, never the hand-off; nothing is published until the human approves (step 6). With `#N`, read the issue first (`gh issue view N --comments`).
2. **Classify the ask:** feature, decision, question, or knowledge. A question may end at step 7 route 0.
3. **Product discovery.** Problem (trigger, who, cost of not solving), value and how it is measured, v1 in and out, the user flow. Branching decisions: run `grilling`. Facts go to sub-agents or the repo; only decisions go to the human. When the topic was already discussed in this session, open each round with recommended answers cited from what was said (confirming is one line, re-dictating is five).
4. **Technical discovery.** Constraints, existing patterns to reuse, integrations. **Close code-readable open questions by reading the file:** an OQ that names a file as its answer source is not open. Dispatch `researcher` (sonnet) only for questions the repo cannot answer; a facts-only brief, answers posted back as text. Touching an external system: capture one real payload now, not a synthesized fixture. One load-bearing unknown remaining: run the `spike` skill (or `prototype` for a UI/state question) before committing to a shape.
5. **Size** per issue-flow.md § Sizing.
6. **Route**, then ask "what does the next reader need, and does any code change?"

   | Route | Artifact |
   |---|---|
   | (0) answered | nothing; say the answer, create no state |
   | (a) one ticket | `.github/ISSUE_TEMPLATE/ticket.md`: `needs-triage`, or `ready-for-agent` only with a `Verified:` comment written in-session (issue-flow.md § Verify gate) |
   | (b) parent feature | `.github/ISSUE_TEMPLATE/feature.md`, see below |
   | (c) a choice was closed | one line in `docs/decisions.md` with the **rejected option**, ending in the issue link |
   | (d) knowledge | a wiki page, create-or-update, named by topic never by session |

   Combinations are explicit: decision that creates work = (c) + (a)/(b); research informing a ticket = (d) + (a); "already exists" = (0), plus closing a related issue as `wontfix` per issue-flow.md.
7. **Route (b), Gate 1.** Write the design note (one screen: question, in/out test, proposed shape, decisions needed, open items), show it, wait. **No acceptance criteria before the human approves it;** objections mean revise and re-show, never patch afterwards. Then write the body once, in order: design note, requirements, ACs `AC-001...`, outcome test, `## Validation`, `## Reversal`. Create or update via `gh issue edit N --body-file <f>` (parent state: issue-flow.md § Parent-issue state). Log the approval in `docs/decisions.md`.
8. **Cold read.** Dispatch `prd-consistency-sim` (opus) with the output of `gh issue view N --json body` pasted into the brief (it has no `gh`). Surface its HIGH RISK and Conflicting signals to the human; patch silences into the body as one-line edits. Run it once, on the final body.
9. **Challenger (conditional, opus):** only when 3 or more OQs remain, validation depth is integration or frontend, or the spec touches agents, commands or other harness files. Brief it with the claims to disprove; fix Tier 1 findings, escalate Tier 2 as numbered options.
10. **Report:** issue number(s), the decisions line, or the wiki path.

### `--roadmap`

Dispatch `tech-product-lead` with PROJECT.md vision: propose at most 8 features in at most 3 phases, each with goal and why. The human edits the list. Then create one stub `feature` parent per item (goal, phase, "spec pending: run `/explore #N`") and rewrite PROJECT.md `## Roadmap` as phase themes ending in `#N` links, nothing else; status is read from GitHub, never copied.

## Example

`/explore #12` where #12 is a stub "export reports". Grill three branching decisions (format, scope, who), read `src/export/` to close two OQs, one spike on streaming large files. Sized: over 500k tokens, so route (b). Design note approved, body written once with AC-001 to AC-006, `prd-consistency-sim` flags one silent default (timezone), patched in one line. Report: "#12 ready for /blueprint; decision line added".

## Anti-patterns

- Writing ACs before the design note is approved: the note is where the human's real decisions happen.
- Asking the human a question the repo or a sub-agent can answer.
- Leaving an OQ that names a file as its answer source.
- Calling `prd-consistency-sim` repeatedly: after iteration its cold read is no longer cold.
- Always-on `challenger`: it is conditional because it costs an opus run.
- Treating the plan-mode file as the spec, or hand-linking issues in a body.
- A decisions line with no rejected option.
- Restating labels or states here instead of pointing at issue-flow.md.
