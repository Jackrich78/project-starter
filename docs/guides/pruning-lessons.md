---
type: guide
title: Pruning lessons
description: Generic lessons from reorganising a large wiki and enforcing a contract on it - how checks lie, how counts lie, when a rule can never go green - each paired with the mechanism in this template that prevents recurrence.
tags: [wiki, linting, verification, pruning]
---

# Pruning lessons

Read before any docs reorganisation or before adding a lint rule. Each lesson was paid for once; the right column is what stops it recurring here.

## 1. The failure renders as success

Nearly every defect had one shape: the broken thing kept reporting green. A deleted spec breaks no test when tests cite its ids as bare strings; a kill switch that defaults to "off" blocks writes while reporting nothing; a search that quietly falls back to one leg still returns results; a lint that checks a field is present passes when the value is wrong; a workflow whose trigger paths exclude the changed files never starts.

**Design the test as "how would this look if it were broken?"** If the answer is "identical", the green is decoration.

| Prevention here |
|---|
| Corpus tests that include near-misses and are seen red (`docs/system/testing-rules.md` 1-2); Layer 0 wiring tests; lint checks the value of `type`, not its presence |

## 2. Verify the verification

Each of these produced a confident wrong "clean": a linter run with a path flag that silently linted a default set; `git stash` as a "before" baseline (it can miss staged renames); a `grep` for the wrong id prefix reading zero hits as "omitted"; a fixed-size `sed` window that caught the next function; two parallel agents each measuring one shared tree and claiming the other's fixes; a link count that ignores citations written as bare paths.

A check sees only what it was built to see. Before trusting a clean run, say what it does *not* look at. Baseline with `git worktree add --detach <tmp> HEAD`, measure once at the end across the combined tree.

| Prevention here |
|---|
| `scripts/wiki_lint.py --all` is the only CI invocation (never a partial path); the reviewer re-runs it, not the author's summary |

## 3. Rules validated on one sample do not transfer

A "highest-yield" structural rule held for one of eight directories that fit it; same naming scheme, three different underlying relationships. A rule that failed on inspection in every batch is not a rule. An exception can swallow its own rule: when 36 of 39 files carry the exemption label, the label is stale, and the real discriminator is elsewhere.

| Prevention here |
|---|
| Pilot a rule on a measured sample before enforcing; the metric is "violations found that a human agrees are real" |

## 4. Discriminate by inbound reference, not by filename

A rule that archived `research-*.md` by name would have moved 86 files that were still cited by live code and specs, and nothing would have failed loudly enough to notice. Before moving or deleting a file, search for its basename everywhere (`docs/`, `.claude/`, `scripts/`, `tests/`). Move links in both directions: links *to* the file and the file's own relative links *out*.

| Prevention here |
|---|
| Broken and orphan links are lint warnings; `post_tool_use.py` nudges when a `docs/` page is missing from `docs/index.md` |

## 5. Deletion is recoverable; "what was rejected" is not

Git history recovers any deleted file, so the cost of over-deleting is discoverability, which makes aggressive pruning defensible. The exception is the one thing code cannot reconstruct: which options were tried and rejected, and why. Re-exploring recovers the option, never the fact that it was already rejected. Deleting binaries reclaims no disk; only a history rewrite does.

| Prevention here |
|---|
| `docs/decisions.md` one-liners carry a `REJECTED <option>: <why not>` clause, logged in the turn the choice is made |

## 6. Free-text fields break automation silently

A human-written string that code depends on drifts: dozens of distinct values in a field the archival rule matched with a `startswith`, so it recognised a fraction of cases; an identifier prefix that grew ten variants. Measure the blast radius before enforcing: an allowed-values check sounded expensive and cost a handful of files, while widening CI to a tree with hundreds of standing errors would have turned every PR red on day one.

| Prevention here |
|---|
| Closed taxonomies: `type` values in `.claude/rules/wiki.md`, state labels in `issue-flow.md` (a test compares the label script to the doc) |

## 7. Find what exists before building

Thirteen capabilities turned out to be built but unreachable in a single day: a contradiction detector that ran once, an experiment plan marked "ready to run" and never run, a generated index made illegible by a free-text field, and an agreed contract that stayed `draft` with no enforcement. An instruction that lives where nothing loads it never runs. A spec that does not name what it reuses has not been researched yet.

| Prevention here |
|---|
| Hard-won rule 5 (CLAUDE.md); `grep -rl` before writing a test; skills are listed by `description`, the only trigger surface |

## 8. Sub-agents earn their keep by refusing

Agents refused a premise in their own brief several times and were right each time: "dead" code that was cited, a rule that held for one case in eight, a "spec" that was a decision log. Brief them to disprove, not to comply, and still check the claim: the one agent whose method was dictated was the only one whose numbers survived independent checking unchanged.

| Prevention here |
|---|
| `challenger` and `qa-reviewer` assume the input holds a wrong claim and return claim-versus-evidence tables |

## 9. Two pages agreeing is not evidence either is right

An agent saw two internal pages disagree, resolved the conflict toward the louder one, and propagated a claim that an external source had withdrawn. A contradiction between internal pages says one is wrong, not which. Resolve toward the external source or the owner. When a claim is withdrawn, say so on the page: a silent deletion reads as staleness and people re-derive the same wrong conclusion.

| Prevention here |
|---|
| `wiki-lint` reports contradictions as questions for a human; CLAUDE.md "verify before disbelieving" and "a wiki claim you observe to be false is fixed in that turn" |

## 10. A count is not a fact until you know what it counts

A "226-hit index" was a grep hit count for a string, and the file held one entry. A page quoted a number of folders that was the validator's total warning count. Name the unit, then re-derive the number with a command that counts that unit.

| Prevention here |
|---|
| Counts in docs are generated or omitted; rosters and inventories are injected, not typed |

## 11. A rule whose precondition can never be met is worse than no rule

A line cap that punished the folders that complied, a size rule whose precondition contradicted an earlier decision, a closed allowlist that cost a hundred moves to buy three renames. A rule that can never go green is a permanent red mark everyone learns to ignore. **Measure the backlog first; delete the rule rather than grant an exemption list.**

## 12. Warning or error is decided by the backlog, not by confidence

The level asks whether the violations can reach zero: a rule whose backlog is already zero goes straight to error (a warning with no standing violations enforces nothing); one with a reachable backlog starts as a warning and graduates by a one-word change; one that can never clear is deleted. The same arithmetic scopes CI: do not add a path to a lint step while it carries hundreds of standing errors, and leave a comment saying so, so no one "fixes" the omission. An advisory check that cannot fail is removed.

| Prevention here |
|---|
| Wiki size cap: over-cap pages carry an explicit `# SPLIT-DEFERRED <reason>` marker or fail (`.claude/rules/wiki.md`) |

## 13. Declaring beats moving

A required one-line purpose per folder cleared a whole backlog with zero file moves, where a closed allowlist wanted about a hundred and forty. The declarations captured facts that existed nowhere else (a tool that hard-codes a directory name, iterations that are siblings for comparison). A purpose line that restates the folder name passes the check and teaches a cold agent nothing: the obligation to write it is the mechanism.

## 14. Verification costs speed, honestly

A careful pass over a few folders per session finds something damaging in nearly every batch; a pattern-matching pass over many would be several times faster and would have shipped those. The lever for going faster is accepting less verification per batch. That is a human decision, not a default to drift into.
