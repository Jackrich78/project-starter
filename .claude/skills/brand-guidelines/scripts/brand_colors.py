"""
Brand Colors — Neutral Starter Palette
---------------------------------------
<!-- CUSTOMIZE: Replace all color values with your brand colors -->

Ready-to-use color constants for Python applications.

Usage with python-pptx:
    from brand_colors import BrandColors
    shape.fill.fore_color.rgb = BrandColors.PRIMARY

Usage as hex strings:
    from brand_colors import HexColors
    css_color = HexColors.PRIMARY  # '#1E3A5F'
"""

try:
    from pptx.dml.color import RGBColor
    _HAS_PPTX = True
except ImportError:
    _HAS_PPTX = False


# CUSTOMIZE: Replace hex values with your brand colors
class HexColors:
    """Brand colors as hex strings"""
    # Primary Colors
    PRIMARY = '#1E3A5F'
    BACKGROUND = '#F8F9FA'
    SECONDARY = '#6B8FA8'

    # Text Colors
    TEXT_PRIMARY = '#1E3A5F'
    BODY_TEXT = '#535250'
    ALT_DARK = '#15191B'
    TEXT_MUTED = '#B7B7B7'

    # Accent
    ACCENT = '#2E6FD9'

    # Backgrounds
    BG_PRIMARY = '#F8F9FA'
    BG_ALT = '#EEF1F5'
    BG_DARK = '#15191B'

    # Supporting Grays
    GRAY_MEDIUM = '#B7B7B7'
    GRAY_LIGHT = '#D9D9D9'


# CUSTOMIZE: Replace RGB tuples with your brand colors
class RGBColors:
    """Brand colors as RGB tuples (r, g, b)"""
    # Primary Colors
    PRIMARY = (30, 58, 95)
    BACKGROUND = (248, 249, 250)
    SECONDARY = (107, 143, 168)

    # Text Colors
    TEXT_PRIMARY = (30, 58, 95)
    BODY_TEXT = (83, 82, 80)
    ALT_DARK = (21, 25, 27)
    TEXT_MUTED = (183, 183, 183)

    # Accent
    ACCENT = (46, 111, 217)

    # Backgrounds
    BG_PRIMARY = (248, 249, 250)
    BG_ALT = (238, 241, 245)
    BG_DARK = (21, 25, 27)

    # Supporting Grays
    GRAY_MEDIUM = (183, 183, 183)
    GRAY_LIGHT = (217, 217, 217)


if _HAS_PPTX:
    class BrandColors:
        """Brand colors as python-pptx RGBColor objects"""
        # Primary Colors
        PRIMARY = RGBColor(30, 58, 95)
        BACKGROUND = RGBColor(248, 249, 250)
        SECONDARY = RGBColor(107, 143, 168)

        # Text Colors
        TEXT_PRIMARY = RGBColor(30, 58, 95)
        BODY_TEXT = RGBColor(83, 82, 80)
        ALT_DARK = RGBColor(21, 25, 27)
        TEXT_MUTED = RGBColor(183, 183, 183)

        # Accent
        ACCENT = RGBColor(46, 111, 217)

        # Backgrounds
        BG_PRIMARY = RGBColor(248, 249, 250)
        BG_ALT = RGBColor(238, 241, 245)
        BG_DARK = RGBColor(21, 25, 27)

        # Supporting Grays
        GRAY_MEDIUM = RGBColor(183, 183, 183)
        GRAY_LIGHT = RGBColor(217, 217, 217)
else:
    # Fallback when python-pptx not installed
    BrandColors = RGBColors


# Quick reference dictionary
COLOR_REFERENCE = {
    'primary': {
        'primary': {'hex': '#1E3A5F', 'rgb': (30, 58, 95)},
        'background': {'hex': '#F8F9FA', 'rgb': (248, 249, 250)},
        'secondary': {'hex': '#6B8FA8', 'rgb': (107, 143, 168)},
    },
    'text': {
        'primary': {'hex': '#1E3A5F', 'rgb': (30, 58, 95)},
        'body': {'hex': '#535250', 'rgb': (83, 82, 80)},
        'alt-dark': {'hex': '#15191B', 'rgb': (21, 25, 27)},
        'muted': {'hex': '#B7B7B7', 'rgb': (183, 183, 183)},
    },
    'accent': {
        'accent': {'hex': '#2E6FD9', 'rgb': (46, 111, 217)},
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
    print("Brand Colors — Neutral Starter Palette")
    print("=" * 50)
    print("\nPrimary Colors:")
    print(f"  Primary:    {HexColors.PRIMARY} {RGBColors.PRIMARY}")
    print(f"  Background: {HexColors.BACKGROUND} {RGBColors.BACKGROUND}")
    print(f"  Secondary:  {HexColors.SECONDARY} {RGBColors.SECONDARY}")

    print("\nText Colors:")
    print(f"  Primary: {HexColors.TEXT_PRIMARY} {RGBColors.TEXT_PRIMARY}")
    print(f"  Body:    {HexColors.BODY_TEXT} {RGBColors.BODY_TEXT}")
    print(f"  Alt:     {HexColors.ALT_DARK} {RGBColors.ALT_DARK}")
    print(f"  Muted:   {HexColors.TEXT_MUTED} {RGBColors.TEXT_MUTED}")

    print("\nAccent:")
    print(f"  Accent:  {HexColors.ACCENT} {RGBColors.ACCENT}")

    print("\nBackgrounds:")
    print(f"  Primary: {HexColors.BG_PRIMARY} {RGBColors.BG_PRIMARY}")
    print(f"  Alt:     {HexColors.BG_ALT} {RGBColors.BG_ALT}")
    print(f"  Dark:    {HexColors.BG_DARK} {RGBColors.BG_DARK}")
