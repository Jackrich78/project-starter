---
updated: 2026-01-24T15:00:00Z
name: retro
description: Extract learnings, iterate on system components, and maintain consistency
args: "[FEAT-XXX | feedback [component-type] [component-name] | analyze]"
---

# /retro Command

Multi-mode command for learning extraction, system feedback iteration, and structural analysis.

## Modes

### Mode 1: Skill Extraction
```bash
/retro [FEAT-XXX or topic]
```
Analyzes session patterns and proposes skills from successful workflows (original behavior).

### Mode 2: System Feedback & Iteration
```bash
/retro feedback [component-type] [component-name] "[feedback]"
```
Accepts feedback on system components and propagates updates across interconnected files.

**Supported component types:**
- `agent` - Update agent definitions and all references
- `command` - Update command definitions and documentation
- `template` - Update templates and dependent files
- `workflow` - Update end-to-end workflows

**Examples:**
```bash
/retro feedback agent product-manager-specialist "rename to tech-product-lead"
/retro feedback command explore "add validation step"
/retro feedback template prd "add technical feasibility section"
```

### Mode 3: Structure Analysis
```bash
/retro analyze
```
Analyzes project structure, generates interconnection map, identifies inconsistencies.

---

## Workflow: Mode 1 (Skill Extraction)

1. **Gather Context**
   - Query `.claude/logs/agent.db` events table for recent activity
   - If FEAT-XXX provided, focus on that feature's workflow

2. **Identify Patterns**
   - Successful multi-step sequences
   - Error recovery approaches that worked
   - Repeated tool usage patterns
   - Effective agent invocation sequences

3. **Cleanup Check**
   - Check for completed spikes: `ls spikes/` - delete if feature is done
   - Check for stale handover files in completed features
   - Verify feature status matches actual state (complete/in-progress)

