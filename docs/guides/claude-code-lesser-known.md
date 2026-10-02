---
type: guide
title: Claude Code lesser-known behaviours
description: Loading and enforcement behaviours of Claude Code that surprise people - CLAUDE.md loading, @imports, what sub-agents see, rules versus hooks - each with its source.
tags: [claude-code, memory, hooks, sub-agents]
---

# Claude Code: lesser-known behaviours

> Re-read 2026-10-02 against the topics in `docs/reference/claude-code.md` (memory, sub-agents, hooks). Claims whose wording we could not re-confirm there are marked *(unverified)* and keep their original source; ask `claude-code-guide` before relying on them. Official pages are the authority.

---

## 1. CLAUDE.md Loading: What Gets Read and When

### Parent directories — loaded at launch

CLAUDE.md files **above** your working directory are loaded automatically when a session starts. Claude Code walks up the directory tree from `cwd` to (but not including) `/`.

### Subfolders — lazy-loaded on access

CLAUDE.md files in child directories are **not** loaded at startup. They load automatically when Claude **reads** a file in that subtree. (The docs specifically say "reads" — writing is not confirmed as a trigger.)

**Example**: If Claude reads `src/utils/helper.js`, the system automatically discovers and loads `src/CLAUDE.md` and `src/utils/CLAUDE.md` if they exist. Claude does not need to explicitly open those files — it happens behind the scenes.

### README files — not part of the memory system

The memory system only recognizes `CLAUDE.md`, `CLAUDE.local.md`, and `.claude/rules/*.md`. README files are not mentioned anywhere in the memory documentation as auto-loaded files. (Note: this is inferred from absence — the docs don't explicitly state "READMEs are excluded," they simply never list them as recognized memory files.)

**Source**: [memory.md](https://code.claude.com/docs/en/memory) — *"CLAUDE.md files in child directories load on demand when Claude reads files in those directories."*

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

**Source**: [memory.md](https://code.claude.com/docs/en/memory) — *"CLAUDE.md files can import additional files using `@path/to/import` syntax."*

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
- Give it a `memory:` file *(only where it cannot become a stored-injection path; see `docs/system/memory-systems.md`)*
- Have the agent read the files it needs during execution

**Source**: [sub-agents.md](https://code.claude.com/docs/en/sub-agents) — *"Subagents receive only this system prompt (plus basic environment details), not the full Claude Code system prompt."*

---

## 4. Rules vs Hooks: Advisory vs Enforcement

These are fundamentally different mechanisms that complement each other.

### Rules (`.claude/rules/*.md`)

- **When loaded**: rules without `paths:` load at session start, same priority as `.claude/CLAUDE.md`; rules with `paths:` are scoped to matching files (this repo's `agents/README.md` relies on that: "loads automatically when you edit a file here"). *(exact trigger unverified; see the memory page)*
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

**Source**: [memory.md](https://code.claude.com/docs/en/memory)

### Hooks (`.claude/settings.json`)

- **When triggered**: at lifecycle points, including SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, SubagentStart, SubagentStop, Stop, PreCompact and SessionEnd (the reference page lists the current set; the count changes, so we do not state one).
- **Nature**: deterministic automation; hook types are `command`, `prompt` and `agent`.
- **Input**: a command hook receives the event as JSON on stdin, not as environment variables.
- **Enforcement**: hard — the model cannot talk its way past one. Exit code 2 blocks where the event supports blocking (PreToolUse blocks the tool call).
- **Output**: stdout reaches the model only as `hookSpecificOutput.additionalContext` (a bare JSON blob is discarded). *Which events can block, and `updatedInput` rewriting of tool input, are unverified here: check the hooks page.*

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py\""
      }]
    }]
  }
}
```

A working example is this repo's own `.claude/hooks/pre_tool_use.py` (`docs/system/hooks.md`).

**Source**: [hooks](https://code.claude.com/docs/en/hooks), [hooks-guide](https://code.claude.com/docs/en/hooks-guide)

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
| `.claude/rules/*.md` | Session start if unscoped; `paths:` rules scoped to matching files | All files, or path-scoped |
| `.claude/agents/*.md` | When agent is spawned | Agent's own context only |
| `@`-imported files | When parent CLAUDE.md loads | Follows parent's timing |
| README files | Not part of memory system | Must be explicitly read or `@`-imported |
