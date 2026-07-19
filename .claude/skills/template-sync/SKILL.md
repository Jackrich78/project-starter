---
name: template-sync
description: Sync template infrastructure (hooks, commands) from ai-workflow-starter to downstream projects. Use when changes are made to .claude/hooks/ or .claude/commands/ in the template repo and need propagating to project-starter (public template) or downstream projects. Invoked via /sync command.
---

# Template Sync

## What Gets Synced

| Directory | Strategy | Rationale |
|-----------|----------|-----------|
| `.claude/hooks/` | Full replace (`--delete`) | All hooks come from template; no project customisation |
| `.claude/commands/` | Overwrite shared + preserve project-specific (no `--delete`) | Projects have their own commands (e.g. `apply.md`, `prep.md`). Shared commands are overwritten — review gate lets you reject individual files via `git checkout`. |
| `.claude/agents/` | Manifest-controlled copy (no `--delete`) | Only files listed in `.claude/agents/.template-manifest` are copied to the target; the manifest itself is copied alongside them. Project-only agents not in the manifest are left untouched. |
| `.claude/settings.template.json` | Reference copy | Copied as-is for the target to diff against its own `.claude/settings.json`; the live `settings.json` is never overwritten. |

## What Does NOT Get Synced

- `CLAUDE.md` — always project-specific
- `.claude/settings.json` — project-specific matcher config, never overwritten (diff against the synced `settings.template.json` to adopt new settings manually)
- `.claude/logs/` — per-project observability data
- `.claude/skills/` — project-specific learned patterns
- `docs/guides/` — excluded from sync

## Observability Sync Boundary (Internal-Only Scaffolding)

`.claude/hooks/` syncs as a full replace, but `.claude/hooks/send_event.py`
(and `.claude/logs/init_db.py`, which isn't synced by this skill but shares
the same schema) carry v2 additions built for the owner's private
observability/eval project: `project_name`/`.env` loading, transcript
persistence and archival (`_persist_representation`, `_archive_transcript`),
`SubagentStart` / `SubagentStop` / `PostToolUseFailure` wiring, and the
`agent_id` / `parent_session_id` columns.

**These must never propagate to the public `project-starter` target.** When
syncing to `project-starter`, the public repo keeps its own minimal v1
`send_event.py` — only genuine bug fixes in the shared v1 surface should
flow across. Downstream *private* projects (not `project-starter`) may
receive the v2 file as-is since they aren't public. See the matching note in
`docs/guides/two-remote-sync.md` and the header comment on the v2 block(s)
in `send_event.py` itself.

## SOP

1. Make changes in `ai-workflow-starter` (the source of truth)
2. Run `/sync` (or `./sync-downstream.sh <target>` directly)
3. Review `git diff .claude/` in the target project
4. If project has modified a template-origin file: review diff carefully, merge manually if needed
5. Commit: `git add .claude/ && git commit -m "chore: sync template hooks and commands"`
6. Repeat for each downstream project

## Default Target

`~/dev/project-starter` — the public template. Sync here first, then to active projects.

## Conflict Handling

- **Template file modified locally:** The diff will show changes. Review and decide — accept template version or manually merge.
- **Project-specific command with same name as template command:** Template version overwrites. Rename the project command first if needed.
- **New hook files in project:** These shouldn't exist — hooks are template-managed. The `--delete` flag removes them.
