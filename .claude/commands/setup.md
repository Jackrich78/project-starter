---
updated: 2026-03-15T00:00:00Z
description: One-time project setup that adapts the template to your project
argument-hint: [optional: path to existing project docs]
---

# /setup — Project Initialization

You are setting up a new project from the project-starter template.

Arguments received: `$ARGUMENTS`

## Mission

Transform a blank project-starter template into a fully configured project with tailored documentation, a feature roadmap, and optional GitHub setup. Replace the manual kickoff process with a guided, repeatable flow.

## Philosophy

**Infer first, ask gaps.** Read everything the user has already prepared before asking a single question. Respect their existing thinking. The interview fills gaps — it doesn't re-interrogate what's already documented.

---

## Pre-flight Checks

Before starting setup, run these checks in order:

### 1. Already-Configured Detection

Read `CLAUDE.md`. Check if it still contains the default template content:

- If the title line is **NOT** "# Project Starter" (the template default), this project appears already configured.
- Warn: "This project appears to already be configured. `/setup` is designed for first-time initialization."
- Suggest: "`/retro` for iterative doc updates, or `/explore` for new features."
- **STOP. Do not proceed.**

### 2. Template Integrity

Verify these exist:
- `.claude/commands/` directory
- `docs/system/architecture.md`
- `docs/templates/` directory

If any are missing: Warn "Template structure appears incomplete. Was this copied from the project-starter template?" Ask user whether to continue or abort.

### 3. Parse Arguments

- If `$ARGUMENTS` provided: treat as path(s) to additional context files to ingest in Phase 1
- If empty: proceed with standard discovery (project directory only)

---

## Phase 1: Context Gathering

This is the core of `/setup`. The interview uses a **4-tier dynamic architecture** that adapts to the project type. The goal: gather enough context to generate meaningful project documentation.

---

### Step 1.1: Ingest Existing Context

Read files to understand what the user has already prepared.

**Automatic scan** (read if they exist):
- Project root: any `.md` files (README.md, BRIEF.md, NOTES.md, etc.)
- `docs/features/` — any files the user has pre-placed
- If `$ARGUMENTS` provided: read those paths too

**Exclude** (template scaffolding, not project context):
- `.claude/` directory
- `node_modules/`
- `stacks/`
- `docs/templates/`
- `docs/system/`
- `docs/guides/`

**Build a context checklist** as you read:

| # | Area | Status | Source |
|---|------|--------|--------|
| 1 | Project name | found / unknown | [file or "needs Q&A"] |
| 2 | One-line description | found / unknown | |
| 3 | Project type | found / unknown | (code / content / workflow / research / hybrid) |
| 4 | Problem being solved | found / unknown | |
| 5 | Target users / audience | found / unknown | |
| 6 | Goals / success criteria | found / unknown | |
| 7 | Tech stack | found / unknown | |
| 8 | Architecture decisions | found / unknown | |
| 9 | Known integrations | found / unknown | |
| 10 | Deployment target | found / unknown | |
| 11 | Known consumers | found / unknown | |
| 12 | First feature idea | found / unknown | |
| 13 | Security / compliance needs | found / unknown | |
| 14 | Timeline / constraints | found / unknown | |

Present what you found:

"I've read [N] files and extracted the following. Let me confirm this is correct before asking about gaps."

Show the user the filled-in checklist items. Use AskUserQuestion to confirm or correct what was inferred.

---

### Step 1.2: Tier 1 — Core Identity (Always Ask)

For items still marked "unknown" after file ingestion, ask conversationally:

**Identity:**
- "What is this project called?"
- "In one sentence, what does it do?"

**Purpose:**
- "What problem does this solve, and for whom?"
- "What does success look like? How will you know this project is working?"

**Starting point:**
- "What are the first 2-3 things you need to build or create?"
  (This seeds the feature roadmap. Deliberately open-ended.)

**Defer pattern:** If the user says "I don't know" or "not sure yet":
- Note it: "Okay, I'll mark [topic] as deferred — we can figure it out later."
- Add to deferred list (written to `backlog.md` in Phase 3)
- Move on. Don't pressure.

