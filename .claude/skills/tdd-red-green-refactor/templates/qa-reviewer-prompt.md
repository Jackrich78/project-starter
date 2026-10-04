---
type: reference
title: "qa-reviewer dispatch prompt (fallback brief)"
description: "Direct brief for qa-reviewer when /qa --issue is not used; the normal path is /qa."
---

Normal path is `/qa --issue {issue}` (its skill forks into `qa-reviewer`). Use this only to dispatch the agent directly. Never paste the builder conversation.

```
Review issue #{issue} in --issue mode.

Gather, read-only:
- gh issue view {issue} --comments   (ACs, Tests: line, Proof: line, close-out)
- the diff: git diff <base>...HEAD, or commits mentioning #{issue}
- the tests named on the Tests: line

Do your full three-ladder review (Security, Standards, Spec). If the diff has
no code files, review against the ticket's Proof: rubric instead.

Your report's FIRST line must be exactly:
<!-- QA-VERDICT: APPROVED|NEEDS_FIXES|BLOCKED|BLOCKED SECURITY -->
Include the claim-vs-evidence table and Tier 2 items as numbered options.
Do not run gh write commands; you cannot write files.
```

The orchestrator then posts the report (`gh issue comment {issue} --body-file`) and handles all four verdicts (see the `qa` skill).
