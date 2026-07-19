# Template Sync Guide

How to propagate hook and command changes from `ai-workflow-starter` to downstream projects.

## Quick Reference

```bash
# Sync to public template (default)
./sync-downstream.sh ~/dev/project-starter

# Sync to any project
./sync-downstream.sh ~/dev/my-project

# Or use the /sync command inside Claude Code
/sync ~/dev/my-project
```

## What Gets Synced

| Directory | Strategy | Detail |
|-----------|----------|--------|
| `.claude/hooks/` | Full replace (`--delete`) | All hooks come from template. Any extra files in target are removed. |
| `.claude/commands/` | Overwrite shared, preserve project-specific | Template commands overwrite same-named files. Project-only commands (e.g. `apply.md`, `prep.md`) are untouched. |

## What Does NOT Get Synced

These are always project-specific — update manually if needed:

- `CLAUDE.md` — including the **model-tier policy** (`## Model Defaults` section); the authoritative tier table lives there and is intentionally not synced (one home, no drift risk).
- `.claude/agents/`
- `.claude/settings.json`
- `.claude/logs/`
- `.claude/skills/`

## Per-Project Workflow

For each downstream project:

```bash
# 1. Run the sync
./sync-downstream.sh ~/dev/<project>

# 2. Review what changed
cd ~/dev/<project>
git diff .claude/

# 3. Reject any file you don't want overwritten
git checkout -- .claude/commands/<file>

# 4. Commit
git add .claude/ && git commit -m "chore: sync template hooks and commands"
```

**Time per project:** ~1 minute (scan the diff, commit).

## Reviewing Command Diffs

The review gate shows a `--stat` summary like:

```
 .claude/commands/build.md    | 107 +++++++++++++++--
 .claude/commands/prime.md    | 268 +++++++-----------
 3 files changed, 150 insertions(+), 100 deletions(-)
```

**What to look for:**
- Large rewrites to `prime.md` or `build.md` — these sometimes reference project-specific paths
- Any command the project has customized — the template version will overwrite it
- New commands (no conflict) — these are always safe

**When in doubt:** `git diff .claude/commands/<file>` to see the full diff, then decide.

## Non-Git Targets

If the target isn't a git repo, the script warns you and skips the review gate. Files are synced but there's no undo. Verify manually.

## Bulk Sync (All Unfixed Projects)

To find which projects still have unfixed hooks:

```bash
for dir in ~/dev/*/; do
  hook="$dir.claude/hooks/post_tool_use.py"
  if [ -f "$hook" ] && grep -q 'input_data.get("tool",' "$hook" 2>/dev/null; then
    echo "UNFIXED: $dir"
  fi
done
```

Then sync each one. Don't batch-commit — review each project's diff individually.
