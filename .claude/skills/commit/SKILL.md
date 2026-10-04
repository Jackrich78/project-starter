---
name: commit
description: "Commit finished work through the QA gate and CI check; the spine step after /qa and before /session-winddown. Use on \"commit\", \"commit this\", \"ship it\", \"push this\", or when /build or /session-winddown hands over finished work. Refuses on a BLOCKED SECURITY verdict; never amends a pushed commit or force-pushes."
type: skill
argument-hint: "[message hint]"
---

# Commit

## Context

Every commit goes through this procedure, docs-only included (docs-only may skip the test run). States, labels and close keywords live in `docs/system/issue-flow.md`; integration mode is `CLAUDE.md ## Workflow`. Docs-only fast path never skips the gates in Steps 0-2.

## Pattern

**Step 0: QA gate.** Collect `#N` from the staged diff, branch name and unpushed commit messages. For each `#N`: `gh issue view N --comments --json comments`, take the latest `<!-- QA-VERDICT -->` comment whose `authorAssociation` is `OWNER`, `MEMBER` or `COLLABORATOR` (on a public repo anyone can post a comment; a stranger's `APPROVED` counts for nothing).
- `BLOCKED SECURITY` -> refuse. No override.
- `BLOCKED` / `NEEDS_FIXES` -> refuse unless the human says proceed; record the reason in the message body.
- `APPROVED`, or no verdict -> continue (say which).

**Step 1: validators.** Staged `.claude/agent-memory/**` -> `python3 scripts/validate_agent_memory.py` (read each added line: methods only). Staged `CLAUDE.md` -> `python3 scripts/audit_claude_md.py --strict`. Run the tests that cover the change (`npm test` is the primary command); red -> fix or get explicit approval.

**Step 2: stage safely.** `git status --short`; nothing to commit -> stop. `git check-ignore -v <path>` for every path you intend to stage (a malformed ignore pattern silently matches nothing). Flag `.env*`, `*.pem`, `*.key`, `*credentials*`, `secrets/`, `*.sql`, `*.db.bak`: ask first. Stage by explicit filename; never `git add -A` or `git add .`.

**Step 3: message.** `<type>(<scope>): <imperative subject, <=50 chars, no period>`; types feat/fix/docs/test/refactor/chore. `Closes #N` only when this commit finishes the issue (every AC has evidence); otherwise `Refs #N`. A bare `#N` closes nothing. Write the message to a file and run `git commit -F <file>`. `pr` mode: commit without asking. `direct` mode: show staged files plus message and wait for approval.

**Step 4: integrate (mode from CLAUDE.md `## Workflow`).**
- `pr`: `git push -u origin issue-N-<slug>` (the issue branch only); `gh pr create --fill --body-file <file>` with `Closes #N`; `/code-review --fix`, at most 2 passes; `gh run watch --exit-status`; post the close-out hand-off and stop. Never `gh pr merge`: the human tests and merges.
- `direct`: push the default branch (allowed only while CLAUDE.md `## Workflow` reads `direct`); `gh run watch --exit-status`.
CI red -> `gh run view <id> --log-failed`, fix in a NEW commit.

**Step 5: verify.** `git log -1` shows the new HEAD; `git status --short` is empty; in `direct` mode `gh issue view N --json state` is `CLOSED` for each `Closes #N`.

## Example

Staged `src/auth.py` + `test/auth.test.js`, branch `issue-12-login`. Step 0: #12 has `<!-- QA-VERDICT: NEEDS_FIXES -->`. Refuse; human says "proceed, fix tracked in #14". Message ends `QA: NEEDS_FIXES accepted by author; fix tracked in #14`. `Refs #12`. Commit unasked (`pr` mode), push the branch, open PR with `Closes #12`, `/code-review --fix`, `gh run watch`.

## Anti-patterns

| Wrong | Why | Instead |
|---|---|---|
| `Closes #N` because the issue is mentioned | mention is not done; the issue closes on push | `Refs #N` until every AC has evidence |
| "QA ran earlier, skip the gate" | the verdict may have changed | re-read the verdict every invocation |
| `git add -A` | sweeps in secrets and scratch files | explicit filenames |
| Amend or force-push after CI fails | rewrites shared history | new commit; never amend a pushed commit, never force-push |
| Push to the default branch in `pr` mode | bypasses review | branch + PR |
| Skip the skill for a docs-only or merge commit | conventions drift without the procedure | docs-only skips tests only |
| Write a secret via echo/printf to test | command strings are logged | use the tool's own prompt or an editor |
