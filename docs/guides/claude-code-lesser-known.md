# Claude Code: Lesser-Known Behaviors Explained

> Validated against official documentation (February 2026). Sources linked per section.

---

## 1. CLAUDE.md Loading: What Gets Read and When

### Parent directories — loaded at launch

CLAUDE.md files **above** your working directory are loaded automatically when a session starts. Claude Code walks up the directory tree from `cwd` to (but not including) `/`.

### Subfolders — lazy-loaded on access

CLAUDE.md files in child directories are **not** loaded at startup. They load automatically when Claude **reads** a file in that subtree. (The docs specifically say "reads" — writing is not confirmed as a trigger.)

**Example**: If Claude reads `src/utils/helper.js`, the system automatically discovers and loads `src/CLAUDE.md` and `src/utils/CLAUDE.md` if they exist. Claude does not need to explicitly open those files — it happens behind the scenes.

### README files — not part of the memory system

The memory system only recognizes `CLAUDE.md`, `CLAUDE.local.md`, and `.claude/rules/*.md`. README files are not mentioned anywhere in the memory documentation as auto-loaded files. (Note: this is inferred from absence — the docs don't explicitly state "READMEs are excluded," they simply never list them as recognized memory files.)

**Source**: [memory.md](https://code.claude.com/docs/en/memory.md) — *"CLAUDE.md files in child directories load on demand when Claude reads files in those directories."*

---

## 2. The `@import` Syntax vs Markdown Links

CLAUDE.md files can reference other files, but **only `@path` syntax triggers auto-loading**:

| Syntax | Behavior |
|--------|----------|
| `@./README.md` | **Auto-imported** into context |
| `@../shared/conventions.md` | **Auto-imported** into context |
| `See [README](./README.md)` | Just text — **not loaded** |
| `` `@./file.md` `` (inside code block) | Ignored — **not loaded** |

### Key details

- **One-time approval**: The first time Claude Code encounters `@` imports in a project, it shows an approval dialog. Once approved (or declined), the decision persists.
- **Recursive imports**: Imported files can themselves use `@` imports, up to **5 hops deep**.
- **Path resolution**: Relative paths resolve from the file containing the import, not the working directory.
- **Code blocks are safe**: Imports inside markdown code spans and code blocks are not evaluated.

**Source**: [memory.md](https://code.claude.com/docs/en/memory.md) — *"CLAUDE.md files can import additional files using `@path/to/import` syntax."*

---

## 3. Sub-Agent Context: What They See (and Don't)

Sub-agents defined in `.claude/agents/` start with a **minimal context**. They do not inherit the parent session's loaded files.

### What a sub-agent receives

1. Its own markdown body as the **system prompt**
2. Basic **environment details** (working directory, platform)
3. Any explicitly listed **skills** from frontmatter (`skills:` field)

### What a sub-agent does NOT receive

The docs state subagents don't get "the full Claude Code system prompt." While specific CLAUDE.md files aren't enumerated, the implication is:

- **Not the full Claude Code system prompt** (explicitly stated)
- **Not skills from the parent conversation** (explicitly stated: *"Subagents don't inherit skills from the parent conversation; you must list them explicitly."*)
- **Not the parent's conversation history** (implied by "only this system prompt")

> **Caveat**: The docs don't explicitly list which memory files (CLAUDE.md, rules, etc.) are excluded. The statement is about the "full system prompt" not being inherited. Built-in Task tool agents (like `general-purpose`) may behave differently from custom `.claude/agents/` subagents.

### Implications

If your sub-agent needs project conventions, you must either:
- Include the relevant instructions directly in the agent's markdown body
- Preload specific skills via the `skills:` frontmatter field
- Have the agent read the files it needs during execution

**Source**: [sub-agents.md](https://code.claude.com/docs/en/sub-agents.md) — *"Subagents receive only this system prompt (plus basic environment details), not the full Claude Code system prompt."*

---

## 4. Rules vs Hooks: Advisory vs Enforcement

These are fundamentally different mechanisms that complement each other.

### Rules (`.claude/rules/*.md`)

- **When loaded**: All rule files load **at session start**, same priority as `.claude/CLAUDE.md`
- **Nature**: Advisory instructions Claude reads and tries to follow
- **Enforcement**: None — Claude interprets them and uses judgment
- **Path scoping**: Rules can target specific files using `paths:` frontmatter with glob patterns

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Rules
- All endpoints must validate input
- Return consistent error shapes
```

Rules without a `paths:` field apply unconditionally to all files.

**Source**: [memory.md](https://code.claude.com/docs/en/memory.md)

### Hooks (`.claude/settings.json`)

- **When triggered**: At specific lifecycle points. The docs define **18 hook events** including: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop, Stop, TeammateIdle, TaskCompleted, ConfigChange, WorktreeCreate, WorktreeRemove, PreCompact, SessionEnd, and more.
- **Nature**: Deterministic automation that executes shell commands or LLM evaluations
- **Enforcement**: Hard — Claude cannot bypass a hook
- **Blocking**: Only some hooks can block actions. PreToolUse and PermissionRequest can block tool calls; most other hooks (PostToolUse, Notification, etc.) cannot.
- **Input modification**: PreToolUse hooks can modify tool inputs via `updatedInput` before execution

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo $TOOL_INPUT | grep -q 'rm -rf' && exit 2 || exit 0"
      }]
    }]
  }
}
```

**Source**: [hooks.md](https://code.claude.com/docs/en/hooks.md), [hooks-guide.md](https://code.claude.com/docs/en/hooks-guide.md)

### When to use which

| Scenario | Use |
|----------|-----|
| "Follow this coding convention" | **Rule** |
| "Never run this dangerous command" | **Hook** |
| "Prefer composition over inheritance" | **Rule** |
| "Auto-format files after every edit" | **Hook** |
| "Use snake_case in Python" | **Rule** |
| "Block commits without test files" | **Hook** |
| "Consider accessibility in UI work" | **Rule** (path-scoped) |
| "Notify me when a build finishes" | **Hook** |

**Key principle**: Rules guide thinking. Hooks enforce actions. Use rules for "how to code well" and hooks for "what must never/always happen."

---

## 5. Quick Reference: File Loading Summary

| File | When loaded | Scope |
|------|-------------|-------|
| `CLAUDE.md` (parent dirs) | Session start | Always in context |
| `CLAUDE.md` (child dirs) | On-demand (when files in that dir are accessed) | Scoped to that subtree |
| `CLAUDE.local.md` | Same as CLAUDE.md | Gitignored, personal overrides |
| `.claude/CLAUDE.md` | Session start | Project-wide |
| `.claude/rules/*.md` | Session start | All files, or path-scoped |
| `.claude/agents/*.md` | When agent is spawned | Agent's own context only |
| `@`-imported files | When parent CLAUDE.md loads | Follows parent's timing |
| README files | Not part of memory system | Must be explicitly read or `@`-imported |
