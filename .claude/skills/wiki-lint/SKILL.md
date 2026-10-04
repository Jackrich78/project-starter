---
name: wiki-lint
description: "Semantic lint of the docs/ wiki: a deterministic pre-pass plus one forked librarian judging contradictions, orphan pages, missing concept pages and stale claims; runs at /session-winddown when due. Use on \"wiki lint\", \"semantic lint\", \"check the docs for contradictions\", \"has the wiki drifted\", or when the last wiki-lint line in docs/log.md is over 14 days old. Fixes structural findings; proposes the rest."
type: skill
context: fork
agent: librarian
---

# Wiki lint

Two speeds. `scripts/wiki_lint.py` catches structural rot in CI. This skill catches what only a reader can: pages that disagree, concepts with no page, claims the repo disproves. Schema and rules: `docs/guides/knowledge-architecture.md`, `.claude/rules/wiki.md`.

You are the forked `librarian`: read-only tools plus Edit, no shell. The two blocks below were run for you before this prompt was built.

## Step 1: deterministic pre-pass (already run)

Output of `python3 scripts/wiki_lint.py --all --json`:

!`python3 scripts/wiki_lint.py --all --json || true`

If it says pyyaml is missing, stop and report `ESCALATION: pip install pyyaml`. If it reports errors, do step 3a for them before judging semantics: do not spend judgement on a structurally broken page.

## Candidate set (already computed)

Files under `docs/` and `.claude/skills/` changed in the last 14 days:

!`git log --since=14.days --name-only --pretty=format: -- docs .claude/skills | sort -u | grep -v '^$' || true`

Empty means nothing changed: say "no candidates, wiki quiet" and stop. Do not widen to the whole wiki unless the user asked for a full sweep.

## Step 2: judge

Read each candidate fully, plus every page it links to (one hop). Report only findings you can cite to `file:line`:

- **contradiction**: two pages make conflicting claims. Quote both.
- **gap**: a concept named on three or more pages (or by three or more candidates) with no page of its own. Name the pages that mention it and the home it should have, per the routing tree.
- **orphan**: a page nothing links to, or one whose `description` no longer matches its body. Say keep or delete.
- **stale claim**: a statement the repo disproves (a path, command, flag, file or count that no longer exists). Grep or Read the source to prove it; quote the evidence. A claim you cannot disprove is not a finding.

Be conservative. Pages disagreeing about taste is not a contradiction. "Might be outdated" without evidence is not a finding.

## Step 3: fix and propose

a. **Structural findings** (missing `type`, broken link with an obvious target, page missing from `docs/index.md`): fix with Edit, smallest change. Never invent a frontmatter value you cannot source.
b. **Everything else**: do not edit. Return a numbered list, each item `N. [kind] file:line: finding. Proposed fix: ...`, so the human can approve by number. A claim you disproved from the repo with no judgement call involved is fixed in this turn (`.claude/rules/wiki.md`).
c. **Log**: Edit `docs/log.md`, adding under today's date heading (create it newest-first if absent): `- **Update** — wiki-lint: N structural fixed, M findings proposed.` This line is the 14-day staleness stamp.

## Report

```
## Pre-pass
<summary line from wiki_lint>
## Fixed
- file:line: what
## Proposed (numbered)
1. [kind] file:line: finding. Proposed fix: ...
## Result
PASS | FAIL: <reason> | ESCALATION: <reason>
## Proposed memory entries
```

The orchestrator re-runs `python3 scripts/wiki_lint.py --all` after your edits and quotes the result: you cannot.

## Nudge convention

Suggest this skill when the newest `wiki-lint` line in `docs/log.md` is more than 14 days old or absent: at wind-down, after a retro, or after a bulk docs edit. One suggestion per session; never run it unasked.

## Failure modes

- Pre-pass block empty or not JSON: report `ESCALATION: pre-pass did not run`; do not judge blind.
- Candidate list very large (over 40 pages): judge the 40 most recently changed and say so.
- Finding needs a content decision: propose, do not edit.
