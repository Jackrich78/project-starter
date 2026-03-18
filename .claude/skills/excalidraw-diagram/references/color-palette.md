<!-- CUSTOMIZE: Replace palette values with your brand hex codes -->

# Color Palette & Brand Style

**This is the single source of truth for all colors and brand-specific styles.** To customize diagrams for your own brand, edit this file — everything else in the skill is universal.

These colors are derived from the brand guidelines skill. If you update brand colors there, update them here too.

---

## Shape Colors (Semantic)

Colors encode meaning, not decoration. Each semantic purpose has a fill/stroke pair.

<!-- CUSTOMIZE: Replace primary/secondary/tertiary/accent hex values with your brand colors -->
| Semantic Purpose | Fill | Stroke | Notes |
|------------------|------|--------|-------|
| Primary/Neutral | `#DBEAFE` | `#2563EB` | Royal Blue tint — structure, frameworks |
| Secondary | `#F3F4F6` | `#374151` | Cool Gray — supporting elements |
| Tertiary | `#F3F4F6` | `#6B7280` | Lighter — background context |
| Start/Trigger | `#FEE2E2` | `#E63946` | Signal Red tint — entry points, triggers |
| End/Success | `#D1FAE5` | `#10B981` | Emerald tint — outcomes, results |
| Warning/Caution | `#FEF3C7` | `#F59E0B` | Amber tint — attention, warnings |
| Decision | `#FEF3C7` | `#F59E0B` | Amber tint — choices, branching |
| AI/LLM | `#EDE9FE` | `#7C3AED` | Violet tint — AI, innovation |
| Inactive/Disabled | `#E5E7EB` | `#9CA3AF` (use dashed stroke) | Gray — disabled states |
| Error | `#FEE2E2` | `#E63946` | Signal Red tint — error states |
| Accent/CTA | `#E63946` | `#E63946` | Signal Red solid — key actions |

**Rules**:
- Always pair a lighter tint fill with a saturated stroke for contrast
- Max 3-4 semantic colors per diagram section
- Use overlapping shapes at section boundaries for visual depth (solid fills — no transparency needed)

---

## Text Colors (Hierarchy)

Use color on free-floating text to create visual hierarchy without containers.

<!-- CUSTOMIZE: Replace heading/subtitle colors with your brand colors -->
| Level | Color | Use For |
|-------|-------|---------|
| Title | `#1A1A2E` | Section headings, major labels (Near Black) |
| Subtitle | `#374151` | Subheadings, secondary labels (Dark Gray) |
| Body/Detail | `#6B7280` | Descriptions, annotations, metadata (Medium Gray) |
| On light fills | `#1A1A2E` | Text inside light-colored shapes |
| On dark fills | `#FFFFFF` | Text inside dark-colored shapes |

---

## Evidence Artifact Colors

Used for code snippets, data examples, and other concrete evidence inside technical diagrams.

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#1A1A2E` | Syntax-colored (language-appropriate) |
| JSON/data example | `#1A1A2E` | `#10B981` (Emerald) |

---

## Default Stroke & Line Colors

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose |
| Structural lines (dividers, trees, timelines) | `#374151` (Dark Gray) or `#1A1A2E` (Near Black) |
| Marker dots (fill + stroke) | `#2563EB` (Royal Blue) |

---

## Background

<!-- CUSTOMIZE: Replace canvas background with your brand background color -->
| Property | Value |
|----------|-------|
| Canvas background | `#FFFFFF` |

---

## Overlapping Elements

A signature technique from the brand guidelines. In diagrams:

- Overlap shapes at section transitions (20-30% overlap)
- Use different semantic colors for overlapping shapes
- Solid fills — Excalidraw doesn't support transparency, but the overlap itself creates visual depth
- Works especially well for showing integration points between systems