Skip questions for items already confirmed in Step 1.1.

---

### Step 1.3: Tier 2 — Project-Type-Specific Questions

Based on what was learned in Tier 1, dynamically select the relevant question set. A project can be hybrid (e.g., coding + content) — ask from multiple sets if applicable.

**If project involves SOFTWARE / CODING:**
- "What's the tech stack?" (language, framework, database, hosting)
- "Where will this be deployed?" (local, cloud, which provider)
- "Any APIs or services this needs to talk to?"
- "Any security or compliance considerations?" (auth, data sensitivity, regulations)
- "Who will use this?" (end users, internal team, API consumers, other services)
- "Is this a new build or extending something existing?"

**If project involves CONTENT CREATION:**
- "What types of content?" (blog posts, video scripts, social media, documentation, presentations)
- "What channels or platforms?" (LinkedIn, YouTube, blog, newsletter, internal docs)
- "Is there a brand voice or style guide to follow?"
- "What's the cadence?" (daily, weekly, campaign-based, ad-hoc)
- "Who's the audience?"

**If project involves WORKFLOWS / AUTOMATION:**
- "What triggers the workflow?" (event, schedule, manual, API call)
- "What systems need to talk to each other?"
- "What's manual today that should be automated?"
- "What volume and frequency?" (10 items/day vs 10,000)
- "What happens when something fails?" (retry, alert, fallback)

**If project involves RESEARCH / ANALYSIS:**
- "What data sources?"
- "What's the output format?" (reports, dashboards, datasets, papers)
- "One-time analysis or ongoing?"
- "Who consumes the output?"
- "What decisions will this research inform?"

**If project type is UNCLEAR or HYBRID:**
- Ask: "This sounds like it involves [X] and [Y] — is that right?"
- Then ask from both relevant sets

Skip questions already answered by ingestion or Tier 1.

---

### Step 1.4: Tier 3 — Deepening

Based on Tier 2 answers, drill deeper where it matters. These are not a fixed list — follow the thread:

- **If multiple components mentioned:** "How do these pieces fit together? Any architecture decisions already made?"
- **If constraints surfaced:** "Tell me more about [constraint]. How firm is it?"
- **If existing work mentioned:** "What can we build on? What should we keep vs replace?"
- **If uncertainty expressed:** "What are you least sure about? We'll mark those as open questions."
- **If timeline mentioned:** "When do you need the first usable version?"
- **If users/audience defined:** "What's the most important thing they need from this?"

This phase is conversational. Follow the thread. Stop when you have enough context to generate meaningful project documentation. You don't need every answer — you need enough to write a useful CLAUDE.md and PROJECT.md.

---

### Step 1.5: Tier 4 — Wrap Up Discovery

Before moving to doc generation:

1. Review the checklist. For each "unknown" item:
   - If it's critical (project name, description, goal): ask one more time
   - If it's deferrable (deployment target, security, integrations): mark as deferred

2. Present summary: "Here's what I know about your project: [summary]. Anything I'm missing or got wrong?"

3. Get explicit go-ahead using AskUserQuestion:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCOVERY COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checklist: [X/14] areas covered
Deferred: [N] items (will go to backlog)
Project type: [detected type(s)]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Options:
- "Generate project documentation"
- "I want to add more context first" → continue conversation, then re-present gate

---

## Phase 2: Generate Project Documentation

Generate these files using the context gathered in Phase 1. Use the existing file contents as a base — preserve the template's workflow sections and replace only the project-specific parts.

---

### 2.1: CLAUDE.md

Read the current `CLAUDE.md` first. Then rewrite:

**Replace/customize:**
- Title and description line → project name and one-line description
- Quick Start → project-specific commands based on tech stack:
  - Python: `pytest` / `docker compose up` or similar
  - Node: `npm test` / `npm run dev`
  - Go: `go test ./...` / `go run .`
  - Content/research projects: remove dev commands, note "See `/explore` to start"
  - If stack unknown: keep template defaults with `<!-- DEFERRED: Quick Start commands -->`

