---
name: md-to-doc
description: Convert a markdown (.md) file into a professionally formatted .docx and optionally .odt, suitable for Google Docs. Use when the user wants to export a markdown document as a Word or Google Docs file with clean typography, structured headings, bullet lists, and code blocks. Triggers include "convert this markdown to docx", "format this for Google Docs", "create a Word document from this markdown", "export as docx", "make a formatted document from this md file".
---

# Markdown → Docx Converter

Convert any `.md` file into a formatted `.docx` (and optionally `.odt`) with clean Open Sans typography.

## Quick Start

```bash
node .claude/skills/md-to-doc/scripts/md-to-doc.cjs <input.md> [output.docx]
```

If `output.docx` is omitted, the output is written as `<input>.docx` alongside the source file.

## What Gets Converted

| Markdown | Output |
|----------|--------|
| `# H1` | Heading 1 — 18pt bold, Open Sans |
| `## H2` | Heading 2 — 14pt bold |
| `### H3` | Heading 3 — 12pt bold |
| `- item` or `* item` | Bullet list with hanging indent |
| `1. item` | Also converted to bullet |
| ` ``` ``` ` | Shaded code block, Source Code Pro 9pt |
| `> quote` | Indented italic blockquote |
| `**bold**`, `*italic*` | Inline bold / italic |
| `` `code` `` | Inline code, Source Code Pro |
| `---` | Horizontal rule (light grey) |
| Empty line | Spacer paragraph |

## Default Fonts (Google Docs compatible)

- **Body**: Open Sans, 11pt — available in Google Docs font picker
- **Mono**: Source Code Pro, 9pt — available in Google Docs font picker

To change fonts: edit `BODY` and `MONO` constants at the top of `scripts/md-to-doc.cjs`.

## ODT for Google Docs

After creating the `.docx`, optionally convert to `.odt` for Google Docs import:

```bash
soffice --headless --convert-to odt output.docx
```

Requires: `brew install libreoffice`

> **Font note**: If Open Sans or Source Code Pro are not installed on the system running LibreOffice, substitution will occur in the `.odt` file. The fonts render correctly when opened in Google Docs (which has them built in).

## Limitations

- **Tables**: Not supported — flatten to bullets or prose
- **Images**: Not supported — use caption text as placeholder
- **Nested lists**: Only top-level bullets (level 0)
- **H4+**: Treated as regular paragraphs

## Dependency

`docx` is already in the project root `package.json`. If not installed:

```bash
npm install  # from project root
```
