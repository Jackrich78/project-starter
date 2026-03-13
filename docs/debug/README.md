# Debug Reports (System-Wide)

This directory contains debug reports for **system-wide bugs** that affect multiple features or core infrastructure.

For **feature-specific bugs**, debug reports are stored in the feature folder: `docs/features/FEAT-XXX/debug-*.md`

## Structure

```
docs/debug/
├── README.md                          # This file
├── [issue-slug]-YYYYMMDD.md          # Debug report
├── [issue-slug]-YYYYMMDD.md          # Debug report
└── ...
```

## Naming Convention

Debug reports follow this pattern:

```
[issue-slug]-YYYYMMDD.md
```

**Examples:**
- `sql-injection-user-search-20260212.md`
- `auth-middleware-500-error-20260115.md`
- `database-connection-timeout-20260308.md`
- `memory-leak-worker-threads-20260420.md`

**Slug format:**
- Lowercase
- Hyphen-separated words
- Descriptive (3-5 words)
- Date: YYYYMMDD format

## When to Use This Directory

Use `docs/debug/` for bugs that:

- Affect **multiple features** (cross-cutting concerns)
- Are in **shared infrastructure** (auth, database, API layer, routing)
- Are **system-level** (configuration, deployment, monitoring)
- Have **no specific feature scope** (FEAT-XXX)

**Examples:**
- Authentication middleware returns 500 for all requests
- Database connection pool exhaustion
- Memory leak in background worker
- CORS configuration blocking all API calls
- Environment variable not loading correctly

## When NOT to Use This Directory

Use feature folder instead (`docs/features/FEAT-XXX/`) for bugs that:

- Affect a **single feature** (e.g., checkout calculation bug)
- Can be **traced to feature code** (e.g., FEAT-012 login form validation)
- Are **contained within feature boundaries**

## Debug Report Template

All debug reports use the same template regardless of location:

```
.claude/skills/debug/references/debug-report-template.md
```

**Required sections:**
- Summary (What was broken, what was fixed, impact)
- Timeline (Discovery → investigation → fix)
- Investigation (Reproduction, diagnostics, hypothesis)
- Root Cause Analysis (Exact failure point, why it failed)
- Solution (Fix approach, code changes, regression test)
- Validation (Test results, manual validation)
- Prevention (How to prevent similar bugs, learnings)

## Workflow

### Creating Debug Reports

Debug reports are created by the `/debug` command:

```bash
/debug "Database connection timeout on production"
```

The debug skill:
1. Classifies bug (type, severity, scope)
2. Determines scope (feature vs system)
3. Investigates and fixes
4. Creates report in correct location:
   - **System bug** → `docs/debug/[slug]-YYYYMMDD.md`
   - **Feature bug** → `docs/features/FEAT-XXX/debug-[slug]-YYYYMMDD.md`

### Referencing Debug Reports

**In commit messages:**
```
fix: resolve database connection timeout

Root cause: Connection pool exhausted under load
Regression test: test/integration/database-connection-pool.test.ts
Debug report: docs/debug/database-connection-timeout-20260212.md
```

**In handover documents:**
```markdown
## Bug Fixes

- Fixed database connection timeout issue
  - Debug report: docs/debug/database-connection-timeout-20260212.md
  - Impact: All API endpoints affected during peak load
  - Fix: Increased connection pool size and added monitoring
```

**In architecture docs:**
```markdown
## Database Layer

Connection pooling configuration updated after connection timeout issue
(see docs/debug/database-connection-timeout-20260212.md).

Current configuration:
- Pool size: 20 (increased from 10)
- Idle timeout: 30s
- Connection timeout: 5s
```

## Index

This section should be manually updated when new debug reports are added.

### By Category

#### Authentication & Authorization
- (No reports yet)

#### Database & Persistence
- (No reports yet)

#### API & Integration
- (No reports yet)

#### Performance & Scaling
- (No reports yet)

#### Infrastructure & Deployment
- (No reports yet)

#### Testing & CI/CD
- (No reports yet)

### By Severity

#### P0 (Critical)
- (No reports yet)

#### P1 (High)
- (No reports yet)

#### P2 (Medium)
- (No reports yet)

#### P3 (Low)
- (No reports yet)

#### P4 (Trivial)
- (No reports yet)

### Recent Reports

(Most recent first)

- (No reports yet)

## Maintenance

### When to Archive

Debug reports should be archived when:

- Bug is ancient (>2 years old)
- Code has been completely refactored (solution no longer relevant)
- System architecture changed fundamentally (context no longer applies)

**Archive process:**
1. Move to `docs/debug/archive/[year]/`
2. Update references in other docs
3. Add note to archive index

### When to Delete

**Never delete debug reports.** They are valuable historical documentation.

If absolutely necessary to delete:
1. Ensure no other docs reference it
2. Create archive entry with summary
3. Document why deletion was necessary

## Integration with Workflow

```
Bug discovered in production
    ↓
/debug "issue description"
    ↓
Debug skill classifies as system bug
    ↓
Investigation and fix
    ↓
Report created: docs/debug/[slug]-YYYYMMDD.md
    ↓
Architecture docs updated
    ↓
/commit
    ↓
Commit references debug report
```

## See Also

- [Debug Skill](../../.claude/skills/debug/SKILL.md) - Systematic debugging workflow
- [Debug Command](../../.claude/commands/debug.md) - Debug command documentation
- [Debug Report Template](../../.claude/skills/debug/references/debug-report-template.md) - Report structure
- [Decision Trees](../../.claude/skills/debug/references/decision-trees.md) - Bug classification
- [System Architecture](../system/architecture.md) - Overall system design
- [Connections](../system/connections.md) - Component relationships
