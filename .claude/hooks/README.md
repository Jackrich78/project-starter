# Hooks

Wired in `.claude/settings.json` (JSON has no comments, so the wiring lives here).
All hooks: Python 3 stdlib, interpreter `python3`, no network, never print a secret.
Tests: `tests/harness/test_hooks.py` (security corpus), `tests/harness/test_settings_wiring.py` (wiring).

| Hook | Event | Matcher | What it does | Fail mode |
|---|---|---|---|---|
| `pre_tool_use.py` | PreToolUse | `Bash\|Read\|Edit\|Write\|MultiEdit\|NotebookEdit` | Blocks exfil, credential reads, secret echo, destructive and eval-style commands, pushes to main/URLs, shell writes to harness files, and commit/push when the QA verdict is `BLOCKED SECURITY`. Asks (labels the permission prompt; adds nothing in auto-accept/bypass modes) before an Edit/Write of a hook, `settings.json`, `.mcp.json` or the tracked waiver file; the private pattern/waiver files block. Logs cautions and asks to `.claude/logs/security.log` (redacted). | Open on internal error; deliberate block = exit 2 + one-line reason; ask = JSON `permissionDecision: ask` |
| `send_event.py` | every event below | `*` where applicable | Opt-in observability (`CLAUDE_HARNESS_OBSERVABILITY=1`); redacted; no-op otherwise. | Open |
| `post_tool_use.py` | PostToolUse | `*` | Nudges when a `docs/` file is missing from `docs/index.md`. | Open |
| `subagent_claim_check.py` | PostToolUse | `Task\|Agent` | Reminds the orchestrator that sub-agent output is a claim, not a fact. | Open |
| `pre_compact.py` | PreCompact | all | Writes a gitignored structural salvage file before compaction. | Open |
| `stop.py` | Stop | all | Reminds about uncommitted work. | Open |
| `session_start_reprime.py` | SessionStart | all | Re-injects this session's salvage file after compact/resume. | Open |
| `session_prime.py` | SessionStart | all | Injects current priorities and a harness-health nudge. | Open |

`send_event.py` is also registered on PreToolUse (`*`), PreCompact, Stop, SessionStart,
SubagentStart, SubagentStop and SessionEnd.

## Security hook notes

- The whole Bash command string is scanned, heredoc bodies included. A commit message that
  names a blocked command can trip it; use `git commit -F <file>`.
- QA gate: `git commit` / `git push` read `.claude/qa/verdict-<branch>` (`/` becomes `__`);
  absent file = allow; first line containing `BLOCKED SECURITY` = block.
  A verdict file older than 24h is ignored (caution logged): re-run `/qa`.
- Direct-mode push: a plain non-force push to `main`/`master` (including bare `git push` while on
  main) is allowed only when the project-root `CLAUDE.md` has a line `- Integration mode: \`direct\``
  (re-read every call; absent or unparseable = blocked). Force, `+refspec`, URL, `--mirror`, `--all`
  and delete pushes stay blocked in every mode.
- Obfuscation blocked on the raw string (heredoc bodies excluded from these checks): backslash-newline
  continuation, ANSI-C `$'...'` quoting, glob (`*?[`), `$var`, `$(...)`, backticks or `${` in a
  reader command's argument (exempt: a literal path under `$CLAUDE_PROJECT_DIR/`, `$PWD/`, `$HOME/`
  that is not a credential path), a `NAME=<credential path>` assignment, and substitution inside any
  network command argument (curl, wget, nc, ssh, scp, rsync, gh, git push).
- Pre-approved execution vectors blocked: `rg --pre`, `find -exec/-execdir/-ok/-okdir/-delete`,
  `git -c`, `git config remote.*.url`, pager/editor env prefixes (`GIT_PAGER`, `PAGER`, `EDITOR`,
  `LESSOPEN`, ...), `less` with `!`/`|`, `vim -c`, `awk system(`, `sed` `w`/`e`, `xargs` into a
  shell or interpreter, `git diff|log|show --output`, `git show <rev>:<credential path>`,
  `gh auth status --show-token`, environment dumps (`export`, `declare -x/-p`, bare `set`, inline
  `os.environ` / `process.env`), `git branch -f|-D main`.
- Audit round 3 (2026-10-02) closed: wrapper prefixes (`env`, `timeout`, `nice`, `watch`, `caffeinate`,
  `script`, `stdbuf`, `busybox`) before a shell or reader; shells and interpreters fed by a pipe,
  here-string, process substitution or heredoc (`echo … | bash`, `bash <<<`, `python3 - <<EOF`);
  `php -r`, `lua -e`, `osascript -e`; shell functions and `{ …; }` groups; `find|ls … | xargs <reader>`;
  `git config` of exec-capable or push-altering keys (`alias.*`, `core.sshCommand`, `core.hooksPath`,
  `remote.*.mirror`, `remote.*.push`, …); abbreviated push flags (`--mirro`, `--delet`) and
  `HEAD:heads/main`; `git stash drop|clear`, `reflog expire`, `gc --prune`, `filter-branch|repo`,
  `update-ref -d`, `rm -rf .git`; shell writes (`>`, `tee`, `sed -i`, `cp`, `mv`, `chmod`, `rm`, `ln`)
  to `.claude/settings*.json`, `.claude/hooks/`, the leak-gate inputs, `.git/hooks`, `.git/config` and
  anything under `~/.claude/`; reads of `~/.claude/{history.jsonl,sessions,shell-snapshots,settings.json,…}`,
  the transcript directory outside `memory/`, `.github/pii-patterns.txt`, `.claude/settings.local.json`,
  `/proc/*/environ`; recursive `grep`/`rg` over `~`, `/`, `~/.config`, `~/.claude`; npm config flags
  that execute (`--node-options`, `--script-shell`, `--prefix`, `--userconfig`); `gh … --jq` expressions
  that read `env`/`$ENV`; an empty-string argument (`cat '' .env`) splitting a command. Reader globs with
  a literal directory and a code/prose extension (`grep x src/*.py`) are allowed again.
- **`ask` adds a reason, not a control.** No Edit/Write entry is pre-approved, so default mode already prompts;
  in auto-accept or bypass modes the ask is logged and auto-approved (observed 2026-10-02). The hard `block`
  verdicts apply in every mode. Known route that stays open everywhere: edit `tests/conftest.py` or
  `package.json`, then run the pre-approved `npm test` (kept for the TDD loop; decision 2026-10-03).
- `scripts/leak_gate.sh --history <base>` scans added lines of `git log -p -m --text <base>..HEAD`, plus
  author/committer lines, commit messages and added/renamed file names. Waiver lines print the pattern's
  index, never its text. An invalid pattern fails the gate (exit 2) instead of silently matching nothing.
- Pure functions for tests: `check_command`, `check_path(path, tool)`, `check_stateful`.
- It is a speed bump against mistakes and prompt injection, not a sandbox. The real controls are the
  permission prompt and `permissions.deny`; a prompt-injected agent that can write a script file and run
  it is outside what a command-string filter can see.
- Registered hooks must exist: deregister in `settings.json` in the same change that deletes a file.


**Enable the event log** (off by default; nothing is written otherwise):

```bash
export CLAUDE_HARNESS_OBSERVABILITY=1   # or set under "env" in .claude/settings.local.json
```

Payloads (`tool_input`, `tool_response`) are redacted (key kept, value `***`) and capped at 32 KB.
Redaction is pattern-based and best effort: do not rely on it for secrets you would not commit.
`agent.db`, `salvage/` and `session-state.json` are gitignored. All hooks fail open and make no network calls.
