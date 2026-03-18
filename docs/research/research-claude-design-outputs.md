# Research: Improving Claude Code Design Output Quality

## Executive Summary

People solve the design quality problem for Claude Code through **three converging patterns**: (1) encoding design intent as **Skills** (reusable markdown + YAML with references), (2) establishing **design system constraints** as semantic rules rather than literal hex codes, and (3) **progressive disclosure** where detailed specifications are loaded contextually only when needed.

The most successful approach is the **Skills-based architecture** paired with **visual design principles** encoded as Markdown guidance, not just token values.

---

## Approach 1: Skills-Based Design System (Most Common)

### How It Works

**Structure:**
- A `.claude/skills/` directory contains skill definitions
- Each skill is a directory with `SKILL.md` (YAML frontmatter + Markdown) plus optional reference files
- Skills load contextually—only when the task requires them

**YAML Frontmatter** tells Claude when to use the skill:
```yaml
---
name: "Frontend Design"
description: "Create distinctive, production-grade interfaces"
when: "user asks to build web components, pages, or applications"
---
```

**Markdown Instructions** (after `---`) provide:
- Visual principles (typography, color, motion)
- What to avoid (clichés, generic aesthetics)
- Context-specific guidance

### Real Examples

#### Example 1: Anthropic's Official Frontend Design Skill
**Retrieved from:** [anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)

**Key Principles Encoded:**

1. **Typography** (Anti-Generic)
   - Avoid: Arial, Inter, Roboto, system fonts
   - Instead: Distinctive display font + refined body font
   - Rule: "Choose fonts that are beautiful, unique, and interesting"

2. **Color & Theme** (Cohesive, Not Scattered)
   - Avoid: Purple gradient on white (clichéd)
   - Instead: Commit to ONE cohesive aesthetic
   - Use CSS variables for consistency across the interface
   - Rule: "Dominant colors and sharp accents outperform timid, evenly-distributed palettes"

3. **Visual Depth** (Atmosphere Over Flatness)
   - Techniques: Gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, grain overlays
   - Rule: "Create atmosphere and depth rather than defaulting to solid colors"

4. **Motion & Interaction** (High-Impact, Not Scattered)
   - One well-orchestrated page load with staggered reveals beats scattered micro-interactions
   - Focus: animation-delay for coordinated entry sequences
   - Rule: "High-impact moments create more delight than scattered micro-interactions"

**Why This Works:**
- Rules are semantic ("distinctive," "cohesive," "atmospheric") not literal
- Guidance precedes coding, preventing generic defaults
- Principles compound: typography + depth + motion = coherent aesthetic

**Impact:** Anthropic reports this skill (277,000+ installs) significantly improves frontend UI generation quality.