**Preserve as-is (these are template workflow sections):**
- Agents section (and command bindings)
- Commands section (but add `/setup` to the list)
- Key Files section (update paths if project-specific files added)
- Principles (Reduce / Offload / Isolate)
- Development Standards
- Context Rules

**Add if relevant:**
- Project-specific principles section (e.g., "Service Principles" for an API service, "Content Guidelines" for content projects)
- Project-specific context rules (if unique patterns emerged from interview)

---

### 2.2: PROJECT.md

Read the current `PROJECT.md`. Rewrite fully:

- **Frontmatter:** version `0.1.0`, status `Active`, updated timestamp
- **Vision:** from interview (goal/purpose — 1-3 sentences)
- **Current State:** "v0 — Initial setup. First feature: [FEAT-001 name or TBD]"
- **Active Features:** placeholder for FEAT-001 (populated in Phase 3)
- **Roadmap:** placeholder (populated in Phase 3 by Tech-Product Lead)
- **Architecture Overview:** based on tech stack and architecture answers
  - If software: component diagram (ASCII art)
  - If content: workflow diagram (topic → draft → review → publish)
  - If workflow: trigger → process → output diagram
  - If unknown: generic placeholder with `<!-- DEFERRED: Architecture diagram -->`
- **Key Decisions:** table from interview answers (Decision | Choice | Rationale)
- **Assumptions:** numbered list of things assumed true (to validate during FEAT-001)
- **Deferred Questions:** reference `docs/features/backlog.md`

Remove all `<!-- CUSTOMIZE -->` placeholders. Replace with actual content or explicit `<!-- DEFERRED: [topic] -->` markers.

---

### 2.3: README.md

Read the current `README.md`. Rewrite:

- **Title:** project name
- **What This Is:** 2-3 sentence description
- **Quick Start:** how to run (based on tech stack, with stubs for TBD items)
- **Project Structure:** key directories and their purpose
- **Development Workflow:** condensed commands/agents reference (link to getting-started.md for details)
- **Documentation:** links to system docs and features

Mark unvalidated sections clearly: "API contract to be validated during FEAT-001" etc.

---

### 2.4: Architecture Topic Module (Conditional)

Create `docs/system/architecture-[project-slug].md` **only** if the project has enough technical context to warrant it (clear tech stack, architecture decisions, integration points).

For simple projects, early-stage greenfield, or content/research projects: **skip this file**, note as deferred in PROJECT.md.

If created:
- Frontmatter with `updated` timestamp
- System overview with diagram
- Key architectural patterns
- Integration points
- Deployment architecture (if known)

---

### 2.5: Update docs/system/architecture.md

Read the existing file. If a topic module was created in 2.4, add it to the "Topic Modules" section (around line 299-304), following the existing pattern:

```markdown
- [architecture-[project].md](architecture-[project].md) — [description] (loaded by `/prime think`, `build`)
```

---

### 2.6: FEAT-000_project-setup

Create `docs/features/FEAT-000_project-setup/README.md`:

```markdown
---
created: [timestamp]
updated: [timestamp]
status: complete
---

# FEAT-000: Project Setup

## Summary

Project initialized from project-starter template using `/setup`.

## Context Documents

[List any files the user provided or that were ingested]

## Setup Decisions

[Key decisions made during setup interview]

## Deferred Questions

[Items marked as deferred — see also docs/features/backlog.md]
```

---

### Doc Generation Approval Gate

Present the list of files created and modified:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOCUMENTATION GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files created/modified:
  CLAUDE.md — [customized / partial]
  PROJECT.md — [vision, architecture, decisions]
  README.md — [customized]
  architecture-[project].md — [created / skipped]
  docs/features/FEAT-000_project-setup/README.md

Deferred items: [N] (marked with <!-- DEFERRED -->)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use AskUserQuestion:
- "Looks good — proceed to feature roadmap"
- "I want to review/adjust the generated files first" → user reviews, you fix, re-present gate

**Do not proceed to Phase 3 until user approves.**

---

## Phase 3: Feature Roadmap

Invoke the Tech-Product Lead agent to break the project vision into features.

