---
type: template
title: "Close-out comment"
description: "The six-line gate 2 hand-off posted on an issue when the PR opens; /retro harvests the Learned line."
---

Post with `gh issue comment N --body-file <file>` when the PR opens (after the push in `direct` mode). Signature on line 1. See `docs/system/issue-flow.md` § Close-out comment.

```markdown
Shipped: <commit SHA, or PR number in pr mode>
Proof: <fenced command output, or the artifact for non-code work>
How to test: <the commands or clicks that let the human check it>
Decided: <each call made without asking, with the option rejected, or "none">
Not covered: <what this does not prove>
Learned: <one line and where it was filed, or "nothing new">
```

- **Shipped:** the exact commit or PR that closed the issue, so the claim can be checked.
- **Proof:** real output from this turn, not a description of output.
- **How to test:** what the human does at gate 2; a live surface gets its steps here.
- **Decided:** the calls the agent made between the gates, so the human can overrule one.
- **Not covered:** the honest gap: untested paths, unchecked live behaviour.
- **Learned:** what the next reader should know that is not in the code; file it (wiki, decisions) and say where.
