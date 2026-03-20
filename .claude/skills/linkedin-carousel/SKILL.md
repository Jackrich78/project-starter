---
name: linkedin-carousel
description: "Generate a branded LinkedIn carousel as PPTX (4:5 portrait, 810pt x 1012.5pt). Creates slide-by-side content markdown for review, then generates PPTX via html2pptx. Use when creating LinkedIn carousel posts for Project Starter."
---

# LinkedIn Carousel Generator

## Overview

Creates a branded 6-slide LinkedIn carousel as PPTX. Two-stage output: content markdown for review, then PPTX generation after confirmation.

## Content Voice

First-person, honest, builder-to-builder. Not marketing. The way you'd explain something to someone at a meetup. Acknowledges there are multiple approaches — this is one you built for yourself.

Guidelines:
- Personal pronouns: "I built", "I kept", "I found"
- Specific over abstract: name the tools, commands, artifacts
- No hype words: "revolutionary", "game-changing", "unlock"
- Generous tone: "Fork it. Steal it. Use it for inspiration."
- Honest about trade-offs: every choice has downsides

## Reference Files

Before generating content, read:

1. **`references/slide-spec.md`** — slide structures, colours, typography, 3-zone layout
2. **`.claude/skills/brand-guidelines/references/colors-and-typography.md`** — v2 brand palette
3. **`references/cta-best-practices.md`** — CTA patterns and data

## Stage 1: Content Markdown

### Workflow

1. Identify the story: what was built, why, what makes it worth sharing
2. Draft 6-slide content matching the template roles (hook → story → solution → visual → before/after → CTA)
3. Write `carousel-content.md` with slide-by-slide copy

### Content Rules

- Headlines: max 8 words, Bebas Neue (uppercase only)
- Body bullets: max 6 words each, max 4 bullets per slide
- Every slide must be readable on a phone screen (20pt+ body, 48pt+ headlines)
- No emojis

### HARD STOP

After writing `carousel-content.md`, output:

> **Confirm slide copy to proceed to PPTX generation.**

Do not proceed until the user confirms.

## Stage 2: PPTX Generation

### Build Workflow

1. Write populated HTML files (one per slide) to workspace directory
2. Create `carousel-build.cjs` using pptxgenjs + html2pptx
3. Configure 4:5 portrait layout: `pptx.defineLayout({ name: 'CAROUSEL', width: 810/72, height: 1012.5/72 })`
4. Convert all 6 slides
5. Run `apply_brand_fonts.py` post-processing
6. Output final `.pptx`

### HTML Construction

For each slide, start from the matching HTML template in `templates/`:

| Slide | Template |
|-------|----------|
| 1 (Hook) | `templates/hook-dark.html` |
| 2 (Story) | `templates/story-light.html` |
| 3 (Solution) | `templates/solution-light.html` |
| 4 (Visual) | `templates/visual-light.html` |
| 5 (Before/After) | `templates/beforeafter-light.html` |
| 6 (CTA) | `templates/cta-dark.html` |

Additional templates available:
| Template | Use case |
|----------|----------|
| `templates/problem-light.html` | Pain-point cards with left borders |
| `templates/insight-light.html` | Compounding/benefit cards with colored borders |

Replace `{{PLACEHOLDER}}` tokens with content from `carousel-content.md`.

### html2pptx Constraints

- Backgrounds and borders only on `<div>` elements (not `<p>`, `<span>`, `<img>`)
- No CSS gradients
- No `background-image: url()` — use `<img>` tags instead
- CSS opacity is silently dropped — pre-bake opacity into RGBA colours
- Never inline `<svg>` — crashes html2pptx

### Brand Font Post-Processing

```bash
python3 .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py <output.pptx>
```

Converts Arial placeholders to Bebas Neue (headings) + Roboto variants (body).
Maps by font name, not size: Arial Black → Bebas Neue, Arial bold+italic → Roboto SemiBold,
Arial bold → Roboto Medium, Arial ≤18pt → Roboto Medium, Arial >18pt → Roboto Light.

## Quality Gates

- [ ] Exactly 6 slides
- [ ] Dimensions are 810pt x 1012.5pt
- [ ] All text readable at phone size (20pt+ body, 48pt+ headlines)
- [ ] Brand fonts applied: Bebas Neue (headlines) + Roboto (body) — or Arial fallback noted
- [ ] `@jackrich7` on every slide (bottom zone)
- [ ] Headshot circle on every slide (bottom zone)
- [ ] No emojis
- [ ] PPTX opens without corruption

## Terminal Review

After PPTX generation, display:

```
CAROUSEL REVIEW
  Slides: [count]
  Dimensions: [verified/failed]
  Fonts: [Bebas Neue + Roboto applied / Arial fallback]

  Next steps:
  1. Upload .pptx to Google Drive, use "Open with Google Slides"
     (Do NOT use "Import slides" — stretches to 16:9)
  2. Verify elements are editable
  3. Export as PDF for LinkedIn upload
```
