# Upstream Workflow Contributions

**Purpose:** Step-by-step guide for contributing improvements from downstream projects back to the project-starter template.

**Updated:** 2026-02-06

---

## Overview

When you discover improvements while working in a downstream project (bug fixes, better prompts, clarified docs), you can contribute them back to the template so all projects benefit.

**The Flow:**
```
Your Project → Fix/Improve → Create PR → Review → Merge to Template → Sync to All Projects
```

**Why this matters:**
- Bug fix in flashcard-app helps project-2 and project-3
- Better prompt discovered in production improves workflow for everyone
- Template evolves based on real-world usage, not theory

---

## When to Upstream

### ✅ Good Candidates for Upstream

| Type | Example | Why |
|------|---------|-----|
| **Bug fixes** | qa-reviewer crashes on null response | Fixes issues others will hit |
| **Prompt improvements** | Better TDD test-writer prompt with evidence | Proven in production |
| **New skills** | Learned pattern worth capturing | Reusable across projects |
| **Doc clarifications** | getting-started.md was confusing | Helps future users |
| **Security fixes** | Fix XSS vulnerability in agent | Critical for all projects |

### ❌ Don't Upstream These

| Type | Example | Why |
|------|---------|-----|
| **Project-specific hacks** | Workaround for flashcard-app's DB schema | Only relevant to one project |
| **Experimental changes** | Trying a new approach, not validated | Too risky for template |
| **Half-baked ideas** | Partial refactor, needs more work | Not ready for production |
| **Project customizations** | Flashcard-specific specialist agent | Belongs in project, not template |
| **Performance tweaks** | Optimization for specific use case | May not generalize |

### Quality Bar Checklist

Before upstreaming, ask:
- [ ] Does this improve the workflow for **ALL** projects?
- [ ] Is it **battle-tested** (used in production)?
- [ ] Does it follow **template conventions** (naming, structure)?
- [ ] Is it **documented** (comments, clear purpose)?
- [ ] Does it have **no project-specific dependencies**?

If all ✅, proceed to upstream.

---

## Step-by-Step: Upstream a Change

### Prerequisites

- Downstream project has `workflow` remote configured (see workflow-sync-guide.md)
- You have write access to project-starter repo (or can fork it)
- Change is committed locally in your downstream project

### Step 1: Verify Your Change

```bash
# From your downstream project (e.g., flashcard-app)
cd ~/dev/flashcard-app

# Ensure change is committed
git status

# View the specific change
git log --oneline -1 .claude/agents/qa-reviewer.md
git diff HEAD~1 .claude/agents/qa-reviewer.md
```

**Important:** Only the workflow files (`.claude/agents/`, `.claude/commands/`, `docs/system/`, `docs/templates/`) should be upstreamed. Never upstream `src/`, `test/`, or project-specific configs.

### Step 2: Create Upstream Branch

```bash
# Create a descriptive branch name
# Format: upstream/<type>-<brief-description>
# Examples: upstream/fix-qa-null, upstream/improve-tdd-prompt

git checkout -b upstream/fix-qa-null

# Ensure only the relevant file(s) are in this commit
git log --oneline --name-only -1
```

### Step 3: Push to Template Repository

```bash
# Push your branch to the template repo (via workflow remote)
git push workflow upstream/fix-qa-null

# You should see:
# remote: Create a pull request for 'upstream/fix-qa-null' on GitHub by visiting:
# remote:   https://github.com/jackrich78/project-starter/pull/new/upstream/fix-qa-null
```

### Step 4: Create Pull Request

#### Option A: Using GitHub CLI (Recommended)

```bash
gh pr create \
  --repo jackrich78/project-starter \
  --base v2 \
  --head upstream/fix-qa-null \
  --title "fix(qa): handle null responses in OWASP checklist" \
  --body "## Context
Discovered this edge case in flashcard-app production.

## Problem
When OWASP security check returns \`null\` instead of \`false\`,
qa-reviewer crashes with: \`TypeError: Cannot read property 'confidence' of null\`

## Solution
Added null checking before accessing confidence score.

## Testing
- Tested in flashcard-app with null responses
- Confirmed qa-reviewer completes without crashing
- All existing tests still pass

## Impact
All projects using qa-reviewer will benefit from this fix.

---
Upstreamed from: flashcard-app
Discovered: 2026-02-06"
```

#### Option B: Using GitHub Web UI

1. Visit the URL shown after `git push workflow`
2. Set **base branch** to `v2` (or `main` if contributing to stable)
3. Fill in PR template:
   - **Title:** Conventional format: `fix(qa):`, `feat(tdd):`, `docs:`, etc.
   - **Body:** Context, problem, solution, testing, impact
   - **Label:** Add `upstream` label if available
