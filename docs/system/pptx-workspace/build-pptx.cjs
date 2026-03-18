'use strict';
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require(path.join(__dirname, '../../../.claude/skills/pptx/scripts/html2pptx.cjs'));

const WORKSPACE = __dirname;
const OUTPUT = path.join(WORKSPACE, '..', 'project-starter-explainer.pptx');

async function build() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Project Starter';
  pptx.title = 'Project Starter — Explainer Deck';

  for (let i = 1; i <= 17; i++) {
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
