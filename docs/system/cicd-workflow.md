# CI/CD Workflow

**Updated:** 2026-01-28T11:00:00Z
**Purpose:** Automated validation and deployment pipeline reference

---

## Overview

The CI/CD system provides fast (<15s) feedback through GitHub Actions workflows, integrated directly into the `/commit` command. Every push triggers automated validation, and the commit workflow waits for CI results before completing.

**Core principle:** "No push completes without CI verification."

---

## Architecture

### Two-Tier Workflow Strategy

```
Base Validation (always runs)
├── Markdown linting (continue-on-error)
├── YAML validation (actionlint)
├── Python hook syntax check
└── Template structure validation

Stack-Specific Tests (path-filtered)
└── Runs only when stack directory changes
```

### Integration Points

| Component | Trigger | Duration | Purpose |
|-----------|---------|----------|---------|
| `.github/workflows/validate.yml` | Every push | <15s | Base validation |
| `.github/workflows/stack-*.yml` | Path-filtered | Varies | Stack-specific tests |
| `/commit` command | Manual | <30s | Git workflow + CI verification |
| `gh CLI` | Required | N/A | CI status monitoring |

---

## The /commit Workflow

### Complete Flow

```
1. Check git status
2. Run local tests (npm test, pytest, etc.)
3. Analyze changes → Generate commit message
4. Preview → User approval
5. Create commit
6. Push to remote
7. ⚙️ VERIFY CI (automatic, mandatory)
   ├── Watch workflow run live
   ├── Report each validation step
   └── Exit with success/failure code
8. Optionally create PR
```

### Step 7: CI Verification (The Critical Part)

After pushing, the command **automatically** runs:

```bash
# Get latest run ID for current branch
BRANCH=$(git branch --show-current)
RUN_ID=$(gh run list --branch "$BRANCH" --limit 1 --json databaseId --jq '.[0].databaseId')

# Watch the run
gh run watch "$RUN_ID" --exit-status
```

**What happens:**
- Waits for the latest workflow run to start
- Shows live progress of validation steps:
  - ✓ Markdown lint
  - ✓ YAML validation
  - ✓ Python hook syntax
  - ✓ Template structure validation
- Exits with code 0 if all pass, non-zero if any fail
- **Cannot be skipped** - it's mandatory

**Expected output:**
```
✓ Pushed to origin/feature-branch
⏳ Waiting for CI pipeline...
  ✓ Markdown lint (8s)
  ✓ YAML validation (3s)
  ✓ Python hook syntax (2s)
  ✓ Template structure validation (1s)
✅ CI passed in 14s
```

---

## Validation Steps

### 1. Markdown Linting

