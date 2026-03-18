#!/usr/bin/env python3
"""
Apply brand fonts to a PPTX presentation.

<!-- CUSTOMIZE: Replace font names with your brand fonts -->

This script post-processes a PPTX file to apply brand typography:
- Bebas Neue for display headings (>=24pt)
- Inter for body text (<24pt)
- JetBrains Mono for code/commands (replaces Courier New)

It also adjusts text frames to prevent wrapping issues when fonts change.

Usage:
    python apply_brand_fonts.py input.pptx output.pptx

Dependencies:
    pip install python-pptx
"""

import sys
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.enum.text import MSO_AUTO_SIZE

# CUSTOMIZE: Replace with your brand fonts
FONT_DISPLAY = "Bebas Neue"
FONT_BODY = "Inter"
FONT_CODE = "JetBrains Mono"

# Threshold for display vs body (in points)
# Bebas Neue for H1 (42pt+), Inter for everything below
DISPLAY_THRESHOLD_PT = 24

# Width expansion factor for text boxes (Bebas Neue is narrower than Arial,
# Inter is similar width — modest expansion handles edge cases)
WIDTH_EXPANSION = 1.05


def apply_brand_fonts(input_path, output_path):
    """Apply brand fonts to all text in the presentation."""
    prs = Presentation(input_path)

    stats = {"display": 0, "body": 0, "code": 0}

    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if not hasattr(shape, 'text_frame'):
                continue

            tf = shape.text_frame
            has_display = False
            has_code = False

            # First pass: identify content type and apply fonts
            for para in tf.paragraphs:
                for run in para.runs:
                    if not run.text.strip():
                        continue

                    current_font = run.font.name or ""
                    font_size = run.font.size

                    # Handle monospace/code fonts
                    if "Courier" in current_font or "Mono" in current_font:
                        run.font.name = FONT_CODE
                        stats["code"] += 1
                        has_code = True
                        continue

                    # Determine target font based on size
                    size_pt = font_size.pt if font_size else 14
                    if size_pt >= DISPLAY_THRESHOLD_PT:
                        run.font.name = FONT_DISPLAY
                        stats["display"] += 1
                        has_display = True
                    else:
                        run.font.name = FONT_BODY
                        stats["body"] += 1

            # Second pass: adjust text frame settings
            if has_display:
                # For display headings: disable word wrap, let shape expand
                tf.word_wrap = False
                tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

            # Expand text box width slightly for all shapes
            if shape.width:
                try:
                    new_width = int(shape.width * WIDTH_EXPANSION)
                    # Keep centered by adjusting left position
                    width_delta = new_width - shape.width
                    shape.left = shape.left - int(width_delta / 2)
                    shape.width = new_width
                except Exception:
                    pass  # Some shapes may not allow width changes

    prs.save(output_path)

    print(f"Brand fonts applied:")
    print(f"  Display ({FONT_DISPLAY}): {stats['display']}")
    print(f"  Body ({FONT_BODY}): {stats['body']}")
    print(f"  Code ({FONT_CODE}): {stats['code']}")
    print(f"\nSaved to: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_brand_fonts.py input.pptx [output.pptx]")
        print("\nIf output not specified, overwrites input file.")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    apply_brand_fonts(input_path, output_path)


if __name__ == "__main__":
    main()
