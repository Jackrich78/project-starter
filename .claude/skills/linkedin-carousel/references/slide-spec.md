# Carousel Slide Specification

Visual specification for LinkedIn carousel slides. All skills generating carousel content reference this file.

---

## Dimensions

- **PPTX:** 810pt x 1012.5pt (hardcoded, overrides html2pptx 16:9 default)
- **Pixel equivalent:** 1080px x 1350px at 96 DPI (4:5 portrait)
- These values are constants. Do not parameterise.

---

## 3-Zone Layout

All templates use a vertical 3-zone grid:

| Zone | Height | Content |
|------|--------|---------|
| **Top zone** | ~60pt | "PROJECT STARTER" Roboto Medium 18pt + lime accent bar `#B1F208`. |
| **Content zone** | flex:1 (~860pt) | The actual content. Headlines 60pt, body 24pt. All mobile-readable. |
| **Bottom zone** | ~100pt | Thin separator line + handle text + headshot circle (80px), right-aligned. |

### Top Zone

- Text: "PROJECT STARTER" in Roboto Medium 18pt, letter-spacing 3px, text-transform uppercase
- HTML font: `font-family: Arial; font-weight: bold;` (post-processed → Roboto Medium)
- Accent bar: 40px wide, 3px tall, Lime Chartreuse `#B1F208`, inline right of text
- Padding: 15px 80px
- On dark slides: text white, accent bar Lime Chartreuse
- On light slides: text `#1A1A2E`, accent bar Lime Chartreuse

### Bottom Zone

- Thin separator: 1px solid Border Gray `#E5E7EB` (light slides) or rgba(255,255,255,0.2) (dark slides)
- Layout: right-aligned (`justify-content: flex-end`), handle text then headshot
- Headshot: 80px circle, `border-radius: 50%; object-fit: cover;`
- Handle: "@jackrich7" in Roboto Medium 18pt, Medium Gray `#6B7280` (light) or white (dark)
- HTML font: `font-family: Arial; font-weight: bold; font-size: 18pt;` (post-processed → Roboto Medium)
- Padding: 0 80px
- Headshot image: `references/jack_headshot_6_no_bg.png` (relative to skill root)

---

## Colour System

### Dark Slides (Bookends: Slides 1 + 6)

| Element | Value |
|---------|-------|
| Background | Deep Teal `#0D5B65` |
| Headlines | White `#FFFFFF` |
| Body text | White `#FFFFFF` at 90% opacity → `rgba(255,255,255,0.9)` |
| Accent bar (top) | Lime Chartreuse `#B1F208` |
| No geometric shapes | Removed in v3 |

### Light Slides (Content: Slides 2-5)

| Element | Value |
|---------|-------|
| Background | White `#FFFFFF` |
| Headlines | Deep Teal `#0D5B65` |
| Body text | Dark Gray `#374151` |
| Muted text | Medium Gray `#6B7280` |
| Card backgrounds | Mint `#E7FBF6` |
| Card heading text | Very Dark Teal `#0A2F33` |
| Card left borders | 4.8pt, coloured per card (Lavender `#B6A2F1`, Teal Mint `#29C9A5`, Lime `#A4E001`) |
| Pivot line borders | 4.8pt Lavender `#B6A2F1` |
| Whitespace | 40%+ of content zone |

**Forbidden:** `#000000` (pure black), gradients, more than 3 accent colours per slide.

---

## Typography

Mobile-optimised — designed for phone screens in LinkedIn feed.

| Element | Font (HTML) | Post-processed | Size | Colour |
|---------|-------------|----------------|------|--------|
| H1 Hero | Arial Black | Bebas Neue Bold | 60pt | `#FFFFFF` (dark) / `#0D5B65` (light) |
| Sub-headline | Arial Black | Bebas Neue Regular | 30pt | Per slide |
| Pipeline badge | Arial Black bold | Bebas Neue Bold | 26pt | `#FFFFFF` |
| Body text | Arial | Roboto Light | 24pt | `#374151` |
| Body (compact) | Arial | Roboto Light | 22pt | `#374151` |
| Callout/pivot | Arial bold italic | Roboto SemiBold Italic | 24-26pt | `#1A1A2E` |
| CTA body | Arial | Roboto Regular | 24pt | `#FFFFFF` |
| License text | Arial | Roboto Light | 20pt | `#FFFFFF` |
| Top zone label | Arial bold | Roboto Medium | 18pt | `#1A1A2E` / `#FFFFFF` |
| Handle | Arial bold | Roboto Medium | 18pt | `#6B7280` / `#FFFFFF` |
| Card heading | Arial bold | Roboto Medium | 24pt | `#0A2F33` |
| Card body | Arial | Roboto Light | 22pt | `#374151` |

