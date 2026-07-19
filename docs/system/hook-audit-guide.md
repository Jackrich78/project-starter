# Hook Audit & Fix Guide

**Created:** 2026-03-13
**Purpose:** Reference for auditing and fixing Claude Code hooks across projects that share the same hook layout.

---

## How to Use This Guide

1. Open this in a session alongside the project you want to audit
2. Compare each hook file against the "Correct Pattern" sections below
3. Apply the minimal fixes shown — don't rewrite hooks from scratch

---

## Bug A — `post_tool_use.py`: Wrong Payload Key Names

**Symptom:** Auto-formatting (Prettier, Black, etc.) never runs after Edit/Write operations. No visible error — the hook silently exits.

**Root cause:** The hook reads keys that don't exist in the Claude Code payload.

### How to Verify

Check lines near the top of `main()` where stdin JSON is parsed. Look for these incorrect keys:

```python
# BROKEN — these keys don't exist in the payload
tool_name = input_data.get("tool", "")
params = input_data.get("params", {})
```

### Correct Claude Code Hook Payload (all hook types)

```json
{
  "session_id": "string",
  "hook_event_name": "PreToolUse | PostToolUse | PreCompact | Stop",
  "tool_name": "Bash | Read | Write | Edit | Glob | Grep | Task | ...",
  "tool_input": { },
  "tool_response": { },
  "cwd": "string",
  "transcript_path": "string"
}
```

Key mapping:
| What you need | Correct key | Wrong key (common mistake) |
|---|---|---|
| Tool name | `tool_name` | `tool`, `name` |
| Tool parameters | `tool_input` | `params`, `parameters`, `input` |
| Hook event | `hook_event_name` | `hook_event_type`, `event` |
| Tool result | `tool_response` | `result`, `output` |

### Fix

Change exactly two lines — the key names in `.get()` calls:

```python
# BEFORE (broken)
tool_name = input_data.get("tool", "")
params = input_data.get("params", {})

# AFTER (correct)
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
```

Then update any downstream references from `params` to `tool_input` (e.g. `params.get("file_path")` becomes `tool_input.get("file_path")`).

### How to Confirm the Fix Works

After fixing, edit or write any `.py` or `.js` file in the project. If Black/Prettier is installed, the file should be auto-formatted. Check with:
```bash
# Should show formatter ran
sqlite3 .claude/logs/agent.db "SELECT payload FROM events WHERE hook_event_type='PostToolUse' AND tool_name='Edit' ORDER BY timestamp DESC LIMIT 1;"
```

---

## Bug B — `stop.py`: Main Branch False Alarm

**Symptom:** Every agent response ends with "You're on the main branch. Create a feature branch first." — even in projects that work directly on `main`.

**Root cause:** The `suggest_next_action()` function has a hard-coded check that flags `main`/`master` as wrong.

### How to Verify

Search for:
```python
if branch in ['main', 'master']:
```

If this exists in `suggest_next_action()`, the hook will always suggest creating a branch when working on main — regardless of project conventions.

### Fix

Remove the branch check block entirely. The rest of the function (test detection, commit suggestion) remains useful.

```python
# REMOVE this block from suggest_next_action():

    # Check if on main branch
    if branch in ['main', 'master']:
        return {
            "action": "create_branch",
            "message": "You're on the main branch. Create a feature branch first.",
            "command": "git checkout -b feat/your-feature-name"
        }
```

If a project DOES use feature branches, re-add this check with project-specific logic (e.g. only flag when source code files are modified, not docs/config).

---

## Bug C — `pre_compact.py`: Feature Status Detection Wrong File Paths

**Symptom:** Features always show status `"exploring"` in session-state.json, even when planning/implementation is complete. Recovery hints after compaction point to wrong state.

**Root cause:** The hook checks for files that don't exist in the standard feature directory layout.

### How to Verify

Check `scan_active_features()` for file existence checks:

```python
# These are the standard feature files:
has_prd = (feat_dir / "prd.md").exists()        # ✓ Standard
has_research = (feat_dir / "research.md").exists()    # ✗ Not standard
has_architecture = (feat_dir / "architecture.md").exists()  # ✗ Not standard
```

