# Hooks

Wired in `.claude/settings.json` (JSON has no comments, so the wiring lives here).
All hooks: Python 3 stdlib, interpreter `python3`, no network, never print a secret.
Tests: `tests/harness/test_hooks.py` (security corpus), `tests/harness/test_hooks_runtime.py` (the rest),
`tests/harness/test_settings_wiring.py` (wiring).

| Hook | Event | Matcher | What it does | Fail mode |
|---|---|---|---|---|
| `pre_tool_use.py` | PreToolUse | `Bash` | Blocks a flat table of dangerous commands: recursive delete of root/home/`*`, pipe-to-shell, disk writes, `.env` reads, environment dumps, secret variables echoed, force pushes. Logs blocks to `.claude/logs/security.log` (URL credentials and token-shaped runs masked). | Open on internal error; block = exit 0 + JSON `permissionDecision: deny` |
| `post_tool_use.py` | PostToolUse | `*` | Nudges when a `docs/` file is missing from `docs/index.md`. | Open |
| `pre_compact.py` | PreCompact | all | Writes a gitignored, redacted structural salvage file before compaction. | Open |
| `stop.py` | Stop | all | Reminds about uncommitted work. | Open |
| `session_start_reprime.py` | SessionStart | all | Re-injects this session's salvage file after compact/resume. | Open |
| `session_prime.py` | SessionStart | all | Injects current priorities, flagged when stale. | Open |

`project_root.py` is a helper the hooks import, not a hook.

## Security hook

A guard against mistakes, not a security boundary: the v2.0.1 rule table plus five rules for risks seen in
real sessions. The real controls are the permission prompt and `permissions.deny` in `settings.json`
(credential-file reads by the Read tool, force and mirror pushes, `sudo`, secret-store CLIs).

- The whole command string is scanned, so a commit message that names a blocked command can trip it:
  write the message to a file and use `git commit -F <file>`.
- `grep -q`, `-c` and `-l` on `.env` pass (presence checks print no values); `.env.example`, `.sample`
  and `.template` are always readable.
- Secret-variable names match upper case only (`$API_KEY` blocks, a loop's `$key` passes).
- Cautions (`git reset --hard`, `npm publish`, `docker system prune`) are allowed and only flagged.

**Known gaps (by design):** Bash reads of credential files other than `.env` (`cat ~/.ssh/id_*`, `cat ~/.aws/credentials`; the Read denies cover the Read tool only), `gh auth token`, a script file, `$(...)`, variables or globs that hide a path, `bash -c`,
`cp .env elsewhere`, Edit/Write of `.env` (only Read is denied), recursive deletes outside root/home/`*`,
`git reset --hard`. Closing them meant a tokenizer that blocked routine work (v3.0.0); see `docs/decisions.md`.

Adding a rule: corpus case first in `tests/harness/test_hooks.py` (`MUST_BLOCK` plus the near-miss in
`MUST_ALLOW`), see it red, then add the pattern. The file is capped at 170 lines by a test.

Registered hooks must exist: deregister in `settings.json` before deleting a file
(`python3` on a missing file exits 2, which blocks every tool call).
`salvage/`, `session-state.json` and `logs/` are gitignored.
