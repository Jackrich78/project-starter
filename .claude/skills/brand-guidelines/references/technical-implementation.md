<!-- CUSTOMIZE: Replace all color values, font names, and variable values with your brand's specifications -->

# Technical Implementation

Code snippets for applying brand colors and typography across different platforms.

## CSS Variables

```css
/* CUSTOMIZE: Replace values with your brand colors and fonts */
:root {
  /* Brand Colors (Bold & Saturated) */
  --brand-red: #E63946;
  --brand-blue: #2563EB;
  --brand-green: #10B981;
  --brand-amber: #F59E0B;
  --brand-violet: #7C3AED;

  /* Text Colors */
  --brand-text-heading: #1A1A2E;
  --brand-text-body: #374151;
  --brand-text-muted: #6B7280;
  --brand-text-light: #9CA3AF;

  /* Backgrounds */
  --brand-bg: #FFFFFF;
  --brand-bg-alt: #F3F4F6;
  --brand-bg-dark: #1A1A2E;

  /* Borders */
  --brand-border: #E5E7EB;
  --brand-border-hover: #D1D5DB;

  /* Typography */
  --brand-font-display: 'Bebas Neue', Impact, 'Arial Black', sans-serif;
  --brand-font-body: 'Inter', Arial, sans-serif;
  --brand-font-mono: 'JetBrains Mono', 'Courier New', monospace;
}

/* Display headings — Bebas Neue */
h1 {
  font-family: var(--brand-font-display);
  color: var(--brand-text-heading);
  font-size: 42pt;
  font-weight: 400;
  letter-spacing: 0.02em;
  line-height: 1.05;
  text-transform: uppercase;
}

/* Sub-headings — Inter with weight variation */
h2 {
  font-family: var(--brand-font-body);
  color: var(--brand-text-heading);
  font-size: 28pt;
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1.2;
}

h3 {
  font-family: var(--brand-font-body);
  color: var(--brand-text-heading);
  font-size: 20pt;
  font-weight: 700;
  line-height: 1.3;
}

/* Body styles — Inter Regular */
body, p, li {
  font-family: var(--brand-font-body);
  color: var(--brand-text-body);
  font-size: 16pt;
  font-weight: 400;
  line-height: 1.6;
}

/* Accent button */
.btn-accent {
  background-color: var(--brand-red);
  color: #FFFFFF;
  border: none;
  font-family: var(--brand-font-body);
  font-weight: 600;
}
```

## Tailwind CSS

```javascript
// CUSTOMIZE: Replace values in tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          red: '#E63946',
          blue: '#2563EB',
          green: '#10B981',
          amber: '#F59E0B',
          violet: '#7C3AED',
          heading: '#1A1A2E',
          body: '#374151',
          muted: '#6B7280',
          bg: '#FFFFFF',
          'bg-alt': '#F3F4F6',
          'bg-dark': '#1A1A2E',
          border: '#E5E7EB',
        }
      },
      fontFamily: {
        display: ['Bebas Neue', 'Impact', 'Arial Black', 'sans-serif'],
        body: ['Inter', 'Arial', 'sans-serif'],
        mono: ['JetBrains Mono', 'Courier New', 'monospace'],
      }
    }
  }
}
```

## Python (python-pptx)

```python
# CUSTOMIZE: See scripts/brand_colors.py for complete color constants
from brand_colors import BrandColors, HexColors

# Apply brand color to a shape
shape.fill.solid()
shape.fill.fore_color.rgb = BrandColors.RED  # Signal Red accent

# Set heading text
run.font.color.rgb = BrandColors.TEXT_HEADING  # Near Black
run.font.name = "Bebas Neue"

# Set body text
run.font.color.rgb = BrandColors.TEXT_BODY  # Dark Gray
run.font.name = "Inter"
```

## Google Fonts Import

```html
<!-- CUSTOMIZE: Replace with your Google Fonts import -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```