4. Click "Create Pull Request"

### Step 5: PR Review and Merge

**What happens next:**
1. Template maintainer (you or team) reviews the PR
2. Automated tests run (if configured)
3. Discussion/feedback if needed
4. Merge to `v2` branch when approved

**After merge:**
```bash
# In template repo
cd ~/dev/project-starter
git checkout v2
git pull origin v2

# Tag new version (patch for bug fix, minor for feature)
git tag v2.1.1 -m "Bug fix: qa-reviewer null handling"
git push origin v2.1.1

# Update CHANGELOG.md
echo "## [v2.1.1] - 2026-02-06
### Fixed
- qa-reviewer: Handle null responses in OWASP checklist (#123)
  Upstreamed from: flashcard-app" >> CHANGELOG.md

git add CHANGELOG.md
git commit -m "chore: update CHANGELOG for v2.1.1"
git push origin v2
```

### Step 6: Sync Back to All Projects

Now the improvement flows back to all downstream projects:

```bash
# In flashcard-app (where it originated)
cd ~/dev/flashcard-app
npm run sync-workflow  # Gets v2.1.1 with your fix

# In project-2
cd ~/dev/project-2
npm run sync-workflow  # Gets the same fix

# In project-3
cd ~/dev/project-3
npm run sync-workflow  # Everyone benefits
```

**Full cycle complete!** 🎉

---

## Common Scenarios

### Scenario 1: Bug Fix (PATCH version)

**Example:** qa-reviewer crashes on edge case

```bash
# In downstream project
git add .claude/agents/qa-reviewer.md
git commit -m "fix(qa): handle null responses"
git checkout -b upstream/fix-qa-null
git push workflow upstream/fix-qa-null

# Create PR with gh CLI
gh pr create --repo jackrich78/project-starter \
  --base v2 \
  --head upstream/fix-qa-null \
  --title "fix(qa): handle null responses in OWASP checklist"

# After merge, tag PATCH: v2.1.1 → v2.1.2
```

### Scenario 2: Prompt Improvement (MINOR version)

**Example:** Better prompt for tdd-test-writer discovered through usage

```bash
# In downstream project
git add .claude/agents/tdd-test-writer.md
git commit -m "feat(tdd): improve test prompt clarity"
git checkout -b upstream/improve-tdd-prompt
git push workflow upstream/improve-tdd-prompt

# Create PR
gh pr create --repo jackrich78/project-starter \
  --base v2 \
  --head upstream/improve-tdd-prompt \
  --title "feat(tdd): improve test-writer prompt for edge cases"

# After merge, tag MINOR: v2.1.0 → v2.2.0
```

### Scenario 3: Documentation Clarification (PATCH version)

**Example:** getting-started.md was confusing

```bash
# In downstream project
git add docs/system/getting-started.md
git commit -m "docs: clarify stack merge instructions"
git checkout -b upstream/clarify-docs
git push workflow upstream/clarify-docs

# Create PR
gh pr create --repo jackrich78/project-starter \
  --base v2 \
  --head upstream/clarify-docs \
  --title "docs: clarify stack merge instructions"

# After merge, tag PATCH: v2.1.0 → v2.1.1
```

### Scenario 4: New Skill Learned (MINOR version)

**Example:** Discovered a useful pattern worth capturing

```bash
# Create new skill in downstream project
mkdir -p .claude/skills/my-new-pattern
# ... create SKILL.md

git add .claude/skills/my-new-pattern/
git commit -m "feat(skills): add pattern for X"
git checkout -b upstream/add-pattern-skill
git push workflow upstream/add-pattern-skill

# Create PR
gh pr create --repo jackrich78/project-starter \
  --base v2 \
  --head upstream/add-pattern-skill \
  --title "feat(skills): add pattern for handling X"

# After merge, tag MINOR: v2.1.0 → v2.2.0
```

---

## Troubleshooting

### Problem: "Permission denied" when pushing to workflow remote

**Cause:** You don't have write access to template repo

**Solution:**
```bash
# Fork the template repo on GitHub
# Add your fork as a remote
git remote add my-fork git@github.com:YOUR-USERNAME/project-starter.git

# Push to your fork instead
git push my-fork upstream/fix-qa-null

# Create PR from your fork to main template repo
gh pr create --repo jackrich78/project-starter \
  --head YOUR-USERNAME:upstream/fix-qa-null \
  --base v2
```

### Problem: Upstream branch includes project-specific files

**Cause:** Git included more than just workflow files

