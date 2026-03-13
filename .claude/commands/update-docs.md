---
updated: 2026-01-24T12:00:00Z
description: Update documentation index and validate cross-references
argument-hint: [scope: all|features|FEAT-XXX]
---

# Documentation Update

You are updating project documentation.

**Scope:** ${ARGUMENTS:-all}

## Mission

Regenerate docs/README.md index, validate cross-references, and optionally update CHANGELOG.

## Workflow

### Step 1: Scan Documentation

Use Glob to find all documentation:
```
docs/features/*/
docs/features/*/research-*.md
docs/system/*.md
docs/spikes/*.md
docs/templates/*.md
```

For each feature folder, determine status by checking which files exist:
- Only `prd.md` → Exploring
- `prd.md` + `plan.md` → Ready for Implementation
- `prd.md` + `plan.md` + implementation files → In Progress
- All complete + tests passing → Complete

### Step 2: Regenerate docs/README.md

Create organized index:

```markdown
---
updated: [current timestamp]
---

# Documentation Index

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| [FEAT-XXX](./features/FEAT-XXX_slug/) | [Status] | [From PRD] |

## System Documentation

- [architecture.md](./system/architecture.md)
- [observability.md](./system/observability.md)
- [integrations.md](./system/integrations.md)
- [connections.md](./system/connections.md)

## Spikes

Experimental investigations in `docs/spikes/`:
- [spike-name.md](./spikes/spike-name.md)

## Templates

Templates in `docs/templates/`:
- prd-template.md
- plan-template.md
- readme-template.md
```

### Step 3: Validate Cross-References

Search for markdown links and verify targets exist:
- Use Grep to find `[text](path)` patterns
- Check if target files exist
- Report broken links

### Step 4: Update CHANGELOG (Optional)

If new features were added or documentation changed significantly:
```markdown
## [Unreleased]

### Changed
- Updated documentation index
- [List specific changes]
```

### Step 5: Present Summary

```
✅ Documentation Updated

Index: docs/README.md regenerated
Features: X (A exploring, B ready, C complete)
Research: Y files
System Docs: Z files

Cross-References: X valid, Y broken
[List any broken links]

CHANGELOG: [Updated/No changes]
```

## Scope Options

- **all** (default) - Full documentation scan
- **features** - Update features section only
- **FEAT-XXX** - Update specific feature only

## Success Criteria

✅ docs/README.md regenerated
✅ All features listed with correct status
✅ Cross-references validated
✅ Broken links reported
