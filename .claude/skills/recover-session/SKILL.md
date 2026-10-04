---
name: recover-session
description: "Find and resume a lost Claude Code session. Use on \"I closed my terminal by accident\", \"I lost my session\", \"find my previous conversation\", \"how do I get back to...\", \"which session id do I resume\"."
type: skill
disable-model-invocation: true
---

# Recover Session

## Context

Every conversation is a `.jsonl` file at `~/.claude/projects/<escaped-project-path>/<session-uuid>.jsonl`. The escaped path is the project path with every `/` replaced by `-` (`/Users/<you>/dev/my-app` becomes `-Users-<you>-dev-my-app`). Each line is `{"message": {"role": ..., "content": ...}}`; content is a string or a list of `{type, text}`. Sub-agent runs appear as small separate files. This is a diagnostic task: list and match filenames only; never print transcript contents (they can hold pasted tokens).

## Pattern

1. **List sessions**: `ls -lt ~/.claude/projects/<project-dir>/*.jsonl | head -20` (project-dir = the absolute project path with `/` replaced by `-`). Newest first: modified time, size, uuid. Very small files are usually sub-agent runs.
2. **Present a numbered table**, newest first (time, size, topic), each with its resume command.
3. **Narrow by phrase** when the human remembers one: `grep -l "phrase" ~/.claude/projects/<project-dir>/*.jsonl` (filenames only, never matching lines), then check the match's mtime and size.
4. **Widen** if not found: `ls ~/.claude/projects/` and repeat for the project they name.
5. **Resume** from the project directory so the right CLAUDE.md loads: `cd <project-dir> && claude --resume <uuid>` (uuid = filename without `.jsonl`).

## Example

```
Found 3 sessions in /Users/<you>/dev/my-app (last 24h):

 1  Oct 01 18:02  448KB  "I want to investigate adding a retry layer to the
                          queue worker..."
    Resume: claude --resume 00000000-0000-0000-0000-000000000001

 2  Oct 01 17:40  719KB  First message is a slash command; likely a build
                          session
    Resume: claude --resume 00000000-0000-0000-0000-000000000002

 3  Sep 30 14:11  321KB  "Notifications stopped arriving after the deploy..."
    Resume: claude --resume 00000000-0000-0000-0000-000000000003

Which one? Or share a phrase you remember typing.
```

## Anti-patterns

- Trusting the largest file: size correlates loosely with topic; verify content.
- Checking only the current project: the work may have been in a sibling directory.
- Listing sessions with no real user message: they are sub-agent files with nothing to resume.
- Pasting real session ids or prompt text into docs or commits: they identify you.
