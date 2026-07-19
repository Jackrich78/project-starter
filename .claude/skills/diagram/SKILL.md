---
name: diagram
description: "Generate brand-themed diagrams from Mermaid syntax. Outputs SVG/PNG using Mermaid CLI with your brand colours. Use standalone or as part of the carousel pipeline for Slide 3/4 diagrams."
---

# Branded Diagram Generator

## Overview

Generates brand-themed architecture diagrams, flowcharts, and sequence diagrams from Mermaid syntax. Applies your brand colour palette and typography. Can be invoked standalone or by the carousel skill for slide diagrams.

## Prerequisites

- `@mermaid-js/mermaid-cli` (mmdc) — install globally: `npm install -g @mermaid-js/mermaid-cli`
- If not installed, output the Mermaid source and instruct user to render manually.

## Brand Theme

Use the theme config at `mermaid-brand-theme.json` in this directory. Pass to mmdc via `--configFile`.

### Colour Mapping

<!-- CUSTOMIZE: Replace hex values with your brand colours -->
| Mermaid Element | Brand Colour | Hex |
|----------------|-------------|-----|
| Primary node fill | Deep Slate Blue | `#1E3A5F` |
| Primary node text | Off-White | `#F8F9FA` |
| Secondary node fill | Steel Blue | `#6B8FA8` |
| Secondary node text | Off-White | `#F8F9FA` |
| Edge/connector | Steel Blue | `#6B8FA8` |
| Accent/highlight | Blue Accent | `#2E6FD9` |
| Background | Off-White | `#F8F9FA` |
| Label text | Charcoal | `#535250` |

## Workflow

1. **Receive diagram spec** — either Mermaid syntax directly or a text description to convert.
2. **Write Mermaid source** — save to temp file (e.g., `/tmp/diagram.mmd`).
3. **Render with theme** — run:
   ```bash
   mmdc -i /tmp/diagram.mmd -o output.svg --configFile .claude/skills/diagram/mermaid-brand-theme.json -b transparent
   ```
4. **Validate output** — check SVG exists and is non-empty.
5. **Deliver** — move to requested output path or `demos/` folder.

## Standalone Invocation

User provides a diagram description or Mermaid syntax. Output SVG to current directory or specified path.

## Carousel Integration

When invoked by the carousel skill:
1. Receive diagram spec from `carousel-content.md` Slide 3 or 4.
2. Render at appropriate size (max 920px wide for 4:5 carousel, max 480px wide for 16:9 video).
3. Return SVG path for embedding in slide HTML via `<img>` tag.

## Diagram Constraints

- Maximum 5 nodes (legibility on mobile).
- Minimum 18pt label text (matches carousel spec).
- No more than 7 edges.
- If diagram exceeds these limits, simplify or recommend text-only.

## Graceful Degradation

If `mmdc` is not installed:
1. Output the Mermaid source as a fenced code block.
2. Note: "Render with Mermaid CLI (`npm i -g @mermaid-js/mermaid-cli`) or paste into mermaid.live"
3. Do not block the carousel pipeline — proceed with diagram placeholder.

## Quality Gates

- [ ] Diagram renders without errors
- [ ] Brand colours applied (no default Mermaid blue/grey)
- [ ] Max 5 nodes, 7 edges
- [ ] Labels readable at 18pt minimum
- [ ] Background transparent (for slide embedding)
- [ ] SVG output is well-formed
