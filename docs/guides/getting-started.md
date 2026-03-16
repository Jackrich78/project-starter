# Getting Started: Using This Template

**Purpose:** Step-by-step guide to create a new project from this starter template.

---

## Quick Start

### Step 1: Copy the Template

```bash
# From your dev directory
mkdir your-project-name
cp -r /path/to/project-starter/. your-project-name/
cd your-project-name
```

### Step 2: Apply a Stack (Optional)

If using a deployment stack (e.g., Cloudflare):

```bash
# Merge stack files to root
cp -r stacks/cloudflare/* .
cp -r stacks/cloudflare/.claude/agents/* .claude/agents/
cp stacks/cloudflare/.gitignore .
cp stacks/cloudflare/.dev.vars.example .

# Clean up (REQUIRED — stacks/ contains duplicate tests and is not needed after merge)
rm -rf stacks/ spikes/
```

### Step 3: Initialize Fresh Git

```bash
rm -rf .git
git init
```

### Step 4: Install Dependencies

```bash
rm -rf node_modules package-lock.json
npm install
```

### Step 5: Verify Setup

```bash
npm test  # All tests should pass
```

### Step 6: Push to GitHub

```bash
# Option A: Create repo with gh CLI (recommended)
gh repo create your-project-name --private --source=. --remote=origin
git add .
git commit -m "chore: initialize project from project-starter"
git push -u origin main

# Option B: Manual (create repo on github.com first)
git add .
git commit -m "chore: initialize project from project-starter"
git remote add origin git@github.com:USERNAME/your-project-name.git
git push -u origin main
```

---

## What You Get

### Core Workflow Commands

> Full descriptions and usage guidance: [commands-reference.md](commands-reference.md)

| Command | Purpose |
|---------|---------|
| `/explore [topic]` | Discover and define a feature → PRD |
| `/blueprint FEAT-XXX` | Create implementation plan with test stubs |
| `/build FEAT-XXX` | TDD implementation with isolated subagents + QA |
| `/qa [target]` | Run security and quality review |
| `/commit` | Git commit with QA gate and CI verification |
| `/handover` | Capture session context for continuation |
| `/retro` | Extract learnings into reusable skills |
| `/prime [mode]` | Load project context (bare, think, build, review, create) |
| `/logs` | Query observability database |
| `/debug [issue]` | Systematic bug investigation and resolution |
| `/create-specialist [lib]` | Create domain-expert sub-agent |
| `/update-docs` | Update documentation index and cross-references |

Skills (modular decision guides that commands import automatically): [skills-reference.md](skills-reference.md)

### TDD Subagent Architecture

Each TDD phase runs in isolated context:

```
/build FEAT-XXX
    ↓
🔴 tdd-test-writer (sees: PRD only) → Test FAILS
    ↓
🟢 tdd-implementer (sees: test only) → Test PASSES
    ↓
🔵 tdd-refactorer (sees: test + impl) → Tests STAY GREEN
    ↓
Handover generated → QA review → /commit
```

### QA Integration

- **Automatic:** QA runs after every `/build`
- **Manual:** Run `/qa` on any file, directory, or feature
- **Blocking:** Security issues block `/commit` until resolved

### Key Directories

```
your-project/
├── .claude/
│   ├── agents/          # Sub-agents (TDD, QA, specialists)
│   ├── commands/        # Slash command definitions
│   ├── skills/          # Learned patterns
│   └── hooks/           # Lifecycle hooks (security, formatting)
├── docs/
│   ├── features/        # Feature documentation (PRD, plan per feature)
│   ├── qa/              # QA review reports
│   ├── system/          # Architecture documentation
│   └── templates/       # Document templates
├── src/                 # Your application code
├── test/                # Your tests
├── CLAUDE.md            # AI startup context (edit this!)
└── PROJECT.md           # Project roadmap and state
```

---

## First Steps After Setup

## Recommended: Run `/setup`

The fastest way to configure your project is the interactive `/setup` command:

```bash
# In Claude Code
/setup
```

This will:
1. Read any existing docs you've prepared and extract project context
2. Interview you about gaps (project name, tech stack, goals, etc.)
3. Generate tailored CLAUDE.md, PROJECT.md, README.md, and architecture docs
4. Create a feature roadmap with the Tech-Product Lead agent
5. Optionally run Librarian + Challenger review
6. Set up GitHub repo (if `gh` CLI is available)

If you have existing planning docs, pass them as arguments:
```bash
/setup path/to/my-notes.md path/to/research/
```

After `/setup` completes, run `/prime` to verify context loads correctly, then `/explore FEAT-001` to start your first feature.

---

## Manual Alternative

