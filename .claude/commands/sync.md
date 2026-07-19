---
description: Sync template hooks and commands to downstream projects
user_invocable: true
---

# /sync — Template Propagation

Sync `.claude/hooks/` and `.claude/commands/` from this template to a downstream project.

**What gets synced:**
- `hooks/` — full replace (`--delete`), all hooks come from template
- `commands/` — overwrite shared, preserve project-specific (review gate before commit)
- `agents/` — manifest-controlled copy: only files listed in `.claude/agents/.template-manifest` are copied
- `.claude/settings.template.json` — reference copy for diffing against the target's own `settings.json`

**What does NOT get synced:** CLAUDE.md, `.claude/settings.json` (never overwritten), `.claude/logs/`, `.claude/skills/`, `docs/guides/`

## Instructions

Target: $ARGUMENTS (default: `~/dev/project-starter`)

1. Verify we're in `ai-workflow-starter` — check that `sync-downstream.sh` exists in the current working directory. If not, abort with a clear message.

2. Resolve the target path:
   - If `$ARGUMENTS` is provided, use it
   - Otherwise default to `~/dev/project-starter`

3. Run the sync script:
   ```bash
   ./sync-downstream.sh <target>
   ```
   The script shows a dry-run preview first, then performs the actual sync.

4. Show the diff to the user:
   ```bash
   cd <target> && git diff .claude/
   ```

5. Ask the user to confirm, then commit:
   ```bash
   cd <target> && git add .claude/ && git commit -m "chore: sync template hooks and commands"
   ```

6. Ask: "Sync to another project?" — if yes, repeat from step 2 with the new path.

## Reference

See `.claude/skills/template-sync/SKILL.md` for detailed sync rules and conflict handling.