**Solution:**
```bash
# Start over with clean branch
git checkout main  # or your project's main branch
git branch -D upstream/fix-qa-null
git checkout -b upstream/fix-qa-null

# Cherry-pick only the relevant commit(s)
git cherry-pick <commit-sha> -- .claude/agents/qa-reviewer.md

# Verify only workflow files included
git status
git diff HEAD~1

# Push cleaned branch
git push workflow upstream/fix-qa-null --force
```

### Problem: Merge conflict in PR

**Cause:** Template changed the same file since you branched

**Solution:**
```bash
# In your downstream project
git fetch workflow v2
git rebase workflow/v2

# Resolve conflicts
# ... edit files, resolve conflicts ...
git add .
git rebase --continue

# Force push updated branch
git push workflow upstream/fix-qa-null --force

# PR will update automatically
```

### Problem: Forgot to create upstream branch

**Cause:** Pushed directly to v2 or main

**Solution:**
```bash
# Create branch from the commit
git checkout -b upstream/fix-qa-null <commit-sha>

# Push new branch
git push workflow upstream/fix-qa-null

# Create PR as normal
```

---

## Best Practices

### 1. One Improvement Per PR

**Good:**
```bash
# PR 1: Fix qa-reviewer null handling
# PR 2: Improve tdd-test-writer prompt
```

**Bad:**
```bash
# PR 1: Fix qa-reviewer + improve tdd + update docs
```

**Why:** Easier to review, easier to revert if needed, clearer git history.

### 2. Use Conventional Commit Format

**Format:** `<type>(<scope>): <subject>`

**Types:**
- `fix`: Bug fixes (PATCH version bump)
- `feat`: New features/improvements (MINOR version bump)
- `docs`: Documentation only
- `refactor`: Code restructuring, no behavior change
- `test`: Test additions or fixes
- `chore`: Maintenance (dependencies, tooling)

**Examples:**
```bash
fix(qa): handle null responses in OWASP checklist
feat(tdd): improve test-writer prompt for edge cases
docs(getting-started): clarify stack merge instructions
refactor(agents): extract common prompt patterns
```

### 3. Write Descriptive PR Bodies

**Good PR Body:**
```markdown
## Context
Discovered in flashcard-app production.

## Problem
qa-reviewer crashes when OWASP check returns null.

## Solution
Added null checking before accessing confidence.

## Testing
- Tested with null responses in flashcard-app
- All existing tests pass

## Impact
Prevents crashes in all projects using qa-reviewer.
```

**Bad PR Body:**
```markdown
Fixed a bug
```

### 4. Test Before Upstreaming

- [ ] Verify the change works in your downstream project
- [ ] Check no project-specific code leaked in
- [ ] Ensure it follows template conventions
- [ ] Run tests if applicable (npm test, etc.)

### 5. Reference Issues in PRs

If there's a related issue:
```bash
gh pr create \
  --title "fix(qa): handle null responses" \
  --body "Fixes #45

[rest of PR body]"
```

---

## Versioning Guidelines

Follow [Semantic Versioning](https://semver.org/):

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix | PATCH | v2.1.0 → v2.1.1 |
| New feature | MINOR | v2.1.0 → v2.2.0 |
| Breaking change | MAJOR | v2.1.0 → v3.0.0 |

**Breaking changes** (rare):
- Removing an agent
- Changing command interface
- Renaming core files

Mark breaking changes clearly:
```bash
git commit -m "feat(agents)!: rename qa-reviewer to qa-analyzer

BREAKING CHANGE: qa-reviewer.md renamed to qa-analyzer.md
All projects need to update imports and references."
```

---

## Quick Reference

### Upstream Checklist

```bash
# 1. Verify change is workflow-only
git status
git diff HEAD~1

# 2. Create upstream branch
git checkout -b upstream/<type>-<description>

# 3. Push to template
git push workflow upstream/<branch-name>

# 4. Create PR
gh pr create --repo jackrich78/project-starter \
  --base v2 \
  --head upstream/<branch-name> \
  --title "<type>(<scope>): <description>"

# 5. After merge, tag version
git tag v2.X.Y -m "Description"
git push origin v2.X.Y

# 6. Update CHANGELOG.md

# 7. Sync all projects
cd ~/project-1 && npm run sync-workflow
cd ~/project-2 && npm run sync-workflow
cd ~/project-3 && npm run sync-workflow
```

---

## Related Documentation

- [Workflow Sync Guide](two-remote-sync.md) - Setup and sync workflow
- [Getting Started](getting-started.md) - Initial project setup
- [Contributing Guide](../../CONTRIBUTING.md) - General contribution guidelines

---

**Questions?** Open an issue in the template repo or discuss in your team channel.