```
Task(
  subagent_type="Product-Engineering Lead",
  description="Create feature roadmap for [project name]",
  prompt="You are setting up a new project. Create an initial feature breakdown and roadmap.

  **Project context:**
  - Read: CLAUDE.md (just generated — project identity and tech stack)
  - Read: PROJECT.md (just generated — vision and architecture)

  **Your task:**
  1. Break the project vision into discrete features (FEAT-001, FEAT-002, etc.)
  2. Phase them: Phase 0 (validate/setup), Phase 1 (core/MVP), Phase 2 (harden/extend)
  3. For each feature: one-line description, effort estimate, dependencies
  4. Identify the critical path
  5. Separate: core features (get directories) vs backlog items (go in backlog.md)

  **Output:**
  1. Update PROJECT.md roadmap section with the phased feature list
  2. Create docs/features/FEAT-001_[slug]/README.md through FEAT-00N for Phase 0-1 features
     - Each README.md: status Planned, one-line goal, effort estimate, dependencies
     - Follow docs/templates/readme-template.md structure
  3. Create or update docs/features/backlog.md with:
     - Phase 2+ features under a 'Backlog' heading
     - Any deferred questions from setup under a 'Deferred Questions' heading
       [Include the deferred items list from Phase 1 here]

  **Constraints:**
  - Maximum 10 features total (keep it focused)
  - Phase 0 should be 1-2 features max (validation/smoke test)
  - Effort estimates are rough: S (< 2h), M (2-8h), L (8-24h), XL (> 24h)
  - The first feature (FEAT-001) should be the smallest thing that proves the approach works

  @.claude/agents/tech-product-lead.md"
)
```

**After Tech-Product Lead completes:**
- Read the updated PROJECT.md to verify roadmap was added
- Read the feature stubs to verify structure
- Confirm backlog.md includes deferred questions from Phase 1
- Present quick summary to user: "[N] features planned across [M] phases. FEAT-001: [name]."

---

## Phase 4: Independent Review (Opt-In)

Ask the user before running reviews:

"Shall I run Librarian + Challenger review on the generated docs? This catches consistency issues and questionable assumptions, but uses context window. You can also run `/qa` later instead."

Use AskUserQuestion:
- "Run reviews now"
- "Skip to git setup"

**If user skips:** Jump to Phase 5. Note in summary that review was skipped.

**If user proceeds:** Invoke Librarian and Challenger in parallel. They review independently — no cross-influence.

---

### 4a: Librarian Review

```
Task(
  subagent_type="Librarian",
  description="Review setup docs for [project name]",
  prompt="A new project was just set up using /setup. Review ALL generated documentation for consistency and convention compliance.

  **Files to review:**
  - CLAUDE.md
  - PROJECT.md
  - README.md
  - docs/system/architecture.md (check topic module link if one was created)
  - docs/features/FEAT-000_project-setup/README.md
  - docs/features/FEAT-001_*/README.md (and any other feature stubs)
  - docs/features/backlog.md

  **Check for:**
  1. All cross-references resolve (no broken links)
  2. Frontmatter present and valid (updated timestamps)
  3. Feature stubs follow docs/templates/readme-template.md
  4. No remaining <!-- CUSTOMIZE --> placeholders (unless marked <!-- DEFERRED -->)
  5. CLAUDE.md commands list includes /setup
  6. Naming conventions (FEAT-XXX_slug format)
  7. PROJECT.md roadmap references match actual feature directories

  **Output:** List issues found, with severity (error/warning/info) and suggested fixes.
  Auto-fix tier-1 issues (formatting, missing timestamps, broken cross-refs).
  Flag tier-2 issues (content gaps, structural concerns) for user review.

  @.claude/agents/librarian.md"
)
```

---

### 4b: Challenger Review

