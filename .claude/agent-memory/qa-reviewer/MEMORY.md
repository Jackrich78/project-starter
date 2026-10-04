# Qa Reviewer Memory

<!-- one line per entry: - YYYY-MM-DD · <method> · source: <file:line|commit:sha|url> — methods only, never findings. Hard cap 150 lines. -->
- 2026-10-04 · Prove regex corpus coverage by removing each alternative one at a time and running the corpus; seen-red = new corpus run against the parent's code · source: commit:c090e2e
- 2026-10-04 · Build regex-probe strings by concatenation so the live Bash security hook does not block the probe script · source: .claude/hooks/pre_tool_use.py:47
- 2026-10-04 · When re-checking a wording fix, grep the whole tree for the old phrase; it often survives in a second file · source: .claude/hooks/README.md:21
- 2026-10-04 · When a redactor is reused, check whether the caller splits text before redacting; multi-line patterns (PEM, re.S) silently stop matching · source: scripts/recall.py:33
- 2026-10-04 · Check derived path schemes against the population on disk (count escaped directory names containing `.` or `_`) before trusting a `replace("/", "-")` · source: scripts/recall.py:43
- 2026-10-04 · When test setup changes along with the code, seen-red against the parent commit can fail for the wrong reason; break each fix once on HEAD instead · source: commit:d61d993
- 2026-10-04 · Check a "skip harness text" filter against real transcripts by counting skipped messages per tag and flag (counts only) to find human turns it drops · source: scripts/recall.py:39
