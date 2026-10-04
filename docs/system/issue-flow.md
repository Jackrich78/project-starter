---
type: domain-doc
title: "Issue flow: how work lives in GitHub Issues"
description: "States, labels, sizing, pickup protocol, close-out shape and QA verdict marker for GitHub Issues as the spec and the work queue; read before touching an issue."
tags: [issues, workflow, github]
---

# Issue flow: how work lives in GitHub Issues

The issue is the spec and the state. This page is the one home for the facts below; the skills `triage`, `to-tickets` and `work-issue` hold procedure and point here. Adapted from Matt Pocock's skills (MIT, https://github.com/mattpocock/skills); see `NOTICE`.

## Artifact map

| Kind of work | Where it lives |
|---|---|
| Spec for one slice | the **ticket body** (`.github/ISSUE_TEMPLATE/ticket.md`) |
| Spec for a feature | the **parent issue** (label `feature`, `.github/ISSUE_TEMPLATE/feature.md`): design note, ACs, outcome test, Validation, Reversal |
| Plan | the **sub-issues** of the parent, one context window each |
| Rejected option | `docs/decisions.md`, `REJECTED <option>`, ending with the issue link |
| What an issue taught | the close-out comment's `Learned:` line |

Create a sub-issue with `gh issue create --parent <P>`; never hand-link in the body. Agents edit an issue body only through the one-line diff assertion (pickup step 7); amendments to an approved parent go in a comment plus a `docs/decisions.md` line.

## Sizing

Unit: one fresh context window of the model you run, not hours.

| Size | Artifact |
|---|---|
| Under half a window | inline; name it in the commit (`Refs #N` if an issue exists) |
| One window | one ticket, no parent |
| More | parent + sub-issues, one window each |

**Tripwire:** a ticket whose build needs a handover before it closes was mis-sized. Split the remainder into a sub-issue (`gh issue create --parent N`) rather than carrying it.

## States

Every open issue carries one kind (`bug`, `enhancement`, `chore`), one priority (`P0`/`P1`/`P2`) and at most one state label.

| State | Signalled by | Command |
|---|---|---|
| raised | `needs-triage` | `gh issue create --title "<t>" --body-file <f> --label needs-triage,<kind>` |
| triaged | `needs-triage` removed, kind + priority set | `gh issue edit N --remove-label needs-triage --add-label <state>,<P>` |
| needs-info | `needs-info` + Triage Notes comment | `gh issue edit N --remove-label <old> --add-label needs-info` then `gh issue comment N --body-file <notes>` |
| ready-for-agent / ready-for-human | label, no assignee | `gh issue edit N --add-label ready-for-agent` (or `ready-for-human`) |
| in progress | assignee + "Working:" comment | `gh issue edit N --add-assignee @me` then `gh issue comment N --body "Working: <session or branch>"` |
| in review | `ready-for-human` + "Built, awaits <step>" comment | `gh issue edit N --remove-label ready-for-agent --add-label ready-for-human --remove-assignee @me` then `gh issue comment N --body "Built, awaits <step>"` |
| done | closed as completed via `Closes #N`, then close-out | `gh issue view N --json state` reads `CLOSED`, then `gh issue comment N --body-file <closeout>` |
| wontfix | `wontfix`, closed as not planned | `gh issue close N --reason "not planned" --comment "<reason>"` then `gh issue edit N --add-label wontfix` |
| duplicate | closed as duplicate | `gh issue close N --duplicate-of M` |

Rules behind the rows:

- **Raised is `needs-triage`** by default. Exception: tickets published by `to-tickets` go straight to `ready-for-agent`.
- **In progress is the assignee, not a label.** The "Working:" comment says which session holds it, because `gh` acts as one account for humans and agents alike.
- **In review** is only for work needing a human or a live surface before it counts (relaunch, deploy, manual check). Code review is not a state: it happens before `/commit` (see Integration modes).
- **Blocked on another issue** is a native edge: `gh issue edit N --add-blocked-by M`, and release the claim (`--remove-assignee @me`). Blocked on information: `needs-info`.
- **Needs-info returns to `needs-triage`** when answered; the answer is recorded in the thread, never only in chat.
- **Done** needs every AC ticked with evidence, `Closes #N` in the closing commit (or PR body in `pr` mode), `state` = `CLOSED`, then the close-out comment. A bare `#N` never closes. Anything needing a live check goes to in review instead.
- **Wontfix** splits three ways: already built (say where), rejected bug (reason), rejected enhancement (one `REJECTED` line in `docs/decisions.md`).
- **Parent close-out cascade:** when the last sub-issue closes (`gh issue view P --json subIssuesSummary`, completed = total), the closing agent posts the parent's close-out answering the outcome test, closes the parent, and moves lasting facts to the wiki. **Abandon cascade:** closing a parent as not planned closes its open sub-issues the same way; the reason goes in `docs/decisions.md` once, at the parent.
- **The last sub-issue is always the `ready-for-human` live check**; its close triggers the parent cascade.

### Parent-issue state

A `feature` parent carries `needs-triage` until its design note is approved, then no state label. Sub-issues carry state from there. A parent is never picked up.

## Labels

Created by `scripts/github/setup_labels.py` (idempotent; `--dry-run` first). The table is checked against the script by `tests/harness/test_labels_match_doc.py`.

