<!-- CUSTOMIZE: Replace all color values and font names with your brand's specifications -->

# Colors & Typography Reference

Complete brand color palette with contrast ratios and typography specifications.

---

## Color Palette

### Brand Colors (Bold & Saturated)

<!-- CUSTOMIZE: Replace with your brand's primary colors -->
| Name | Hex | RGB | Personality | Use For |
|------|-----|-----|-------------|---------|
| Signal Red | `#E63946` | (230, 57, 70) | Energy, urgency | Primary CTAs, key metrics, brand anchor |
| Royal Blue | `#2563EB` | (37, 99, 235) | Trust, structure | Technical content, frameworks, architecture |
| Emerald | `#10B981` | (16, 185, 129) | Growth, success | Results, benefits, positive indicators |
| Amber | `#F59E0B` | (245, 158, 11) | Attention, warmth | Highlights, warnings, important notes |
| Violet | `#7C3AED` | (124, 58, 237) | Innovation, premium | AI/tech features, differentiation |

**Rule**: Max 2-3 saturated colors per slide or diagram section. These are accents, not backgrounds.

### Text Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Near Black | `#1A1A2E` | (26, 26, 46) | Headings, primary text — all Bebas Neue text |
| Dark Gray | `#374151` | (55, 65, 81) | Body text, paragraphs — default Inter text |
| Medium Gray | `#6B7280` | (107, 114, 128) | Muted text, captions, secondary labels |
| Light Gray | `#9CA3AF` | (156, 163, 175) | Disabled text, subtle annotations |

### Backgrounds

<!-- CUSTOMIZE: Replace with your brand's background colors -->
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| White | `#FFFFFF` | (255, 255, 255) | Primary background — slides, diagrams, docs |
| Cool Gray | `#F3F4F6` | (243, 244, 246) | Alt background — cards, callout boxes |
| Near Black | `#1A1A2E` | (26, 26, 46) | Dark sections, code blocks, evidence artifacts |

### Supporting Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Border Gray | `#E5E7EB` | (229, 231, 235) | Dividers, borders, subtle structure |
| Hover Gray | `#D1D5DB` | (209, 213, 219) | Hover states, disabled elements |

---

## Contrast Ratios (WCAG)

| Combination | Ratio | Level | Notes |
|-------------|-------|-------|-------|
| Near Black (#1A1A2E) on White (#FFFFFF) | ~16.2:1 | AAA | Headings |
| Dark Gray (#374151) on White (#FFFFFF) | ~9.7:1 | AAA | Body text |
| Medium Gray (#6B7280) on White (#FFFFFF) | ~5.2:1 | AA | Muted text |
| Signal Red (#E63946) on White (#FFFFFF) | ~4.6:1 | AA | Accent elements |
| Royal Blue (#2563EB) on White (#FFFFFF) | ~4.8:1 | AA | Accent elements |
| White (#FFFFFF) on Near Black (#1A1A2E) | ~16.2:1 | AAA | Inverted sections |

---

## Typography

### Font Stack

<!-- CUSTOMIZE: Replace font names with your brand fonts -->
| Role | Font | Weight | Google Fonts | Fallback |
|------|------|--------|-------------|----------|
| Display / H1 | Bebas Neue | 400 (only weight — it's bold by design) | [Bebas Neue](https://fonts.google.com/specimen/Bebas+Neue) | Impact, Arial Black, sans-serif |
| H2 | Inter | ExtraBold (800) | [Inter](https://fonts.google.com/specimen/Inter) | Arial, sans-serif |
| H3 | Inter | Bold (700) | Inter | Arial, sans-serif |
| Subtitle | Inter | SemiBold (600) | Inter | Arial, sans-serif |
| Body | Inter | Regular (400) | Inter | Arial, sans-serif |
| Small / Caption | Inter | Medium (500) | Inter | Arial, sans-serif |
| Code | JetBrains Mono | Regular (400) | [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) | Courier New, monospace |

### Size Scale

| Level | Font | Size | Weight | Line Height | Letter Spacing | Color |
|-------|------|------|--------|-------------|----------------|-------|
| H1 Hero | Bebas Neue | 56pt | 400 | 1.0 | 0.02em | `#1A1A2E` |
| H1 | Bebas Neue | 42pt | 400 | 1.05 | 0.02em | `#1A1A2E` |
| H2 | Inter | 28pt | ExtraBold (800) | 1.2 | -0.01em | `#1A1A2E` |
| H3 | Inter | 20pt | Bold (700) | 1.3 | 0 | `#1A1A2E` |
| Subtitle | Inter | 18pt | SemiBold (600) | 1.4 | 0 | `#374151` |
| Body | Inter | 16pt | Regular (400) | 1.6 | 0 | `#374151` |
| Standard | Inter | 14pt | Regular (400) | 1.5 | 0 | `#374151` |
| Small | Inter | 12pt | Regular (400) | 1.4 | 0 | `#6B7280` |
| Caption | Inter | 11pt | Medium (500) | 1.4 | 0.01em | `#6B7280` |
| Big Number | Bebas Neue | 72pt | 400 | 1.0 | 0 | Any brand color |

### Typography Rules

- **Bebas Neue is uppercase-only** — it has no lowercase glyphs. Use it exclusively for short, punchy headlines (5-8 words max)
- **Never mix fonts** in the same text block
- **Inter weight = hierarchy**: Regular (body) < SemiBold (subtitle) < Bold (H3) < ExtraBold (H2)
- **Minimum body size**: 16pt for presentations, 14pt for documents
- **Minimum readable size**: 12pt — anything smaller is invisible to general audiences
- **Line height increases as size decreases**: Big headlines are tight (1.0), body text is open (1.6)

### Pairing Philosophy

The Bebas Neue + Inter pairing works through **extreme contrast**:

- **Bebas Neue**: Tall, narrow, geometric, all-caps — commands attention
- **Inter**: Wide, open, humanist curves, mixed-case — invites reading

The tension between the two creates visual energy. Bebas Neue says "look here." Inter says "now read this." Don't dilute this by using Bebas Neue for too many elements — one or two per page maximum.
