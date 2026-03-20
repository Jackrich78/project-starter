<!-- CUSTOMIZE: Replace with your own aesthetic direction and visual philosophy -->

# Aesthetic Direction

The visual philosophy behind this design system. Read this before creating any visual content — it guides *how* to use colors and typography, not just *which* ones.

---

## Visual Identity: Teal Nature Palette

Inspired by modern editorial design with a nature-grounded colour philosophy. The aesthetic is:

- **Grounded** — Deep teal backgrounds evoke depth and trust, not corporate coldness
- **Fresh** — Lime chartreuse accents cut through with energy and modernity
- **Clean** — White backgrounds, generous whitespace, minimal decoration
- **Simple** — Reduce to essentials, let content and colour do the work

### The Core Technique: Color as Structure

Colour lives in **borders, accent bars, and card backgrounds**, not in the UI chrome. Backgrounds are white or deep teal. Bold, saturated colours appear in:

- Card left borders (4.8pt, coloured per semantic meaning)
- Top zone accent bars (Lime Chartreuse)
- Pipeline badges (filled with brand colours)
- Key metrics and callout numbers

**Never** use saturated colours as full-page backgrounds or large text blocks. They are accents and structural elements.

### Signature Visual: Converging/Diverging Pipeline

The pipeline diagram (Slide 4) is a signature layout where:

- **Left column** (command badges) narrows from top to bottom — uncertainty fades
- **Right column** (artifact boxes) expands from top to bottom — understanding builds
- Filled badges on the left, outlined boxes on the right
- Each row shares a colour from the brand palette
- The visual symmetry communicates the compounding nature of the workflow

### Whitespace as a Design Element

The most important design tool is **empty space**:

- At least 40% of any slide should be whitespace
- Hero elements need 200px+ of breathing room
- Dense information needs more whitespace, not less
- When in doubt, remove elements rather than adding them

---

## Design Principles

### 1. Contrast Creates Hierarchy

The system uses extreme contrast to guide the eye:

- **Bebas Neue at 60pt** next to **Roboto Light at 22pt** — the size gap IS the hierarchy
- **Deep Teal `#0D5B65`** on **white `#FFFFFF`** — saturated on neutral
- **One bold element per section** — everything else supports it

### 2. Color Has Purpose

Every colour choice should answer "why this colour here?"

| Color | Personality | Use When... |
|-------|------------|-------------|
| Deep Teal | Trust, depth, nature | Dark backgrounds, headline text |
| Lime Chartreuse | Energy, freshness, brand anchor | Top accent bar, primary attention |
| Lavender | Creativity, calm, memory | "Remembers" theme, pivot lines |
| Teal Mint | Growth, progress, planning | "Plans" theme, positive indicators |
| Lime Green | Action, completion, shipping | "Evolves" theme, commit step |

**Rule**: Max 2-3 accent colours per slide/diagram. More than that creates visual noise.

### 3. Typography Tells the Story

Headlines (Bebas Neue) make **bold statements**. Body text (Roboto) **explains and supports**.

- Headlines should be short and punchy (5-8 words max)
- If a headline needs two lines, it's too long
- Body text should be scannable — bullets, short paragraphs, clear structure
- Use Roboto weight variations (Light, Medium, SemiBold) for sub-hierarchy

### 4. Audience-First Design

This system targets non-technical audiences:

- Prefer familiar metaphors over technical jargon
- Use colour to make data feel approachable, not intimidating
- Large text, generous spacing — don't make people squint
- One idea per visual — complexity kills comprehension

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Rainbow slides (all 5 colours) | Visual chaos, no hierarchy | Max 2-3 colours per slide |
| Saturated colour backgrounds | Overwhelms content, hard to read | White or deep teal backgrounds, colour in borders/accents |
| Small, dense text | Non-technical audience loses interest | 20pt minimum body, generous spacing |
| Decorative elements without purpose | Clutter, dilutes message | Every shape should carry meaning |
| Overlapping geometric shapes | Dated, "v1" feel | Use card blocks with coloured left borders for structure |
| Drop shadows and gradients | Dated, busy, distracting | Flat colours, card blocks for depth |
| Centered everything | Passive, lacks energy | Left-aligned text, asymmetric layouts |

---

## Application by Format

### Pitch Decks (PPTX)
- Title slides: Bebas Neue hero text on deep teal background
- Content slides: White background, left-aligned Roboto body, card blocks with coloured borders
- Data slides: Large Bebas Neue numbers in brand accent + Roboto labels
- Pipeline slides: Converging/diverging layout with coloured badges

### Technical Diagrams (Excalidraw)
- White canvas, roughness 0 (clean/modern)
- Shapes use the semantic colour palette
- Section boundaries marked by colour, not boxes-around-boxes
- Evidence artifacts (code snippets) on dark (#0D5B65) backgrounds

### Documents (DOCX/Reports)
- White background, dark teal heading text
- Bebas Neue for document title and chapter headings only
- Roboto for all other text
- Colour appears only in charts, diagrams, and callout boxes
