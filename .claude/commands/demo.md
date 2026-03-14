---
updated: 2026-02-25T00:00:00Z
description: Turn a completed build into polished LinkedIn content (carousel, video, post, or full package)
argument-hint: [post|carousel|video|full] [optional: file path]
---

# Demo: LinkedIn Content Pipeline

Generating LinkedIn demo content for: **$ARGUMENTS**

## Mission

Surface the genuine story in a completed build — surprise, decision, trade-off — then generate on-brand LinkedIn content in the requested format. Story extraction comes first. Formatting comes second.

Read `docs/features/FEAT-028_linkedin-demo-pipeline/prd.md` Stage 0 through Stage 1 for complete question design and scaffold format.

---

## Stage 0: Demo Brief (The Front Door)

Before any content is generated, run Stage 0. This is the interactive phase that surfaces the story. It is not optional.

### Step 1: Context Loading

Check for pre-loaded context:

1. **Content pasted in conversation** — if the user pasted a handover doc, session notes, PRD, or any relevant text before running `/demo`, reference it as build context.
2. **File path provided** — if a file path appears in `$ARGUMENTS` (after the format keyword), read the file and use it as build context. Accept any markdown file from any location on the filesystem.
3. **No context** — proceed open-ended. All qualifying questions asked without pre-populated details.

Context gives the facts. The questions surface the story. Context does NOT replace the qualifying questions.

### Step 2: Qualifying Questions

Present all five questions at once. These are the brief. They are asked before generation begins.

```
Before we generate content, let's find the story.

1. What surprised you during this build?
   (An unexpected constraint, a decision that changed direction,
   something that almost broke — state it as a specific event)

2. What decision did you make that someone else might have made differently?
   (What was the fork in the road? What was the option you didn't take, and why?)

3. What did you give up or leave out?
   (The honest limitation — what would have been better in an ideal world
   that you deliberately excluded, deferred, or simplified?)

4. What is the specific outcome — in measurable or observable terms?
   (A number, a before/after, a capability that now exists that didn't before.
   "Faster" is not an answer. "From 45 minutes to 8 minutes" is.)

5. Finish this sentence: "Someone should read this because ___"
   (If you cannot finish it with a specific reason, this moment is not ready to post.
   This is a postability filter — proceed only if the sentence can be completed.)
```

If context was loaded, reference specific details from it when asking: "I see you built X using Y approach — what surprised you about that?"

**Follow-up if answers are weak:**
- "What surprised you" answered vaguely -> "Was there a moment where you almost chose a different approach? Did anything break or fail?"
- "What decision" answered vaguely ("I chose this because it was simpler") -> "What was the approach you did not take? Why exactly did it lose?"
- "What did you give up" answered vaguely ("I'd have documented it better") -> "What would have been better in an ideal world that you explicitly excluded or deferred? Name the specific thing."
- Outcome non-specific -> "Give me a before/after or a specific number, even rough. If there's no metric, name the capability that now exists that didn't before."
- No decision identified -> "What did you not use, and why did it lose?"

**Quality check on "what I'd do differently":** If the answer is fewer than 15 words or contains no specific technical claim, prompt once: "Can you be more specific? What exactly would change — which component, which decision point, which constraint would you handle differently?" Do not generate a substitute if the answer remains vague. Proceed with what is provided and flag in the review checklist.

**Exploration builds (no measurable metric):** If the build was a spike or research session with no before/after metric, "a capability now exists that didn't before" counts as an outcome. Format: "Before: [what wasn't possible]. Now: [what is]."

### Step 3: Build Type Detection

Identify the build type from the brief answers. Ask the user if not inferable.

| Type | Definition | Primary Format |
|------|-----------|---------------|
| **Type 1: Tool/Skill Demo** | New capability shipped. Interesting thing is what it now makes possible. | Carousel + post |
| **Type 2: Architecture Decision** | Genuine technical choice made. Interesting thing is the reasoning. | Post or carousel |
| **Type 3: Failure Post-Mortem** | Something broke, was wrong, or had to be rebuilt. | Post-only (primary) |
| **Type 4: Workflow Revelation** | Process faster/easier/more powerful than expected. | Video + post |
| **Type 5: System Benchmark** | Something measured — speed, reliability, cost, quality. | Carousel + post |

### Step 4: Assemble Demo Brief

Compile answers into the brief template:

