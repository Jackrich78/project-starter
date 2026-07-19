---
updated: 2026-03-13T00:00:00Z
---

# Two-Remote Sync Guide

How to maintain a private repo (source of truth) alongside a public open source repo.

## Model Overview

```
Private repo (origin)          Public repo (public)
├── Full git history            ├── Single clean commit
├── All files (agents,          ├── Core harness files only
│   skills, features, demos)    ├── No personal content
├── Personal content            └── No history leak risk
└── Source of truth
```

- **Private repo** = your working repo with full history, all files, personal content
- **Public repo** = sanitized snapshot published as a single commit per release
- **Flow is strictly one-way**: private → public (never pull back)

## How It Works

The sync uses `git archive HEAD` to export a clean copy of committed files into a
disposable temp directory, applies the exclusion blacklist, then pushes as a fresh
single-commit repo.

**Why `git archive` instead of squash branches:**
- Only exports **committed tracked files** — untracked files cannot accidentally appear
- Deterministic: output is exactly what's in git at that commit, not what's on your filesystem
- Force-push replaces the entire public repo history on each sync — any mistake is
  corrected by re-running the workflow
- Your private repo is **never touched** by deletions — all cleanup happens in `/tmp/`

## Setup (One-Time)

1. Create an empty public repo on GitHub (no README, no .gitignore)
2. Add it as a second remote in your private repo:
   ```bash
   git remote add public git@github.com:YOUR_USERNAME/project-starter.git
   git remote -v  # verify both remotes listed
   ```

## Exclusion List

`.github/public-exclude.txt` is the authoritative record of what stays private.
Edit this file when you add new private content (brand skills, personal retros, etc.).

## Release Gate Data Files

Three files under `.github/` drive the blocking gate in step 7 of the push
workflow (`scripts/public_release_gate.sh`):

- **`.github/public-exclude.txt`** — the blacklist of paths deleted from the
  temp export before the gate runs (step 4 above).
- **`.github/pii-patterns.txt`** — content patterns the gate greps for
  (`grep -rInE`) across whatever survives the blacklist: one POSIX extended
  regex per line, `#` comments allowed. Covers known leak categories (Spanish
  DNI/NIE numbers, brand/name tokens, emails, secrets, absolute local paths).
  It's a blacklist, not a smart filter — known-safe false positives (e.g.
  `user@example.com` in test fixtures) still hit and get waived individually.
- **`.github/release-waivers.txt`** — the only way past a gate hit. One line
  per waiver: `path:pattern-or-rule # reason`, where `path` is relative to
  the export tree root and `pattern-or-rule` is either the exact regex line
  from `pii-patterns.txt` that matched or one of the gate's file-type rule
  IDs (`filetype:handover`, `filetype:bak`, `filetype:agentdb`,
  `filetype:env`, `filetype:archive`, `filetype:workspace`,
  `filetype:demos`, `filetype:image`). Every applied waiver prints on every
  run, so suppressions stay visible instead of silently accumulating. There
  is no bypass flag — an un-waived hit always exits non-zero.

Update `pii-patterns.txt` when a new leak category shows up (new brand, new
secret format); update `release-waivers.txt` only for confirmed false
positives, never to suppress a real leak.

`pii-patterns.txt` and `release-waivers.txt` are maintainer-private — they're
listed in `public-exclude.txt` and never ship in the public snapshot, because
`pii-patterns.txt` itself enumerates the personal tokens it protects. A fresh
clone (or the public template) won't have either file. Start from
**`.github/pii-patterns.example.txt`**, which ships publicly with the same
structure and placeholder patterns (`YOUR_NAME`, `YOUR_BRAND`, example ID
formats, no real personal tokens) — copy it to `pii-patterns.txt` and fill in
your own tokens before running the release gate.

## Push Workflow

Run this from your private repo root whenever you want to sync to public.
**Use bash, not zsh** — step 4's blacklist deletion relies on bash expanding
glob characters (e.g. `docs/features/FEAT-*`) after variable substitution;
zsh does not do this by default and will silently skip those deletions.

