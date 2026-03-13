---
updated: 2026-02-01T12:00:00Z
description: Create git commit with conventional format, QA gate, and CI verification
argument-hint: [message]
---

# Git Commit

Message hint: **$ARGUMENTS**

## Mission

Create a clean, conventional commit with QA gate enforcement and automated CI verification. Concise messages that describe WHAT changed and WHY.

**Flow:** **QA Gate** → Tests → Analyze → Preview → Commit → Push → **Verify CI** → Done

---

## Workflow

### Step 0: QA Gate Check (NEW)

Before proceeding with any commit:

1. **Detect feature context** from recent file changes or context:
   ```bash
   # Check for feature folder in staged/modified files
   git status --short | grep -E "docs/features/FEAT-[0-9]+"
   ```

2. **If feature detected**, look for QA report:
   ```bash
   # Find most recent qa-report for this feature
   ls -t docs/qa/FEAT-XXX-*.md 2>/dev/null | head -1
   ```

3. **Check QA status** in the report frontmatter:
   - **APPROVED**: Proceed with commit
   - **NEEDS_FIXES**: Warn user
   - **BLOCKED**: Warn user (security issue pending)
   - **No report found**: Note that QA hasn't run

**If BLOCKED or NEEDS_FIXES:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  QA ISSUES PENDING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: FEAT-XXX
QA Report: docs/qa/FEAT-XXX-[scope]-YYYYMMDD.md
Status: NEEDS_FIXES | BLOCKED

Issues:
- [List from report]

Options:
1. Run /qa to resolve issues first (recommended)
2. Override and commit anyway (requires explicit confirmation)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If user explicitly confirms override, proceed. Otherwise, suggest running `/qa` first.

**If no feature context or APPROVED:**

Continue to Step 1.

---

### Step 1: Check Status

```bash
git status
```

- Show changed files
- If no changes: "Nothing to commit"

### Step 2: Run Tests (MANDATORY)

```bash
npm test  # or pytest, cargo test, etc.
```

**CRITICAL: This step is MANDATORY, not optional.**

- If tests fail: "Fix tests before committing OR skip unrelated failures with explicit user approval"
- If no test command exists: Document this as a blocker
- Never skip this step silently

**Why:** Catches issues locally in seconds vs. minutes in CI

### Step 3: Analyze Changes

Detect commit type from files changed:

| Type | When to Use |
|------|-------------|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Test additions/changes |
| `refactor` | Code change, no behavior change |
| `chore` | Maintenance, dependencies |

Infer scope from file paths:
- `docs/features/FEAT-123/` → `FEAT-123`
- `src/auth/` → `auth`
- `.claude/` → `tooling`

### Step 4: Generate Message

**Format:** `<type>(<scope>): <description>`

**Rules:**
- Subject line: 50 characters max
- Imperative mood: "Add" not "Added"
- No period at end
- Body only if truly necessary
- Do not include Co-Authored-By (template default — users may override in their CLAUDE.md)
- NEVER mention Claude or AI

**Good examples:**
```
feat(FEAT-009): add two-phase discovery to explore
fix(auth): handle expired token refresh
docs(readme): update installation steps
refactor(api): extract validation to middleware
test(auth): add integration tests for login
```

**Bad examples:**
```
Updated stuff                          # Too vague
feat: Add new feature for users        # Redundant ("feature")
Fixed the bug in the thing             # Past tense, unclear
```

### Step 5: Preview and Confirm

Show the user:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMMIT PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Message: <type>(<scope>): <description>

Files to stage:
  M .claude/commands/explore.md
  M .claude/commands/plan.md
  A docs/features/FEAT-009/plan.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceed with commit?
```

Wait for user approval.

### Step 6: Commit

```bash
git add [relevant files]
git commit -m "<message>"
```

### Step 7: Push and Verify CI (MANDATORY)

After successful commit, ask user: "Push to remote?"

If user confirms push:

```bash
# Push to remote
git push -u origin <branch>
```

**Then AUTOMATICALLY verify CI (non-optional):**

```bash
# Check if gh CLI is available
if command -v gh &> /dev/null; then
  echo "⏳ Waiting for CI pipeline..."

  # Get the latest run ID for current branch
  BRANCH=$(git branch --show-current)
  RUN_ID=$(gh run list --branch "$BRANCH" --limit 1 --json databaseId --jq '.[0].databaseId')

  # Watch the run
  gh run watch "$RUN_ID" --exit-status
else
  echo "❌ gh CLI not found. Install: brew install gh && gh auth login"
  echo "📋 Check manually: https://github.com/[owner]/[repo]/actions"
  exit 1
fi
```

**CI Verification Rules:**
- `gh run watch --exit-status` watches the latest workflow run
- Exits with code 0 if CI passes, non-zero if fails
- Shows live progress (markdown lint, YAML validation, hook checks, structure validation)
- **MANDATORY** - cannot skip this step when pushing
- If CI fails, show which step failed and suggest fixes

**Expected output:**
```
✓ Pushed to origin/harness-v2
⏳ Waiting for CI pipeline...
  ✓ Markdown lint (continue-on-error)
  ✓ YAML validation
  ✓ Python hook syntax
  ✓ Template structure validation
✅ CI passed in 12s
```

---

## Safety

- Never force push to main/master
- Warn if secrets detected (.env, credentials, API keys)
- Always preview before commit
- Require user approval
- **Require gh CLI for push operations** (enforces CI verification)

---

## PR Creation (Optional)

After CI passes, optionally offer PR creation:

```bash
gh pr create --title "<commit message>" --body "..."
```

PR body format:
```markdown
## Summary
- [Bullet points from commits]

## Test Plan
- [How to verify]

✅ CI Status: All checks passed
```

---

## CI Troubleshooting

### If CI Fails

When `gh run watch` reports failure:

1. **Identify which step failed:**
   ```bash
   gh run view $RUN_ID --log-failed
   ```

2. **Common failures and fixes:**

   | Failed Step | Likely Cause | Fix |
   |-------------|--------------|-----|
   | Markdown lint | Formatting issues | Run `markdownlint --fix **/*.md` locally |
   | YAML validation | Workflow syntax error | Run `actionlint .github/workflows/*.yml` |
   | Python hook syntax | Syntax error in .claude/hooks/ | Check Python files with `python3 -m py_compile` |
   | Template structure | Missing required file | Check `validate-structure.sh` output |

3. **Fix and re-push:**
   ```bash
   # Make fixes
   git add .
   git commit --amend --no-edit
   git push --force-with-lease
   ```

4. **Re-verify CI:**
   ```bash
   BRANCH=$(git branch --show-current)
   RUN_ID=$(gh run list --branch "$BRANCH" --limit 1 --json databaseId --jq '.[0].databaseId')
   gh run watch "$RUN_ID" --exit-status
   ```

### Prerequisites for Push

Before running `/commit` with push:
- ✅ `gh` CLI installed: `brew install gh`
- ✅ `gh` authenticated: `gh auth login`
- ✅ Verify with: `gh auth status`

---

## Success Criteria

- ✅ **QA gate passed** (APPROVED or no feature context)
- ✅ Tests pass locally (if available)
- ✅ No secrets in staged files
- ✅ Message follows conventional format
- ✅ Subject ≤50 characters
- ✅ User approved the preview
- ✅ Commit created successfully
- ✅ **CI pipeline passed (if pushed)**

---

## See Also

- [/qa Command](./qa.md) - Run QA review
- [/build Command](./build.md) - Integrated TDD + QA
- [QA Storage](../../docs/qa/README.md) - QA report location and naming
