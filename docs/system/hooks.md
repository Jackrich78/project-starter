---
type: domain-doc
title: Hooks
description: Contract of each harness hook (event, input, output channel, fail mode), the deny-hook categories, the QA gate, the compaction salvage mechanism, and how to add or test a pattern.
tags: [hooks, security, enforcement]
---

# Hooks

Enforcement that holds regardless of model reasoning. Inventory and wiring table: `.claude/hooks/README.md` (the JSON in `.claude/settings.json` has no comments). Conventions: `.claude/rules/hooks.md`. Confirm event semantics with `claude-code-guide` before changing one (`docs/reference/claude-code.md`).

## Contracts

All hooks: Python 3 stdlib, interpreter `python3`, no network, never print a secret. Input is JSON on stdin. **Fail open**: any internal error exits 0 with empty stdout; the one deliberate non-zero exit is the security block (exit 2, one-line reason on stderr).

| Hook | Event | Output channel | Reader |
|---|---|---|---|
| `pre_tool_use.py` | PreToolUse (Bash, Read, Edit, Write, MultiEdit) | exit 2 + stderr reason to block; cautions to `.claude/logs/security.log` (redacted) | the model sees the block reason |
| `post_tool_use.py` | PostToolUse | `hookSpecificOutput.additionalContext`: "docs/index.md does not list X" | the model |
| `subagent_claim_check.py` | PostToolUse (Task, Agent) | `additionalContext`: sub-agent output is a claim | the orchestrator |
| `pre_compact.py` | PreCompact | writes salvage file; no stdout | the next session (below) |
| `session_start_reprime.py` | SessionStart | `additionalContext`: the salvage text, only after compact or resume | the model |
| `session_prime.py` | SessionStart | `additionalContext`: current priorities (stale flag after 14 days) and a harness-health nudge (after 30 days) | the model |
| `stop.py` | Stop | `systemMessage`: uncommitted work; decision-log changed | the human |
| `send_event.py` | most events | SQLite row, only when opted in (`observability.md`) | `/logs`, `agile-coach` |

**stdout reaches nobody** unless wrapped as `hookSpecificOutput.additionalContext` (model) or `systemMessage` (human). A bare JSON blob on stdout is discarded, and a hook whose output is "fixed" without naming its reader has changed nothing anyone sees.

## The deny hook

Scans the whole Bash command (heredoc bodies included) plus Read/Edit/Write paths. A commit message that names a blocked command can trip it; use `git commit -F <file>`. It is a speed bump against mistakes and prompt injection, not a sandbox. Verdicts: allow, caution (logged, allowed), block.

Blocked categories:

- **Exfiltration**: `curl`/`wget` sending a local file (`-F f=@`, `--data-binary @`, `-d@`, `-T`, `--post-file`), `nc`/`socat`, `scp`/`rsync` to a remote, `gh gist`, `gh api` write methods or request bodies or GraphQL mutations, `gh` write verbs aimed at an explicit repo (`-R`, `GH_REPO=`), `gh secret|variable`, `gh repo delete`, `gh release create`.
- **Credential access**: reads of `.env*`, `~/.ssh`, `~/.aws`, `~/.netrc`, `~/.config/gh`, `~/.docker`, `~/.npmrc`, `~/.pypirc`, `~/.kube`, `~/.gnupg`, `*.pem`, `*.key`, `~/.claude/projects`; keychain reads; `git credential`; `env`/`printenv` dumps; `ps` with environment; secret variables expanded into `echo`/`printf`.
- **Destructive**: recursive `rm` of root, home or cwd targets in any flag order; `git reset --hard`, `git clean -f`, discarding all changes; deleting `main`; `git remote` mutation; `sudo`, `mkfs`, `dd if=`, `chmod 777`, fork bombs.
- **Execution**: `eval`, `sh -c`, pipe-to-shell downloads, inline interpreter code that touches credentials or the network.
- **Git push**: force in any spelling (`--force*`, `+refspec`, trailing `-f`), `--all`, `--mirror`, deletes, URLs instead of a named remote, any push to main/master.
- **Caution only** (logged): ordinary `git push`, other `gh` write verbs, `npm publish`, `pip install` from a URL, `docker`.

`settings.json` adds `permissions.deny` for the same credential paths and force-push forms, and keeps `permissions.allow` to read-only verbs: nothing that executes, writes, pushes or posts is ever pre-approved.

**QA gate.** On `git commit` or `git push`, the hook reads `.claude/qa/verdict-<branch>` (`/` becomes `__`). Absent file allows; a first line containing `BLOCKED SECURITY` blocks until `/qa --issue N` is re-run and clears it. The file is written by the orchestrator from the `/qa` fork's verdict marker, so the gate is only as honest as that step: `/commit` treats the local file as authoritative and, when it is absent, accepts an issue-comment verdict only from the repo owner, a member or a collaborator.

**Harness-file edits ask.** An Edit/Write of a file under `.claude/hooks/`, of `.claude/settings.json`, of `.mcp.json` or of the tracked `.github/leak-waivers.txt` returns `permissionDecision: ask` with a reason. This labels the prompt Claude Code already shows in default mode (no Edit/Write entry is pre-approved); in auto-accept and bypass modes it is logged and waved through, so it adds no control there. The private gate inputs (`.github/pii-patterns.txt`, `.github/release-waivers.txt`) and `.claude/settings.local.json` block for every tool. Shell-side writes to the same files (`>`, `tee`, `sed -i`, `cp`, `mv`, `rsync`, `patch`, `chmod`, `rm`, `git checkout -- <path>`) are blocked, with paths normalised (`..`, `./`, directory targets). Known limit in every mode: an agent that can edit a pytest conftest file or `package.json` and then run the pre-approved `npm test` executes code without a prompt; the allow list trades that for a frictionless TDD loop (decision 2026-10-03).

## Salvage and re-prime

Compaction keeps prose but loses structure: exact paths, commands, dispatched agents, the user's own recent words. `pre_compact.py` parses the tail of the transcript with no LLM call and writes `.claude/salvage/salvage-<session>-<ts>.md` (6 KB cap, newest 10 kept, sub-agent and meta lines skipped), plus `session-state.json`. `session_start_reprime.py` injects it as `additionalContext` only when the session source is `compact` or `resume`, picking the file by **session id**; with no match it falls back to the newest file only if under an hour old, because a wrong re-prime is worse than none. `/clear` is not re-primed: a cleared session starts clean by intent. Salvage is gitignored and unredacted, so treat it as local-only.

## Adding or changing a pattern

1. Add the corpus case first to `tests/harness/test_hooks.py` (`MUST_BLOCK`, `MUST_ALLOW` or `CAUTION`), including the near-miss that must still pass.
2. Run it and see it **red**. A pattern whose case never failed is untested.
3. Change the pattern; run green. Check the allow side did not regress.
4. `check_command`, `check_path` and `check_stateful` are pure functions; test them directly.

## Test the wiring first (Layer 0)

Hook logic tests pass with the hook unregistered. `tests/harness/test_settings_wiring.py` parses `settings.json` as a document: every registered command resolves to an existing file and compiles, every event is a known one, every matcher names a real tool, the security hook covers all guarded tools, `defaultMode` is `default`, credential reads are denied, and `permissions.allow` holds no write or exec verbs. Hooks run under the system `python3`, which can be older than CI's: avoid 3.10+ syntax, and note a syntax check proves syntax only.

**Deregister before delete.** Remove the hook from `settings.json` in the same change that deletes its file; a registered hook with a missing file errors on every tool call.
