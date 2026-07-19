---
name: icon
description: "Render Lucide icons to branded PNGs. Use standalone for any branded content, or as part of the carousel pipeline for decorative slide accents."
---

# Icon Rendering Skill

Renders Lucide SVG icons to branded PNG files with a configurable stroke colour.

## Workflow

```bash
node .claude/skills/icon/scripts/render-icon.cjs <name> <size> [opacity] [output-dir]
```

**Examples:**
```bash
# Default: 120px, solid colour
node .claude/skills/icon/scripts/render-icon.cjs git-branch 120

# Custom opacity
node .claude/skills/icon/scripts/render-icon.cjs shield 80 0.3

# Custom output directory
node .claude/skills/icon/scripts/render-icon.cjs code 120 1.0 ./output/icons
```

## Constraints

- Max 1 icon per slide
- Carousel size: 120px
- Video size: 80px
- Default opacity: 100% (1.0)
- For reduced opacity, pass a value < 1.0 (pre-baked into RGBA stroke colour since html2pptx drops CSS opacity)
- Position: top-right of content zone (when used in slides)

## Brand Colour

<!-- CUSTOMIZE: Replace with your brand's icon stroke colour -->
`#A8BCCF` (pale steel) — applied as the stroke colour at full opacity by default.

## Icon Catalogue

See [references/icon-catalogue.md](references/icon-catalogue.md) for the curated list of approved icons by topic.

## Integration

Carousel and other presentation skills call this script directly. The script is self-contained and requires only `sharp` and `lucide-static` as npm dependencies.