If you prefer to configure manually (or `/setup` isn't available):

### 1. Update PROJECT.md

Replace the template content with your project's:
- Vision and goals
- Current status
- Roadmap

### 2. Update CLAUDE.md

Customize the quick start section:
- Your test command
- Your dev command
- Project-specific context rules

See [Working With Claude](working-with-claude.md) for guidance on what to include and how to keep it lean.

### 3. Configure Stack (if applicable)

For Cloudflare stack:
- Update `wrangler.toml` with your project name
- Create `.dev.vars` from `.dev.vars.example`
- Set up D1 database: `npx wrangler d1 create your-db-name`

### 4. Start Your First Feature

```bash
# In Claude Code
/explore [describe your first feature]
```

This will:
1. Research the feature space
2. Create a PRD in `docs/features/FEAT-001_your-feature/`
3. Guide you through planning and implementation

---

## Available Stacks

| Stack | What It Includes |
|-------|------------------|
| **cloudflare** | Workers, D1 (SQLite), R2 (storage), KV, Queues, Vitest tests |

See `stacks/README.md` for detailed stack documentation.

---

## Development Workflow

### Typical Feature Flow

```
1. /explore [idea]        → Creates PRD
2. /blueprint FEAT-XXX    → Creates plan + test stubs
3. /build FEAT-XXX        → TDD implementation + QA
4. /commit                → Commit with QA gate + CI
```

### QA Status Guide

| Status | Meaning | Action |
|--------|---------|--------|
| `APPROVED` | All checks passed | Ready for `/commit` |
| `NEEDS_FIXES` | Issues found | Fix and re-run `/qa` |
| `BLOCKED` | Security issue | Human decision required |

---

## Troubleshooting

### Tests fail after setup

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm test
```

### Duplicate test files

Make sure you ran:
```bash
rm -rf stacks/ spikes/
```

### gh CLI not found

```bash
brew install gh
gh auth login
```

### QA blocking commit unexpectedly

Check for pending QA report:
```bash
ls docs/qa/
```

Review and resolve issues, or override with explicit confirmation.

---

## Optional: SAST with Semgrep

The QA reviewer can run Semgrep static analysis before LLM review for deterministic security scanning. This is completely optional — without Semgrep, QA review works LLM-only.

### Install Semgrep

```bash
# macOS
brew install semgrep

# pip (any platform)
pip install semgrep
```

### Verify Configuration

```bash
# Check rules are valid
semgrep --validate --config .semgrep/rules/

# Test scan (should exit 0 or 1, not 2+)
semgrep scan --config .semgrep/rules/ --json --metrics=off .
```

### What You Get

- 15 security rules across 7 rule files (JS/TS + Python + secrets detection)
- Offline scanning (no network, no registry)
- Findings automatically merged into QA reports with `[SAST]` attribution
- Graceful degradation: remove `.semgrep.yml` to disable, or just don't install Semgrep

### Customizing Rules

Add custom rules to `.semgrep/rules/` and reference them in `.semgrep.yml`. See the [Semgrep rule syntax docs](https://semgrep.dev/docs/writing-rules/rule-syntax) for patterns.

---

## Adding to an Existing Project

If you have an existing project and want to adopt this workflow without cloning the full template:

### 1. Copy the workflow files

```bash
# From the template directory into your project root
cp -r /path/to/project-starter/.claude your-project/
cp /path/to/project-starter/CLAUDE.md your-project/
```

### 2. Copy the documentation structure

```bash
mkdir -p your-project/docs/{features,qa,system,templates}
cp /path/to/project-starter/docs/templates/* your-project/docs/templates/
cp /path/to/project-starter/docs/system/architecture.md your-project/docs/system/
# Copy other system docs as reference; update them to reflect your actual architecture
```

### 3. Integrate CLAUDE.md

If you already have a `CLAUDE.md`, merge the relevant sections — particularly the command bindings (Quick Start block) and Context Rules. If you don't have one, use the template version and update the project name and dev commands.

### 4. Update system docs to match your project

Replace the placeholder content in `docs/system/architecture.md` and `docs/system/integrations.md` with your actual system design, tech stack, and external services. Agents use these to understand your codebase — generic content produces generic results.

### 5. Baseline your existing features (optional)

Ask Claude Code to scan your codebase and create stub documentation for your major existing features:

```
Please scan the codebase and create basic PRD stubs in docs/features/ for the main existing features. Mark each as "Status: Implemented (baseline)".
```

This gives agents the feature context they need to avoid re-implementing what already exists.

### 6. Install dependencies and verify

```bash
cd your-project
npm install
npm test  # Template scaffold tests should pass
```

---

## See Also

- [Working With Claude](working-with-claude.md) - Configure project context and steer Claude in sessions
- [Architecture](../system/architecture.md) - System design and patterns
- [Connections](../system/connections.md) - File relationship map
- [Stacks README](../../stacks/README.md) - Stack details and contribution guide
