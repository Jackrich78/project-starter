---
paths:
  - .claude/hooks/**
  - .claude/settings.json
---

# Hook and settings conventions

Hooks are enforcement: a rule that must hold regardless of model reasoning. Knowledge belongs in skills and docs, not here. Before changing a hook event, matcher or settings key, confirm the current semantics with `claude-code-guide` (`docs/reference/claude-code.md`). Inventory and fail modes: `.claude/hooks/README.md`.

- **Python 3 standard library only, interpreter `python3`.** No third-party imports, no imports from outside `.claude/hooks/`, no network calls.
- **Fail open** on any internal error: exit 0 with empty stdout. The only deliberate non-zero exit is the security hook's block (exit 2 with a one-line reason).
- **stdout reaches nobody** unless wrapped as `{"hookSpecificOutput": {"hookEventName": "<Event>", "additionalContext": "..."}}`. Name the reader before adding output.
- **Never print, log or persist a secret.** Anything written to disk passes through `send_event.redact()`. Presence checks use `[ -n "$X" ]`, never `${X:+...}`.
- **Deregister before deleting:** remove the hook from `settings.json` in the same change that deletes the file — a registered hook with a missing file fails every tool call.
- **Every pattern change ships a corpus case** in `tests/harness/test_hooks.py` (MUST_BLOCK / MUST_ALLOW / CAUTION), seen red once.
- **`settings.json`:** `permissions.allow` holds read-only verbs only; nothing that executes, writes, pushes, or posts (`python3`, `uv`, `node -e`, `curl`, `git add/commit/push`, `gh` write verbs, `gh api`) is ever pre-approved. `tests/harness/test_settings_wiring.py` checks the wiring and this rule.
- **Observability is opt-in** (`CLAUDE_HARNESS_OBSERVABILITY=1`); the event store is gitignored and redacted.
