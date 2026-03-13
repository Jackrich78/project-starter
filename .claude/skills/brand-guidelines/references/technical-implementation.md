<!-- CUSTOMIZE: Replace all color values, font names, and variable values with your brand's specifications -->

# Technical Implementation

Code snippets for applying brand colors and typography across different platforms.

## CSS Variables

```css
/* CUSTOMIZE: Replace values with your brand colors and fonts */
:root {
  /* Primary Colors */
  --brand-primary: #1E3A5F;
  --brand-background: #F8F9FA;
  --brand-secondary: #6B8FA8;
  --brand-body-text: #535250;
  --brand-accent: #2E6FD9;

  /* Backgrounds */
  --brand-bg-alt: #EEF1F5;
  --brand-bg-dark: #15191B;

  /* Typography */
  --brand-font-heading: 'Your Heading Font', Arial, sans-serif;
  --brand-font-body: 'Your Body Font', Arial, sans-serif;
  --brand-font-mono: 'Your Mono Font', 'Courier New', monospace;
}

/* Heading styles */
h1, h2, h3 {
  font-family: var(--brand-font-heading);
  color: var(--brand-primary);
}

/* Body styles */
body, p, li {
  font-family: var(--brand-font-body);
  color: var(--brand-body-text);
  line-height: 1.5;
}

/* Accent button */
.btn-accent {
  background-color: var(--brand-accent);
  color: #ffffff;
  border: none;
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
          primary: '#1E3A5F',
          secondary: '#6B8FA8',
          accent: '#2E6FD9',
          body: '#535250',
          bg: '#F8F9FA',
          'bg-alt': '#EEF1F5',
        }
      },
      fontFamily: {
        heading: ['Your Heading Font', 'Arial', 'sans-serif'],
        body: ['Your Body Font', 'Arial', 'sans-serif'],
      }
    }
  }
}
```

## Python (python-pptx)

```python
# CUSTOMIZE: See scripts/brand_colors.py for complete color constants
from brand_colors import BrandColors, HexColors

# Apply primary color to a shape
shape.fill.solid()
shape.fill.fore_color.rgb = BrandColors.PRIMARY

# Set text color
run.font.color.rgb = BrandColors.BODY_TEXT
```

## Google Fonts Import

```html
<!-- CUSTOMIZE: Replace with your Google Fonts import -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Your+Heading+Font:wght@400;600;700&family=Your+Body+Font:wght@400;700&display=swap" rel="stylesheet">
```