#### Example 2: Interface Design Skill (Dammyjay93)
**Retrieved from:** [Dammyjay93/interface-design](https://github.com/Dammyjay93/interface-design)

**Unique Approach:** Memory + Enforcement

This skill maintains consistency *across sessions* by:
1. **Reading** skill files and principles
2. **Loading** `.interface-design/system.md` (project-specific design rules)
3. **Stating design choices** before each component
4. **Offering to save** new patterns discovered during work

**Key Files:**
- `.claude/skills/interface-design/SKILL.md` - Core skill definition
- `.interface-design/system.md` - Persistent project design rules (persists across sessions)

**Pattern:** The skill acts as "design memory"—it enforces consistency by:
- Suggesting design direction based on previous choices
- Asking for confirmation before changing direction
- Saving new patterns automatically for future components

**Why This Matters:** Solves the session-drift problem—without memory, each Claude session starts fresh and makes independent design decisions.

---

## Approach 2: Excalidraw Diagrams (Format-Specific Design)

### The Problem

Excalidraw diagrams are JSON objects where every element has properties (position, color, stroke, fill, roughness). Generic JSON lacks visual polish—diagrams look "AI-generated" without explicit style guidance.

### How People Solve It

#### Excalidraw Diagram Skill (coleam00)
**Retrieved from:** [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill)

**Design Approach:**

1. **Color Palettes as Reference Files**
   - `references/color-palette.md` defines:
     ```
     Primary: #3B82F6
     Accent: #F59E0B
     Neutral: #E5E7EB
     Dark Mode: #1F2937
     ```
   - Markdown format—Claude reads and applies consistently

2. **Element Templates as JSON Patterns**
   - `references/element-templates.md` shows correct Excalidraw JSON structure
   - Example: Standard rectangle with consistent styling
   - Prevents Claude from guessing JSON properties

3. **JSON Schema Reference**
   - `references/json-schema.md` documents all Excalidraw properties:
     - `roughness: 0` = formal diagrams
     - `roughness: 1` = friendly sketches
     - `fontSize`, `fontFamily`, `strokeColor`, `backgroundColor`, etc.

4. **Iterative Rendering Loop**
   - Claude generates JSON → renders to PNG → views output → fixes iteratively
   - This is THE key workflow: you cannot design Excalidraw JSON blind
   - `references/render_excalidraw.py` converts JSON to PNG for visual feedback

**Design Philosophy:**
- "Diagrams should argue, not display"—color and style choices should make the visual argument clearer
- For complex diagrams, build one section at a time
- Always render and verify—don't attempt full JSON in one pass

**Why This Works:**
- Markdown color palettes are human-readable and Claude-parseable
- JSON templates show structure without forcing specific values
- Rendering loop closes the feedback gap between intent and output

**Sources Referenced:**
- [Excalidraw JSON Schema](https://docs.excalidraw.com/docs/codebase/json-schema) - Official Excalidraw format docs
- [Excalidraw CLI Features](https://github.com/ahmadawais/excalidraw-cli) - Zero-config hand-drawn styling

---

## Approach 3: PowerPoint/PPTX (Template-Based Design)

### The Problem

AI-generated slides often ignore corporate templates or apply formatting inconsistently, resulting in off-brand or visually incoherent presentations.

### How People Solve It

#### Solution 1: Template-Aware Generation (python-pptx)
**Retrieved from:** [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) and [pptx-from-layouts-skill](https://github.com/tristan-mcinnis/pptx-from-layouts-skill)

**Workflow:**

1. **Profile Template's Slide Master**
   - Extract available layouts (title slide, content, 2-column, etc.)
   - Parse fonts, colors, and spacing from slide master
   - Store in reference file

2. **Map Content to Layouts Semantically**
   - "Title slide" → use title layout
   - "Comparison" → use 2-column layout
   - "Data insight" → use chart layout
   - NOT just placing text on blank slides

3. **Preserve Template Styling**
   - Place content in proper placeholders (not text overlays)
   - Use template fonts, colors, and spacing
   - Maintain aspect ratios and grid alignment

4. **Generate via python-pptx**
   - Claude produces JSON manifest
   - Script converts manifest → `.pptx` using template

**Key Difference from Generic PPTX:**
- Generic: Claude outputs content → you paste into PowerPoint
- Template-Aware: Claude reads template → outputs properly formatted `.pptx` with zero manual work

#### Solution 2: Claude for PowerPoint (Native Integration)
**Retrieved from:** [Claude Help Center - Use Claude for PowerPoint](https://support.claude.com/en/articles/13521390-use-claude-for-powerpoint)

**Features:**
- Claude reads your existing deck's template, layouts, fonts, colors, and slide master
- Edits respect formatting rules
- Outputs real `.pptx` files (not outlines)

**Current Limitation:**
- "Design still requires a human touch or a tool like Gamma"
- Content quality is excellent, but visual design is professional-but-not-striking

**Implication:** PowerPoint design quality remains the hardest problem—even template compliance doesn't guarantee visually engaging slides.

---

## Approach 4: Design Tokens as Code (Emerging)

### The Problem

How do you encode a Figma design system in a way Claude can consume and apply repeatably?

### How People Solve It

#### Figma Design Token Export Plugins
**Retrieved from:**
- [Figma Raw](https://www.figma.com/community/plugin/1491678546144854232/figma-raw-export-design-data-for-ai-llm-agents)
- [Figma to AI JSON](https://www.figma.com/community/plugin/1587577656366372788/figma-to-ai-json)
- [lukasoppermann/design-tokens](https://github.com/lukasoppermann/design-tokens)

**Workflow:**

1. **Export Figma Variables to JSON**
   ```json
   {
     "colors": {
       "primary": "#3B82F6",
       "primary-dark": "#1E40AF",
       "neutral-100": "#F3F4F6"
     },
     "typography": {
       "heading-1": {
         "font": "Inter",
         "size": "32px",
         "weight": 700,
         "lineHeight": "1.2"
       }
     },
     "spacing": {
       "xs": "4px",
       "sm": "8px",
       "md": "16px"
     }
   }
   ```

2. **Load as Skill Reference**
   - Store JSON in `references/design-tokens.json`
   - Claude reads before generating interfaces
   - Ensures consistency with design system

3. **Apply in Generated Code**
   - CSS variables from tokens
   - Component spacing from tokens
   - Color palettes from tokens
   - Typography from tokens

**Why This Works (Sometimes):**
- ✅ Single source of truth (one JSON file)
- ✅ Direct export from design tool
- ❌ Literal token values (hex codes) don't encode *why* choices were made
- ❌ Gap between "design intent" (coherence, hierarchy) and "design tokens" (color 23)

**Key Insight:**
- Design tokens alone are insufficient—you need *principles* (why this color?)
- Best practice: tokens + principles
- Example: "Primary color is #3B82F6 for trust; use sparingly for high-impact actions only"

---

## Approach 5: Brand Guidelines Skill (Complete Package)

### Structure

**Retrieved from:** [ComposioHQ/awesome-claude-skills - Brand Guidelines](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/brand-guidelines)

A complete brand guidelines skill bundles:

1. **SKILL.md** - Activation rules and instructions
2. **Color Palette** (`references/colors.md` or `.json`)
3. **Typography Rules** (font families, sizes, weights)
4. **Layout Principles** (spacing, grid, alignment)
5. **Component Examples** (buttons, cards, forms with styled examples)
6. **Brand Voice** (tone, messaging guidelines)
7. **Visual Examples** (reference images, screenshots)

**Advantage of Skill Approach:**
- Loaded only when needed (context-efficient)
- Reusable across projects
- Shareable with team
- Composable (brand-guidelines + frontend-design + your-custom-skill all apply together)

---

## Synthesis: The Gap Between Design Intent and Output

### The Core Problem

Claude can generate **format** (valid JSON, valid PPTX) and **content** (coherent text), but not automatically **intent** (why this aesthetic?).

**How people bridge this:**

| Gap | Solution | Example |
|-----|----------|---------|
| **Generic fonts** | Principle before code | "Choose distinctive, beautiful fonts—never Arial or Inter" |
| **Scattered colors** | Explicit constraint | "Use one dominant color + one sharp accent throughout" |
| **Flat design** | Technique list | "Add depth: shadows, gradients, textures, layered transparencies" |
| **Inconsistent motion** | Focus rule | "One orchestrated page load with staggered reveals beats scattered micro-interactions" |
| **Off-brand PPTX** | Template-aware generation | Profile slide master → map content to layouts → generate from template |
| **Generic diagrams** | Render-feedback loop | Generate JSON → render PNG → view → fix → iterate |
| **Drift across sessions** | Persistent rules file | `.interface-design/system.md` stays in repo, loaded every session |

### Why Semantic Rules Beat Token Specifications

**Literal Approach (Doesn't Scale):**
```
Color1: #3B82F6
Color2: #F59E0B
FontSize: 14px
```
→ Claude uses colors but no sense of *role* or *hierarchy*

**Semantic Approach (Works):**
```
## Color Strategy
- Primary color (#3B82F6) signals trust—use sparingly for highest-importance actions
- Accent color (#F59E0B) draws attention—use for CTAs and state changes
- Neutrals (#E5E7EB) for text and backgrounds
- Never mix more than 3 colors in one component
```
→ Claude understands *why* and applies consistently

---

## Concrete Implementation Pattern (Recommended)

Based on research, here's the repeatable pattern:

```
project/
├── .claude/
│   ├── skills/
│   │   ├── brand-guidelines/
│   │   │   ├── SKILL.md              # Activation rules + instructions
│   │   │   └── references/
│   │   │       ├── colors.md         # Semantic color guidance
│   │   │       ├── typography.md     # Font + type scale rules
│   │   │       ├── spacing.md        # Grid + alignment principles
│   │   │       └── components.md     # Visual examples
│   │   ├── frontend-design/          # Anthropic's skill or custom
│   │   └── excalidraw-diagrams/      # For visual diagrams
│   └── CLAUDE.md                     # Project-wide design standards
├── .interface-design/
│   └── system.md                     # Persistent design decisions (persists across sessions)
└── src/
```

**Key Files:**

1. **SKILL.md** (Activation)
   ```yaml
   ---
   name: "Brand Guidelines"
   description: "Apply [Company] brand guidelines"
   when: "user builds UI, creates presentations, or generates visuals"
   ---

   # Brand Guidelines

   You are designing for [Company]. Before building, commit to one aesthetic direction...
   ```

2. **references/colors.md** (Semantic Guidance)
   ```markdown
   ## Primary (#3B82F6)
   Signals trust and confidence. Use for:
   - Primary CTA buttons (max 1-2 per screen)
   - High-importance actions
   - Trust indicators (verified badges, secure icons)

   Avoid: Using as background or in large areas—reserve for moments.
   ```

3. **.interface-design/system.md** (Persistent Memory)
   ```markdown
   # [Project Name] Design System

   ## Established Patterns
   - Font pairing: Playfair Display + Inter
   - Color: Teal primary (#06B6D4), warm accent (#F59E0B)
   - Spacing: 8px grid
   - Card elevation: 1px border + 2px shadow

   ## Saved Patterns
   - CTA buttons: Rounded corners (rounded-lg), bold text, white text on color
   - Form inputs: Subtle focus ring, vertical spacing 16px
   ```

---

## What Works Best by Format

### Excalidraw Diagrams
✅ **Best Practice:** Color palette reference + JSON templates + render loop
- Specific hex codes needed (JSON requires exact values)
- Semantic guidance: "Use accent color for emphasis, primary for structure"
- Absolute requirement: render-verify-iterate (cannot design blind)

### PowerPoint/PPTX
✅ **Best Practice:** Template-aware generation (profile master → map content → generate)
- Hard constraint: template fonts, colors, and layouts must be extracted first
- Limitation: design quality still requires human review (tool limitation, not AI limitation)
- Works best with predefined slide layouts (title, content, 2-column, etc.)

### Frontend/UI
✅ **Best Practice:** Skills + design principles + persistent system.md
- Semantic rules > literal tokens
- Principle-first workflow (aesthetic direction before code)
- Session memory critical (reusable patterns file)

### Brand Consistency Across All Formats
✅ **Best Practice:** Composable skills + shared references
- Load multiple skills together (brand-guidelines + frontend-design)
- Store common guidance in shared markdown files
- Use persistent project-level system.md for institutional memory

---

## Open-Source Examples & Resources

### Excalidraw Skills
- [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) - Primary reference, includes render loop
- [edwingao28/excalidraw-skill](https://github.com/edwingao28/excalidraw-skill) - Live canvas version
- [rnjn/cc-excalidraw-skill](https://github.com/rnjn/cc-excalidraw-skill) - Alternative implementation

### Design System Skills
- [Anthropic frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) - Official, 277k+ installs
- [Dammyjay93/interface-design](https://github.com/Dammyjay93/interface-design) - With session memory
- [ComposioHQ/awesome-claude-skills - brand-guidelines](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/brand-guidelines) - Complete example

### PowerPoint Skills
- [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) - Full office suite support
- [tristan-mcinnis/pptx-from-layouts-skill](https://github.com/tristan-mcinnis/pptx-from-layouts-skill) - Template-first PPTX generation

### Figma Design Token Export
- [Figma Raw Plugin](https://www.figma.com/community/plugin/1491678546144854232/figma-raw-export-design-data-for-ai-llm-agents) - Direct Figma → AI JSON
- [lukasoppermann/design-tokens](https://github.com/lukasoppermann/design-tokens) - Amazon-style dictionary format

### Community Collections
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - 100+ skills organized by category
- [Anthropic/skills](https://github.com/anthropics/skills) - Official Anthropic skill repository

---

## Key Learnings

1. **Skills Solve Context Efficiency**: Loading design guidance only when needed prevents context pollution while making guidelines available when they matter.

2. **Semantic Rules > Literal Tokens**: "Distinctive fonts" beats "use font 23". Design principles guide consistent decisions; design tokens provide implementation details.

3. **Render-Feedback Loops Are Essential for Diagrams**: You cannot design Excalidraw JSON blind. Render → view → fix is the required workflow.

4. **Template Compliance Matters for Office Formats**: PowerPoint design quality jumps when you profile the template first and map content semantically to layouts.

5. **Session Persistence Prevents Design Drift**: Maintaining a project-level system.md file (persisted in repo) enables Claude to build on previous design decisions across sessions.

6. **Composite Skills Work Well**: Brand guidelines + frontend design + format-specific skills can load together and reinforce each other.

7. **The Design Intent Gap Is Real**: There's no silver bullet—the best approach combines principles (semantic guidance) + tokens (literal values) + feedback loops (verification).

---

## Sources

- [Anthropic: Package your brand guidelines in a skill](https://claude.com/resources/use-cases/package-your-brand-guidelines-in-a-skill)
- [Anthropic Skills Repository - Frontend Design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- [Anthropic Claude Code Docs - Extend with Skills](https://code.claude.com/docs/en/skills)
- [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill)
- [Dammyjay93/interface-design](https://github.com/Dammyjay93/interface-design)
- [Excalidraw Documentation - JSON Schema](https://docs.excalidraw.com/docs/codebase/json-schema)
- [Excalidraw CLI](https://github.com/ahmadawais/excalidraw-cli)
- [Claude Help Center - Use Claude for PowerPoint](https://support.claude.com/en/articles/13521390-use-claude-for-powerpoint)
- [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills)
- [tristan-mcinnis/pptx-from-layouts-skill](https://github.com/tristan-mcinnis/pptx-from-layouts-skill)
- [Figma Raw - Export Design Data for AI/LLM](https://www.figma.com/community/plugin/1491678546144854232/figma-raw-export-design-data-for-ai-llm-agents)
- [lukasoppermann/design-tokens](https://github.com/lukasoppermann/design-tokens)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Why use Markdown in your Agents' System Prompt?](https://medium.com/@edprata/why-use-markdown-in-your-agents-system-prompt-41ad258a25c7)
- [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Skill Authoring Best Practices - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [How to Give Your AI Coding Agent a Visual Brain: Excalidraw Diagram Skill](https://atalupadhyay.wordpress.com/2026/03/04/how-to-give-your-ai-coding-agent-a-visual-brain-excalidraw-diagram-skill-for-claude-code/)
- [Improving Frontend Design Through Skills - Claude Blog](https://claude.com/blog/improving-frontend-design-through-skills)
- [Marie Claire Dean: I Built 63 Design Skills For Claude](https://marieclairedean.substack.com/p/i-built-63-design-skills-for-claude)