```
DEMO BRIEF
----------
The interesting thing:   [The surprise, decision, or failure — one sentence]
Context:                 [What you built — 10 words max]
Specific outcome:        [A number or before/after]
What I'd do differently: [Required — user's actual answer, not generated]
Audience:                [Who this is for]
Build type:              [Type 1-5]
Demo type:               [carousel | video | full | post]
Archetype:               [show-your-work | systems-story | reality-check]
```

"What I'd do differently" is VERBATIM FROM USER INPUT — do not generate or rephrase. If the user did not provide a specific answer, ask once. Do not generate a substitute.

---

## Stage 1: Narrative Scaffold

### Step 5: Generate Scaffold

From the brief, generate the narrative scaffold:

```
NARRATIVE SCAFFOLD
------------------
Hook (1 sentence, stops scroll):
  "[The result, constraint, or decision — not the journey]"

The tension (why the hook matters):
  [2-3 sentences on what was hard, broken, or unclear — specific, not abstract.]

The decision (what was chosen and why):
  [The fork in the road — what was chosen, what was rejected, and the concrete reason]

The honest detail (trade-off or what went wrong):
  [The part that almost didn't work, or the limitation being acknowledged]

The specific outcome:
  [The number or before/after — both endpoints named]

The CTA (challenge invitation):
  "[A genuine question that requires reading the content to answer]"

Archetype: [show-your-work | systems-story | reality-check]
Audience:  [Specific description]
```

### Step 6: Scaffold Confirmation (HARD STOP)

Display the scaffold, then write ONLY:

"Does this scaffold capture the story correctly? Confirm to proceed, or correct any section."

Do NOT write additional content. Do NOT begin skill invocation. Wait for the user to respond. This is not optional.

After scaffold is confirmed: each skill receives the same scaffold as input. No skill re-extracts.

---

## Stage 2: Format Routing

Parse the format from `$ARGUMENTS` (first word: `post`, `carousel`, `video`, or `full`). Route accordingly:

### `post` — Text-only LinkedIn post
1. Invoke `linkedin-post` skill with scaffold + build type
2. Output: post caption file

### `carousel` — Carousel LinkedIn post
1. Invoke `linkedin-carousel` skill with scaffold + build type -> PPTX
2. Invoke `linkedin-post` skill with scaffold + build type + CTA framing: "Swipe to see..." -> caption
3. User next step: review slides in Google Slides -> export PDF -> upload PDF + caption to LinkedIn

### `video` — Video LinkedIn post
1. Invoke `linkedin-carousel` skill with scaffold + build type -> PPTX (4:5 carousel for upload)
2. Invoke `linkedin-carousel` skill with scaffold + build type + `video: true` -> PPTX (16:9 video slides using `templates/video/` at 720pt x 405pt, content left-biased for speaker overlay)
3. Invoke `linkedin-script` skill with scaffold + build type + slide cues -> script (references 16:9 video slides)
4. Invoke `linkedin-post` skill with scaffold + build type + CTA framing: "Watch to see..." -> caption
5. User next step: record screen demo using 16:9 slides as visual aids -> add captions via Kapwing -> upload video + caption to LinkedIn

### `full` — Both carousel + video posts (two separate LinkedIn posts)
Run carousel path + video path with shared scaffold. Two separate post captions:
1. Invoke `linkedin-carousel` skill with scaffold + build type -> `carousel.pptx` (4:5, for LinkedIn upload)
2. Invoke `linkedin-carousel` skill with scaffold + build type + `video: true` -> `video-slides.pptx` (16:9, for screen recording)
3. Invoke `linkedin-post` skill with scaffold + "swipe" CTA framing -> carousel post caption
4. Invoke `linkedin-script` skill with scaffold + build type + slide cues -> script (references 16:9 slides)
5. Invoke `linkedin-post` skill with scaffold + "watch" CTA framing -> video post caption

---

## Stage 3: Quality Gate

### Step 8: Quality Checks

Run on all generated outputs:

**Voice compliance gate (10-item checklist):**
- [ ] Hook states a specific result, constraint, or decision — not a vague outcome
- [ ] Does not start with "I'm excited/proud/thrilled/happy to share/announce"
- [ ] At least one trade-off or limitation named
- [ ] Outcome section includes "what-I'd-do-differently" (from brief input, not generated)
- [ ] No hype vocabulary: game-changer, revolutionary, groundbreaking, powerful, amazing, incredible, cutting-edge, next-level, unleash, transformative, robust (filler), seamless
- [ ] CTA invites challenge or genuine question and requires reading the content to answer
- [ ] No emojis anywhere in the output
- [ ] No sentences over 20 words; slide headlines max 8 words
- [ ] At least one concrete metric (time, percentage, count, step reduction)
- [ ] No passive construction on key claims — actor must be named

