/**
 * render-icon.cjs - Render Lucide SVG icons to branded PNGs
 * Usage: node render-icon.cjs <icon-name> [size] [opacity] [output-dir]
 * Example: node render-icon.cjs git-branch 120 0.4 ./output
 */
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const BRAND_COLOR = '#A8BCCF'; // pale steel — CUSTOMIZE: replace with your brand's icon stroke colour
const ICONS_DIR = path.resolve(__dirname, '../../../../node_modules/lucide-static/icons');

function hexToRgba(hex, opacity) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

async function renderIcon(name, size = 120, opacity = 1.0, outputDir = process.cwd()) {
  const svgPath = path.join(ICONS_DIR, `${name}.svg`);
  if (!fs.existsSync(svgPath)) {
    throw new Error(`Icon not found: ${svgPath}. Available icons in: ${ICONS_DIR}`);
  }

  let svg = fs.readFileSync(svgPath, 'utf-8');

  // Replace stroke with RGBA pre-baked opacity (CSS opacity silently dropped by html2pptx)
  const color = opacity < 1.0 ? hexToRgba(BRAND_COLOR, opacity) : BRAND_COLOR;
  svg = svg.replace(/stroke="currentColor"/g, `stroke="${color}"`);
  svg = svg.replace(/width="\d+"/, `width="${size}"`);
  svg = svg.replace(/height="\d+"/, `height="${size}"`);

  fs.mkdirSync(outputDir, { recursive: true });

  const suffix = opacity < 1.0 ? `-${Math.round(opacity * 100)}pct` : '';
  const outPath = path.join(outputDir, `${name}-${size}px${suffix}.png`);

  const start = Date.now();
  await sharp(Buffer.from(svg)).resize(size, size).png().toFile(outPath);
  const elapsed = Date.now() - start;

  console.log(`Rendered ${name} at ${size}px (opacity: ${opacity}) in ${elapsed}ms -> ${outPath}`);
  return outPath;
}

// CLI mode
if (require.main === module) {
  const [,, name, size, opacity, outputDir] = process.argv;
  if (!name) {
    console.error('Usage: node render-icon.cjs <icon-name> [size] [opacity] [output-dir]');
    process.exit(1);
  }
  renderIcon(name, parseInt(size) || 120, parseFloat(opacity) || 1.0, outputDir || process.cwd())
    .catch(err => { console.error(err.message); process.exit(1); });
}

module.exports = { renderIcon };
