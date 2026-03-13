<!-- CUSTOMIZE: Replace palette values with your brand hex codes -->

# Color Palette & Brand Style

**This is the single source of truth for all colors and brand-specific styles.** To customize diagrams for your own brand, edit this file — everything else in the skill is universal.

---

## Shape Colors (Semantic)

Colors encode meaning, not decoration. Each semantic purpose has a fill/stroke pair.

<!-- CUSTOMIZE: Replace primary/secondary/tertiary/accent hex values with your brand colors -->
| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#6B8FA8` | `#1E3A5F` |
| Secondary | `#EEF1F5` | `#1E3A5F` |
| Tertiary | `#F8F9FA` | `#6B8FA8` |
| Start/Trigger | `#fed7aa` | `#c2410c` |
| End/Success | `#a7f3d0` | `#047857` |
| Warning/Reset | `#fee2e2` | `#dc2626` |
| Decision | `#fef3c7` | `#b45309` |
| AI/LLM | `#ddd6fe` | `#6d28d9` |
| Inactive/Disabled | `#D9D9D9` | `#999999` (use dashed stroke) |
| Error | `#fecaca` | `#b91c1c` |
| Accent/CTA | `#2E6FD9` | `#2E6FD9` |

**Rule**: Always pair a darker stroke with a lighter fill for contrast.

---

## Text Colors (Hierarchy)

Use color on free-floating text to create visual hierarchy without containers.

<!-- CUSTOMIZE: Replace heading/subtitle colors with your brand colors -->
| Level | Color | Use For |
|-------|-------|---------|
| Title | `#1E3A5F` | Section headings, major labels |
| Subtitle | `#6B8FA8` | Subheadings, secondary labels |
| Body/Detail | `#535250` | Descriptions, annotations, metadata |
| On light fills | `#15191B` | Text inside light-colored shapes |
| On dark fills | `#F8F9FA` | Text inside dark-colored shapes |

---

## Evidence Artifact Colors

Used for code snippets, data examples, and other concrete evidence inside technical diagrams.

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#15191B` | Syntax-colored (language-appropriate) |
| JSON/data example | `#15191B` | `#22c55e` (green) |

---

## Default Stroke & Line Colors

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose |
| Structural lines (dividers, trees, timelines) | Primary stroke (`#1E3A5F`) or Gray (`#535250`) |
| Marker dots (fill + stroke) | Primary fill (`#6B8FA8`) |

---

## Background

<!-- CUSTOMIZE: Replace canvas background with your brand background color -->
| Property | Value |
|----------|-------|
| Canvas background | `#F8F9FA` |