| Label | Group | Meaning |
|---|---|---|
| `needs-triage` | state | Needs a human's evaluation |
| `needs-info` | state | Waiting on more information |
| `ready-for-agent` | state | Fully specified; an agent can pick it up |
| `ready-for-human` | state | Needs a human to act, decide or check live |
| `wontfix` | state | Will not be actioned; closed as not planned |
| `P0` | priority | Drop everything |
| `P1` | priority | Next up |
| `P2` | priority | When there is room |
| `bug` | kind | Something is broken |
| `enhancement` | kind | New capability or improvement |
| `chore` | kind | Internal tidiness; no user-visible change, no incident |
| `feature` | parent | Parent issue holding a feature's spec; never picked up by agents |

<!-- Areas: the `area:*` labels are listed once, on the `Areas (labels)` line in CLAUDE.md; scripts/github/setup_labels.py reads them from there. -->

**Deliberately absent:** `in-progress`, `blocked`, `in-review` labels (assignee, native edges and `ready-for-human` cover them); milestones; GitHub Projects (a third status surface). Teams wanting milestones add them knowingly.

## Integration modes

In `direct` mode the security hook permits a non-force push to the default branch only while CLAUDE.md `## Workflow` reads `direct`; force, URL and refspec pushes stay blocked in every mode.

Mode is read from CLAUDE.md `## Workflow` (`Integration mode: pr | direct`).

| | `pr` | `direct` |
|---|---|---|
| Branch | `gh issue develop N --checkout --name issue-N-<slug>` | default branch |
| Commits | `Refs #N` | `Closes #N` |
| Close keyword | PR body carries `Closes #N` (`gh pr create --body-file`) | the commit message |
| Review | `/code-review`; human merges `gh pr merge <PR> --squash --delete-branch` | `/code-review` on the diff |
| Close-out | after merge | after push |

The QA verdict marker lives on the issue in both modes; `/commit` reads it there and the hook reads the local mirror `.claude/qa/verdict-<branch>` that `/qa` writes alongside it.

## Verify gate

Nothing reaches `ready-for-agent` without a `Verified:` comment (what was checked against the repo, with evidence) or, for new sub-issues, the `to-tickets` fact-check gate, whose publish is that record. Promotion without either is a defect.

## Agent pickup protocol (`work-issue`)

1. **Choose.** A named issue wins. Otherwise the frontier:
   `gh issue list --state open --label ready-for-agent --search "no:assignee -label:feature -is:blocked" --json number,title,labels,createdAt,parent`
   `-is:blocked` counts only open blockers (a closed blocker stays in `blockedBy`, so never filter that client-side); the search index lags seconds behind a write. Prefer a sibling of an in-progress parent (the `parent` field), then P0 to P2, then oldest.
2. **Claim** before any other write: assignee + "Working:" comment.
3. **Read** `gh issue view N --comments`; the list view omits comments.
4. **Re-verify `Current state`** against today's repo; comment what changed before building.
5. **Build** at the agreed seam: TDD with isolated sub-agents for code, then `/qa --issue N`.
6. **Open a sub-issue** when a task outgrows the window, and replace its checklist line with the link.
7. **Tick checkboxes one at a time:** pull the body to a file, keep a `.orig` copy, flip one `- [ ]` to `- [x]`, assert `diff` shows exactly one changed line, then `gh issue edit N --body-file`. ACs tick only with evidence in hand.
8. **Blocked:** on information, swap to `needs-info`, post Triage Notes, release the claim. On an issue, add the native edge and release.
9. **Finish** via `/commit`, confirm `CLOSED`, post the close-out; last sibling triggers the parent cascade.

**Standing permission:** approving a parent's design note permits working through its sub-issues without a fresh "next" each time. A standalone ticket or a feature's first sub-issue starts only on the human's word. Agents stop at `needs-info` and at the live-check sub-issue. One sub-issue per context window.

## Close-out comment

Template: `docs/templates/closeout-comment.md`. Four lines: `Shipped:` (commit SHA or PR), `Proof:` (fenced command output), `Not covered:` (what this does not prove), `Learned:` (one line plus where filed, or "nothing new"). `/retro` harvests `Learned:` from `gh issue list --state closed --search "closed:>YYYY-MM-DD" --json number,title,comments`.

## QA verdict marker

`/qa --issue N` posts one comment whose first line is
`<!-- QA-VERDICT: APPROVED|NEEDS_FIXES|BLOCKED|BLOCKED SECURITY -->`.
`/commit` reads the latest marker on any `#N` it references: `NEEDS_FIXES` warns, `BLOCKED` stops, `BLOCKED SECURITY` refuses with no override. The hook enforces the last through `.claude/qa/verdict-<branch>`.

## Non-code work

Documents, research and decisions use the same flow. Put a `Proof:` line in the ticket instead of `Tests:` (the artifact and how it is checked). `/qa --issue` routes to `challenger` when the diff has no code.

## Agent signature

The `Agent signature` value in CLAUDE.md `## Workflow` is the first line of every agent-authored issue and comment (after the QA verdict marker, when there is one), because `gh` acts as the human's account. Empty value disables it.

## `gh` capabilities

Needs `gh` 2.96 or newer; `scripts/github/check_gh.sh` probes the version, auth, `--parent`, `--blocked-by` and the list JSON fields, and fails closed.

| Capability | Command |
|---|---|
| Parent/child | `gh issue create --parent`, `gh issue edit --add-sub-issue` |
| Blocking edges | `gh issue create --blocked-by`, `gh issue edit --add-blocked-by` |
| Close reasons, duplicates | `gh issue close --reason "not planned"`, `--duplicate-of` |
| Frontier excludes open blockers | search term `-is:blocked` |
| List fields | `gh issue list --json parent,blockedBy,subIssuesSummary` |
| Issue-linked branch | `gh issue develop N --checkout` |

Older `gh`: upgrade. There is no in-session fallback (`gh api` is denied by `settings.json` and the hook blocks GraphQL mutations by design).
