---
type: reference
title: Claude Code — official documentation pointers
description: URL-only map of the official Claude Code docs the harness depends on, by topic. No content is copied here, so the page cannot go stale in substance; the stamp says when it was last checked against the docs.
last_checked: 2026-10-02
---

# Claude Code — official documentation pointers

**Rule (CLAUDE.md § Governing documents):** before changing anything under `.claude/agents/`, `.claude/hooks/`, `.claude/settings*.json`, `.claude/rules/` or a skill's frontmatter, ask the built-in `claude-code-guide` agent whether the mechanism still works the way the change assumes, and cite its answer in the commit body. `/harness-health` re-checks this page's topics and bumps `last_checked`; `tests/harness/test_reference_stamp.py` fails when the stamp is older than 90 days.

| Topic | What the harness relies on | Official page |
|---|---|---|
| Sub-agents | frontmatter: `name`, `description`, `model`, `effort`, `tools`, `disallowedTools`, `memory` (user/project/local), `maxTurns`, `isolation: worktree`, `background`, `hooks`, `skills` | https://code.claude.com/docs/en/sub-agents |
| Skills | `SKILL.md` frontmatter: `description` (the trigger surface), `disable-model-invocation`, `allowed-tools`, `context: fork`, `agent`, `model`, `argument-hint`; `$ARGUMENTS`, `$0…`, `${CLAUDE_PROJECT_DIR}` | https://code.claude.com/docs/en/skills |
| Memory (CLAUDE.md, rules, auto-memory) | load order global → project → directory → `.claude/rules/*.md` (`paths:`) → auto-memory; CLAUDE.md sizing guidance. Path-scoped `.claude/rules/*.md` load in the main thread only; a sub-agent sees none of them, so a brief must restate what it needs (see the TDD templates). | https://code.claude.com/docs/en/memory |
| Hooks | events (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, Stop, SubagentStart/Stop, PreCompact, SessionEnd …); types `command`, `prompt`, `agent`; stdin JSON, `hookSpecificOutput.additionalContext`, exit 2 to block | https://code.claude.com/docs/en/hooks · https://code.claude.com/docs/en/hooks-guide |
| Settings and permissions | `permissions.allow/deny`, `defaultMode`, hook wiring, `settings.local.json` | https://code.claude.com/docs/en/settings |
| Model configuration | aliases `opus`, `sonnet`, `haiku`; `CLAUDE_CODE_SUBAGENT_MODEL`; `/effort` levels | https://code.claude.com/docs/en/model-config |
| Best practices | explore → plan → code; verify with automated checks; short CLAUDE.md; writer ≠ reviewer; hooks for deterministic rules | https://code.claude.com/docs/en/best-practices |
| How Claude Code works | plan mode, `/code-review`, `/security-review`, `/simplify`, `/loop`, worktrees, compaction | https://code.claude.com/docs/en/how-claude-code-works |
| Plugins and evals | `claude plugin`, marketplace, `claude plugin eval` | https://code.claude.com/docs/en/plugins |
| GitHub CLI (`gh`) | sub-issues (`--parent`, `--add-sub-issue`), `--blocked-by`, `-is:blocked` search, `gh issue develop` — needs gh ≥ 2.96 | https://cli.github.com/manual/ |

**Checked 2026-10-02 against:** sub-agents, skills, memory, hooks, model-config, best-practices (via `claude-code-guide`). Record each re-check as a line in `docs/log.md`.
