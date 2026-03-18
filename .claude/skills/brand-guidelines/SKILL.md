<!-- CUSTOMIZE: Replace all placeholder values with your brand's colors, fonts, and style -->
---
name: brand-guidelines
description: "Apply your brand identity (colors, typography, visual style) to presentations, documents, reports, and marketing materials. Use when creating or styling any branded content. Provides color palette, typography hierarchy, visual style principles, and technical implementation code."
---

# Brand Guidelines

<!-- CUSTOMIZE: Replace "Your Brand" with your organization name -->
Apply your brand identity to any branded content. Read the aesthetic direction first, then use the quick reference below.

**Before creating anything visual**, read [aesthetic-direction.md](references/aesthetic-direction.md) to understand the design philosophy. The quick reference below gives you the values; the aesthetic direction tells you *how* to use them.

## Quick Reference

### Brand Colors (Bold & Saturated)

<!-- CUSTOMIZE: Replace all hex values with your brand colors -->
| Color | Hex | Use For |
|-------|-----|---------|
| Signal Red | `#E63946` | Primary CTAs, key metrics, brand anchor |
| Royal Blue | `#2563EB` | Technical content, frameworks, architecture |
| Emerald | `#10B981` | Results, benefits, positive indicators |
| Amber | `#F59E0B` | Highlights, warnings, important notes |
| Violet | `#7C3AED` | AI/tech features, differentiation |

**Rule**: Max 2-3 saturated colors per slide/diagram. Color in **shapes and graphics**, not in backgrounds or large text blocks.

### Text & Background

| Role | Hex | Name |
|------|-----|------|
| Headings | `#1A1A2E` | Near Black |
| Body text | `#374151` | Dark Gray |
| Muted/captions | `#6B7280` | Medium Gray |
| Background | `#FFFFFF` | White |
| Alt background | `#F3F4F6` | Cool Gray |
| Dark sections | `#1A1A2E` | Near Black |

