---
name: youtube-transcript-extract
description: Extract key learnings from YouTube video transcripts, filtering out promotional content, filler words, and tangents. Use when the user provides a raw YouTube transcript and wants a clean summary of core insights, main points, or actionable takeaways. Handles different video styles (tutorials, interviews, lectures, commentary).
---

# YouTube Transcript Extract

## Overview

Transform raw YouTube transcripts into structured, actionable insights by filtering promotional content, filler language, and tangents while preserving core teachings, key arguments, and practical advice.

## Quick Start

When a user provides a YouTube transcript:

1. **Identify content type** (tutorial, interview, lecture, commentary)
2. **Apply appropriate analysis pattern** (see [prompt-patterns.md](references/prompt-patterns.md))
3. **Filter aggressively**:
   - Remove sponsor reads, channel promotion
   - Cut filler words (um, uh, like, basically)
   - Skip tangential stories
4. **Extract core value**:
   - Main concepts and arguments
   - Actionable insights
   - Technical details
   - Key examples
5. **Format clearly** with structured output

## Workflow

### Step 1: Detect Content Type

Read the first ~500 words of the transcript to identify the style:

- **Tutorial**: Step-by-step instructions, "first we'll...", "next you need to..."
- **Interview**: Multiple speakers, Q&A format, back-and-forth dialogue
- **Lecture**: Single speaker, structured presentation, educational tone
- **Commentary**: Opinion/analysis, "I think...", "the problem with..."

### Step 2: Load Appropriate Pattern

Consult [prompt-patterns.md](references/prompt-patterns.md) for the specific analysis template matching the content type. This file contains:

- Filtering rules per content type
- Output structure templates
- Quality checklist

### Step 3: Analyze with Extended Thinking

For transcripts >5000 words, use extended thinking to:
1. Map overall structure and main themes
2. Extract key points per section
3. Consolidate and remove duplication
4. Format final output

This prevents important details from being lost in long content.

### Step 4: Format Output

Use the structured template from prompt-patterns.md:

```markdown
# [Video Topic]

**Content Type**: [Detected type]
**Main Focus**: [1-2 sentence summary]

---

## Key Learnings
[Appropriate sections based on content type]

---

## Actionable Items
- [ ] [Concrete takeaways]
```

## Filtering Principles

**Always remove:**
- "Don't forget to like and subscribe"
- Sponsor reads and product placements
- "Um", "uh", "like", "you know", "basically"
- Repetitive restatements
- Off-topic personal stories

**Always preserve:**
- Core concepts and frameworks
- Actionable advice
- Technical specifications
- Examples illustrating main points
- Questions that advance understanding

## Examples

**User request:**
> "Summarize this React tutorial transcript"

**Your response:**
1. Detect: Tutorial content type
2. Load tutorial pattern from references/prompt-patterns.md
3. Extract: Main goal, key steps, technical details, tools mentioned
4. Filter: Sponsor mentions, "smash that subscribe button", filler words
5. Output: Structured summary with steps, important details, resources

---

**User request:**
> "Extract the main points from this interview"

**Your response:**
1. Detect: Interview/discussion content type
2. Load interview pattern from references/prompt-patterns.md
3. Extract: Participants, key insights per speaker, notable questions
4. Filter: Introductions, promotional content, tangents
5. Output: Structured summary with insights, debates, takeaways

## Quality Standards

Before delivering output, verify:

- ✅ No promotional language remains
- ✅ Main points are clear and concise
- ✅ No filler words or repetition
- ✅ Actionable insights highlighted
- ✅ Logical structure maintained
- ✅ Technical accuracy preserved

## Resources

- **[prompt-patterns.md](references/prompt-patterns.md)**: Detailed analysis patterns for each content type, filtering rules, output templates
