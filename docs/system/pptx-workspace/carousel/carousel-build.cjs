'use strict';
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require(path.join(__dirname, '../../../../.claude/skills/pptx/scripts/html2pptx.cjs'));

const WORKSPACE = __dirname;
const OUTPUT = path.join(WORKSPACE, '..', '..', 'project-starter-carousel.pptx');

async function build() {
  const pptx = new pptxgen();

  // 4:5 portrait layout (810pt x 1012.5pt)
  pptx.defineLayout({ name: 'CAROUSEL', width: 810 / 72, height: 1012.5 / 72 });
  pptx.layout = 'CAROUSEL';
  pptx.author = 'Jack Richardson';
  pptx.title = 'Project Starter — LinkedIn Carousel';

  for (let i = 1; i <= 6; i++) {
    const num = String(i).padStart(2, '0');
    const slideFile = path.join(WORKSPACE, `slide${num}.html`);
    console.log(`Processing slide ${num}...`);
    await html2pptx(slideFile, pptx);
  }

  await pptx.writeFile({ fileName: OUTPUT });
  console.log(`\nCreated: ${OUTPUT}`);
}

build().catch(err => {
  console.error('\nBuild failed:', err.message);
  process.exit(1);
});
