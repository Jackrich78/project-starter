---
updated: 2026-01-24T12:00:00Z
description: Create a specialist sub-agent for a library or framework
argument-hint: [library-name] [scope]
---

# Create Specialist Sub-Agent

Creating specialist for: **$ARGUMENTS**

## Mission

Create a domain-specific specialist sub-agent that provides expertise for a library, framework, or technical domain.

---

## Arguments

- **library-name** (required): Name of the library/framework (e.g., "Supabase", "FastAPI")
- **scope** (optional): "narrow" (default, library-specific) or "broad" (category-wide)

---

## Workflow

### Step 1: Check Existing Specialists

```
Use Glob: .claude/agents/*-specialist.md

If specialist for this library exists:
  Ask user: "A [Library] specialist already exists. Update it or skip?"
```

### Step 2: Parse Arguments

```
library_name = first argument (required)
scope = second argument or "narrow"

If scope = "narrow":
  Focus on [library_name] only
  Example: "Supabase Specialist"

If scope = "broad":
  Cover category including [library_name]
  Example: "Database Specialist" covering Postgres, Supabase, MySQL
  Ask user: "Which libraries should this cover?"
```

### Step 3: Research the Library

Use WebSearch to gather information:

```
Search queries:
- "[library] documentation getting started 2026"
- "[library] best practices patterns"
- "[library] common gotchas pitfalls"

Extract:
- Common patterns and usage
- Integration points
- Gotchas and workarounds
- Tool access requirements
```

Time-box research to 90 seconds maximum.

### Step 4: Create Specialist File

Write to `.claude/agents/[library-name]-specialist.md`

**Filename convention (kebab-case):**
- "Supabase" → `supabase-specialist.md`
- "PydanticAI" → `pydantic-ai-specialist.md`
- "Next.js" → `nextjs-specialist.md`

**File structure:**

```markdown
---
created: [timestamp]
updated: [timestamp]
name: [Library] Specialist
description: Domain expert for [library] providing patterns, gotchas, and integration guidance
tools: [Read, WebSearch, Write]
status: active
---

# [Library] Specialist

[Brief description of what this specialist provides]

## Primary Objective

Provide domain-specific expertise for [library] including best practices, common patterns, and integration guidance.

## Core Expertise

### Common Patterns
- [Pattern 1 from research]
- [Pattern 2 from research]
- [Pattern 3 from research]

### Known Gotchas
- [Gotcha 1]: [Workaround]
- [Gotcha 2]: [Workaround]

### Integration Points
- [How to integrate with other tools/libraries]

## When to Invoke

This specialist is useful when:
- Working with [library] APIs or configuration
- Debugging [library]-specific issues
- Designing architecture involving [library]

## Invocation Example

Task(
  subagent_type="general-purpose",
  description="Get [Library] expertise",
  prompt="You are the [Library] Specialist.
  Answer this question: [question]
  @.claude/agents/[library]-specialist.md"
)
```

### Step 5: Present Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECIALIST CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NAME: [Library] Specialist
📁 FILE: .claude/agents/[library-name]-specialist.md
🔍 SCOPE: [Narrow/Broad]

Research sources:
- WebSearch: [queries used]

Capabilities:
- Domain-specific patterns
- Known gotchas and workarounds
- Integration guidance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The specialist is now available for invocation by other agents.
```

---

## Error Handling

**Missing library name:**
```
Usage: /create-specialist [library-name] [scope]

Examples:
  /create-specialist Supabase
  /create-specialist PydanticAI narrow
  /create-specialist Database broad
```

**Research incomplete:**
```
Research yielded limited results.
Created specialist with basic structure.
Consider manually editing to add:
- Additional patterns
- Specific gotchas
- Integration examples
```

---

## Success Criteria

- ✅ Specialist file created at `.claude/agents/[library]-specialist.md`
- ✅ Valid YAML frontmatter
- ✅ Research-based content populated
- ✅ Kebab-case filename
- ✅ Ready for invocation
