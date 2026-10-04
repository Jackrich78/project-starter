---
paths:
  - .claude/hooks/**
  - .claude/settings.json
---

# Hook and settings conventions

Hooks are enforcement: a rule that must hold regardless of model reasoning. Knowledge belongs in skills and docs, not here. Before changing a hook event, matcher or settings key, confirm the current semantics with `claude-code-guide` (`docs/reference/claude-code.md`). Inventory and fail modes: `.claude/hooks/README.md`.

- **Python 3 standard library only, interpreter `python3`.** No third-party imports, no imports from outside `.claude/hooks/`, no network calls.
- **Fail open** on any internal error: exit 0 with empty stdout. The security hook blocks with exit 0 and a JSON `permissionDecision: "deny"`; no hook exits non-zero on purpose.
- **stdout reaches nobody** unless wrapped as `{"hookSpecificOutput": {"hookEventName": "<Event>", "additionalContext": "..."}}`. Name the reader before adding output.
- **Never print, log or persist a secret.** The salvage passes through `pre_compact.redact()`; the security log masks URL credentials and token-shaped runs. Presence checks use `[ -n "$X" ]`, never `${X:+...}`.
- **Deregister before deleting:** remove the hook from `settings.json` before deleting the file — `python3` on a missing file exits 2, which blocks every tool call.
- **Every pattern change ships a corpus case** in `tests/harness/test_hooks.py` (MUST_BLOCK / MUST_ALLOW / CAUTION), seen red once.
- **`settings.json`:** `permissions.allow` holds read-only verbs only; nothing that executes, writes, pushes, or posts (`python3`, `uv`, `node -e`, `curl`, `git add/commit/push`, `gh` write verbs, `gh api`) is ever pre-approved. `tests/harness/test_settings_wiring.py` checks the wiring and this rule.
