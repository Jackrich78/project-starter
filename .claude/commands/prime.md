---
updated: 2026-02-26
description: Load project context at session start. Modes shape what gets loaded and how to think.
argument-hint: <think|build|review|create> [FEAT-XXX]
---

# /prime — Context Loader

Arguments received: `$ARGUMENTS`

Parse `$ARGUMENTS`:
- If empty → **bare** mode
- If first token is `think`, `build`, `review`, or `create` → that mode; remaining tokens are FEAT-ID
- If only a FEAT-ID with no mode → ask user which mode they want

---

## Step 1: Git State (All Modes)

Run and capture:
```bash
git branch --show-current && git status --short && git log --oneline -3
```

---

## Step 2: Load Files by Mode

Mode determines **mindset + which modules to load**. FEAT-ID determines **scope**.

### bare (no args)
- Glob `docs/features/FEAT-*` → list directory names only
- Output: branch, status, feature count. Stop.

### think [FEAT-ID]
- Read `docs/system/architecture.md`
- Read `PROJECT.md`
- If no FEAT-ID: Glob `docs/features/FEAT-*` → list directory names
- Framing: **"Explore widely, question assumptions, consider alternatives"**

### build [FEAT-ID]
- Read `docs/system/architecture.md`
- Read `docs/system/architecture-tdd.md` (warn and continue if missing)
- Read `docs/system/architecture-qa.md` (warn and continue if missing)
- Framing: **"Make it work. Focus on passing tests, minimal implementation"**

### review [FEAT-ID]
- Read `docs/system/architecture.md`
- Read `docs/system/architecture-qa.md` (warn and continue if missing)
- Framing: **"Find what's wrong. Be suspicious, check edge cases"**

### create [FEAT-ID]
- Read `docs/system/architecture.md`
- Read `PROJECT.md`
- Framing: **"Communicate effectively. Think about audience, narrative, clarity"**

If FEAT-ID present in any mode → load feature files (see Step 3).

---

## Step 3: Feature File Loading (When FEAT-ID Present)

1. Glob `docs/features/FEAT-{ID}*/*` to find the feature folder.
   If no match: warn "Feature FEAT-{ID} not found" and continue.
2. Extract folder path from first result.
3. Read if they exist (warn and skip if missing):
   - `{folder}/README.md` — full file
   - `{folder}/prd.md` — first 40 lines
   - `{folder}/plan.md` — first 40 lines
4. If `{folder}/handover.md` exists: read it automatically.

---

## Step 4: Output Summary (3-5 lines max)

```
Context: [branch] | [N changed files or "clean"]
Mode: [mode] — [framing statement]
[If feature:] FEAT-{ID}: [title] ([status])
[If handover:] Handover loaded ([age])
```

Files are loaded into context. Do not dump file contents to the user.