**CTA quality gate (5 tests):**
1. Post-dependency: Can this CTA be answered without reading the post? If yes: reject.
2. Disagreement invitation: Does it allow for "no" or "I'd do it differently"?
3. Specificity: Does it implicitly define what a useful response looks like?
4. Authenticity: Is the author actually curious about the answer?
5. Brand consistency: Does it sound like the Pragmatic Strategist?

If CTA fails 2+ tests, generate 3 alternatives from `.claude/skills/linkedin-shared/references/cta-bank.md` and present for user selection.

---

## Stage 4: Terminal Summary

### Step 9: Print Summary

```
DEMO COMPLETE
─────────────
Narrative type:  [archetype]
Audience:        [audience from scaffold]
Build type:      [Type 1-5]

Files generated:
  [list each file path — only files that actually exist]

User next steps:
  [format-specific instructions for publishing]

Review checklist:
  [ ] Read the hook aloud — does it stop the scroll?
  [ ] Check "what I'd do differently" — is it your actual words?
  [ ] Verify the metric is accurate

Known limitations:
  [list any: vague "what I'd do differently", missing metric, diagram placeholders, etc.]

Degradation status:
  Brand fonts: [applied / Arial fallback — reason]
  Diagram:     [SVG rendered / .mmd source only — render instructions]

Files by format:
  Carousel: carousel-content.md, carousel.pptx, post-carousel.md
  Video:    video-slides.pptx, script.md, post-video.md
  Shared:   brief.md, scaffold.md, pipeline-diagram.mmd
```

### Step 10: Post-Publish Protocol

Append the post-publish protocol to every post caption file:

```
---
POST-PUBLISH PROTOCOL (appended to every post file)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEFORE PUBLISHING
  Comment on 5-7 posts from your network (15+ words, genuine engagement)
  Signals active community membership, boosts initial distribution

FIRST 60 MINUTES AFTER POSTING
  Respond to every comment within 60 minutes
  Responses: 15+ words — extend the thread, ask a follow-up question
  First 60 minutes: 23-47% reach boost from early engagement
  Comments (10+ words): 5x more algorithmic weight than reactions
```

---

## Stage 5: Archive

### Step 11: Archive Outputs

Archive all outputs to `demos/[YYYYMMDD]-[slug]/` where:
- `YYYYMMDD` = today's date
- `slug` = first 3 words of "the interesting thing" from the demo brief, lowercased, hyphenated

Example: `demos/20260225-context-window-broke/`

Files in the archive folder (only those relevant to the chosen format):
- `brief.md` — archived demo brief (always)
- `scaffold.md` — confirmed narrative scaffold (always)
- `carousel-content.md` — slide copy for review (carousel + video paths)
- `carousel.pptx` — branded 4:5 PPTX (carousel path: for LinkedIn upload)
- `video-slides.pptx` — branded 16:9 PPTX (video path: recording visual aids, left-biased layout)
- `script.md` — script + slide cues + production notes (video path)
- `post-carousel.md` — carousel post caption + post-publish protocol (carousel path)
- `post-video.md` — video post caption + post-publish protocol (video path)
- `post.md` — post caption + post-publish protocol (post-only path)
- `slides/` — HTML slide source files (for debugging/re-rendering)
- `pipeline-diagram.mmd` — Mermaid diagram source (if mmdc unavailable)

---

## Guardrails

**Does NOT:**
- Call skills without a confirmed narrative scaffold
- Generate content without completing Stage 0
- Override user's explicit format choice
- Print paths for files that don't exist
- Attach both carousel and video to the same LinkedIn post (they are mutually exclusive)
- Generate "what I'd do differently" — this is VERBATIM FROM USER INPUT
- Continue past scaffold confirmation without user response

**Silent failure warnings:**
1. "What-I'd-do-differently" must be labeled as VERBATIM FROM USER INPUT — do not generate or rephrase
2. Scaffold confirmation is a HARD STOP — after displaying scaffold, write ONLY the confirmation prompt. Do not write additional content until user responds.
3. Carousel dimension override may silently fall back to 16:9 — run 1-slide test before building full carousel

**References:**
- `docs/features/FEAT-028_linkedin-demo-pipeline/prd.md` — full PRD
- `.claude/skills/linkedin-shared/references/cta-bank.md` — shared CTA asset
- `.claude/skills/linkedin-shared/references/voice-rules.md` — voice compliance rules
