#!/usr/bin/env python3
"""PostToolUse hook (matcher: Task|Agent) — claim-verification reminder.

Fires after every sub-agent return and injects a one-line reminder into the
orchestrator's context. Encodes the CLAUDE.md rule "sub-agent outputs are
claims, not facts" as a mechanism rather than prose, so it holds regardless
of which model is orchestrating (Opus, Sonnet, Fable).

Fail-open: any error exits 0 with no output — never blocks the tool result.

Also carries an alert-only routing nudge: when a
general-purpose (or unnamed) sub-agent dispatch's description matches a
known keyword, appends a line naming the agent that dispatch should
probably have gone to instead. Never blocks, never changes the dispatch —
advisory only.
"""

from __future__ import annotations

import json
import re
import sys

REMINDER = (
    "Sub-agent output is claims, not facts. Before acting on it, emit a "
    "CLAIM->CHECK table (claim | check command | result) and verify the key "
    "claims against actual state (git status/diff, file reads, test runs). "
    "A 1-turn ack-style return means the work was NOT done - retry. "
    "AND: if several agents were briefed from one context pack you wrote, "
    "that is ONE source - report it as N runs of your own framing, never as "
    "independent agreement, in replies AND in any document you write."
)

# Precedence order: first match wins.
_KEYWORD_ROWS = [
    (r"\b(qa|security)\b", "qa-reviewer"),
    (r"\b(draft|document|memo)\b", "drafter"),
    (r"\b(audit|wiki|docs)\b", "librarian"),
    (r"\b(refute|challenge|critique)\b", "challenger"),
    (r"\b(research|investigate|sources)\b", "researcher"),
    (r"\b(decide|fundamentals|first.principles)\b", "first-principles-thinker"),
]
_REVIEW_RE = re.compile(r"\breview\b", re.IGNORECASE)
_REVIEW_QA_TRIGGER_RE = re.compile(r"\b(diff|build|code)\b", re.IGNORECASE)


def _route(description: str) -> str | None:
    for pattern, agent in _KEYWORD_ROWS:
        if re.search(pattern, description, re.IGNORECASE):
            return agent
    if _REVIEW_RE.search(description):
        if _REVIEW_QA_TRIGGER_RE.search(description):
            return "qa-reviewer"
        return "challenger"
    return None


def _nudge(tool_input: dict) -> str | None:
    subagent_type = tool_input.get("subagent_type") or ""
    if subagent_type != "general-purpose" and subagent_type != "":
        return None
    description = tool_input.get("description") or ""
    if not isinstance(description, str) or not description:
        return None
    return _route(description)


def main() -> int:
    try:
        raw = sys.stdin.read()  # hook input
        context = REMINDER
        try:
            payload = json.loads(raw)
        except Exception:
            return 0  # unparseable input: stay silent
        if not isinstance(payload, dict) or not payload:
            return 0
        tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
        if isinstance(tool_input, dict):
            agent = _nudge(tool_input)
            if agent:
                context = (
                    context
                    + f" Consider dispatching to `{agent}` instead of general-purpose."
                )
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": context,
                    }
                }
            )
        )
    except Exception:
        pass  # fail-open: a broken reminder must never block tool flow
    return 0


if __name__ == "__main__":
    sys.exit(main())
