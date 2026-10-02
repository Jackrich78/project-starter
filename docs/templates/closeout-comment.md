---
type: template
title: "Close-out comment"
description: "The four-line comment posted on an issue after it closes; /retro harvests the Learned line."
---

Post with `gh issue comment N --body-file <file>`. Start with the agent signature from CLAUDE.md `## Workflow`. See `docs/system/issue-flow.md` § Close-out comment.

```markdown
Shipped: <commit SHA, or PR number in pr mode>
Proof: <fenced command output, or the artifact for non-code work>
Not covered: <what this does not prove>
Learned: <one line and where it was filed, or "nothing new">
```

- **Shipped:** the exact commit or PR that closed the issue, so the claim can be checked.
- **Proof:** real output from this turn, not a description of output.
- **Not covered:** the honest gap: untested paths, unchecked live behaviour.
- **Learned:** what the next reader should know that is not in the code; file it (wiki, decisions) and say where.
