<!-- CUSTOMIZE: Replace all placeholder values with your brand's colors, fonts, and style -->
---
name: brand-guidelines
description: "Apply your brand identity (colors, typography, visual style) to presentations, documents, reports, and marketing materials. Use when creating or styling any branded content. Provides color palette, typography hierarchy, visual style principles, and technical implementation code."
---

# Brand Guidelines

<!-- CUSTOMIZE: Replace "Your Brand" with your organization name -->
Apply your brand identity to any branded content.

## Quick Reference

<!-- CUSTOMIZE: Replace all hex values with your brand colors -->
**Core Colors:**
- Primary: `#1E3A5F` (headings, brand identity) — Deep Slate Blue
- Background: `#F8F9FA` (primary background) — Off-White
- Secondary: `#6B8FA8` (accents, supporting elements) — Steel Blue
- Body: `#535250` (body text) — Charcoal
- Accent: `#2E6FD9` (CTAs - use sparingly, max 2-3 per page) — Blue Accent

<!-- CUSTOMIZE: Replace with your brand fonts -->
**Typography:**
- Headings: Your Heading Font (36pt/24pt/18pt)
- Body: Your Body Font (16pt/14pt/12pt)
- Fallback: Arial, sans-serif

**Core Principles:**
- Professional & Trustworthy (high contrast, clean layouts)
- Clear Hierarchy (consistent heading/body/accent usage)
- Systems Thinking (show connections, flows, architecture)
- Authentic (real screenshots, actual examples)

## Color Combinations

**Most Common Patterns:**

1. **Primary headings on background** → `#1E3A5F` text on `#F8F9FA` background
2. **Body text on background** → `#535250` text on `#F8F9FA` background
3. **Secondary accents on background** → `#6B8FA8` elements on `#F8F9FA` background

**Emphasis:**
- Accent on background (sparingly) → `#2E6FD9` on `#F8F9FA`
- Light text on primary (high impact) → `#F8F9FA` text on `#1E3A5F` background

**Forbidden:**
- Light text on light backgrounds
- Secondary text on primary background (low contrast)
- Multiple accent colors on same slide
- Pure black (#000000) — use primary or body color instead

## Typography Rules

<!-- CUSTOMIZE: Replace font names and sizes with your brand's typography -->
**Font Hierarchy:**
- **Your Heading Font** for all headings (H1/H2/H3)
- **Your Body Font** for all body text and paragraphs
- **Arial** fallback when brand fonts unavailable

**Size Scale:**
- H1 Hero: 46pt | H1: 36pt | H2: 24pt | H3: 18pt
- Body: 16pt | Standard: 14pt | Small: 12pt | Caption: 11pt

**Rules:**
- Never mix fonts in same text block
- Maintain 1.4-1.6 line height for body text
- Minimum 24pt for text in social media images

## Visual Style Principles

**1. Professional & Trustworthy**
- High contrast (WCAG AA: 4.5:1 minimum)
- Clean, grid-based layouts
- Real data and authentic examples

**2. Clear Hierarchy**
- Consistent heading/body/accent usage
- Size and weight create visual hierarchy
- Generous white space

**3. Systems Thinking**
- Show connections with arrows and flow diagrams
- Visual flows (left-to-right, top-to-bottom)
- Architecture diagrams showing relationships

## Resources

**Detailed specifications:**
- See [colors-and-typography.md](references/colors-and-typography.md) for complete color palette with RGB values and contrast ratios
- See [technical-implementation.md](references/technical-implementation.md) for CSS variables, Python-PPTX code, and implementation snippets

**Scripts:**
- `scripts/brand_colors.py` — Python constants for all brand colors (RGB and hex)
- `scripts/apply_brand_fonts.py` — Font post-processor for PPTX files

**Extending this skill:**
- Add an `assets/` directory for logos and brand imagery
- Add a `references/slide-examples/` directory with example slide screenshots
- Add a `references/visual-examples.md` for layout patterns

## Quality Checklist

Before finalizing branded content:
- [ ] Text meets WCAG AA contrast (4.5:1 minimum)
- [ ] Primary color for headings, body color for text
- [ ] Correct background color (not pure white)
- [ ] Accent color used sparingly (max 2-3 elements)
- [ ] Correct fonts for headings vs body
- [ ] Font sizes follow hierarchy
- [ ] Generous white space, not overcrowded

## Application by Content Type

<!-- CUSTOMIZE: Adjust colors and fonts for each content type -->
**PowerPoint/Slides:**
- Title: 46pt Heading Font `#6B8FA8` or `#1E3A5F`
- Content heading: 36pt Heading Font `#1E3A5F`
- Body: 16pt Body Font `#535250`
- Background: `#F8F9FA` or `#EEF1F5`
- Bullets: `#6B8FA8`

**Documents/Reports:**
- H1: 36pt Heading Font `#1E3A5F`
- H2: 24pt Heading Font `#1E3A5F`
- H3: 18pt Heading Font `#1E3A5F`
- Body: 14pt Body Font `#535250`
- Background: White or `#F8F9FA`

## Integration with PPTX Skill

When used with PPTX generation:
1. Load this skill first to establish brand context
2. Use color constants from `scripts/brand_colors.py`
3. Apply typography hierarchy and visual principles
4. Validate with quality checklist

### Post-Processing for Brand Fonts

The `html2pptx` workflow only supports web-safe fonts (Arial, etc.). To apply brand fonts after generating a PPTX:

```bash
# Apply brand fonts to an existing PPTX
python .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py input.pptx output.pptx

# Or overwrite the input file
python .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py presentation.pptx
```

**Requirements:**
- `pip install python-pptx`
- Target platform must have your brand fonts installed

**Troubleshooting:**
If pip fails with "externally-managed-environment" error:
```bash
python3 -m venv venv && source venv/bin/activate && pip install python-pptx
python .claude/skills/brand-guidelines/scripts/apply_brand_fonts.py presentation.pptx
```
