---
name: git-housekeeping
description: "Audit and clean stale git state: orphan worktrees, merged or stale branches (local and remote), accumulated stashes, orphan commits on dead branches. Use on \"clean up branches\", \"tidy the repo\", \"what worktrees do I have\", \"clean my stashes\", \"post-merge cleanup\", \"too many branches\"."
type: skill
disable-model-invocation: true
---

# Git Housekeeping

## Context

Worktrees outlive their work, squash-merged branches look unmerged, stashes pile up, and orphan commits sit on top of merged branches where `git branch -D` silently loses them. This is a triage tool, not an auto-clean: audit first, rescue second, delete last, each mutation approved per item. Never delete before rescuing.

## Pattern

1. **Audit (read-only, always first).** Gather:
   ```bash
   git worktree list
   git fetch --prune origin
   git branch --merged origin/main;  git branch --no-merged origin/main
   git branch -r --merged origin/main;  git branch -r --no-merged origin/main
   git stash list            # peek with: git stash show stash@{N} --stat
   git log origin/main..<branch> --oneline     # every unmerged branch
   gh pr list --state all --head <branch> --json number,state,title
   ```
   Report tables for worktrees, local branches, remote branches, stashes, and orphan commits, each item triaged:
   - **safe**: content is on main (merge or squash-merge with PR record), clean worktree, obsolete WIP stash.
   - **review**: diff exists, direction unclear; the human decides.
   - **rescue**: commits not on main and no merged PR; deleting would lose work.
2. **Rescue (approved items only).** Branch off `origin/main`, cherry-pick the orphan, run the tests touching those files, then propose push and PR. Push and PR creation are gated: ask first. The PR body says what the orphan was, why it never shipped, where it was found.
3. **Delete (approved items only).**
   - `git worktree remove <path>`
   - `git branch -d <name>` (refuses unmerged); `-D` only after merge is confirmed
   - `git stash drop stash@{N}`, highest index first
   - Remote branches: **ask before any batch `git push origin --delete a b c`**; list the exact names and get a yes. Treat remote deletes as permanent.
4. **Summarise** with a Before / After table and list what was deleted (reflog keeps local ~90 days).

Invariants: the audit is always first; check `git log origin/main..<branch>` before proposing any unmerged delete (squash-merged and unshipped both show as `--no-merged`); never `git worktree move` mid-session (project dir is fixed at session start; rename at session boundaries); in stacked PRs, retarget the dependent PR's base to main before merging.

## Example

Audit finds 4 worktrees, 18 local and 31 remote branches, 3 stashes. Branch `fix/retry-bug` is `--no-merged`, has 1 commit, no PR: marked rescue. Human approves: cherry-pick onto a fresh branch, tests pass, PR proposed. Only then are the 17 safe local branches deleted, and the 30 safe remote names are listed for one confirmed batch delete.

## Anti-patterns

- Proposing deletion without the audit, or judging by `--merged` alone.
- Chaining rescue and delete in one response: each phase has its own approval gate.
- Auto-resolving review items instead of surfacing them.
- Running during active feature work or after a single-PR commit: overkill and distracting.
