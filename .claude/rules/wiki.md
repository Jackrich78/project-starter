---
paths:
  - docs/**
---

# Wiki conventions (`docs/`)

Schema and routing authority: `docs/guides/knowledge-architecture.md`. `scripts/wiki_lint.py --all` enforces the structural rules in CI.

- **Frontmatter is required** with a `type` from the taxonomy (`domain-doc`, `guide`, `reference`, `decision-record`, `overview`, `template`, `skill`); `title`, `description` (one sentence an agent uses to decide whether to open the page) and `tags` are recommended. Optional: `status: draft|stable|deprecated`, `decay_tier`, `stale_after`, `updated`, `supersedes` (target must exist).
- **Reserved filenames:** `index.md` (headed sections of bullet links + one-line descriptions) and `log.md` (append-only, newest first, bold verb). Never name a concept page either.
- **Size cap 300 lines per page.** A page that must exceed it carries `# SPLIT-DEFERRED <reason>` on its own line; an unmarked over-cap page fails lint.
- **One home per fact.** Before writing, route by *kind of fact* (system fact → `system/`, how-to → `guides/`, choice → `decisions.md`, pointer list → `reference/`). Skills and agents point here, never restate.
- **Decisions:** one line in `docs/decisions.md`, `YYYY-MM-DD — DECISION — why — REJECTED <option>: <why not> — <link>`, in the turn the choice is made.
- **A page you observe to be false is fixed in that turn.** Do not note it, queue it, or propose a new lint instead.
- **Links** are relative paths; broken or orphan links are lint warnings, never silent.
- **Add every new page to `docs/index.md`** and a line to `docs/log.md` in the same change.
