---
updated: 2026-01-24T12:00:00Z
description: Capture session context for seamless handover to next session
argument-hint: [FEAT-ID]
---

# Session Handover

Capture the current session's progress, learnings, and context for seamless continuation in the next session.

## Your Mission

Generate a concise `handover.md` document that gives the next session everything it needs to continue exactly where this session left off.

## Usage

```bash
# With explicit feature ID
/handover FEAT-XXX

# Without argument (will detect from context or ask)
/handover
```

## Workflow Steps

### Step 1: Determine Feature ID

**If FEAT-ID provided:** Use `$ARGUMENTS`

**If no argument:**
1. Check recent file changes for `docs/features/FEAT-XXX/` paths
2. Check conversation context for feature references
3. If still unclear, ask user:
   ```
   Use AskUserQuestion:
   "Which feature is this session for?"
   - List detected FEAT-XXX options from docs/features/
   ```

### Step 2: Validate Feature Folder Exists

```bash
ls docs/features/FEAT-XXX/
```

If folder doesn't exist:
```
⚠️ Feature folder docs/features/FEAT-XXX/ not found.

Create it first with /explore, or specify a different FEAT-ID.
```

### Step 3: Read Existing Handover (If Present)

```bash
cat docs/features/FEAT-XXX/handover.md
```

If exists:
1. **Extract the "Generated" timestamp** from the first line (e.g., `*Generated: 2026-01-26 14:30*`) you MUST state the date hour and minutes.
2. **Preserve this timestamp** in the new handover
3. **Add "Updated" timestamp** with current time
4. **Evaluate each section** for relevance:

| Keep | Remove |
|------|--------|
| Unresolved blockers | Resolved blockers |
| Decisions still applicable | Decisions superseded |
| Learnings relevant to remaining work | Learnings about completed work |
| In-progress items | Completed items |
| Files still being worked on | Files no longer relevant |

Mark preserved items with "(from previous session)" in the new handover.

### Step 4: Analyze Current Session

Review the conversation to extract:

1. **What was accomplished** - Tasks completed, files created/modified
2. **What failed and why** - Approaches that didn't work
3. **Decisions made** - Technical choices and rationale
4. **Open questions** - Unresolved issues, uncertainties
5. **Files touched** - Key file paths with line numbers where relevant

### Step 5: Capture Git State

Run these commands:
```bash
git branch --show-current
git status --short
git log --oneline -1
```

### Step 6: Generate Handover Document

Create `docs/features/FEAT-XXX/handover.md` following this exact template:

**If creating new handover:**
```markdown
# Session Handover - FEAT-XXX
*Generated: YYYY-MM-DD HH:MM*

## Current State
[1-2 sentences: Where did we leave off? What's the immediate context?]
```

**If updating existing handover (preserve Generated timestamp):**
```markdown
# Session Handover - FEAT-XXX
*Generated: YYYY-MM-DD HH:MM*
*Updated: YYYY-MM-DD HH:MM*

## Current State
[1-2 sentences: Where did we leave off? What's the immediate context?]

## Progress This Session
- [x] Completed item
- [x] Another completed item
- [ ] In-progress item (partial)

## Key Decisions
- Chose X over Y because Z
- Decided to use [approach] for [reason]

## What Didn't Work
- Attempted X, failed because Y
- Tried [approach], blocked by [reason]

## Blockers/Uncertainties
- Need clarification on: [specific question]
- Blocked by: [specific blocker]
- Uncertain about: [specific uncertainty]

## Next Steps
1. [First priority - be specific]
2. [Second priority]
3. [Third priority if applicable]

## Relevant Files
- `path/to/file.ts:123` - Brief description of relevance
- `docs/features/FEAT-XXX/architecture.md` - Design decisions
- `path/to/another/file.py` - What this file does

## Git State
- **Branch:** `branch-name`
- **Status:** [clean | X files modified, Y untracked]
- **Last Commit:** `abc1234` - Commit message summary
```

### Step 7: Check Token Budget

**Target:** 800-1200 tokens
**Hard limit:** 1500 tokens

If over limit, prioritize in this order:
1. Next Steps (must keep)
2. Blockers/Uncertainties (must keep)
3. What Didn't Work (keep if space)
4. Key Decisions (summarize if needed)
5. Progress This Session (summarize if needed)