**Forbidden**: Pure black (#000000) for text — use Near Black. Saturated colors as full-page backgrounds. Light text on light backgrounds.

### Typography

<!-- CUSTOMIZE: Replace with your brand fonts -->
| Level | Font | Size | Weight |
|-------|------|------|--------|
| H1 Hero | Bebas Neue | 56pt | 400 (bold by design) |
| H1 | Bebas Neue | 42pt | 400 |
| H2 | Inter | 28pt | ExtraBold (800) |
| H3 | Inter | 20pt | Bold (700) |
| Subtitle | Inter | 18pt | SemiBold (600) |
| Body | Inter | 16pt | Regular (400) |
| Standard | Inter | 14pt | Regular (400) |
| Small | Inter | 12pt | Regular (400) |
| Caption | Inter | 11pt | Medium (500) |
| Big Number | Bebas Neue | 72pt | 400 |

**Bebas Neue** is uppercase-only. Use for short, punchy headlines (5-8 words). Max 1-2 Bebas elements per page.

**Inter** handles everything else. Use weight variation (Regular through ExtraBold) for sub-hierarchy.

**Fallbacks**: Bebas Neue -> Impact, Arial Black, sans-serif. Inter -> Arial, sans-serif.

### Core Principles

1. **Bold Geometry** — Saturated colors in geometric shapes, white backgrounds, overlapping elements for depth
2. **Extreme Contrast** — Big Bebas Neue headlines next to clean Inter body creates visual energy
3. **Whitespace is Design** — At least 40% whitespace per slide. Dense information needs more space, not less
4. **Color Has Purpose** — Every saturated color choice should answer "why this color here?"
5. **Audience-First** — Non-technical audiences. Large text, familiar metaphors, one idea per visual

## Color Combinations

**Most Common Patterns:**

1. **Near Black headings on White** -> `#1A1A2E` text on `#FFFFFF` background (AAA contrast)
2. **Dark Gray body on White** -> `#374151` text on `#FFFFFF` background (AAA contrast)
3. **White text on Near Black** -> `#FFFFFF` text on `#1A1A2E` background (inverted sections)

**Accent Usage:**
- Signal Red numbers/metrics on White -> `#E63946` for key stats, bold callouts
- Royal Blue shapes/borders on White -> `#2563EB` for structural elements, diagrams
- Emerald for positive data -> `#10B981` for growth charts, success indicators

**Forbidden:**
- Light text on light backgrounds
- More than 3 saturated colors on one slide
- Saturated colors as full-page backgrounds
- Pure black (#000000) — use Near Black (#1A1A2E)
- Drop shadows, gradients, or decorative borders

## Application by Content Type

### PowerPoint/Slides
<!-- CUSTOMIZE: Adjust colors and fonts for each content type -->
- Title slide: Bebas Neue 56pt `#1A1A2E` + one geometric color block
- Content heading: Bebas Neue 42pt `#1A1A2E`
- Sub-heading: Inter ExtraBold 28pt `#1A1A2E`
- Body: Inter Regular 16pt `#374151`
- Background: `#FFFFFF`
- Accent bars/shapes: Any brand color (Signal Red, Royal Blue, etc.)
- Section dividers: Overlapping geometric shapes in 2-3 brand colors

### Technical Diagrams (Excalidraw)
- Canvas: `#FFFFFF`
- Shape fills: Brand colors with lighter tint fills + darker stroke
- Text hierarchy: Near Black titles, Dark Gray labels, Medium Gray annotations
- Evidence artifacts: `#1A1A2E` background + colored text
- Overlapping shapes encouraged at section boundaries

### Documents/Reports
- H1: Bebas Neue 42pt `#1A1A2E`
- H2: Inter ExtraBold 28pt `#1A1A2E`
- H3: Inter Bold 20pt `#1A1A2E`
- Body: Inter Regular 14pt `#374151`
- Background: `#FFFFFF`

## Resources

**Detailed specifications:**
- See [aesthetic-direction.md](references/aesthetic-direction.md) for design philosophy and anti-patterns
- See [colors-and-typography.md](references/colors-and-typography.md) for complete color palette with RGB values and contrast ratios
- See [technical-implementation.md](references/technical-implementation.md) for CSS variables, Python-PPTX code, and implementation snippets

**Scripts:**
- `scripts/brand_colors.py` — Python constants for all brand colors (RGB and hex)
- `scripts/apply_brand_fonts.py` — Font post-processor for PPTX files (applies Bebas Neue + Inter)

**Extending this skill:**
- Add an `assets/` directory for logos and brand imagery
- Add a `references/slide-examples/` directory with example slide screenshots
- Add a `references/visual-examples.md` for layout patterns

## Quality Checklist

Before finalizing branded content:
- [ ] Text meets WCAG AA contrast (4.5:1 minimum)
- [ ] Near Black for headings, Dark Gray for body
- [ ] White background (not off-white, not colored)
- [ ] Max 2-3 saturated colors used as accents
- [ ] Bebas Neue for H1 only (short headlines, max 1-2 per page)
- [ ] Inter with correct weight for each hierarchy level
- [ ] Font sizes follow the scale (no sizes between levels)
- [ ] At least 40% whitespace on slides
- [ ] No drop shadows, gradients, or decorative borders
- [ ] Geometric shapes overlap where appropriate for visual depth

## Integration with PPTX Skill

When used with PPTX generation:
1. Load this skill first to establish brand context
2. Use color constants from `scripts/brand_colors.py`
3. Apply typography hierarchy and visual principles
4. Validate with quality checklist

### Post-Processing for Brand Fonts

The `html2pptx` workflow only supports web-safe fonts (Arial, etc.). To apply brand fonts after generating a PPTX:

```bash
# Apply Bebas Neue + Inter to an existing PPTX
python .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py input.pptx output.pptx

# Or overwrite the input file
python .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py presentation.pptx
```

**Requirements:**
- `pip install python-pptx`
- Target platform must have Bebas Neue and Inter installed (available free from Google Fonts)

**Troubleshooting:**
If pip fails with "externally-managed-environment" error:
```bash
python3 -m venv venv && source venv/bin/activate && pip install python-pptx
python .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py presentation.pptx
```
