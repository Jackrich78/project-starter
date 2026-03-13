#!/usr/bin/env node
// md-to-doc.cjs — Generic Markdown → .docx converter
// Usage: node md-to-doc.cjs <input.md> [output.docx]
// Requires: npm install docx (already in project root package.json)

"use strict";

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun,
  HeadingLevel, AlignmentType, LevelFormat, BorderStyle, ShadingType
} = require("docx");

// ── Fonts (Google Docs compatible) ──────────────────────────────────────────
const BODY = "Open Sans";
const MONO = "Source Code Pro";

// ── Inline parser: **bold**, *italic*, `code` ────────────────────────────────
function inline(text, opts = {}) {
  const { size = 22, italic = false } = opts;
  if (!text) return [new TextRun({ text: "", font: BODY, size })];
  const runs = [];
  const re = /\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`/g;
  let i = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > i) {
      runs.push(new TextRun({ text: text.slice(i, m.index), font: BODY, size, italics: italic }));
    }
    if (m[1])      runs.push(new TextRun({ text: m[1], bold: true, italics: italic, font: BODY, size }));
    else if (m[2]) runs.push(new TextRun({ text: m[2], italics: true, font: BODY, size }));
    else if (m[3]) runs.push(new TextRun({ text: m[3], font: MONO, size: 20 }));
    i = re.lastIndex;
  }
  if (i < text.length) {
    runs.push(new TextRun({ text: text.slice(i), font: BODY, size, italics: italic }));
  }
  return runs.length ? runs : [new TextRun({ text, font: BODY, size, italics: italic })];
}

// ── Block builders ───────────────────────────────────────────────────────────
function h1(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: BODY })] });
}
function h2(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, font: BODY })] });
}
function h3(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: t, font: BODY })] });
}
function para(text) {
  return new Paragraph({ children: inline(text) });
}
function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullet-list", level: 0 },
    children: inline(text)
  });
}
function codeLine(text) {
  return new Paragraph({
    spacing: { before: 0, after: 0 },
    shading: { fill: "F2F2F2", type: ShadingType.CLEAR },
    indent: { left: 360, right: 360 },
    children: [new TextRun({ text: text || " ", font: MONO, size: 18 })]
  });
}
function blockquote(text) {
  return new Paragraph({
    indent: { left: 360 },
    spacing: { before: 60, after: 60 },
    children: inline(text, { italic: true })
  });
}
function hr() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC", space: 1 } },
    children: [new TextRun("")]
  });
}
function spacer() {
  return new Paragraph({ spacing: { after: 60 }, children: [new TextRun("")] });
}

// ── Markdown parser ──────────────────────────────────────────────────────────
function parseMarkdown(md) {
  const lines = md.split("\n");
  const children = [];
  let inCode = false;

  for (const raw of lines) {
    const line = raw.trimEnd();

    // Fenced code block toggle
    if (line.startsWith("```")) { inCode = !inCode; continue; }
    if (inCode) { children.push(codeLine(raw)); continue; }

    if (/^-{3,}$/.test(line))     { children.push(hr());                            continue; }
    if (line.startsWith("# "))    { children.push(h1(line.slice(2)));               continue; }
    if (line.startsWith("## "))   { children.push(h2(line.slice(3)));               continue; }
    if (line.startsWith("### "))  { children.push(h3(line.slice(4)));               continue; }
    if (/^[-*] /.test(line))      { children.push(bullet(line.slice(2)));           continue; }
    if (/^\d+\. /.test(line))     { children.push(bullet(line.replace(/^\d+\. /, ""))); continue; }
    if (line.startsWith("> "))    { children.push(blockquote(line.slice(2)));       continue; }
    if (line.trim() === "")       { children.push(spacer());                        continue; }

    children.push(para(line));
  }
  return children;
}

// ── Document assembly ────────────────────────────────────────────────────────
function buildDoc(children) {
  return new Document({
    styles: {
      default: { document: { run: { font: BODY, size: 22 } } },
      paragraphStyles: [
        {
          id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 36, bold: true, color: "1A1A1A", font: BODY },
          paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
        },
        {
          id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 28, bold: true, color: "2D2D2D", font: BODY },
          paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
        },
        {
          id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 24, bold: true, color: "404040", font: BODY },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
        }
      ]
    },
    numbering: {
      config: [{
        reference: "bullet-list",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }]
    },
    sections: [{
      properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      children
    }]
  });
}

// ── CLI ──────────────────────────────────────────────────────────────────────
const [,, inputPath, outputPath] = process.argv;
if (!inputPath) {
  console.error("Usage: node md-to-doc.cjs <input.md> [output.docx]");
  process.exit(1);
}

const outPath = outputPath || inputPath.replace(/\.md$/, ".docx");
const md = fs.readFileSync(inputPath, "utf8");
const doc = buildDoc(parseMarkdown(md));

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log("Created: " + outPath);
});
