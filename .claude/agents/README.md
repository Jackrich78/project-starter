# Sub-agents

One file per agent; the harness injects the roster from each file's `name` and `description` at session start, so this page holds no inventory (a hand-maintained list drifts within weeks). To see what exists: `ls .claude/agents/`. Which agent to call for what: CLAUDE.md § Delegation & model policy. The shape of a new agent: `TEMPLATE.md`; create one with `/persona`.

## Design principles

1. **Single responsibility** — one agent, one job; a reviewer that can write is not a reviewer.
2. **Stateless** — an agent starts cold with the brief it is given; durable learning goes to its memory file as methods, never findings.
3. **Least privilege** — tools are the minimum the job needs; `memory:` only where it cannot become a stored-injection path.
4. **Explicit stance** — judgement-tier agents assume the input holds a wrong claim and return claim-vs-evidence tables.
5. **Self-healing, never silent** — two attempts, revert on regression, always `PASS` / `FAIL: <reason>` / `ESCALATION: <reason>`.
6. **Role decides the model** — Opus to plan and judge, Sonnet to build and draft, Haiku for volume; `tests/harness/test_model_tier_table.py` keeps frontmatter honest.

## How work flows through them

```
/explore  ──► grilling (inline) · researcher (sonnet) · prd-consistency-sim (opus, cold read) · challenger (opus, conditional)
/blueprint ─► codebase-design (skill) · researcher · prd-consistency-sim · challenger
to-tickets ─► challenger fact-check (10/10)
/build  ───► work-issue ──► tdd-test-writer (RED) ──► tdd-implementer (GREEN) ──► tdd-refactorer
/qa --issue ► qa-reviewer (opus, clean context; Security · Standards · Spec ladders) ──► <!-- QA-VERDICT --> on the issue
/commit  ──► hook-enforced gate on BLOCKED SECURITY
winddown ──► agile-coach (sonnet, read-only retro) ──► human approves ──► librarian (Edit-only) applies
non-code ──► researcher · drafter · first-principles-thinker · challenger against the ticket's Proof: line
```

Hand-offs are files on disk and GitHub Issues, never live messages between agents; the orchestrator runs the gate between steps (`docs/guides/agent-harness-patterns.md`).

## Contract checks

- `python3 scripts/adoption_check.py` — memory block first, Failure Recovery, ESCALATION, model and effort pins, Stance on Opus agents.
- `python3 scripts/validate_agent_memory.py --check-roster` — every agent has a memory file and vice versa; entries are one-line methods under the 150-line cap.
- `npm test` — tier table, memory-flag allowlist, first-heading rule.

Full rules: `.claude/rules/agents.md` (loads automatically when you edit a file here).
