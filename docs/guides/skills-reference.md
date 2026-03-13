---
updated: 2026-03-08
---

# Skills Reference

Skills are modular decision guides bundled with context, templates, and references. Commands import them automatically when relevant. You can also invoke them directly. Skills live in `.claude/skills/` — add your own via `/retro` or manually.

21 skill directories ship with the harness. 16 are part of the public workflow; 5 are personal content-creation extensions excluded from the core template.

---

## Development Workflow

Guides for building and validating code.

| Skill | What it does | When to invoke |
|-------|-------------|----------------|
| `debug` | Structured 6-phase debugging process: classify the issue type, investigate root cause without guessing, implement a targeted fix, add a regression test, verify, and document the learning. | When a bug is more than a typo fix — logic errors, integration failures, or anything that needs systematic investigation rather than trial and error. |
| `spike` | Time-boxed technical investigation (2–8 hours) to answer a specific question before committing to an approach. Produces a FINDINGS.md and a research doc; the spike directory is deleted after learnings are extracted. | When you're unsure which of two approaches will actually work, or when a key assumption in the plan hasn't been validated yet. |
| `tdd-red-green-refactor` | Orchestrates the TDD cycle using three isolated subagents: the test writer sees only the PRD, the implementer sees only the failing tests, the refactorer sees tests and implementation. Isolation prevents each agent from being biased by what others know. | When implementing any feature with `/build`, or when applying TDD to a specific component outside the full build workflow. |
| `test-strategy` | Decision guide for choosing the right test type (unit, integration, E2E) and placing tests in the correct directory. Prevents testing at the wrong pyramid level and catches test-to-directory mismatches. | Before writing tests in `/blueprint`, or when unsure whether something should be a unit test or an integration test. |

## Content & Visual

Create documents, diagrams, and presentations.

| Skill | What it does | When to invoke |
|-------|-------------|----------------|
| `diagram` | Generates diagrams from Mermaid syntax and outputs them as SVG or PNG using Mermaid CLI with your brand colors. | When you need a flowchart or sequence diagram and Mermaid syntax is a faster starting point than drawing. |
| `excalidraw-diagram` | Creates Excalidraw diagram JSON files designed to *argue* a point, not just display information. Follows a methodology: write the visual argument first, then build section-by-section, then render and review. | When you need a diagram that teaches a concept — architectural decisions, workflow patterns, system structure. Not for simple flowcharts. |
| `icon` | Renders Lucide icons to PNG files with your brand stroke color. | When you need a standalone icon for a slide, document, or diagram accent. |
| `pptx` | Creates and edits PowerPoint files (.pptx) from HTML templates via the html2pptx pipeline. Handles layout, typography, and image embedding. | When creating a presentation deck — explainer slides, demo decks, or any structured visual content. |
| `docx` | Creates, edits, and analyzes Word documents (.docx) including tracked changes and comments. | When the output needs to be a Word document — proposals, reports, or any content destined for review in a word processor. |
| `md-to-doc` | Converts a markdown file into a formatted .docx with clean typography, structured headings, and code blocks. | When you've written content in markdown and need a polished Word document output — for Google Docs, client delivery, or formal documentation. |
| `pdf` | Extracts text and tables from PDFs, creates new PDFs, merges or splits documents, and handles form fields programmatically. | When working with PDF files at scale — form filling, report generation, or extraction. |

## Technical

Extend and integrate the harness.

| Skill | What it does | When to invoke |
|-------|-------------|----------------|
| `ci-validation` | Validates GitHub Actions workflow files locally before you push, catching syntax errors and configuration issues in seconds instead of waiting for the CI runner. | Before committing any change to `.github/workflows/*.yml`. Prevents broken CI from blocking the team. |
| `mcp-builder` | Step-by-step guide for creating MCP (Model Context Protocol) servers that let Claude interact with external services through custom tools. Covers both Python (FastMCP) and TypeScript (MCP SDK). | When you want to give Claude persistent access to an external API or service beyond what's available through standard tools. |
| `skill-creator` | Guide for creating new skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations. Covers skill structure, frontmatter, and quality criteria. | When `/retro` identifies a pattern worth preserving, or when you want to package domain knowledge into a reusable skill. |
| `brand-guidelines` | Template for applying a consistent brand identity (colors, typography, visual style) to presentations, documents, and diagrams. Ships with a neutral professional palette — replace the placeholder values with your brand's actual values. | When you need branded output and haven't yet customized the palette. After customizing: referenced automatically by `diagram`, `excalidraw-diagram`, and `pptx` skills. |

## Utilities

Standalone tools.

| Skill | What it does | When to invoke |
|-------|-------------|----------------|
| `youtube-transcript-extract` | Processes a raw YouTube transcript and extracts the core insights, filtering out promotional content, filler words, and tangents. Works across tutorials, interviews, lectures, and commentary. | When you paste a raw transcript and want a clean summary of what was actually taught — not the full transcript. |