Compare against actual convention. The standard feature directory layout uses `prd.md` and `plan.md`:

```
docs/features/FEAT-XXX_description/
├── prd.md          ← Product requirements (created by /explore)
├── plan.md         ← Implementation plan (created by /blueprint)
├── handover.md     ← Session handover (created by /handover)
└── working/        ← Research notes, design docs (varies by project)
```

### Fix

Replace the file checks and status logic:

```python
# BEFORE (broken)
has_prd = (feat_dir / "prd.md").exists()
has_research = (feat_dir / "research.md").exists()
has_architecture = (feat_dir / "architecture.md").exists()

status = "unknown"
if has_architecture:
    status = "ready_for_implementation"
elif has_research:
    status = "planning"
elif has_prd:
    status = "exploring"

# AFTER (correct)
has_prd = (feat_dir / "prd.md").exists()
has_plan = (feat_dir / "plan.md").exists()

status = "unknown"
if has_plan:
    status = "ready_for_implementation"
elif has_prd:
    status = "planning"
```

Also update the feature dict to match:

```python
# BEFORE
active_features.append({
    "id": feat_dir.name,
    "path": str(feat_dir.relative_to(project_root)),
    "status": status,
    "has_prd": has_prd,
    "has_research": has_research,
    "has_architecture": has_architecture
})

# AFTER
active_features.append({
    "id": feat_dir.name,
    "path": str(feat_dir.relative_to(project_root)),
    "status": status,
    "has_prd": has_prd,
    "has_plan": has_plan
})
```

---

## General Hook Audit Checklist

When reviewing any project's hooks:

- [ ] **Payload keys match Claude Code spec** — `tool_name`, `tool_input`, `tool_response`, `hook_event_name`
- [ ] **Feature file paths match project conventions** — check actual directory layout, not assumptions
- [ ] **Branch strategy matches project workflow** — not all projects use feature branches
- [ ] **Hooks fail open** — all hooks exit 0 on error (never block legitimate work)
- [ ] **Regex patterns tested against real commands** — write a test script, don't eyeball
- [ ] **`settings.json` matchers are set** — PreToolUse should have `"matcher": "Bash"` to avoid running on non-Bash tools unnecessarily

---

## Reference: `settings.json` Hook Registration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 $(git rev-parse --show-toplevel)/.claude/hooks/pre_tool_use.py" },
          { "type": "command", "command": "python3 $(git rev-parse --show-toplevel)/.claude/hooks/send_event.py" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          { "type": "command", "command": "python3 $(git rev-parse --show-toplevel)/.claude/hooks/post_tool_use.py" },
          { "type": "command", "command": "python3 $(git rev-parse --show-toplevel)/.claude/hooks/send_event.py" }
        ]
      }
    ]
  }
}
```

**Note:** `$(git rev-parse --show-toplevel)` resolves the project root at runtime. This works correctly when Claude Code is running inside a git repo. If you see hook path resolution errors, verify you're in a git working directory.

---

## Propagation SOP

When hook fixes are applied in `ai-workflow-starter` (the template source of truth), propagate using the `/sync` command:

1. **Run:** `/sync /path/to/project` (or `/sync` for default target `~/dev/project-starter`)
2. The command runs `sync-downstream.sh` with dry-run preview, then actual sync
3. **Review:** Shows `git diff .claude/` automatically
4. **Merge if needed:** If the project has local hook modifications, manually merge rather than blind-overwrite
5. **Commit:** Prompted to commit after review
6. **Repeat:** Asked if you want to sync another project

You can also run the script directly: `./sync-downstream.sh /path/to/project`

### What gets synced

- `.claude/hooks/` — full replace (`--delete`) — all hooks come from template
- `.claude/commands/` — overwrite shared, preserve project-specific (no `--delete`) — review gate before commit

### What does NOT get synced

- `CLAUDE.md` — always project-specific
- `.claude/agents/` — projects may have custom agents
- `.claude/settings.json` — project-specific matcher config
- `.claude/logs/` — per-project observability data
- `.claude/skills/` — project-specific learned patterns

---

*Source: Audit performed 2026-03-13 against Claude Code hook spec and live observability data (475 events, 6 sessions).*
