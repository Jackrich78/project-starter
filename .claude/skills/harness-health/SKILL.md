---
name: harness-health
description: "Check the harness for drift: size caps, adoption, memory, wiki, gh setup, leaks, coupling, and upstream Claude Code changes. Use on \"harness health\", \"is the harness still sound\", monthly, or after /retro harness. Files at most one issue."
type: skill
disable-model-invocation: true
---

# Harness health

## Context

Self-maintenance, monthly or on demand. Stamp and URL map: `docs/reference/claude-code.md` (`last_checked`). Budget: seven local scripts plus one bounded `claude-code-guide` call; no other web research.

## Pattern

1. Run each, capture exit status and the first failing lines:
   - `python3 scripts/audit_claude_md.py --strict`
   - `python3 scripts/adoption_check.py`
   - `python3 scripts/validate_agent_memory.py --check-roster`
   - `python3 scripts/wiki_lint.py --all`
   - `bash scripts/github/check_gh.sh`
   - `bash scripts/leak_gate.sh`
   - `bash scripts/coupling_lint.sh --summary`
2. One call to `claude-code-guide`: "What changed since <last_checked> in sub-agents, skills, hooks, memory, settings, model config? At most 10 bullets, each with a URL." Treat the answer as a claim: spot-check anything you will act on.
3. Report: failures by script, upstream changes that touch a mechanism the harness uses.
4. Anything to act on: `gh issue list --search "Harness health in:title" --state open`. Exists -> `gh issue comment` or edit it; else one issue titled `Harness health <YYYY-MM>`, labels `chore,needs-triage`, body-file with the findings. Never more than one.
5. Bump `last_checked:` in `docs/reference/claude-code.md` and append one line to `docs/log.md` (date, scripts run, issue link). Both edits go through `/commit`.

## Example

All green except `wiki_lint` (2 orphans) and one upstream bullet on a new hook event -> one issue "Harness health 2026-10", stamp bumped, log line added.

## Anti-patterns

- Fixing findings inline: file them; fixes are separate work.
- Filing one issue per finding.
- Bumping `last_checked` when the guide call failed: the stamp claims a check that did not happen.
- Trusting the guide's answer unverified.
