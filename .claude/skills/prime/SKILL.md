---
name: prime
description: Load project context at session start - git state, current state and roadmap, the ready-for-agent frontier, and the last handover on the issue you were working. Use on "prime", "start a session", "where were we", "/prime". Under 15k tokens, output 25 lines or fewer.
type: skill
disable-model-invocation: true
argument-hint: "[think|build|review]"
---

# /prime

## Context

Start of every session. CLAUDE.md is already loaded: do NOT re-read it. Budget under 15k tokens; offload any wider read to a sub-agent.

## Pattern

0. Human input first: run `python3 scripts/github/human_input.py` and print its output before anything else.
1. Git: `git branch --show-current`, `git status --short | wc -l` (dirty count), `git log --oneline -3`.
2. Read `PROJECT.md` sections Current state and Roadmap only.
3. Frontier: `gh issue list --state open --label ready-for-agent --search "no:assignee -label:feature -is:blocked" --json number,title,labels,parent --limit 10`.
4. Handover: find the issue with the latest `# Session Handover` comment (`gh issue list --state open --search "Session Handover in:comments" --json number,title`, then `gh issue view N --comments`). Extract the blocker (first line) and next step. Its status lines are "from handover, unverified" unless step 0 shows nothing newer on that issue.
5. Mode hint (optional argument):
   - `think`: read the tail (last ~20 lines) of `docs/decisions.md`.
   - `build`: point at `.claude/rules/testing.md`; do not load it until a test is written.
   - `review`: nothing extra.
6. Print at most 25 lines: human input (step 0 output); branch/dirty/commits; state in two lines; roadmap themes; frontier (`#N title`); the handover issue with blocker and next step. End with one suggested next command.

## Example

```
v3 · 0 dirty · a1b2c3 feat: ... 
State: 2 features shipped; auth in flight
Frontier: #14 chore: add health check | #15 ...
Mine: #12 (Working: since 2026-10-01) - blocker: CI red on lint
Next: /build #12
```

## Anti-patterns

- Re-reading CLAUDE.md or whole docs "for safety".
- Printing issue bodies; give numbers and titles, open on demand.
- Treating an empty frontier as an error: say so and suggest `/explore` or `triage`.
