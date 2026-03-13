---
updated: 2026-01-24T12:00:00Z
name: [agent-name]
description: [One sentence describing what this agent does and when to use it]
tools: [Tool1, Tool2, Tool3]
status: [active, stub, planned]
color: [blue, orange, yellow, green, purple]
---

# [Agent Name]

[One paragraph introducing the agent's purpose and philosophy. Include a memorable principle in quotes.]

## Primary Objective

[Single sentence defining the agent's core mission. What is the ONE thing this agent accomplishes?]

## Simplicity Principles

1. **[Principle Name]**: [Brief description]
2. **[Principle Name]**: [Brief description]
3. **[Principle Name]**: [Brief description]
4. **[Principle Name]**: [Brief description]
5. **[Principle Name]**: [Brief description]

## Core Responsibilities

### 1. [Primary Responsibility]

[Description of main responsibility]

**Key Actions:**
- [Specific action or task]
- [Specific action or task]
- [Specific action or task]

**Approach:**
- [How the agent approaches this responsibility]
- [Decision-making criteria]
- [Quality standards]

### 2. [Secondary Responsibility]

[Description of secondary responsibility]

**Key Actions:**
- [Specific action or task]
- [Specific action or task]

### 3. [Additional Responsibility]

[If needed for completeness]

## Tools Access

**Available Tools:**
- **[Tool Name]**: [When and how to use it]
- **[Tool Name]**: [When and how to use it]
- **[Tool Name]**: [When and how to use it]

**Tool Usage Guidelines:**
- [Best practice for tool usage]
- [When to use multiple tools in parallel]
- [Error handling for tool failures]

## Output Files

**Primary Output:**
- **Location**: `[exact file path]`
- **Format**: [Markdown/JSON/etc.]
- **Purpose**: [What this file accomplishes]

**Additional Outputs (if applicable):**
- **Location**: `[file path]`
- **Format**: [Format]
- **Purpose**: [Purpose]

**Naming Conventions:**
- [Convention 1]
- [Convention 2]

## Workflow

### Phase 1: [Initial Phase Name]
1. [First step with specific action]
2. [Second step with specific action]
3. [Third step with specific action]

### Phase 2: [Main Work Phase Name]
1. [Analysis or processing step]
2. [Creation or transformation step]
3. [Validation or verification step]

### Phase 3: [Completion Phase Name]
1. [Finalization step]
2. [Handoff or update step]
3. [Reporting step]

## Quality Criteria

Before completing work, verify:
- ✅ [Specific quality check]
- ✅ [Specific quality check]
- ✅ [Specific quality check]
- ✅ [Specific quality check]
- ✅ [Specific quality check]

## Integration Points

**Triggered By:**
- [What initiates this agent's work]
- [Command or condition that activates it]

**Invokes:**
- [Other agents or tools this agent calls]
- [External systems accessed]

**Updates:**
- [Files or systems modified by this agent]
- [Documentation maintained]

**Reports To:**
- [Who receives this agent's output]
- [How results are communicated]

## Guardrails

**NEVER:**
- [Forbidden action with clear rationale]
- [Forbidden action with clear rationale]
- [Forbidden action with clear rationale]

**ALWAYS:**
- [Required action with clear rationale]
- [Required action with clear rationale]
- [Required action with clear rationale]

**VALIDATE:**
- [Critical validation before proceeding]
- [Critical validation before proceeding]

## Example Workflow

**Scenario:** [Concrete example of when this agent is used]

**Input:**
```
[Example input or trigger]
```

**Process:**
1. [Step 1 with specific example]
2. [Step 2 with specific example]
3. [Step 3 with specific example]

**Output:**
```
[Example output showing expected format and structure]
```

**Outcome:** [What was accomplished]

## Assumptions & Defaults

When information is missing, this agent assumes:
- [Default assumption 1 with rationale]
- [Default assumption 2 with rationale]
- [Default assumption 3 with rationale]

These defaults ensure the agent can work autonomously while remaining transparent about decisions made.

## Error Handling

**Common Errors:**
- **[Error Type]**: [How to handle] → [Fallback behavior]
- **[Error Type]**: [How to handle] → [Fallback behavior]
- **[Error Type]**: [How to handle] → [Fallback behavior]

**Recovery Strategy:**
- [How the agent recovers from failures]
- [When to escalate to main agent]
- [How to preserve partial progress]

## Related Documentation

- [Link to related SOP]
- [Link to template used]
- [Link to example output]
- [Link to related agents]

---

## Specialist Sub-Agents

When using this template for **specialist sub-agents** (library/framework experts created via `/create-specialist`):

**Auto-Population Sources:**
- Use WebSearch and User input to populate sections
- Prioritize official documentation and maintained sources
- Target <2 minutes total creation time (30s template + 90s research)

**Key Sections for Specialists:**
- **Core Responsibilities**: 3-5 library-specific expertise areas
- **Common Patterns**: Framework-specific patterns from official docs
- **Known Gotchas**: Pitfalls, workarounds, and anti-patterns
- **Integration Points**: How to use with other tools/frameworks
- **Tools Access**: Typically WebSearch, Read, Write

**Naming Conventions:**
- Filename: `[library-name]-specialist.md` (kebab-case)
- Name field: `[Library] Specialist`
- Example: `pydantic-ai-specialist.md` → "PydanticAI Specialist"

**Knowledge Sources:**
Document research sources used for auto-population:
- WebSearch: Note URLs and retrieval dates
- User Input: Flag manual sections added

See [Specialist Creator Agent](specialist-creator.md) for automated creation workflow.

---

**Template Version:** 1.1.0
**Last Updated:** 2026-01-24
**Status:** [Active/Stub/Planned]
