---
updated: 2026-02-01T12:00:00Z
description: Run QA review on target (file, directory, feature, or sweep)
argument-hint: [target] [--feature FEAT-XXX]
---

# QA Review

Target: **$ARGUMENTS**

## Mission

Run an independent security and quality review on the specified target. The qa-reviewer subagent operates with clean context, applying OWASP security checks and code quality validation.

## Usage

```bash
# Sweep recent changes
/qa

# Review a specific file
/qa src/auth/tokens.ts

# Review a directory
/qa src/utils/

# Review a feature (uses handover if available)
/qa --feature FEAT-018

# Review with feature context
/qa src/auth/ --feature FEAT-018
```

---

## Target Types

| Target | Scope | Context Source |
|--------|-------|----------------|
| (empty) | Sweep recent git changes | `git diff HEAD~1` |
| `src/path/file.ts` | Single file | Direct file read |
| `src/path/` | Directory (recursive) | All files in directory |
| `--feature FEAT-XXX` | Feature scope | handover.md + PRD |

---

## Workflow

### Step 1: Parse Target

```
If no arguments:
  → Sweep mode: Review all files changed since last commit
  → git diff HEAD~1 HEAD --name-only

If path argument:
  → File: Review single file
  → Directory: Review all files recursively

If --feature FEAT-XXX:
  → Feature mode: Read handover.md for context
  → Scope to files mentioned in handover
```

### Step 2: Gather Context

**For feature-scoped reviews:**
```
Read: docs/features/FEAT-XXX/handover.md (if exists)
Read: docs/features/FEAT-XXX/prd.md
Extract: Key files from handover
```

**For file/directory reviews:**
```
List all files in scope
Get git diff for changes (if in git)
No handover context (standalone review)
```

**For sweep reviews:**
```
git diff HEAD~1 HEAD --name-only
Review all changed files
No specific feature context
```

### Step 3: Invoke QA Reviewer

```
Task(
  subagent_type="qa-reviewer",
  description="QA: Review [target description]",
  prompt="Review the following files/changes.

  Scope: [target]
  Files: [list of files]
  Context: [handover summary if feature mode]

  @.claude/agents/qa-reviewer.md

  Perform:
  1. OWASP security review (≥80% confidence only)
  2. Code quality review
  3. Test coverage check (if tests exist)

  Create report following qa-report-template.md"
)
```

### Step 4: Create Report

The qa-reviewer creates a report in `docs/qa/` with appropriate naming:

| Scope | Report Name |
|-------|-------------|
| Feature | `FEAT-XXX-[description]-YYYYMMDD.md` |
| Directory | `[path-slug]-YYYYMMDD.md` |
| File | `[filename-slug]-YYYYMMDD.md` |
| Sweep | `sweep-YYYYMMDD.md` |

### Step 5: Present Findings

After review completes:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QA REVIEW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Report: docs/qa/[report-name].md
📊 Status: [APPROVED | NEEDS_FIXES | BLOCKED]

Issues Found:
  🔴 Critical: [X]
  🟡 Warning: [Y]
  🔵 Info: [Z]

[If APPROVED]
✅ Ready for /commit

[If NEEDS_FIXES]
⚠️ Address issues and re-run /qa

[If BLOCKED]
🛑 Human decision required (security issue)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Examples

### Example 1: Sweep Recent Changes

```
User: /qa

Step 1: git diff HEAD~1 HEAD --name-only
  → src/auth/tokens.ts
  → src/middleware/auth.ts
  → test/auth/tokens.test.ts

Step 2: No feature context (sweep mode)

Step 3: Invoke qa-reviewer for 3 files

Step 4: Creates docs/qa/sweep-20260201.md

Step 5: Present findings
```

### Example 2: Feature-Scoped Review

```
User: /qa --feature FEAT-018

Step 1: Feature mode, FEAT-018

Step 2: Read docs/features/FEAT-018_auth/handover.md
  → Key files: src/auth/*.ts, test/auth/*.ts
  Read PRD for requirements context

Step 3: Invoke qa-reviewer with handover context

Step 4: Creates docs/qa/FEAT-018-auth-20260201.md

Step 5: Present findings with feature context
```

### Example 3: Directory Review

```
User: /qa src/utils/

Step 1: Directory mode, src/utils/

Step 2: List all files in src/utils/
  → src/utils/validators.ts
  → src/utils/helpers.ts
  → src/utils/index.ts

Step 3: Invoke qa-reviewer for directory

Step 4: Creates docs/qa/src-utils-20260201.md

Step 5: Present findings
```

---

## Report Status Actions

### APPROVED

No action required. Code is ready for commit.

```
/qa → APPROVED → /commit (unblocked)
```

### NEEDS_FIXES

Issues found that should be addressed:

1. Review report in `docs/qa/`
2. Address each issue
3. Re-run `/qa` to verify fixes
4. Loop until APPROVED

```
/qa → NEEDS_FIXES
  → Fix issues
  → /qa (again)
  → APPROVED
  → /commit
```

### BLOCKED

Critical security issue requiring human decision:

1. QA has escalated via AskUserQuestion
2. Human reviews and decides
3. Apply decision
4. Re-run `/qa` to confirm resolution

```
/qa → BLOCKED
  → Human decision (block | accept | false positive)
  → Apply decision
  → /qa (again)
  → APPROVED
  → /commit
```

---

## Integration with /build

When used within `/build`:
- QA is automatic after TDD completes
- Uses handover.md for context
- Iterates until APPROVED

When used standalone:
- Manual invocation for targeted reviews
- Can review any files, not just feature builds
- Useful for pre-commit checks on arbitrary changes

---

## Options

| Option | Description |
|--------|-------------|
| `--feature FEAT-XXX` | Use feature handover for context |
| (path) | Target specific file or directory |
| (empty) | Sweep recent git changes |

---

## Success Criteria

- ✅ Target correctly identified (file/directory/feature/sweep)
- ✅ Context gathered (handover if feature mode)
- ✅ qa-reviewer invoked with clean context
- ✅ Report created in docs/qa/ with correct naming
- ✅ Status clearly communicated (APPROVED/NEEDS_FIXES/BLOCKED)

---

## See Also

- [QA Reviewer Agent](.claude/agents/qa-reviewer.md) - Review logic
- [QA Report Template](docs/templates/qa-report-template.md) - Report format
- [QA Storage](docs/qa/README.md) - Report naming and lifecycle
- [/build Command](.claude/commands/build.md) - Integrated QA
- [/commit Command](.claude/commands/commit.md) - QA gate enforcement