4. **Propose Skills**
   - Pattern name and trigger condition
   - Step-by-step execution pattern
   - Concrete example from session
   - Anti-patterns (what didn't work)

4. **Human Review**
   - Present proposed skill to user
   - Ask for approval/modification
   - Create `.claude/skills/[skill-name].md` on approval

---

## Workflow: Mode 2 (System Feedback)

### Phase 1: Understand Feedback
1. Parse user feedback and target component
2. Read current component definition
3. Identify scope of change (rename, enhance, restructure, update)

### Phase 2: Map Interconnections
1. **Use Grep** to find all references to component
2. Build dependency graph:
   - **Direct references**: Markdown links `[text](component-file.md)`, @references
   - **Indirect references**: Agent invocations in commands, command triggers in workflows
   - **Documentation references**: READMEs, indexes, handovers, plans
   - **Configuration references**: settings.json, hook configurations
3. Identify affected files with specific line numbers

### Phase 3: Plan Updates
1. Determine update sequence (dependencies first, then dependents)
2. For each affected file, plan specific edits:
   - Use Edit tool for precise string replacements
   - Preserve formatting and structure
   - Update both content and metadata (timestamps, frontmatter)
3. Validate no circular dependencies or broken references
4. Create change log

### Phase 4: Execute Updates
1. Update files in dependency order using Edit tool
2. Verify each change maintains consistency
3. Update indexes and cross-references last (README.md files)
4. Use atomic edits - one Edit per file section

### Phase 5: Verification
1. **Grep for old references** to ensure complete migration
2. Validate all markdown links resolve correctly
3. Check agent invocation paths still work
4. Generate summary report showing:
   - Files modified
   - References updated
   - Any remaining inconsistencies

---

## Workflow: Mode 3 (Structure Analysis)

1. **Scan Project Structure**
   - Use Glob to find all agents, commands, templates
   - Read README files and indexes
   - Build component inventory

2. **Map Interconnections**
   - Parse command → agent invocations
   - Extract agent → agent dependencies
   - Identify template usage patterns
   - Build cross-reference graph

3. **Identify Inconsistencies**
   - Broken markdown links
   - Orphaned files (not referenced anywhere)
   - Missing index entries
   - Outdated frontmatter timestamps
   - Circular dependencies

4. **Generate Report**
   - Create `docs/system/structure-report-[timestamp].md`
   - Include visual dependency graph
   - List inconsistencies with severity (error, warning, info)
   - Suggest fixes

---

## Examples

### Mode 1: Skill Extraction
```bash
/retro FEAT-009
```

Analyzes FEAT-009 implementation session and proposes skills like:
- "agent-refactoring" - Pattern for reducing agent token count
- "security-hook-creation" - Pattern for creating pre_tool_use hooks

**Output:** `.claude/skills/[skill-name].md`

### Mode 2: System Feedback
```bash
# Rename an agent
/retro feedback agent product-manager-specialist "rename to tech-product-lead"

# Enhance a command
/retro feedback command explore "add validation step after PRD creation"

# Update a template
/retro feedback template prd "add technical feasibility assessment section"
```

**Output:** Updates to affected files + verification report

### Mode 3: Structure Analysis
```bash
/retro analyze
```

**Output:** `docs/system/structure-report-[timestamp].md` with:
- Component inventory
- Dependency graph
- Broken links and inconsistencies
- Suggested fixes

---

## Output Formats

### Mode 1 Output: Skill File
Creates skill files at `.claude/skills/[skill-name].md`:

```markdown
---
name: [skill-name]
trigger: [when to suggest this skill]
source: retro FEAT-XXX
---

# [Skill Name]

## Context
When to use (1-2 sentences)

## Pattern
Step-by-step execution

## Example
Concrete application from session

## Anti-Patterns
What NOT to do
```

### Mode 2 Output: Update Report
Console output showing:
```
Updated 4 files:
✓ .claude/agents/tech-product-lead.md (renamed from product-manager-specialist.md)
✓ .claude/agents/README.md (line 54: link updated)
✓ docs/features/FEAT-009/handover.md (line 8: reference updated)

Verification:
✓ No remaining references to "product-manager-specialist"
✓ All markdown links valid
```

### Mode 3 Output: Structure Report
Markdown file with:
- Component inventory (agents, commands, templates)
- Dependency graph (visual + structured)
- Inconsistencies report (broken links, orphans, outdated timestamps)
- Recommended fixes

---

## Implementation Guidelines

### Following Claude Code Best Practices

**Tool Selection:**
1. **Discovery**: Use Grep (not bash grep) to find references
2. **Pattern matching**: Use Glob (not bash find) to locate files
3. **Reading**: Use Read tool (not cat/head/tail)
4. **Editing**: Use Edit tool (not sed/awk) for atomic string replacements
5. **Communication**: Output text directly (not echo commands)

**Update Strategy:**
1. **Read before edit**: Always read files before modifying
2. **Atomic edits**: One Edit call per distinct change
3. **Dependency order**: Update dependencies before dependents
4. **Verify after each change**: Grep to confirm successful updates
5. **No broken states**: Ensure references remain valid throughout process

**Interconnection Awareness:**
1. **Agent files** may be referenced in:
   - `.claude/agents/README.md` (index)
   - `docs/features/*/handover.md` (progress tracking)
   - `docs/features/*/prd.md` or `plan.md` (invocation notes)
   - `.claude/commands/*.md` (command workflows)
   - Other agent files (integration points)

2. **Command files** may be referenced in:
   - `CLAUDE.md` (command list)
   - `docs/system/connections.md` (workflow diagrams)
   - `.claude/agents/README.md` (triggers section)
   - Other command files (workflow chains)

3. **Templates** may be referenced in:
   - Command files (usage documentation)
   - `docs/system/architecture.md` (structural documentation)

### Consistency Maintenance Rules

**When renaming a file:**
1. Use bash `mv` for file operation
2. Grep for old filename in entire codebase
3. Update all references found
4. Verify with second Grep (should return no results)

**When updating agent definitions:**
1. Update agent file itself
2. Update `.claude/agents/README.md` (index entry)
3. Check recent handover files for mentions
4. Update any command files that invoke the agent

**When updating command definitions:**
1. Update command file itself
2. Check if listed in `CLAUDE.md`
3. Update `docs/system/connections.md` workflow diagrams
4. Check agent files for invocation patterns

---

## Notes

### Mode 1 (Skill Extraction)
- Run after completing a feature or significant work session
- Queries events from `.claude/logs/agent.db`
- Skills are suggestions - human approval required

### Mode 2 (System Feedback)
- Use for ANY system component updates to ensure consistency
- Prevents manual tracking of interconnections
- Follows Claude Code best practices for file operations
- Generates verification report for audit trail

### Mode 3 (Structure Analysis)
- Run periodically to catch drift and inconsistencies
- Useful after major refactoring or multi-file changes
- Creates snapshot of project structure at point in time
- Identifies technical debt in documentation

### Cleanup Reminders
- **Spikes**: Delete `spikes/spike-*` directories after feature is complete (research is preserved in `docs/features/FEAT-XXX/research-*.md`)
- **Stacks**: After merging a stack to root, delete `stacks/` to avoid duplicate tests
- **Empty dirs**: Remove unused directories like `test/` if empty
