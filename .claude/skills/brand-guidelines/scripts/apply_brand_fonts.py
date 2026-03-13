#!/usr/bin/env python3
"""
Apply brand fonts to a PPTX presentation.

<!-- CUSTOMIZE: Replace font names with your brand fonts -->

This script post-processes a PPTX file to apply brand typography:
- Your Heading Font for headings (>=18pt)
- Your Body Font for body text (<18pt)
- Your Mono Font for code/commands (replaces Courier New)

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
FONT_HEADING = "Your Heading Font"
FONT_BODY = "Your Body Font"
FONT_CODE = "Your Mono Font"  # e.g., Roboto Mono, Fira Code, JetBrains Mono

# Threshold for heading vs body (in points)
HEADING_THRESHOLD_PT = 18

# Width expansion factor for text boxes (adjust if your fonts are wider/narrower than Arial)
WIDTH_EXPANSION = 1.08


def apply_brand_fonts(input_path, output_path):
    """Apply brand fonts to all text in the presentation."""
    prs = Presentation(input_path)

    stats = {"heading": 0, "body": 0, "code": 0}

    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if not hasattr(shape, 'text_frame'):
                continue

            tf = shape.text_frame
            has_heading = False
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
                    if size_pt >= HEADING_THRESHOLD_PT:
                        run.font.name = FONT_HEADING
                        stats["heading"] += 1
                        has_heading = True
                    else:
                        run.font.name = FONT_BODY
                        stats["body"] += 1

            # Second pass: adjust text frame settings
            if has_heading:
                # For headings: disable word wrap, let shape expand
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
    print(f"  Headings ({FONT_HEADING}): {stats['heading']}")
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
