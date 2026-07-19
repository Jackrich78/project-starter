# YouTube Transcript Analysis Prompt Patterns

This file contains prompt patterns and guidance for analyzing YouTube transcripts across different content styles.

## Core Analysis Approach

Use **abstractive summarization** (rewrite and distill) rather than extractive (copy-paste). This produces cleaner, more concise outputs while filtering promotional content naturally.

## Universal Filtering Rules

**Always filter out:**
- Promotional content (sponsor reads, product placements, affiliate links)
- Channel promotion (subscribe, like, bell icon reminders)
- Filler words and verbal tics (um, uh, like, you know, basically)
- Tangential stories unrelated to the main topic
- Repetitive restatements of the same point

**Always preserve:**
- Core concepts and main arguments
- Actionable insights and practical advice
- Examples that illustrate key points
- Technical details and specifications
- Questions that drive the discussion forward

## Content Type Detection

Identify the content type first to apply the appropriate analysis pattern:

- **Tutorial/How-To**: Step-by-step instruction, focuses on process
- **Interview/Discussion**: Q&A format, multiple speakers, conversational
- **Lecture/Educational**: Single speaker, structured presentation of information
- **Commentary/Opinion**: Personal perspective, analysis, critique
- **News/Update**: Time-sensitive information, announcements

## Prompt Patterns by Content Type

### Tutorial/How-To

```
Analyze this tutorial transcript and extract:

**Main Goal**: [What the tutorial teaches]

**Prerequisites**: [Required knowledge/tools]

**Key Steps**:
1. [Step with core action]
2. [Step with core action]
[Continue...]

**Important Details**:
- [Technical specifications]
- [Common pitfalls to avoid]
- [Tips for success]

**Tools/Resources Mentioned**:
- [Tool name]: [Purpose]

Ignore: sponsor mentions, channel promotion, personal anecdotes unrelated to the tutorial.
```

### Interview/Discussion

```
Analyze this interview transcript and extract:

**Participants**: [Names/roles]

**Main Topic**: [Central discussion theme]

**Key Insights**:
1. [Speaker]: [Core point made]
2. [Speaker]: [Core point made]
[Continue...]

**Notable Questions Asked**:
- [Question that revealed important information]

**Disagreements/Debates**:
- [Points of contention and different perspectives]

**Actionable Takeaways**:
- [Practical advice mentioned]

Ignore: introductions, sponsor reads, off-topic tangents, repetitive restatements.
```

### Lecture/Educational

```
Analyze this lecture transcript and extract:

**Central Thesis**: [Main argument/teaching point]

**Key Concepts**:
1. **[Concept]**: [Definition and significance]
2. **[Concept]**: [Definition and significance]
[Continue...]

**Supporting Evidence**:
- [Data, research, examples used]

**Framework/Model Presented**:
[Structured approach or mental model taught]

**Practical Applications**:
- [How to apply this knowledge]

**Further Learning**:
- [Resources or topics mentioned for deeper study]

Ignore: housekeeping, promotional content, filler stories.
```

### Commentary/Opinion

```
Analyze this commentary transcript and extract:

**Topic**: [What's being discussed]

**Speaker's Position**: [Main stance/opinion]

**Supporting Arguments**:
1. [Argument with reasoning]
2. [Argument with reasoning]
[Continue...]

**Counterarguments Addressed**:
- [Alternative view mentioned and response]

**Evidence/Examples**:
- [Specific cases or data cited]

**Conclusion/Call to Action**:
[Final takeaway or recommendation]

Ignore: channel promotion, sponsor mentions, personal stories that don't support the argument.
```

## Output Format Template

Always structure output with clear hierarchy:

```markdown
# [Video Title/Topic]

**Content Type**: [Tutorial/Interview/Lecture/Commentary]
**Main Focus**: [1-2 sentence summary]

---

## Key Learnings

[Use appropriate section headers based on content type pattern above]

---

## Notable Quotes

> "[Direct quote if particularly insightful]"
> — [Speaker/timestamp reference if available]

---

## Actionable Items

- [ ] [Concrete action viewer can take]
- [ ] [Tool to explore]
- [ ] [Concept to research further]
```

## Quality Checklist

Before finalizing output, verify:

- ✅ All promotional content removed
- ✅ Main points clear and concise
- ✅ No repetitive information
- ✅ Actionable insights highlighted
- ✅ Technical details preserved
- ✅ Logical flow maintained
- ✅ No filler language (um, uh, like, basically)

## Extended Thinking Guidance

For complex or lengthy transcripts (>5000 words), use extended thinking to:
1. First pass: Identify content type and main themes
2. Second pass: Extract key points per section
3. Third pass: Filter and consolidate, removing duplication
4. Final pass: Format and structure output

This prevents important details from being lost in long transcripts.
