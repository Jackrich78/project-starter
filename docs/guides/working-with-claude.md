# Working With Claude

**Purpose:** How to configure your project context and steer Claude's behaviour during sessions.

---

## Configuring Your Project Context

Claude Code loads two key files at startup. Getting these right is the highest-leverage thing you can do for output quality.

### CLAUDE.md — the startup brain

CLAUDE.md is loaded automatically at the start of **every session** — even when it's not relevant. This makes it powerful and expensive at the same time.

**What to put here:**
- Your actual test command (`npm test`, `pytest`, `cargo test`)
- Your dev server command (`npm run dev`, etc.)
- Tech stack in one line (e.g., "TypeScript, Cloudflare Workers, D1")
- Project-specific rules Claude must always follow (e.g., "never commit .env", "use Vitest not Jest")
- Command bindings if you've customised them

**What NOT to put here:**
- Full architecture documentation (load on-demand via `/prime`)
- Long feature descriptions
- Anything that only matters in specific contexts

**Target:** Under 50 lines. Every line costs tokens on every session.

**Example — before (template placeholder):**
```
# Project Starter
Lean agent harness template for AI-assisted development.

## Quick Start
npm test
npm run dev
```

**Example — after (configured for your project):**
```
# Acme API
Node.js REST API — Express, Postgres, Vitest.

## Quick Start
npm test          # Vitest unit + integration
npm run dev       # Express on :3000, hot reload

## Rules
- Never use raw SQL — always use the query builder in src/db/
- All routes need request validation via src/middleware/validate.ts
- Tests live in test/ mirroring src/ structure
```

**How to configure:** In your first Claude Code session, type:
```
Help me update CLAUDE.md and PROJECT.md for my project. I'm building [your description].
```

Claude will ask clarifying questions and produce a tailored CLAUDE.md. This one conversation shapes every session that follows.

---

### PROJECT.md — the project memory

PROJECT.md is loaded on-demand by `/prime`. It's the right place for information that matters when planning and building, but doesn't need to load constantly.

**What to put here:**
- Vision and problem statement (1-2 paragraphs)
- Current status and recent milestones
- Roadmap with rough priorities
- Key decisions already made (see table below)

**The "Key Decisions" table** is particularly valuable. It stops Claude from relitigating choices you've already settled:

```markdown
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth method | JWT (no sessions) | Stateless deployment on Workers |
| Database | D1 (SQLite) | Free tier, no ops, acceptable scale |
| Test framework | Vitest | Native ESM, faster than Jest |
```

Without this, Claude may propose alternatives in every session. With it, settled decisions stay settled.

---

## Steering Claude During Sessions

Once your project is configured, these phrases let you adjust Claude's behaviour in the moment without starting over.

### The five intent modes

---

#### 1. Slow down & reason deeply

**When to use:** Before complex decisions, architectural choices, or difficult debugging.

| Phrase | Effect |
|--------|--------|
| `think carefully` | Activates extended reasoning before responding |
| `think ultra hard` | Maximum reasoning effort — use for high-stakes decisions |
| `step by step` | Forces sequential explanation, surfaces hidden assumptions |
| `walk me through this exactly` | Detailed narration of logic — good for auditing a plan |

---

#### 2. Stop — don't fill gaps

**When to use:** When Claude seems confident without having read the relevant file; when wrong assumptions have burned you before.

| Phrase | Effect |
|--------|--------|
| `do not assume` | Claude must state what it doesn't know |
| `do not guess` | Stronger — refuses to proceed on uncertain information |
| `ask if unsure` | Invites questions rather than confident-sounding speculation |
| `ask me questions` | Claude interviews you before acting |

---

#### 3. Verify before moving on

**When to use:** After implementation, before a commit, when you want Claude to catch errors it introduced.

| Phrase | Effect |
|--------|--------|
| `validate your work` | Claude reviews its own output for correctness |
| `check your work` | Shorter form — same intent |
| `do user end to end testing` | Claude traces the full user journey through the code |

---

#### 4. Challenge the approach

**When to use:** Before committing to a direction; when a plan feels too convenient; stress-testing architecture.

| Phrase | Effect |
|--------|--------|
| `take the contrarian view` | Claude argues against its own proposal |
| `ask the sub agents` | Spawns a fresh-context agent to review the plan independently |

---

#### 5. Control scope & output

**When to use:** Preventing scope creep, reining in verbosity, stopping silent changes to unrelated code.

| Phrase | Effect |
|--------|--------|
| `tell me succinctly` | Short answer only — suppresses elaboration |
| `only change what I asked` | Strict scope enforcement — no opportunistic refactors |
| `preserve references` | Don't touch cross-references, links, or imports outside the target |

---

### Combining phrases for effect

Phrases stack. The right combinations produce qualitatively different behaviour:

**Before a risky refactor:**
```
Think ultra hard, do not assume, list files before modifying, validate your work when done.
```

**When Claude is being verbose:**
```
Tell me succinctly.
```

**When a plan might be wrong:**
```
Take the contrarian view, then ask me questions before proceeding.
```

**When debugging a subtle issue:**
```
Step by step. Do not guess. Ask me questions if you need more context.
```

---

### Workflow-specific tips

- **Always `/prime [mode] FEAT-XXX` before starting** — mode shapes mindset, not just context. `think` loads planning instincts; `build` loads TDD discipline.
- **`/handover` before you stop, even mid-session** — the messy in-progress state IS the state the next session needs to recover. Clean handovers save 10+ minutes of re-orientation.
- **`/retro` is where value compounds** — skip it and patterns stay in the chat log. Run it and they become reusable skills that improve every future session.

---

## See Also

- [Getting Started](getting-started.md) — Setup steps and first session
- [Commands Reference](commands-reference.md) — Full command documentation
- [Architecture](../system/architecture.md) — System design and patterns
