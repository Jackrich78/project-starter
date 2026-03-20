# LinkedIn Carousel Review — Project Starter (Final)

## Context for Reviewer

### What is Project Starter?

Project Starter is an open-source workflow template for Claude Code (Anthropic's CLI for AI-assisted development). Claude Code gives you raw materials — a blank CLAUDE.md, unstructured memory, session context — but no opinionated workflow. Project Starter is the structure layer: commands, agents, skills, and documentation patterns that make sessions compound.

**What's in the box:**
- **13 commands** — `/explore`, `/blueprint`, `/build`, `/qa`, `/commit`, `/handover`, `/prime`, `/retro`, `/logs`, `/create-specialist`, `/update-docs`, `/debug`, `/setup`
- **12 specialized agents** — researcher, challenger, first-principles-thinker, QA reviewer, TDD subagents (test-writer, implementer, refactorer), prompt specialist, librarian, and more
- **18 skills** — learned patterns for brand guidelines, diagram generation, document creation, test strategy, etc.
- **Stack-agnostic** — works with any language, any framework
- **MIT Licensed** — fully open source

### Who is the creator?

Jack Richardson (@jackrich7 on LinkedIn). Builder, not a marketer. Tone: first-person, honest, builder-to-builder — like explaining it to someone at a meetup.

### The origin story

Jack was using ChatGPT, Claude, and other UI wrappers but kept copying and pasting between chat windows. Same repetitive loop every time. He wanted to be closer to the code — to understand what the agent was actually doing. Claude Code got him there. But sessions still didn't compound. Every morning was a fresh start. So he built the structure layer: Project Starter.

### Two tensions this solves

1. **Proximity** — Chat AI keeps you too far from the code. You're describing what you want, not building it. Project Starter is CLI-first, TDD-driven, close to the code.
2. **Compounding** — Even with Claude Code, sessions don't connect. No structure, no workflow, no memory of decisions. Project Starter makes sessions build on each other.

### Carousel format

6 slides, 4:5 portrait (1080x1350px), uploaded to LinkedIn as PDF. Dark bookend slides (1 + 6), light content slides (2-5). V2 brand: Near Black `#1A1A2E`, White, Signal Red `#E63946`, Royal Blue `#2563EB`, Emerald `#10B981`, Amber `#F59E0B`. Fonts: Bebas Neue (headlines, uppercase) + Inter (body).

---

## Final Carousel Content

### Slide 1 — Hook (Dark)

**Headline:** SESSION 50 IS SMARTER THAN SESSION 1

**Subline:** I open-sourced the workflow that got me there.

**Intent:** Concrete, challengeable claim. Works whether or not you know Claude Code. Creates genuine curiosity. "Smarter" implies compounding — the central thesis. "Open-sourced" signals generosity immediately.

---

### Slide 2 — The Human Moment (Light)

**Headline:** I WAS COPYING AND PASTING BETWEEN CHAT WINDOWS

**Body:**
- I tried every UI — ChatGPT, Claude, wrappers. Same loop.
- I wanted to be closer to the code — to understand what the agent was actually doing.
- *Claude Code got me there. But sessions still didn't compound.*

**Intent:** The real origin story. Every developer who's used chat AI has done the copy-paste dance. The pivot line ("Claude Code got me there. But...") sets up the solution without naming it yet. This is a story slide, not a feature slide.

---

### Slide 3 — Solution (Light)

**Headline:** PROJECT STARTER

**Tagline:** A Claude Code workflow where every session builds on the last.

**Stats:**
- **13** commands — from /explore to /commit
- **12** specialized agents — TDD, QA, research, planning
- **18** skills — reusable patterns your sessions learn once and keep

**Positioning:** Works with any stack · MIT License

**Intent:** The reveal. Numbers have context (what they do, not just how many). "Reusable patterns your sessions learn once and keep" reinforces compounding. "Works with any stack" is concrete.

---

### Slide 4 — How It Works (Light)

**Headline:** FIVE COMMANDS. ONE LOOP.

**Pipeline:** /explore → /blueprint → /build → /qa → /commit. Each produces an artifact the next one reads. Final step: changelog + merged.

**Intent:** The screenshot moment. Visually distinctive, shareable, save-worthy. Tells a complete story from idea to shipped. Colored command badges are mobile-readable.

---

### Slide 5 — Before/After (Light)

**Headline:** SESSION 1 vs SESSION 50

**Session 1:** Re-explain the architecture. Re-define the patterns. Hope it follows.

**Session 50:** /explore — it already knows the codebase, the standards, and the last three decisions.

**Takeaway:** The difference isn't the model. It's the harness.

**Intent:** Felt contrast. The reader recognizes "Session 1" as their current experience. "Session 50" shows what's possible. "It's the harness" — one word that reframes everything. This slide mirrors the hook and closes the loop.

---

### Slide 6 — CTA (Dark)

**Headline:** FORK IT. BREAK IT. TELL ME WHAT'S MISSING.

**License:** MIT License

**Note:** Link in comments

**Comment driver:** What's the first thing you re-explain to your AI every session?

**Intent:** Generous + invites challenge. "Tell me what's missing" drives both forks AND comments. The question is specific and answerable — people reply with their own version. GitHub link deliberately moved to first comment to protect algorithm distribution.

---

## Companion Post Text

**Opening (before "See more" fold — first 210 characters):**

> My 50th Claude Code session was no smarter than my first. Same questions. Same mistakes. Same context loss. I spent three months building the system that fixed it. Here's what actually worked...

**Full post:**

> My 50th Claude Code session was no smarter than my first. Same questions. Same mistakes. Same context loss. I spent three months building the system that fixed it. Here's what actually worked...
>
> I was copying and pasting between chat windows — ChatGPT, Claude, wrappers. Same loop every time. I wanted to be closer to the code, to see what the agent was actually doing. Claude Code got me there.
>
> But sessions still didn't compound. Every morning was a fresh start. So I built the structure layer.
>
> Project Starter is a workflow template that sits on top of Claude Code. 13 commands. 12 agents. 18 skills. MIT licensed.
>
> The core loop: /explore → /blueprint → /build → /qa → /commit. Each command produces an artifact the next one reads. Over time, your sessions get smarter — not because the model improved, but because the context compounds.
>
> This isn't vibe coding. Every feature starts with a test spec, not a prompt.
>
> Swipe to see how it works.

**First comment (pinned):** github.com/jackrich78/project-starter

---

## Evolution Log

- **v1:** Generic hook ("I kept starting every AI session from scratch"), "Sound familiar?" problem, wrong numbers (14/12/17)
- **v2 (round 1 review):** Hook swapped to "Session 50", problem scoped to Claude Code, numbers corrected, CTA question made specific
- **v3 (round 2 review + creator input):** Slide 2 rewritten as real origin story (copying between chat windows → Claude Code → harness). Slide 5 rewritten as before/after. CTA changed to "Fork it. Break it. Tell me what's missing." GitHub URL moved to first comment. Ogilvy word-level polish applied throughout. "Vibe coding" tension added to companion post.

---

## Open Questions for Reviewer

1. Does "SESSION 50 IS SMARTER THAN SESSION 1" stop the scroll?
2. Does the slide 2 story (copying between chat windows) feel authentic and relatable?
3. Is "THE CLAUDE CODE MEMORY PROBLEM" too niche as an implied framing, or does it correctly self-select?
4. Does the before/after on slide 5 land? Is "It's the harness" a strong enough closer?
5. Is the CTA question natural enough to drive real comments?
6. Does the companion post earn the "See more" click in the first two lines?
7. Does the arc flow naturally, or does any slide feel like it's selling?
