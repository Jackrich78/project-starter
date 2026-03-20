<!-- CUSTOMIZE: Replace all color values and font names with your brand's specifications -->

# Colors & Typography Reference

Complete brand color palette with contrast ratios and typography specifications.

---

## Color Palette

### Brand Colors (Teal-Based Nature Palette)

<!-- CUSTOMIZE: Replace with your brand's primary colors -->
| Name | Hex | RGB | Personality | Use For |
|------|-----|-----|-------------|---------|
| Deep Teal | `#0D5B65` | (13, 91, 101) | Depth, trust, nature | Dark backgrounds, headline text on light slides |
| Very Dark Teal | `#0A2F33` | (10, 47, 51) | Authority, grounding | Card heading text |
| Lime Chartreuse | `#B1F208` | (177, 242, 8) | Energy, freshness | Top accent bar, primary brand accent |
| Lavender | `#B6A2F1` | (182, 162, 241) | Creativity, calm | Card borders ("remembers"), pivot lines |
| Teal Mint | `#29C9A5` | (41, 201, 165) | Growth, progress | Card borders ("plans"), positive indicators |
| Light Mint | `#A7EDDD` | (167, 237, 221) | Clarity, lightness | Card borders (QA step), lighter teal variant |
| Lime Green | `#A4E001` | (164, 224, 1) | Action, completion | Card borders ("evolves", commit step) |

**Rule**: Max 2-3 accent colours per slide or diagram section. These are accents, not backgrounds.

### Text Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Near Black | `#1A1A2E` | (26, 26, 46) | Callout text, emphasis — bold italic Roboto |
| Deep Teal | `#0D5B65` | (13, 91, 101) | Headings on light backgrounds — all Bebas Neue text on light slides |
| Very Dark Teal | `#0A2F33` | (10, 47, 51) | Card headings — Roboto Medium on card blocks |
| Dark Gray | `#374151` | (55, 65, 81) | Body text, paragraphs — default Roboto text |
| Medium Gray | `#6B7280` | (107, 114, 128) | Muted text, captions, handles, secondary labels |
| Light Gray | `#9CA3AF` | (156, 163, 175) | Disabled text, subtle annotations |

### Backgrounds

<!-- CUSTOMIZE: Replace with your brand's background colors -->
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| White | `#FFFFFF` | (255, 255, 255) | Primary background — slides, diagrams, docs |
| Mint | `#E7FBF6` | (231, 251, 246) | Card/block background — benefit cards, comparison blocks |
| Deep Teal | `#0D5B65` | (13, 91, 101) | Dark sections, bookend slides (1 + 6) |

### Supporting Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Border Gray | `#E5E7EB` | (229, 231, 235) | Dividers, borders, subtle structure |
| Hover Gray | `#D1D5DB` | (209, 213, 219) | Hover states, disabled elements |

---

## Contrast Ratios (WCAG)

| Combination | Ratio | Level | Notes |
|-------------|-------|-------|-------|
| Deep Teal (#0D5B65) on White (#FFFFFF) | ~7.5:1 | AAA | Headings on light slides |
| Very Dark Teal (#0A2F33) on Mint (#E7FBF6) | ~11.8:1 | AAA | Card headings |
| Dark Gray (#374151) on White (#FFFFFF) | ~9.7:1 | AAA | Body text |
| Medium Gray (#6B7280) on White (#FFFFFF) | ~5.2:1 | AA | Muted text |
| White (#FFFFFF) on Deep Teal (#0D5B65) | ~7.5:1 | AAA | Dark slide text |
| Lime Chartreuse (#B1F208) on Deep Teal (#0D5B65) | ~8.2:1 | AAA | Accent bar on dark |

---

## Typography

### Font Stack

<!-- CUSTOMIZE: Replace font names with your brand fonts -->
| Role | Font | Weight | Google Fonts | Fallback |
|------|------|--------|-------------|----------|
| Display / H1 | Bebas Neue | Bold | [Bebas Neue](https://fonts.google.com/specimen/Bebas+Neue) | Impact, Arial Black, sans-serif |
| Sub-headline | Bebas Neue | Regular | Bebas Neue | Impact, Arial Black, sans-serif |
| Body | Roboto Light | 300 | [Roboto](https://fonts.google.com/specimen/Roboto) | Arial, sans-serif |
| Body (emphasis) | Roboto Medium | 500 | Roboto | Arial, sans-serif |
| Callout / Pivot | Roboto SemiBold | 600 Italic | Roboto | Arial, sans-serif |
| Small / Label | Roboto Medium | 500 | Roboto | Arial, sans-serif |
| Code | JetBrains Mono | Regular (400) | [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) | Courier New, monospace |

### Size Scale

| Level | Font | Size | Weight | Line Height | Letter Spacing | Color |
|-------|------|------|--------|-------------|----------------|-------|
| H1 Hero | Bebas Neue | 60pt | Bold | 1.0 | 0.02em | `#0D5B65` (light) / `#FFFFFF` (dark) |
| Sub-headline | Bebas Neue | 30pt | Regular | 1.1 | 0.02em | Per slide |
| Pipeline badge | Bebas Neue | 26pt | Bold | 1.0 | 0 | `#FFFFFF` |
| Body | Roboto Light | 24pt | 300 | 1.4 | 0 | `#374151` |
| Body (compact) | Roboto Light | 22pt | 300 | 1.4 | 0 | `#374151` |
| Callout | Roboto SemiBold | 24-26pt | 600 Italic | 1.4 | 0 | `#1A1A2E` |
| Card heading | Roboto Medium | 24pt | 500 | 1.3 | 0 | `#0A2F33` |
| Card body | Roboto Light | 22pt | 300 | 1.4 | 0 | `#374151` |
| License | Roboto Light | 20pt | 300 | 1.4 | 0 | `#FFFFFF` 70% |
| Top bar / Handle | Roboto Medium | 18pt | 500 | 1.4 | 3px | `#1A1A2E` / `#FFFFFF` |

### Typography Rules

- **Bebas Neue is uppercase-only** — it has no lowercase glyphs. Use it exclusively for short, punchy headlines (5-8 words max)
- **Never mix fonts** in the same text block
- **Roboto weight = hierarchy**: Light (body) < Medium (labels, emphasis) < SemiBold Italic (callouts)
- **Minimum body size**: 20pt for presentations, 14pt for documents
- **Minimum readable size**: 18pt — anything smaller is invisible on mobile
- **Line height increases as size decreases**: Big headlines are tight (1.0), body text is open (1.4)

### Pairing Philosophy

The Bebas Neue + Roboto pairing works through **extreme contrast**:

- **Bebas Neue**: Tall, narrow, geometric, all-caps — commands attention
- **Roboto**: Clean, neutral, versatile weight range — invites reading

The tension between the two creates visual energy. Bebas Neue says "look here." Roboto says "now read this." Don't dilute this by using Bebas Neue for too many elements — one or two per page maximum.

### Font Post-Processor Mapping

The `apply_brand_fonts.py` script maps HTML placeholder fonts to brand fonts:

| HTML Font | Condition | Maps To |
|-----------|-----------|---------|
| `Arial Black` | Any | Bebas Neue |
| `Arial` | bold + italic | Roboto SemiBold (clears bold, keeps italic) |
| `Arial` | bold only | Roboto Medium (clears bold) |
| `Arial` | normal, ≤18pt | Roboto Medium |
| `Arial` | normal, >18pt | Roboto Light |
| `Courier` / `Mono` | Any | JetBrains Mono |