**Tool:** markdownlint-cli2
**Config:** `.markdownlint.json`
**Behavior:** `continue-on-error: true` (warns but doesn't fail)

**Purpose:** Catch formatting issues early without blocking

### 2. YAML Validation

**Tool:** actionlint
**Target:** `.github/workflows/*.yml`
**Behavior:** Fails on errors

**Purpose:** Validate workflow syntax before GitHub runs them

### 3. Python Hook Syntax

**Tool:** `python3 -m py_compile`
**Target:** `.claude/hooks/*.py`
**Behavior:** Fails on syntax errors

**Purpose:** Catch Python errors in hooks before they break workflows

### 4. Template Structure

**Script:** `.github/tests/validate-structure.sh`
**Checks:** Required files (CLAUDE.md, PROJECT.md, etc.)
**Behavior:** Fails on missing files

**Purpose:** Ensure template integrity

---

## Prerequisites

### Required: gh CLI

The `/commit` workflow **requires** the GitHub CLI for CI verification.

**Installation:**
```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli
```

**Authentication:**
```bash
gh auth login
# Choose:
# - github.com
# - HTTPS protocol (recommended)
# - Authenticate via browser
```

**Verify:**
```bash
gh auth status
# Should show: ✓ Logged in to github.com
```

### Why gh CLI is Required

Without `gh` CLI, the `/commit` command:
- Cannot verify CI status automatically
- Cannot show live workflow progress
- Cannot detect CI failures before you move on
- Defeats the purpose of integrated CI/CD

**The requirement is intentional.** Manual CI checking (opening GitHub in browser) is error-prone and slow.

---

## Troubleshooting

### CI Failure Scenarios

| Failed Step | Symptom | Fix |
|-------------|---------|-----|
| **Markdown lint** | Formatting issues reported | Run `markdownlint --fix **/*.md` locally |
| **YAML validation** | Workflow syntax error | Run `actionlint .github/workflows/*.yml` |
| **Python hook syntax** | Syntax error in hooks | Check with `python3 -m py_compile .claude/hooks/*.py` |
| **Template structure** | Missing required file | Check output of `.github/tests/validate-structure.sh` |

### How to Fix and Re-Push

```bash
# 1. View failed logs
gh run view --log-failed

# 2. Make fixes locally
# (fix the specific issue)

# 3. Amend commit
git add .
git commit --amend --no-edit

# 4. Force push (safe with --force-with-lease)
git push --force-with-lease

# 5. Re-verify CI
BRANCH=$(git branch --show-current)
RUN_ID=$(gh run list --branch "$BRANCH" --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status
```

### Common Issues

**"gh: command not found"**
```bash
# Install gh CLI (see Prerequisites above)
brew install gh
gh auth login
```

**"No workflow run found"**
```bash
# Workflow may not have started yet. Wait 5-10s and retry:
gh run list --branch <your-branch> --limit 1
```

**"CI taking too long (>30s)"**
```bash
# Check which step is slow:
gh run view
# Usually means:
# - Network issues downloading actions
# - actionlint downloading binary
# - First run (actions being cached)
```

---

## CI Workflow Files

### Base Validation: `.github/workflows/validate.yml`

**Triggers:**
- Every push to any branch
- Every pull request

**Jobs:**
1. Checkout code
2. Markdown lint (markdownlint-cli2, continue-on-error)
3. YAML validation (actionlint)
4. Python hook syntax check
5. Template structure validation

**Customization:** Add language-specific steps after line 60 (marked with `# CUSTOMIZATION:`)

**Example additions:**
```yaml
# TypeScript type checking
- name: TypeScript Check
  run: npx tsc --noEmit

# ESLint
- name: Lint TypeScript
  run: npx eslint .

# Python linting
- name: Ruff Check
  run: ruff check .
```

### Stack Workflows: `.github/workflows/stack-*.yml`

**Example:** `.github/workflows/stack-cloudflare.yml`

**Triggers:**
- Push with changes to `stacks/cloudflare/**`
- Pull request with changes to `stacks/cloudflare/**`

**Jobs:**
1. Checkout code
2. Setup Node.js
3. Install dependencies in stack directory
4. Run stack tests (`npm test`)

**Pattern:** One workflow per stack, path-filtered

---

## Local Validation

### Before Pushing

Run these locally to catch issues before CI:

```bash
# Markdown linting
npx markdownlint-cli2 "**/*.md"

# YAML validation (workflows)
bash <(curl -sL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
./actionlint -color .github/workflows/*.yml

# Python hook syntax
find .claude/hooks -name "*.py" -exec python3 -m py_compile {} \;

# Template structure
.github/tests/validate-structure.sh
```

### Using the ci-validation Skill

```bash
# Validates workflows locally before pushing
# See .claude/skills/ci-validation/ for full guide
```

---

## Best Practices

### 1. Always Push Through /commit

```bash
# ✅ Good: Integrated CI verification
/commit

# ❌ Bad: Manual push bypasses verification
git push
```

### 2. Fix CI Failures Immediately

Don't accumulate broken CI runs. Fix and re-push right away:
```bash
# View failure
gh run view --log-failed

# Fix, amend, re-push
git add . && git commit --amend --no-edit && git push --force-with-lease
```

### 3. Keep CI Fast (<15s)

The base validation workflow is optimized for speed:
- Uses fast linters (markdownlint-cli2, actionlint)
- Caches action downloads
- Runs validation in parallel where possible

If CI becomes slow:
- Check which step is slow: `gh run view`
- Consider moving heavy tests to stack-specific workflows
- Ensure actions are properly cached

### 4. Test Workflows Locally

Before pushing workflow changes:
```bash
actionlint .github/workflows/*.yml
```

### 5. Use continue-on-error Wisely

Markdown linting uses `continue-on-error: true` because:
- Formatting issues shouldn't block deploys
- Warnings are still visible in logs
- Can be addressed later

Don't use `continue-on-error` for:
- Security checks
- Critical validation (YAML syntax, Python syntax)
- Tests

---

## Security Considerations

### Secret Scanning

GitHub's built-in secret scanning is **separate** from workflows.

**To enable:**
1. Go to repository **Settings**
2. Navigate to **Code security and analysis**
3. Enable **Secret scanning**
4. (Optional) Enable **Push protection** to block commits with secrets

**No workflow configuration needed** - GitHub scans automatically.

### Workflow Security

- Never use `--no-verify` with git commands
- Never force push to main/master (blocked in `/commit` command)
- Always use `actions/checkout@v4` (pinned versions)
- Don't store secrets in workflow files (use GitHub Secrets)

---

## Monitoring and Debugging

### View Recent Runs

```bash
# List recent workflow runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# View logs for failed run
gh run view --log-failed
```

### Query Run History

```bash
# Runs on specific branch
gh run list --branch feature-branch

# Failed runs only
gh run list --status failure

# Runs for specific workflow
gh run list --workflow validate.yml
```

### Watch Live Run

```bash
# Watch latest run (used by /commit)
gh run watch --exit-status

# Watch specific run
gh run watch <run-id>
```

---

## Related Documentation

- See your own feature docs in `docs/features/` for project-specific CI/CD details
- [.github/workflows/README.md](../../.github/workflows/README.md) - Workflow customization guide
- [.claude/commands/commit.md](../../.claude/commands/commit.md) - Commit command reference
- [observability.md](./observability.md) - Logging and debugging

---

## Success Criteria

You know CI/CD is working correctly when:

✅ `/commit` automatically verifies CI after pushing
✅ CI completes in <15 seconds for base validation
✅ All four validation steps pass (markdown, YAML, Python, structure)
✅ `gh run watch` shows live progress
✅ CI failures block before you move on to next task
✅ Stack workflows only run when their directories change
