---
type: guide
title: "The wiki schema"
description: "What a conformant wiki page is, the frontmatter keys, the type taxonomy, and the routing tree for where a new fact goes; read before adding, moving or querying a page."
tags: [wiki, schema, routing, lint]
---

# The wiki schema

The routing and structure authority for `docs/`. Read it before adding, moving or querying a page. `.claude/rules/wiki.md` is the short form that loads when you touch `docs/`; `scripts/wiki_lint.py` enforces the mechanical part.

## What "conformant" means

Three rules, all checked by `scripts/wiki_lint.py`:

1. Every page under `docs/` (and every `.claude/skills/*/SKILL.md`) has parseable YAML frontmatter.
2. The frontmatter has a `type` from the taxonomy below.
3. The page is at most 300 lines, or carries a `# SPLIT-DEFERRED <reason>` line (then lint warns instead of failing).

A page with only `type: guide` is conformant. Everything else is optional richness.

## Frontmatter

| Key | Status | Meaning |
|---|---|---|
| `type` | required | Kind of page; must be in the taxonomy. |
| `title` | recommended | Human name, independent of the filename. |
| `description` | recommended | One sentence an agent uses to decide whether to open the page. Feeds the index. |
| `tags` | recommended | Keywords for grep. |
| `status` | optional | `draft`, `stable` (default) or `deprecated`. Deprecated pages are kept, not deleted. |
| `decay_tier` | optional | How fast the page goes stale: `reference` 365d, `process` 182d, `active` 91d, `figures` 30d. An unknown value is an error, because a typo silently disables the staleness check. |
| `stale_after` | optional | `YYYY-MM-DD`. An explicit override: wins over `decay_tier`. A warning once passed. |
| `updated` | optional | `YYYY-MM-DD` of the last meaningful change. |
| `supersedes` | optional | Path (or list) of the page(s) this one replaces. The target must exist (error otherwise). Resolved relative to the page, then the repo root, then `archive/`. |

Staleness for a tiered page is derived, so it moves when the page moves: `max(updated, last git commit date) + interval`. Staleness is always a warning, never a failure.

## Taxonomy

| `type` | Home | Use for |
|---|---|---|
| `domain-doc` | `docs/system/` | How a part of the system works (a fact about this project). |
| `guide` | `docs/guides/` | A practitioner how-to; steps a person or agent follows. |
| `reference` | `docs/reference/` | Pointer lists, link collections, lookup tables. Also skill-only assets in `.claude/skills/<x>/references/`. |
| `decision-record` | `docs/decisions.md`, `docs/archive/` | The decision log and superseded full entries. |
| `overview` | any directory | A map of a subject that mostly points elsewhere. |
| `template` | `docs/templates/` | A shape to copy (close-out comment, research memo). |
| `skill` | `.claude/skills/<name>/SKILL.md` | A skill file. |
| `research` | `docs/guides/` or `docs/system/` | A finished investigation worth keeping: question, answer, sources, confidence. |
| `qa-report` | `docs/system/` | A QA or audit result worth keeping beyond the issue it was found on. |

Adding a type means editing `ALLOWED_TYPES` in `scripts/wiki_lint.py`, this table and `.claude/rules/wiki.md` in one change.

## Reserved filenames

- `index.md`: a directory's progressive-disclosure listing. Headed sections of bullet links, each with a one-line description. No `type` required.
- `log.md`: append-only, newest first. ISO date heading, then a bold verb per line (**Creation**, **Update**, **Deprecation**). No `type` required.

Never name a concept page `index.md` or `log.md`. Pages under any `archive/` directory are not linted: an archive records what a page said when it was retired.

## Linking

Use relative paths (`../system/issue-flow.md`). Links inside code fences and inline code are examples, not references, and are ignored. A broken link is a warning. Every page under `docs/` (except `index.md`, `log.md` and `archive/`) must be linked from `docs/index.md`, or lint warns "not indexed". New page means a line in `docs/index.md` and a line in `docs/log.md`, in the same change.

## Size cap

300 lines per page. A page that must exceed it carries `# SPLIT-DEFERRED <reason>` on its own line; an unmarked over-cap page is an error. The marker is a debt note, not a licence: it still warns on every run.

## Ingest: where a new fact goes

Route by kind of fact. First match wins; one home per fact.

| The fact is… | It goes in |
|---|---|
| A system fact (how something works here) | `docs/system/<topic>.md` (`domain-doc`) |
| A how-to someone will follow | `docs/guides/<topic>.md` (`guide`) |
| A choice between options | `docs/decisions.md`, one line, rejected option included |
| A pointer list or lookup table | `docs/reference/` |
| An asset only one skill uses | `.claude/skills/<x>/references/<topic>.md`; the SKILL.md says "Read `references/<topic>.md`" |
| Current sprint state, a confirmed preference | Claude Code auto-memory (outside the repo; see `docs/system/memory-systems.md`) |
| A sub-agent's method | `.claude/agent-memory/<name>/MEMORY.md` (methods only; the orchestrator writes it) |
| An operating rule or convention | `CLAUDE.md` or `.claude/rules/`, per the layer table in `CLAUDE.md` |
| Work state: status, a blocker, a next step | The GitHub issue. Never a page. |

Nothing fits? Ask whether it needs storing at all, or whether it is derivable from the code. Then add the page to `docs/index.md` and `docs/log.md`.

Two standing rules:

- **One home per fact.** Everywhere else points to it with a link; skills and agents point here, never restate. Two copies drift, and the stale one gets believed.
- **The ~3x rule.** If you have prompted the same workflow about three times, make it a skill instead of a fourth prompt.

## Query: grep first, disclose progressively

1. Start at `docs/index.md`; read the one-line descriptions before opening anything.
2. `grep -ril <term> docs/` for a term you can name; read `description:` before the body.
3. No embeddings and no vector store for the wiki. Grep over a small, well-described corpus beats retrieval infrastructure you have to keep in sync.
4. A fact you cannot cite to a page is a fact to go and check.

## Lint: two speeds

- **Deterministic, in CI on every PR:** `python3 scripts/wiki_lint.py --all` (add `--json` for tools, `--strict` to fail on warnings). Structural rot is an error and exits 1; links and staleness are warnings and exit 0. It needs `pyyaml`.
- **Semantic, human-triggered:** the `wiki-lint` skill runs the deterministic pass, then one forked `librarian` reads recently changed pages for what only a reader can catch: contradictions, orphans, concepts used often with no page, claims the repo disproves. Run it about every 14 days. If the newest `wiki-lint` line in `docs/log.md` is over 14 days old (or absent), suggest a run at wind-down.
- **Outer loop:** the same trap hit twice is itself a trigger for an ad hoc pass on the affected pages.

## A false page is fixed in the turn you notice it

Do not note it, queue it, or answer it with a proposal for a new lint. Edit the page, add a `docs/log.md` line, and say so in your reply. A durable fact established in conversation lands on its page in that same conversation.