**Minimum readable:** 18pt body, 48pt headlines. Anything below 18pt is invisible on mobile.

---

## Slide Structures

### Slide 1 — Hook (Dark)

- Background: `#0D5B65`
- Large headline: 60pt, white, Bebas Neue
- Subline: 24pt, white at 90% opacity, Roboto Light
- No geometric accent shapes (removed in v3)
- **Template:** `templates/hook-dark.html`

### Slide 2 — Story (Light)

- Background: `#FFFFFF`
- Headline: 60pt, Deep Teal `#0D5B65`
- Body lines: 24pt Roboto Light, stacked with spacing
- Emphasis line: 24pt Roboto Medium (bold)
- Pivot line: 24pt Roboto SemiBold Italic, Lavender `#B6A2F1` left border 4.8pt
- **Template:** `templates/story-light.html`

### Slide 3 — Solution / Benefits (Light)

- Background: `#FFFFFF`
- Headline: 60pt, Deep Teal `#0D5B65`
- Three benefit cards on Mint `#E7FBF6` background with coloured left borders:
  - Card 1: Lavender `#B6A2F1` border ("remembers")
  - Card 2: Teal Mint `#29C9A5` border ("plans")
  - Card 3: Lime `#A4E001` border ("evolves")
- Card heading: 24pt Roboto Medium, Very Dark Teal `#0A2F33`
- Card body: 22pt Roboto Light, Dark Gray `#374151`
- Footer: 22pt Roboto Light, muted
- **Template:** `templates/solution-light.html` or `templates/insight-light.html`

### Slide 4 — Pipeline / How It Works (Light)

- Background: `#FFFFFF`
- Headline: 60pt, Deep Teal `#0D5B65`
- Converging/diverging layout:
  - **Left column (filled badges, narrowing):** Commands cascade from widest to narrowest
    - `/Explore the problem` #0D5B65 width ~4.915"
    - `/blueprint the plan` #B6A2F1 width ~4.155"
    - `/build the tests` #29C9A5 width ~3.415"
    - `/qa the work` #A7EDDD width ~2.730"
    - `/commit it` #A4E001 width ~1.969"
  - **Right column (outlined, expanding):** Artifacts expand from narrowest to widest
    - `prd.md` #0D5B65 border width ~1.969"
    - `plan.md` #B6A2F1 border width ~2.730"
    - `tests + code` #29C9A5 border width ~3.415"
    - `qa-report.md` #A7EDDD border width ~4.155"
    - `changelog + merged` #A4E001 border width ~4.915"
  - Badge text: Bebas Neue Bold 26pt white (font-family: 'Arial Black')
  - Artifact text: Roboto Light 22pt muted
  - Arrows: ↓ 31.7pt muted
  - Outlined borders: 2.2pt
  - Annotations: "Uncertainty fades" (left col), "Understanding builds" (right col)
- **Template:** `templates/visual-light.html`

### Slide 5 — Before/After / Proof (Light)

- Background: `#FFFFFF`
- Headline: 60pt, Deep Teal `#0D5B65`
- Two comparison cards on Mint `#E7FBF6`:
  - "Day 1" card: Lavender `#B6A2F1` left border 4.8pt
  - "Week 2" card: Teal Mint `#29C9A5` left border 4.8pt
- Takeaway line: 24pt Roboto SemiBold Italic, `#1A1A2E`
- **Template:** `templates/beforeafter-light.html`

### Slide 6 — CTA (Dark)

- Background: `#0D5B65`
- Large headline: 60pt, white, Bebas Neue
- Body: 24pt Roboto, white
- License: 20pt Roboto Light, white at 70%
- Comment driver: 24pt Roboto, white at 90%, italic
- No geometric shapes (removed in v3)
- **Template:** `templates/cta-dark.html`

---

## Attribution Rules

- `@jackrich7` — every slide, bottom zone, with headshot circle
- `github.com/jackrich78/project-starter` — Slide 6 only
