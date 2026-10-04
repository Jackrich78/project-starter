---
name: setup
description: One-time bootstrap of a cloned project-starter into your own project - fills CLAUDE.md and PROJECT.md, wires GitHub (repo, labels, templates), turns a roadmap into stub feature issues, makes the founding commit. Use on "set up this project", "first run", "/setup", or right after cloning. Idempotent; safe to rerun.
type: skill
disable-model-invocation: true
argument-hint: "[--step N] [--dry-run]"
---

# /setup

## Context

Run once after cloning, rerun any time. Every step checks its own marker and prints `ok` (done, nothing to do), `skip` (not applicable) or `do` (acting) before it touches anything. `--step N` runs one step. `--dry-run` prints what each step would do and writes nothing (no file edits, no `gh` writes, no commit). Ask at most the 6 questions below, one block, only for what you could not infer. Principles are not part of setup (see the end).

## Pattern

1. **Context** (marker: none, always runs). Infer from root `*.md`, `package.json` / `pyproject.toml` / `go.mod`, `git remote -v`, `gh auth status`, existing issues and labels. Ask only what is missing:
   - Q1 project name + one-liner (skip if inferred)
   - Q2 the problem, and for whom
   - Q3 the first 2-3 things to build
2. **Workflow** (marker: CLAUDE.md has no `<!-- pr | direct` comment left on the `Integration mode` line). Q4 integration mode `pr | direct`. Inference rule: propose `pr` if the repo is public or has more than one collaborator, else `direct`; the owner decides. Write it to CLAUDE.md `## Workflow` (the only place the mode is read from), plus Q6.
3. **Docs** (marker: CLAUDE.md contains no `<!-- CUSTOMIZE` and PROJECT.md vision has none). Using Q1-Q3 and the detected stack:
   - CLAUDE.md: replace the first `<!-- CUSTOMIZE -->` line with one sentence (what, for whom); fill `## Workflow`: the mode, and the `Areas (labels)` line as `area:a, area:b` (the single home for areas; `setup_labels.py` reads it); fill the Quick start commands (test, run).
   - PROJECT.md: title, frontmatter `version: 0.1.0`, Vision (3 sentences max), Current state (one paragraph). Roadmap is step 5. Keep PROJECT.md under 60 lines.
   - Identity: `package.json` `name` and `version: 0.1.0` (if the file exists); README first heading = the project name, CI badge owner/repo from `git remote get-url origin`.
   - `docs/system/current-priorities.md`: replace the three placeholder bullets with real lines (in flight: the founding commit; blocked: none; next: `/explore #<first parent>`) and bump `updated`. Until then the session primer prints a one-line notice instead of the body.
   - The template ships no sample content to delete. `docs/decisions.md` entries about the template's own development stay as history. Do not create DECISIONS, PRINCIPLES or feature folders.
4. **GitHub** (marker: `scripts/github/check_gh.sh` exits 0, `python3 scripts/github/setup_labels.py --dry-run` reports `0 to create`, and `.github/ISSUE_TEMPLATE/ticket.md` + `feature.md` exist).
   - Origin points at the template repo: `git remote rename origin upstream`.
   - No origin: ask Q5 visibility `private | public`, then `gh repo create <name> --source=. --remote=origin --<visibility>`.
   - Run `scripts/github/check_gh.sh` (gh 2.96+, authenticated, origin resolves). Fail closed: stop on non-zero.
   - Labels come from CLAUDE.md: Q6 area labels (propose 3-5 from the stack, accept defaults) are written to the `Areas (labels)` line (step 3); the script reads that line. Run `python3 scripts/github/setup_labels.py --dry-run`, show it, then rerun without `--dry-run` on a yes. Existing labels print as `update` by design. Flags: `--repo`, `--prune-defaults`.
   - Confirm the two issue templates exist; report if not.
   - `pr` mode only: PRINT, never run, the branch-protection `gh api` command (require a PR and the status check `validate` on the default branch). Say it is the owner's to run.
5. **Roadmap** (marker: `gh issue list --label feature --state all` is non-empty). Dispatch `tech-product-lead` (opus, per CLAUDE.md) with Q1-Q3, PROJECT.md and a scratch path under the session scratchpad it may Write the proposal to (in plan mode it cannot write and returns the body inline instead): propose at most 8 features in at most 3 phases, the smallest proof of the approach first. Show the list; the owner edits and approves (this is Q3's follow-through, not a new question). Then create one stub per feature: `gh issue create --label feature --label needs-triage --label enhancement --label P2`, body = goal, phase, why, and `spec: run /explore #N`. Never write acceptance criteria here. Write PROJECT.md `## Roadmap` as phase themes ending in `#N` links, nothing else (GitHub owns status).
6. **Librarian gate** (always). Dispatch `librarian` with: cross-references resolve; no `<!-- CUSTOMIZE` left in the sections steps 3 and 5 filled; `## Workflow` present; every `#N` in PROJECT.md resolves (`gh issue view N`); `python3 scripts/wiki_lint.py --all` clean. Verify its claims on disk before reporting.
7. **Founding commit** (marker: `git log --oneline --grep='^chore: initialize .* from project-starter'` is non-empty, so reruns after later commits still print `ok`). Ask before pushing. Stage by explicit path from `git status --short` (never `git add -A`; flag `.env*`, `*.pem`, `*.key`, `*credentials*`, `secrets*`), `git commit -m "chore: initialize <name> from project-starter"`, `git push -u origin HEAD`, `gh run watch`. Then print the smoke checklist and the next step.

## Smoke checklist (every line must pass)

```
npm test                                         exit 0
scripts/github/check_gh.sh                       exit 0
python3 scripts/github/setup_labels.py --dry-run   0 to create
git ls-files .claude/skills/build/SKILL.md        non-empty
gh issue list --label feature                    N issues
python3 scripts/wiki_lint.py --all                exit 0
gh run watch                                     validate: success
Next: /explore #<first parent>
```

Close by printing: "Principles: run `grilling` on PROJECT.md when ready; the three template ones stay until then."

## Example

`/setup --dry-run` on a fresh clone prints `do` for steps 1-7 with the exact command each would run, asks no writes, exits.

## Anti-patterns

- Asking more than 6 questions, or re-asking what the repo already answers.
- Writing a spec or acceptance criteria into a stub issue; `/explore` owns the spec.
- Running the branch-protection command, force-pushing, or pushing without the owner's yes.
- Reading the integration mode from anywhere but CLAUDE.md `## Workflow`.
- Checking the founding-commit marker against HEAD (a later commit would re-run step 7).
- Restating issue status in PROJECT.md.
