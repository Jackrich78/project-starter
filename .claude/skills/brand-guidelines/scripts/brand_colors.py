"""
Brand Colors — Bold Geometry Palette
-------------------------------------
<!-- CUSTOMIZE: Replace all color values with your brand colors -->

Ready-to-use color constants for Python applications.

Usage with python-pptx:
    from brand_colors import BrandColors
    shape.fill.fore_color.rgb = BrandColors.RED

Usage as hex strings:
    from brand_colors import HexColors
    css_color = HexColors.RED  # '#E63946'
"""

try:
    from pptx.dml.color import RGBColor
    _HAS_PPTX = True
except ImportError:
    _HAS_PPTX = False


# CUSTOMIZE: Replace hex values with your brand colors
class HexColors:
    """Brand colors as hex strings"""
    # Brand Colors (Bold & Saturated)
    RED = '#E63946'
    BLUE = '#2563EB'
    GREEN = '#10B981'
    AMBER = '#F59E0B'
    VIOLET = '#7C3AED'

    # Text Colors
    TEXT_HEADING = '#1A1A2E'
    TEXT_BODY = '#374151'
    TEXT_MUTED = '#6B7280'
    TEXT_LIGHT = '#9CA3AF'

    # Backgrounds
    BG_WHITE = '#FFFFFF'
    BG_ALT = '#F3F4F6'
    BG_DARK = '#1A1A2E'

    # Borders & Supporting
    BORDER = '#E5E7EB'
    BORDER_HOVER = '#D1D5DB'

    # Legacy aliases (for backward compatibility)
    PRIMARY = RED
    SECONDARY = BLUE
    ACCENT = RED
    BACKGROUND = BG_WHITE
    BODY_TEXT = TEXT_BODY
    TEXT_PRIMARY = TEXT_HEADING
    ALT_DARK = BG_DARK
    BG_PRIMARY = BG_WHITE
    GRAY_MEDIUM = TEXT_MUTED
    GRAY_LIGHT = BORDER


# CUSTOMIZE: Replace RGB tuples with your brand colors
class RGBColors:
    """Brand colors as RGB tuples (r, g, b)"""
    # Brand Colors (Bold & Saturated)
    RED = (230, 57, 70)
    BLUE = (37, 99, 235)
    GREEN = (16, 185, 129)
    AMBER = (245, 158, 11)
    VIOLET = (124, 58, 237)

    # Text Colors
    TEXT_HEADING = (26, 26, 46)
    TEXT_BODY = (55, 65, 81)
    TEXT_MUTED = (107, 114, 128)
    TEXT_LIGHT = (156, 163, 175)

    # Backgrounds
    BG_WHITE = (255, 255, 255)
    BG_ALT = (243, 244, 246)
    BG_DARK = (26, 26, 46)

    # Borders & Supporting
    BORDER = (229, 231, 235)
    BORDER_HOVER = (209, 213, 219)

    # Legacy aliases
    PRIMARY = RED
    SECONDARY = BLUE
    ACCENT = RED
    BACKGROUND = BG_WHITE
    BODY_TEXT = TEXT_BODY
    TEXT_PRIMARY = TEXT_HEADING
    ALT_DARK = BG_DARK
    BG_PRIMARY = BG_WHITE
    GRAY_MEDIUM = TEXT_MUTED
    GRAY_LIGHT = BORDER