```bash
# 1. Ensure you're on main and up to date
git checkout main && git pull origin main

# 2. Fresh temp dir
rm -rf /tmp/project-starter-release && mkdir /tmp/project-starter-release

# 3. Export committed files — NO untracked files, NO .git history
git archive HEAD | tar -x -C /tmp/project-starter-release

# 4. Apply the blacklist (deletes from temp copy only — private repo is untouched)
while IFS= read -r pattern; do
  [[ -z "$pattern" || "$pattern" == \#* ]] && continue
  rm -rf /tmp/project-starter-release/$pattern
done < .github/public-exclude.txt

# 5. Handle glob patterns (explicit filenames for safety)
rm -f /tmp/project-starter-release/docs/system/retro-*.md

# 5b. Apply public-version overrides (see "Observability Sync Boundary") —
#     files where the public repo keeps its own simpler version instead of
#     the internal one (v1 send_event.py / init_db.py, minimal settings.json)
cp -R .github/public-overrides/. /tmp/project-starter-release/
rm -rf /tmp/project-starter-release/.github/public-overrides

# 6. Sanity check — count files and review manifest
find /tmp/project-starter-release -type f | wc -l
find /tmp/project-starter-release -type f | sort

# 6b. Doc-count drift check — hand-written agent/command/skill counts rot
scripts/check_doc_counts.sh --strict

# 7. Public release gate — BLOCKING, no bypass flag. Every hit must be fixed
#    or waived in .github/release-waivers.txt before continuing to step 8.
scripts/public_release_gate.sh /tmp/project-starter-release

# 8. Push as a fresh single-commit repo (force-push replaces entire public history)
cd /tmp/project-starter-release
git init
git branch -m master main 2>/dev/null || true
git add .
git commit -m "feat: release vX.Y.Z"
git remote add origin git@github.com:YOUR_USERNAME/project-starter.git
git push origin main --force

# 9. Verify
cd /tmp && git clone https://github.com/YOUR_USERNAME/project-starter.git verify-clone
cd /tmp/verify-clone && npm test

# 10. Clean up temp dirs
rm -rf /tmp/project-starter-release /tmp/verify-clone
```

## Reviewing Before Push

Always do a manual review of the file manifest (step 6) before pushing. Key checks:

**Must be present:**
- `.claude/agents/` — all agent definitions
- `.claude/commands/` — all commands (except any in exclude list)
- `.claude/skills/` — generic skills only
- `docs/system/` — architecture and setup docs
- Root files: `CLAUDE.md`, `README.md`, `PROJECT.md`, `CLAUDE.md`, `LICENSE`

**Must NOT be present:**
- Any `docs/features/FEAT-*/` directories
- Brand-specific skills listed in `public-exclude.txt`
- Runtime files: `agent.db`, `security.log`, `session-state.json`
- Any credentials, API keys, or tokens

## What Goes Public vs Private

| Content | Public? | Reason |
|---------|---------|--------|
| `.claude/agents/` | Yes | Core agent definitions |
| `.claude/commands/` (except `demo.md`) | Yes | Core workflow commands |
| `.claude/skills/` (generic skills) | Yes | Reusable skill patterns |
| `docs/system/` | Yes | Architecture & setup docs |
| `stacks/` | Yes | Deployment scaffolding |
| `test/`, `.github/` | Yes | Test infrastructure |
| `CLAUDE.md`, `PROJECT.md` | Yes | Template versions |
| `.claude/skills/[your-brand]/` | No | Brand-specific assets |
| `docs/features/FEAT-*` | No | Personal feature docs |
| `workspace/` | No | Personal working files |
| `docs/research/` | No | Personal notes |
| `.env`, credentials, API keys | No | Secrets |

## Pulling from Public

**Never pull from the public repo into your private repo.** The histories are divergent
(single squash commit vs full history) and merging will create conflicts.

If external contributors submit PRs to the public repo:
1. Review the PR on GitHub
2. Cherry-pick or manually apply the changes to your private repo
3. Push the next release as usual (which includes those changes)

## Observability Sync Boundary (Internal-Only Scaffolding)

`.claude/hooks/send_event.py` and `.claude/logs/init_db.py` contain v2
additions built for the owner's private observability/eval project:
`project_name`/`.env` loading, transcript persistence and archival
(`_persist_representation`, `_archive_transcript`), `SubagentStart` /
`SubagentStop` / `PostToolUseFailure` wiring, and the `agent_id` /
`parent_session_id` columns.

These are **internal-only** and must never propagate to the public
project-starter repo via `/sync` or this two-remote-sync process — the
public repo keeps its own minimal v1 `send_event.py`. Only genuine bug fixes
in the shared v1 surface should flow across; the v2 additions are marked
with a header comment in `send_event.py` itself as a reminder.

**Enforcement:** `.github/public-overrides/` holds the public versions of
these files (v1 `send_event.py`, v1 `init_db.py`, and a `settings.json`
without the v2 hook wiring). Step 5b of the push workflow copies them over
the export tree, so the boundary is applied mechanically on every release —
not from memory. When a genuine bug fix lands in the shared v1 surface,
update the copy in `public-overrides/` too. See also
`.claude/skills/template-sync/SKILL.md`, which documents the same boundary
for the `/sync` command (a separate propagation path from this guide's
`git archive` release process).

## Maintenance

When you add new private content, update `.github/public-exclude.txt` before the next
sync. The exclude file itself goes public — it's transparent to contributors about scope.
Update `.github/pii-patterns.txt` when a new leak category appears.