### Step 8: Identify Permanent Learnings

Review "What Didn't Work" and "Key Decisions" for learnings that:
- Apply beyond this feature
- Would help future development
- Are gotchas others should know

If valuable learnings found, suggest running `/retro` to extract them as skills:
```
"These learnings seem valuable beyond this feature.
Consider running /retro to extract them as reusable skills."
```

### Step 9: Write Handover File

Write the generated content to `docs/features/FEAT-XXX/handover.md`.

If file existed, this overwrites it (preserved items already merged in Step 3).

### Step 10: Confirm Completion

```
✅ Handover saved to docs/features/FEAT-XXX/handover.md

To continue in next session:
  1. Start new Claude Code session
  2. Run: Read docs/features/FEAT-XXX/handover.md
  3. Continue with the documented next steps

Token count: ~XXX tokens
```

## Merge Strategy (Critical)

When a previous `handover.md` exists:

1. **Read it first** before generating new content
2. **Evaluate relevance** of each item against current session progress
3. **Preserve** items still relevant, marking them "(from previous session)"
4. **Discard** items that are:
   - Completed (move to Progress section as done)
   - Superseded by new decisions
   - No longer applicable
5. **Merge** with new session learnings
6. **Result** is a fresh, clean file (not append-only)

### Example Merge

**Previous handover had:**
```markdown
## Blockers/Uncertainties
- Need to decide: REST vs GraphQL
- Auth token refresh logic unclear
```

**This session resolved REST vs GraphQL, but not auth tokens.**

**New handover shows:**
```markdown
## Blockers/Uncertainties
- Auth token refresh logic unclear (from previous session)

## Key Decisions
- Chose REST over GraphQL because simpler client integration
```

## Important Notes

- **Feature folder required** - Cannot run without existing `docs/features/FEAT-XXX/`
- **Overwrites existing** - Previous handover is replaced (with relevant items preserved)
- **Concise is critical** - Next session loads this first, keep it scannable
- **Be specific** - "Fix the bug" is useless; "Fix auth token expiry in `src/auth.ts:45`" is actionable
- **Git state matters** - Next session needs to know branch and uncommitted work

## Token Budget Guidelines

| Section | Target Tokens |
|---------|---------------|
| Current State | 50-100 |
| Progress This Session | 100-200 |
| Key Decisions | 100-200 |
| What Didn't Work | 100-150 |
| Blockers/Uncertainties | 50-100 |
| Next Steps | 100-150 |
| Relevant Files | 50-100 |
| Git State | 30-50 |
| **Total** | **800-1200** |

## Example Output

```markdown
# Session Handover - FEAT-XXX
*Generated: 2025-01-15 14:30*

## Current State
Implementing OAuth2 login flow. Frontend form complete, backend token exchange WIP.

## Progress This Session
- [x] Created login form component (`src/components/LoginForm.tsx`)
- [x] Set up OAuth2 provider configuration
- [x] Added auth routes to Express server
- [ ] Token exchange endpoint (50% complete)

## Key Decisions
- Chose PKCE flow over implicit for better security
- Using httpOnly cookies for token storage (not localStorage)

## What Didn't Work
- Attempted passport.js, too much boilerplate for our needs
- Tried storing tokens in Redux, SSR hydration issues

## Blockers/Uncertainties
- Refresh token rotation strategy unclear - need to research best practices
- Should we support multiple OAuth providers? (from previous session)

## Next Steps
1. Complete token exchange endpoint in `src/server/auth.ts:89`
2. Add refresh token rotation logic
3. Write integration tests for auth flow

## Relevant Files
- `src/components/LoginForm.tsx` - Frontend login UI
- `src/server/auth.ts:45-120` - OAuth routes (WIP)
- `docs/features/FEAT-XXX/architecture.md` - Auth design decisions

## Git State
- **Branch:** `feat/FEAT-XXX-oauth`
- **Status:** 4 files modified
- **Last Commit:** `a1b2c3d` - Add OAuth provider config
```

## See Also

- `.claude/skills/` - Reusable learnings from /retro
- `docs/features/FEAT-XXX/prd.md` - Feature requirements
- `docs/features/FEAT-XXX/plan.md` - Technical decisions
