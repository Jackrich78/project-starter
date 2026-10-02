---
name: commit
description: "Commit with the QA gate, leak gate and CI check. Use on \"commit\", \"commit this\", \"ship it\", \"push this\", or when /build, /qa or session-winddown hands over finished work. Refuses on a BLOCKED SECURITY verdict; never amends a pushed commit or force-pushes."
type: skill
disable-model-invocation: true
argument-hint: "[message hint]"
---

# Commit

## Context

Every commit goes through this procedure, docs-only included (docs-only may skip the test run). States, labels and close keywords live in `docs/system/issue-flow.md`; integration mode is `CLAUDE.md ## Workflow`. Docs-only fast path never skips the gates in Steps 0-2.

## Pattern

**Step 0: QA gate.** Collect `#N` from the staged diff, branch name and unpushed commit messages. Read `.claude/qa/verdict-<branch>` (`/` becomes `__`); that local file is authoritative. If it is absent, for each `#N`: `gh issue view N --comments --json comments`, take the latest `<!-- QA-VERDICT -->` comment whose `authorAssociation` is `OWNER`, `MEMBER` or `COLLABORATOR` (on a public repo anyone can post a comment; a stranger's `APPROVED` counts for nothing).
- `BLOCKED SECURITY` -> refuse. No override; the security hook blocks it too.
- `BLOCKED` / `NEEDS_FIXES` -> refuse unless the human says proceed; record the reason in the message body.
- `APPROVED`, or no verdict -> continue (say which).

**Step 0b: leak and coupling gates.** If `.github/pii-patterns.txt` exists: `bash scripts/leak_gate.sh --require-patterns`; any hit -> refuse. If `scripts/coupling_lint.sh` exists, run it.

**Step 1: validators.** Staged `.claude/agent-memory/**` -> `python3 scripts/validate_agent_memory.py` (read each added line: methods only). Staged `CLAUDE.md` -> `python3 scripts/audit_claude_md.py --strict`. Run the tests that cover the change (`npm test` is the primary command); red -> fix or get explicit approval.

**Step 2: stage safely.** `git status --short`; nothing to commit -> stop. `git check-ignore -v <path>` for every path you intend to stage (a malformed ignore pattern silently matches nothing). Flag `.env*`, `*.pem`, `*.key`, `*credentials*`, `secrets/`, `*.sql`, `*.db.bak`: ask first. Stage by explicit filename; never `git add -A` or `git add .`.

**Step 3: message.** `<type>(<scope>): <imperative subject, <=50 chars, no period>`; types feat/fix/docs/test/refactor/chore. No `Co-Authored-By` trailer, no mention of AI. `Closes #N` only when this commit finishes the issue (every AC has evidence); otherwise `Refs #N`. A bare `#N` closes nothing. Write the message to a temp file in one Bash call, then run `git commit -F <file>` in a SEPARATE call: the security hook scans heredoc bodies, and one denial would kill both. Show staged files plus message; wait for approval.

**Step 4: integrate (mode from CLAUDE.md `## Workflow`).**
- `pr`: push the branch; `gh pr create --fill --body-file <file>` with `Closes #N`; `/code-review --fix`, at most 2 passes; `gh run watch --exit-status`; the human merges.
- `direct`: push the default branch (the security hook permits a push to the default branch only while CLAUDE.md `## Workflow` reads `direct`); `gh run watch --exit-status`.
CI red -> `gh run view <id> --log-failed`, fix in a NEW commit.

**Step 5: verify.** `git log -1` shows the new HEAD; `git status --short` is empty; in `direct` mode `gh issue view N --json state` is `CLOSED` for each `Closes #N`.

## Example

Staged `src/auth.py` + `test/auth.test.js`, branch `issue-12-login`. Step 0: #12 has `<!-- QA-VERDICT: NEEDS_FIXES -->`. Refuse; human says "proceed, fix tracked in #14". Message ends `QA: NEEDS_FIXES accepted by author; fix tracked in #14`. `Refs #12`. Push, open PR with `Closes #12`, `/code-review --fix`, `gh run watch`.

## Anti-patterns

| Wrong | Why | Instead |
|---|---|---|
| `git commit -m` inline | hook scans the command string; blocked words in a message trip it | `-F <tempfile>`, separate call |
| `Closes #N` because the issue is mentioned | mention is not done; the issue closes on push | `Refs #N` until every AC has evidence |
| "QA ran earlier, skip the gate" | the verdict may have changed | re-read the verdict every invocation |
| `git add -A` | sweeps in secrets and scratch files | explicit filenames |
| Amend or force-push after CI fails | rewrites shared history | new commit; never amend a pushed commit, never force-push |
| Push to the default branch in `pr` mode | bypasses review | branch + PR |
| Skip the skill for a docs-only or merge commit | conventions drift without the procedure | docs-only skips tests only |
| Write a secret via echo/printf to test | command strings are logged | use the tool's own prompt or an editor |