```
Task(
  subagent_type="challenger",
  description="Challenge setup docs for [project name]",
  prompt="A new project was just set up using /setup. Review the project framing critically.

  **Read:**
  - CLAUDE.md
  - PROJECT.md
  - docs/features/backlog.md

  **Challenge:**
  1. Is the project scope clear and realistic?
  2. Are the assumptions valid or overly optimistic?
  3. Is the feature roadmap ordered correctly? Dependencies respected?
  4. Are there obvious missing considerations (security, deployment, data)?
  5. Is the first feature (FEAT-001) actually the right starting point?
  6. Any red flags in the architecture or approach?

  Max 3 issues. Be constructive.

  @.claude/agents/challenger.md"
)
```

---

### Handling Review Results

After both agents complete:

1. **Tier-1 issues (Librarian auto-fixes):** Accept and move on
2. **Tier-2 issues (from either agent):** Present to user:
   - "The Librarian found: [issues]"
   - "The Challenger raises: [concerns]"
   - "How would you like to handle these?"
3. Apply user's decisions
4. If no issues: "Both reviewers passed. Ready for git setup."

---

## Phase 5: Git & GitHub Setup

### 5.1: Detect Git State

Run:
```bash
git remote -v
git log --oneline -1 2>/dev/null
ls -d .git 2>/dev/null
```

Determine:
- Is `.git` present?
- Does `origin` point to the template repo (contains "project-starter" or similar)?
- Has a first commit been made?

---

### 5.2: Git Remote Setup

**If origin points to template repo:**
- Ask: "Your git origin currently points to the template repo. I'd recommend renaming it to `upstream` so you can still pull template updates via `/sync`, and creating a new `origin` for your project. Shall I do that?"
- If yes: `git remote rename origin upstream`

**If no `.git` directory:**
- Ask: "No git repository found. Shall I initialize one?"
- If yes: `git init`

---

### 5.3: GitHub Repo Creation

Run: `which gh` to check for GitHub CLI.

**If `gh` is installed:**
- Ask: "Shall I create a GitHub repo? It'll be private by default."
- If yes:
  ```bash
  gh repo create [project-name] --private --source=. --remote=origin
  git add -A
  git commit -m "chore: initialize [project-name] from project-starter template"
  git push -u origin main
  ```
- If user wants public: use `--public` flag instead

**If `gh` is NOT installed:**
- Output manual instructions:
  ```
  To push this project to GitHub:
  1. Create a new private repo at github.com/new named [project-name]
  2. Run:
     git remote add origin https://github.com/YOUR-USERNAME/[project-name].git
     git add -A
     git commit -m "chore: initialize [project-name] from project-starter template"
     git push -u origin main
  3. For easier workflow next time: brew install gh && gh auth login
  ```

**Skip option:** User can skip this entire phase. Note in summary.

---

## Phase 6: Summary

Present a clear summary of what was done:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT SETUP COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: [name] — [one-line description]
Type: [code / content / workflow / research / hybrid]

Files created/modified:
  CLAUDE.md — [customized]
  PROJECT.md — [vision, roadmap with N features]
  README.md — [customized]
  architecture-[project].md — [created / skipped]
  FEAT-000_project-setup/README.md
  FEAT-001_[name]/README.md
  [... other feature stubs]
  backlog.md — [N deferred items, M backlog features]

Review: [Librarian: N issues (M fixed) | Challenger: N concerns (resolved) | Skipped]
Git: [origin renamed to upstream | repo created at URL | skipped]

Deferred questions: [N items in backlog.md]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next steps:
  1. Run /prime to verify your project context loads correctly
  2. Run /explore FEAT-001 to flesh out your first feature
  3. Review docs/features/backlog.md for deferred items
```

---

## Success Criteria

Before completing setup, verify:

- CLAUDE.md has project-specific content (not template defaults)
- PROJECT.md has vision, architecture overview, and feature roadmap
- README.md describes this project (not the template)
- No remaining `<!-- CUSTOMIZE -->` placeholders (except explicit `<!-- DEFERRED -->`)
- Feature stubs exist for Phase 0-1 features
- `backlog.md` contains deferred items and Phase 2+ features
- `FEAT-000_project-setup/` exists with setup context
- Librarian review passed or was explicitly skipped
- Challenger review passed or was explicitly skipped
- User signed off on generated docs before feature breakdown
