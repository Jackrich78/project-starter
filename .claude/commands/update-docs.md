---
updated: 2026-03-16T00:00:00Z
description: Update documentation index and validate cross-references
argument-hint: [scope: all|features|FEAT-XXX|health]
---

# Documentation Update

You are updating project documentation.

**Scope:** ${ARGUMENTS:-all}

## Mission

Regenerate docs/README.md index, validate cross-references, run documentation health checks, and optionally update CHANGELOG.

---

## Workflow

### Step 1: Scan Documentation

Use Glob to find all documentation:
```
docs/features/*/
docs/features/*/research-*.md
docs/system/*.md
docs/sop/*.md
docs/research/**/*.md
docs/templates/*.md
```

For each feature folder, determine status by checking which files exist:
- Empty or only placeholder files → Placeholder
- Only `prd.md` or `brief.md` → Exploring
- `prd.md` + research files → Research Complete
- `prd.md` + `plan.md` or full planning docs (architecture, acceptance, testing) → Planning Complete
- Working directories, implementation files, or `handover.md` → Active / In Progress
- All docs complete + `handover.md` noting completion → Complete / Implemented

**Note:** Feature structures vary. Check for README.md, handover.md, working/, archive/ directories as additional status signals.

### Step 2: Regenerate docs/README.md

Create organized index with sections for:
- Features (grouped by status: Implemented, Active, Planning, Placeholder)
- Content System (v3 files with version note)
- LinkedIn Tools (Comment Sidekick, Visual Spec)
- Job Application Pipeline (if applicable)
- Research files
- Reference Library
- Skills
- Commands
- SOPs
- System Documentation
- Templates
- Archive
- Navigation links

Read the first 5-10 lines of each feature's PRD/README to extract descriptions.

### Step 3: Validate Cross-References

Search for markdown links and verify targets exist:
- Use Grep to find `[text](path)` patterns in docs/README.md
- Check if target files exist
- Report broken links with file and line number

### Step 4: Documentation Health Check

**This step runs on `all` or `health` scope.** Skip for `features` or `FEAT-XXX` scopes.

#### 4a: Agents Index Audit

1. Glob `.claude/agents/*.md` to find all agent files
2. Exclude README.md and TEMPLATE.md from the list
3. Read `.claude/agents/README.md`
4. Compare: flag agents that exist as files but are missing from the README
5. Flag agents listed in README but whose files don't exist
6. Report: "Agents index: X agents indexed, Y files found, Z mismatches"

If mismatches found, offer to regenerate agents/README.md.

#### 4b: Commands Audit

1. Glob `.claude/commands/*.md` to find all command files
2. Exclude setup.md from the count (meta-command)
3. Read CLAUDE.md
4. Check: does CLAUDE.md's Commands section list all found commands?
5. Report: "Commands: X in CLAUDE.md, Y files found, Z missing from CLAUDE.md"

If mismatches found, list the missing commands.

#### 4c: Skills Audit

1. Glob `.claude/skills/*/SKILL.md` to find all skills
2. Check CLAUDE.md Skills section
3. Report mismatches

#### 4d: System Doc Staleness Check

For each file in `docs/system/*.md`:
1. Read the file header to find `Last Updated` or frontmatter `updated` field
2. Compare against current date
3. Flag files older than 90 days as "stale"
4. Report: "System docs: X files, Y stale (>90 days)"

List stale files with their last-updated dates.

#### 4e: Stray File Detection

1. Glob `*.md` at project root
2. Expected root files: CLAUDE.md, PROJECT.md, README.md, AC.md, CHANGELOG.md, .gitignore
3. Flag any unexpected .md files at root level
4. Report: "Stray files: [list] — consider moving to docs/research/ or a feature folder"

#### 4f: Content Version Check

1. Glob `docs/content/*-v3.md` to check if v3 files exist
2. If v3 exists: Grep CLAUDE.md for "v2" references — flag if found
3. Report: "Content version: v3 active, CLAUDE.md [consistent/inconsistent]"

### Step 5: Update CHANGELOG (Optional)

If new features were added or documentation changed significantly:
```markdown
## [Unreleased]

### Changed
- Updated documentation index
- [List specific changes]
```

### Step 6: Present Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Documentation Updated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Index: docs/README.md regenerated
Features: X (A implemented, B active, C planning, D placeholder)
Research: Y files
System Docs: Z files

Cross-References: X valid, Y broken
[List any broken links]

Health Check:
  Agents:   X indexed / Y files [✓ consistent | ⚠ Z mismatches]
  Commands: X in CLAUDE.md / Y files [✓ consistent | ⚠ Z missing]
  Skills:   X in CLAUDE.md / Y found [✓ consistent | ⚠ Z missing]
  System:   X files, Y stale (>90 days) [list stale files]
  Stray:    [none | list stray files]
  Content:  v[N] active [✓ consistent | ⚠ CLAUDE.md references old version]

CHANGELOG: [Updated/No changes]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Scope Options

- **all** (default) — Full documentation scan + health check
- **health** — Health check only (Steps 4-6), skip index regeneration
- **features** — Update features section of docs/README.md only
- **FEAT-XXX** — Update specific feature entry only

## Success Criteria

✅ docs/README.md regenerated (unless health-only scope)
✅ All features listed with correct status
✅ Cross-references validated
✅ Broken links reported
✅ Health check completed with no unacknowledged issues
