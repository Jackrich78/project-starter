# Integrations

**Updated:** 2026-03-06
**Purpose:** External systems and how they're used

---

## Overview

The harness integrates with external tools for research, code execution, and IDE features. All integrations are optional and fail gracefully.

---

## WebSearch

**Purpose:** Live web search for current information

**Scope:** Available to Researcher, Specialist Creator, Prompt Specialist, N8N Specialist, First Principles Thinker

### Usage Patterns

**Research queries:**
```
WebSearch("OAuth 2.0 best practices 2026")
WebSearch("Supabase authentication documentation")
```

**Comparison queries:**
```
WebSearch("JWT vs session tokens security comparison")
```

**Current information:**
```
WebSearch("Claude Code latest features")
```

### When to Use

- Current/recent information needed
- Comparing multiple approaches
- Finding official sources

### When NOT to Use

- Information already in codebase
- Static knowledge (use existing docs)
- User has provided the information

---

## IDE Integration

**Purpose:** VS Code diagnostics and code execution

### Available Tools

| Tool | Purpose |
|------|---------|
| `mcp__ide__getDiagnostics()` | Get lint errors, type errors |
| `mcp__ide__executeCode()` | Run code in Jupyter kernel |

### Usage

**Get diagnostics for file:**
```
mcp__ide__getDiagnostics(uri="file:///path/to/file.ts")
```

**Get all diagnostics:**
```
mcp__ide__getDiagnostics()
```

### When Available

IDE tools are only available when Claude Code is running in VS Code with the extension installed. They fail gracefully if unavailable.

---

## Future MCPs

Placeholder for additional integrations:

### Planned

- **CI/CD MCP** - Trigger builds, check pipeline status
- **Database MCP** - Query development databases safely

### Considerations for New MCPs

1. **Scope carefully** - Which agents need access?
2. **Fail gracefully** - What happens when unavailable?
3. **Document in this file** - Keep integration docs centralized

---

## Integration Principles

### 1. Optional by Default

All integrations should work when unavailable. Agents should degrade gracefully if a tool is missing.

### 2. Minimal Scope

Grant MCP access only to agents that need it:
- WebSearch → Research-focused agents
- IDE → Main agent when in VS Code

### 3. Explicit Fallbacks

Document what happens when integration fails:
- IDE unavailable → Skip diagnostics
- WebSearch fails → Ask user

### 4. No Secrets in Code

Integration credentials are managed externally:
- Claude Code settings
- Environment variables
- MCP server configuration

---

## Troubleshooting

### WebSearch Failing

1. Check network connectivity
2. Verify no rate limiting
3. Try simpler query

### IDE Tools Missing

1. Ensure VS Code extension is installed
2. Check Claude Code is running in VS Code (not terminal)
3. Verify file URIs are correct format

---

## See Also

- [architecture.md](architecture.md) - Agent tool access
- [observability.md](observability.md) - Integration logging
- `.claude/agents/researcher.md` - Research agent details
