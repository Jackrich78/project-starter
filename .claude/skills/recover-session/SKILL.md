---
name: recover-session
description: "Find and resume a lost Claude Code session. Use on \"I closed my terminal by accident\", \"I lost my session\", \"find my previous conversation\", \"how do I get back to...\", \"which session id do I resume\"."
type: skill
disable-model-invocation: true
---

# Recover Session

## Context

Every conversation is a `.jsonl` file at `~/.claude/projects/<escaped-project-path>/<session-uuid>.jsonl`. The escaped path is the project path with every `/` replaced by `-` (`/Users/<you>/dev/my-app` becomes `-Users-<you>-dev-my-app`). Each line is `{"message": {"role": ..., "content": ...}}`; content is a string or a list of `{type, text}`. Sub-agent runs appear as small separate files. This is a diagnostic task: use `scripts/recall.py` for every read of a transcript; never `cat`, `grep` or inline Python over that directory (the security hook blocks it, and the script redacts).

## Pattern

1. **List sessions**: `python3 scripts/recall.py --list --days 30` (widen `--days` if needed). One line per session, newest first: id, modified time, size, and the first real user message, redacted and cut to 80 chars. Sub-agent files and sessions with no prose message are skipped. The script is the sanctioned reader: the security hook refuses `cat`, `grep` or inline Python over the transcript directory.
2. **Present a numbered table**, newest first (time, size, topic), each with its resume command.
3. **Narrow by phrase** when the human remembers one: `python3 scripts/recall.py "phrase" --days 90` (redacted output with the session id per line; the security hook refuses raw `grep`/`cat` over the transcript directory, because transcripts hold pasted tokens), then check the match's mtime and first message.
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
- Writing a helper script into the repo: one-off diagnosis, not a feature.
- Pasting real session ids or prompt text into docs or commits: they identify you.
