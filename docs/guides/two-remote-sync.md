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

## Push Workflow

Run this from your private repo root whenever you want to sync to public:

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
  rm -rf "/tmp/project-starter-release/$pattern"
done < .github/public-exclude.txt

# 5. Handle glob patterns (explicit filenames for safety)
rm -f /tmp/project-starter-release/docs/system/retro-*.md

# 6. Sanity check — count files and review manifest
find /tmp/project-starter-release -type f | wc -l
find /tmp/project-starter-release -type f | sort

# 7. Privacy greps (all must return zero hits before pushing)
grep -ri "YOUR_BRAND\|YOUR_NAME" /tmp/project-starter-release --include="*.md" --include="*.json"
grep -ri "FEAT-0[0-9][0-9]" /tmp/project-starter-release --include="*.md"
grep -ri "/Users/YOUR_USERNAME" /tmp/project-starter-release --include="*.md"
grep -ri "sk-\|api_key\s*=\|password\s*=" /tmp/project-starter-release --include="*.md" --include="*.json"

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

## Maintenance

When you add new private content, update `.github/public-exclude.txt` before the next
sync. The exclude file itself goes public — it's transparent to contributors about scope.
