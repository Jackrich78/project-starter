---
type: domain-doc
title: Hooks
description: Contract of each harness hook (event, input, output channel, fail mode), what the security guard blocks and does not, the compaction salvage mechanism, and how to add or test a pattern.
tags: [hooks, security, enforcement]
---

# Hooks

Enforcement that holds regardless of model reasoning. Inventory and wiring table: `.claude/hooks/README.md` (the JSON in `.claude/settings.json` has no comments). Conventions: `.claude/rules/hooks.md`. Confirm event semantics with `claude-code-guide` before changing one (`docs/reference/claude-code.md`).

## Contracts

All hooks: Python 3 stdlib, interpreter `python3`, no network, never print a secret. Input is JSON on stdin. **Fail open**: any internal error exits 0 with empty stdout. The security guard blocks with exit 0 and a JSON `permissionDecision: "deny"` on stdout.

| Hook | Event | Output channel | Reader |
|---|---|---|---|
| `pre_tool_use.py` | PreToolUse (Bash) | JSON deny with the matched rule; blocks appended to `.claude/logs/security.log` | the model sees the reason |
| `post_tool_use.py` | PostToolUse | `hookSpecificOutput.additionalContext`: "docs/index.md does not list X" | the model |
| `pre_compact.py` | PreCompact | writes salvage file; no stdout | the next session (below) |
| `session_start_reprime.py` | SessionStart | `additionalContext`: the salvage text, only after compact or resume | the model |
| `session_prime.py` | SessionStart | `additionalContext`: current priorities (stale flag after 14 days) | the model |
| `stop.py` | Stop | `systemMessage`: uncommitted work; decision-log changed | the human |

**stdout reaches nobody** unless wrapped as `hookSpecificOutput.additionalContext` (model) or `systemMessage` (human). A bare JSON blob on stdout is discarded, and a hook whose output is "fixed" without naming its reader has changed nothing anyone sees.

## The security guard

A guard against mistakes, not a sandbox: a flat regex table over the Bash command string (v2.0.1's rules less `eval(`, plus secret-read, env-dump and force-push rules added on 2026-10-04 for risks seen in real sessions). Verdicts: allow, caution (allowed, flagged), block.

- **Destructive**: recursive `rm` of `/`, `~` or `*`; `sudo rm`; `chmod 777`; `mkfs`; `dd if=`; writes to `/dev/sd*` or `/etc/`; fork bombs.
- **Execution**: `curl`/`wget` piped to a shell.
- **Secrets into the transcript**: reading a secret file: `.env*` (not `.example`/`.sample`/`.template`), `.dev.vars`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `.secret*`, `credentials.json`, `.git-credentials`, `.npmrc`, `.pypirc`, `id_rsa`/`id_ed25519` (not `.pub`), `settings.local.json`; `grep`/`rg` printing those files' lines (`-q`, `-c`, `-l` pass); bare `env`, `printenv`, `set`, `export`; `echo`/`printf`/`printenv` of an upper-case `*KEY|TOKEN|SECRET|PASSW*` variable.
- **Force push** in any position (`--force*`, `-f`, `--mirror`, `+refspec`).
- **Caution only**: `git reset --hard`, `npm publish`, `docker system prune`.

`settings.json` carries the rest: `permissions.deny` for credential-file reads by the Read tool, Claude Code's private state, force and mirror pushes, `sudo`, `gh secret|variable`, `gh repo delete`; `permissions.allow` holds read-only verbs only, plus `npm test` for the TDD loop (it runs whatever the tests contain). No `defaultMode` is set, so the owner's own mode governs.

Known gaps are listed in `.claude/hooks/README.md`. A command-string filter cannot see a script file, so gaps are documented rather than closed: the 2026-10-04 decision rejected the evasion-resistant v3.0.0 hook, which blocked routine work.

**QA gate** lives in `/commit` step 0, not in a hook: it reads the latest `<!-- QA-VERDICT -->` issue comment from the owner, a member or a collaborator and refuses on `BLOCKED SECURITY`.

## Salvage and re-prime

Compaction keeps prose but loses structure: exact paths, commands, dispatched agents, the user's own recent words. `pre_compact.py` parses the tail of the transcript with no LLM call and writes `.claude/salvage/salvage-<session>-<ts>.md` (6 KB cap, newest 10 kept, sub-agent and meta lines skipped), plus `session-state.json`. `session_start_reprime.py` injects it as `additionalContext` only when the session source is `compact` or `resume`, picking the file by **session id**; with no match it falls back to the newest file only if under an hour old, because a wrong re-prime is worse than none. `/clear` is not re-primed: a cleared session starts clean by intent. Salvage is gitignored and redacted by pattern (best effort), so treat it as local-only.

## Adding or changing a pattern

1. Add the corpus case first to `tests/harness/test_hooks.py` (`MUST_BLOCK`, `MUST_ALLOW` or `CAUTION`), including the near-miss that must still pass.
2. Run it and see it **red**. A pattern whose case never failed is untested.
3. Change the pattern; run green. Check the allow side did not regress.
4. `check_command(cmd)` is a pure function returning `{allowed, reason, severity}`; test it directly. The hook file is capped at 170 lines.

## Test the wiring first (Layer 0)

Hook logic tests pass with the hook unregistered. `tests/harness/test_settings_wiring.py` parses `settings.json` as a document: every registered command resolves to an existing file and compiles, every event is a known one, every matcher names a real tool, the security hook is wired on `Bash`, credential reads are denied, and `permissions.allow` holds no write or exec verbs. Hooks run under the system `python3`, which can be older than CI's: avoid 3.10+ syntax, and note a syntax check proves syntax only.

**Deregister before delete.** Remove the hook from `settings.json` before deleting its file: `python3` on a missing file exits 2, which blocks every tool call.
