# QA Integration & Hooks

> Module of [architecture.md](architecture.md). Loaded by `/prime build` and `/prime review`.

---

## Hook System

Four lifecycle hooks configured in `.claude/settings.json`:

### PreToolUse (Security)

**Trigger:** Before Bash execution
**File:** `.claude/hooks/pre_tool_use.py`

Blocks dangerous patterns:
- `rm -rf /`, `rm -rf ~`, `rm -rf *`
- `sudo rm`, `chmod 777`
- `curl|bash`, `wget|bash` (code injection)
- `eval()`, fork bombs, disk operations

Caution patterns (allowed but logged):
- `git push --force`
- `git reset --hard`
- `npm publish`

### PostToolUse (Quality)

**Trigger:** After Edit/Write tools
**File:** `.claude/hooks/post_tool_use.py`

Auto-formats by extension:
- `.js/.ts/.tsx/.json` → Prettier
- `.py` → Black
- `.rs` → rustfmt
- `.go` → gofmt

Detects docs/ changes, suggests `/update-docs`.

### PreCompact (Session State)

**Trigger:** Before context compaction
**File:** `.claude/hooks/pre_compact.py`

Saves to `.claude/session-state.json`:
- Active features and their status
- Recent file changes
- Recovery hints for next session

### Stop (Suggestions)

**Trigger:** After agent response
**File:** `.claude/hooks/stop.py`

Provides:
- Git status summary
- Suggested commit message (conventional format)
- Next action recommendation

---

## QA Integration

After TDD completes, an independent QA review validates security and quality.

### QA Flow

```
TDD Complete (all tests GREEN)
    ↓
┌─────────────────────────────────┐
│ Handover Generated              │
│ → docs/features/FEAT-XXX/       │
│    handover.md                  │
│ → Captures: what built, files,  │
│    decisions                    │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ Task(qa-reviewer)               │
│ Input: handover.md (NOT builder │
│        conversation)            │
│ Output: docs/qa/FEAT-XXX-*.md   │
│                                 │
│ Checks:                         │
│ - OWASP security (≥80% conf)   │
│ - Code quality                  │
│ - TDD compliance (10 items):   │
│   #1-7: Standard (pass/cov/etc)│
│   #8: AC coverage              │
│   #9: Pyramid level placement  │
│   #10: Anti-pattern detection  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ QA Status                       │
│                                 │
│ APPROVED → /commit unblocked   │
│ NEEDS_FIXES → iterate          │
│ BLOCKED → escalate to human    │
└─────────────────────────────────┘
```

### SAST Integration (Semgrep)

The QA reviewer uses a "sandwich method" for security analysis:

1. **Semgrep (deterministic):** Runs first, produces machine-verifiable findings
2. **LLM (contextual):** Analyzes SAST results, adds context, runs OWASP checklist

**Graceful Degradation:**

| Condition | Behavior |
|-----------|----------|
| No `.semgrep.yml` | Skip silently, LLM-only review |
| Config exists, no `semgrep` binary | Note in report, LLM-only review |
| Config exists, scan fails (exit 2+) | NEEDS_FIXES with actionable error |
| Config exists, scan succeeds | Full sandwich method |

**Configuration:**

| File | Purpose |
|------|---------|
| `.semgrep.yml` | Root config referencing local rule files |
| `.semgrep/rules/` | Local YAML rules (offline, no registry) |

All rules are local YAML files -- no network fetch, no registry references (`p/...`).

**Report Attribution:**

Every finding tagged with source: `[SEVERITY][SAST]` or `[SEVERITY][LLM]`. SAST findings are never removed by the LLM -- only annotated with context.

### E2E Testing & Browser MCP

E2E tests use browser automation MCP tools when available. When no browser MCP is configured, `/build` writes E2E stubs with documented steps and generates manual checklists.

### Two-Tier Escalation

| Tier | Issues | Action |
|------|--------|--------|
| Tier 1 | Style, complexity, suggestions | Listed in qa-report |
| Tier 2 | Security vulnerabilities | AskUserQuestion to human |

### QA Report Storage

All QA reports stored in `docs/qa/`:
- `FEAT-XXX-[scope]-YYYYMMDD.md` - Feature reviews
- `[path-slug]-YYYYMMDD.md` - Directory reviews
- `sweep-YYYYMMDD.md` - Codebase sweeps

---

## See Also

- [architecture.md](architecture.md) — Core system architecture
- [architecture-tdd.md](architecture-tdd.md) — TDD subagent architecture
- [QA Reviewer](../../.claude/agents/qa-reviewer.md) — QA agent definition
- [QA Storage](../qa/README.md) — Report naming and lifecycle