if _HAS_PPTX:
    class BrandColors:
        """Brand colors as python-pptx RGBColor objects"""
        # Brand Colors (Bold & Saturated)
        RED = RGBColor(230, 57, 70)
        BLUE = RGBColor(37, 99, 235)
        GREEN = RGBColor(16, 185, 129)
        AMBER = RGBColor(245, 158, 11)
        VIOLET = RGBColor(124, 58, 237)

        # Text Colors
        TEXT_HEADING = RGBColor(26, 26, 46)
        TEXT_BODY = RGBColor(55, 65, 81)
        TEXT_MUTED = RGBColor(107, 114, 128)
        TEXT_LIGHT = RGBColor(156, 163, 175)

        # Backgrounds
        BG_WHITE = RGBColor(255, 255, 255)
        BG_ALT = RGBColor(243, 244, 246)
        BG_DARK = RGBColor(26, 26, 46)

        # Borders & Supporting
        BORDER = RGBColor(229, 231, 235)
        BORDER_HOVER = RGBColor(209, 213, 219)

        # Legacy aliases
        PRIMARY = RED
        SECONDARY = BLUE
        ACCENT = RED
        BACKGROUND = BG_WHITE
        BODY_TEXT = TEXT_BODY
        TEXT_PRIMARY = TEXT_HEADING
        ALT_DARK = BG_DARK
        BG_PRIMARY = BG_WHITE
        GRAY_MEDIUM = TEXT_MUTED
        GRAY_LIGHT = BORDER
else:
    # Fallback when python-pptx not installed
    BrandColors = RGBColors


# Quick reference dictionary
COLOR_REFERENCE = {
    'brand': {
        'red': {'hex': '#E63946', 'rgb': (230, 57, 70), 'use': 'CTAs, key metrics, brand anchor'},
        'blue': {'hex': '#2563EB', 'rgb': (37, 99, 235), 'use': 'Technical content, frameworks'},
        'green': {'hex': '#10B981', 'rgb': (16, 185, 129), 'use': 'Results, benefits, positive'},
        'amber': {'hex': '#F59E0B', 'rgb': (245, 158, 11), 'use': 'Highlights, warnings'},
        'violet': {'hex': '#7C3AED', 'rgb': (124, 58, 237), 'use': 'Innovation, AI, premium'},
    },
    'text': {
        'heading': {'hex': '#1A1A2E', 'rgb': (26, 26, 46)},
        'body': {'hex': '#374151', 'rgb': (55, 65, 81)},
        'muted': {'hex': '#6B7280', 'rgb': (107, 114, 128)},
        'light': {'hex': '#9CA3AF', 'rgb': (156, 163, 175)},
    },
    'background': {
        'white': {'hex': '#FFFFFF', 'rgb': (255, 255, 255)},
        'alt': {'hex': '#F3F4F6', 'rgb': (243, 244, 246)},
        'dark': {'hex': '#1A1A2E', 'rgb': (26, 26, 46)},
    },
}


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    """Convert RGB tuple to hex color string"""
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)


if __name__ == '__main__':
    print("Brand Colors — Bold Geometry Palette")
    print("=" * 50)
    print("\nBrand Colors:")
    print(f"  Signal Red:  {HexColors.RED} {RGBColors.RED}")
    print(f"  Royal Blue:  {HexColors.BLUE} {RGBColors.BLUE}")
    print(f"  Emerald:     {HexColors.GREEN} {RGBColors.GREEN}")
    print(f"  Amber:       {HexColors.AMBER} {RGBColors.AMBER}")
    print(f"  Violet:      {HexColors.VIOLET} {RGBColors.VIOLET}")

    print("\nText Colors:")
    print(f"  Heading: {HexColors.TEXT_HEADING} {RGBColors.TEXT_HEADING}")
    print(f"  Body:    {HexColors.TEXT_BODY} {RGBColors.TEXT_BODY}")
    print(f"  Muted:   {HexColors.TEXT_MUTED} {RGBColors.TEXT_MUTED}")
    print(f"  Light:   {HexColors.TEXT_LIGHT} {RGBColors.TEXT_LIGHT}")

    print("\nBackgrounds:")
    print(f"  White: {HexColors.BG_WHITE} {RGBColors.BG_WHITE}")
    print(f"  Alt:   {HexColors.BG_ALT} {RGBColors.BG_ALT}")
    print(f"  Dark:  {HexColors.BG_DARK} {RGBColors.BG_DARK}")
