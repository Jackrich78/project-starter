<!-- CUSTOMIZE: Replace with your own aesthetic direction and visual philosophy -->

# Aesthetic Direction

The visual philosophy behind this design system. Read this before creating any visual content — it guides *how* to use colors and typography, not just *which* ones.

---

## Visual Identity: Bold Geometry

Inspired by modern editorial design (Design Council, Pentagram, Swiss Style). The aesthetic is:

- **Bold** — Heavy headlines, saturated colors, confident layouts
- **Geometric** — Clean shapes, overlapping forms, structured compositions
- **Clean** — White backgrounds, generous whitespace, minimal decoration
- **Simple** — Reduce to essentials, let content and color do the work

### The Core Technique: Color as Structure

Color lives in the **graphics and shapes**, not in the UI chrome. Backgrounds are white. Text is near-black. Bold, saturated colors appear in:

- Geometric shapes (rectangles, circles, abstract forms)
- Section dividers and accent bars
- Data visualization and diagrams
- Key metrics and callout numbers

**Never** use saturated colors as full-page backgrounds or large text blocks. They are accents and structural elements.

### Overlapping Elements for Depth

A signature technique: geometric shapes that **overlap and layer** to create visual depth and energy. Even without transparency blending:

- Overlap shapes at edges (20-30% overlap)
- Use different saturated colors for adjacent overlapping shapes
- The overlap creates visual rhythm and movement
- Works in Excalidraw (solid fills), PPTX (positioned shapes), and web (CSS positioning)

Example: Three rectangles in Red, Blue, and Green, each offset 40px right and 20px down, creating a cascading stack.

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

- **Bebas Neue at 48pt** next to **Inter at 14pt** — the size gap IS the hierarchy
- **Signal Red #E63946** on **white #FFFFFF** — saturated on neutral
- **One bold element per section** — everything else supports it

### 2. Color Has Purpose

Every color choice should answer "why this color here?"

| Color | Personality | Use When... |
|-------|------------|-------------|
| Signal Red | Energy, urgency, brand anchor | Primary CTAs, key metrics, brand moments |
| Royal Blue | Trust, structure, depth | Technical content, frameworks, architecture |
| Emerald | Growth, success, positive | Results, benefits, progress indicators |
| Amber | Attention, warmth, caution | Highlights, warnings, important notes |
| Violet | Innovation, premium, special | AI/tech features, differentiation, creative elements |

**Rule**: Max 2-3 saturated colors per slide/diagram. More than that creates visual noise.

### 3. Typography Tells the Story

Headlines (Bebas Neue) make **bold statements**. Body text (Inter) **explains and supports**.

- Headlines should be short and punchy (5-8 words max)
- If a headline needs two lines, it's too long
- Body text should be scannable — bullets, short paragraphs, clear structure
- Use Inter weight variations (Regular, SemiBold, Bold, ExtraBold) for sub-hierarchy

### 4. Audience-First Design

This system targets non-technical audiences:

- Prefer familiar metaphors over technical jargon
- Use color to make data feel approachable, not intimidating
- Large text, generous spacing — don't make people squint
- One idea per visual — complexity kills comprehension

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Rainbow slides (all 5 colors) | Visual chaos, no hierarchy | Max 2-3 colors per slide |
| Saturated color backgrounds | Overwhelms content, hard to read | White backgrounds, color in shapes |
| Small, dense text | Non-technical audience loses interest | 16pt minimum body, generous spacing |
| Decorative elements without purpose | Clutter, dilutes message | Every shape should carry meaning |
| Uniform boxes in a grid | Generic, boring, "AI-generated" feel | Vary shapes, sizes, and patterns |
| Drop shadows and gradients | Dated, busy, distracting | Flat colors, overlap for depth |
| Centered everything | Passive, lacks energy | Left-aligned text, asymmetric layouts |

---

## Application by Format

### Pitch Decks (PPTX)
- Title slides: Bebas Neue hero text + one geometric color block
- Content slides: White background, left-aligned Inter body, color accent bar on one edge
- Data slides: Large Bebas Neue numbers in saturated color + Inter labels
- Use overlapping geometric shapes as decorative elements on section dividers

### Technical Diagrams (Excalidraw)
- White canvas, roughness 0 (clean/modern)
- Shapes use the semantic color palette (see color-palette.md)
- Section boundaries marked by color, not boxes-around-boxes
- Evidence artifacts (code snippets) on dark (#1A1A2E) backgrounds
- Overlapping shapes at section transitions for visual flow

### Documents (DOCX/Reports)
- White background, near-black text
- Bebas Neue for document title and chapter headings only
- Inter for all other text
- Color appears only in charts, diagrams, and callout boxes
