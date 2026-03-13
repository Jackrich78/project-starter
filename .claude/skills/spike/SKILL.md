---
name: spike
description: Time-boxed technical investigation to reduce uncertainty and validate approaches before committing to implementation. Use when (1) user invokes /spike [topic], (2) agent detects high uncertainty during /explore or /blueprint, (3) PRD contains "Requires spike" note, (4) team confidence in approach is <50%, or (5) multiple viable solutions exist and proof-of-concept needed. Guides through full lifecycle: initiate, execute, extract learnings, cleanup.
---

# Spike Skill

Time-boxed technical investigations that validate approaches before committing to full implementation. Spikes answer "should we do this?" and "how should we do this?" questions.

**Key principle:** Spikes are temporary code that generates permanent knowledge.

## When to Spike

### Decision Checklist

**Use spike when ALL apply:**
- [ ] Question is narrow and testable ("Does X work with Y?" not "How does X work?")
- [ ] Team confidence <50% (high uncertainty)
- [ ] Risk of wrong approach is significant (rework >20% of feature effort)
- [ ] Investigation fits in <8 hours
- [ ] Won't consume >5-10% of release budget

**Don't spike when ANY apply:**
- [ ] Answer exists in documentation (read first)
- [ ] Question is too broad (>8h → needs Prototype/MVP/Research Project)
- [ ] Team confidence >70% (just build it)
- [ ] Low pivot cost (easy to change later)
- [ ] Goal is procrastination disguised as "research"

### Spike vs Other Investigation Types

| Investigation | Duration | Output | Use When |
|---------------|----------|--------|----------|
| **Spike** | 2-8 hours | Throwaway code + research doc | Validate specific technical approach |
| **Prototype** | Days | Working demo (may keep) | Demonstrate feasibility to stakeholders |
| **MVP** | Weeks | Shippable product | Test market fit with real users |
| **Design Sprint** | 5 days | User-validated design | Understand user needs before building |
| **Research Project** | Open-ended | Formal research | Strategic technology evaluation |

## Interactive Workflow

This skill guides through four phases interactively.

### Phase 1: Initiate

**1. Define the question:**
```
What specific technical uncertainty needs validation?

Examples of GOOD questions:
- "Does npm workspaces work with Wrangler bundling?"
- "Can D1 handle 10k concurrent reads with <200ms latency?"
- "Does our auth module work with Lambda@Edge?"

Examples of BAD questions:
- "Explore authentication" (too vague)
- "How should we architect the backend?" (too broad)
- "Make a proof-of-concept" (says how, not why)
```

**2. Set time box:**
- Simple validation: 2-4 hours
- Complex integration: 4-6 hours
- Architecture exploration: 6-8 hours max
- **If >8 hours needed:** Split into smaller questions

**3. Define success/failure criteria:**
```
Success: [What validates the approach works]
Failure: [What indicates we should stop/pivot]
```

**4. Create spike structure:**

```bash
# Create spike directory
mkdir -p spikes/spike-[topic]-$(date +%Y%m%d)
cd spikes/spike-[topic]-$(date +%Y%m%d)
```

Create two files using templates from `references/`:
- `FINDINGS.md` - Running notes (REQUIRED) - see references/findings-template.md
- `README.md` - Context & goals - see references/readme-template.md

### Phase 2: Execute

**1. Write minimal code:** Only what's needed to validate the question

**2. Document continuously:** Update FINDINGS.md as you discover (not at the end)

**3. Note gotchas immediately:** Don't rely on memory

**4. Stay time-boxed:** Set a timer. Stop when time's up regardless of completion.

### Phase 3: Extract Learnings (REQUIRED)

**When spike completes (success, failure, OR time expired), extract findings to permanent documentation.**

#### Time Expiration Handling

Regardless of completion status, make a decision:

**Complete (Approach Validated):**
- Extract findings to research doc
- Update PRD/plan with validated approach
- Proceed to implementation

**Incomplete (Partial Results):**
- Document partial findings (don't discard)
- Analyze: is question answerable with more time or too broad?
- Options:
  - Proceed with qualified confidence ("works but requires X")
  - Schedule follow-up spike with narrower scope
  - Pivot to different approach

**Failed (Proves Infeasibility):**
- Document WHY approach failed (critical for team learning)
- Identify alternative from spike learnings
- This is SUCCESS - you prevented wasted development time

#### Create Research Document

**Location:** `docs/features/FEAT-XXX_[name]/research-spike-[topic]-[timestamp].md`

**Structure:**
```markdown
# Spike Research: [Topic]

**Date:** YYYY-MM-DD
**Spike Location:** spikes/spike-[topic]-[timestamp]/
**Duration:** X hours (of Y budgeted)
**Outcome:** Success | Partial | Failed

## Objective
What we were validating

## Findings

### What Worked
- Key discoveries
- Validated approaches

### What Didn't Work
- Failed approaches
- Blockers encountered

### Gotchas & Edge Cases
- Unexpected issues
- Workarounds needed

## Recommendation
- [ ] Proceed with approach
- [ ] Proceed with modifications: [specify]
- [ ] Do not proceed, use alternative: [specify]

## Implementation Notes
Guidance for actual implementation based on spike learnings

## References
- Spike code location (before cleanup)
- External documentation consulted
```

**Update feature documentation:**
- Link research doc in `docs/features/FEAT-XXX/README.md`
- Update handover.md with key findings
- Update PRD with validated technical decisions

### Phase 4: Cleanup

**When to clean up:**
- Feature fully implemented and shipped
- Spike resulted in "do not proceed" (cleanup immediately)
- Spike superseded by another spike (keep latest only)

**Process:**
```bash
# 1. Verify research doc exists
ls docs/features/FEAT-XXX/research-spike-[topic]-*.md

# 2. Verify link in feature README
grep "research-spike-[topic]" docs/features/FEAT-XXX/README.md

# 3. Delete spike directory
rm -rf spikes/spike-[topic]-[timestamp]/

# 4. Commit cleanup
git rm -rf spikes/spike-[topic]-[timestamp]/
git commit -m "chore: clean up spike after FEAT-XXX implementation"
```

**IMPORTANT:** Never delete spike code until research doc is created and linked.

## Success Metrics

Measure spike success with four metrics:

| Metric | Good | Bad |
|--------|------|-----|
| **Time-to-Decision** | Within time-box | >40 hours |
| **Knowledge Gain** | Team understanding +70% | <20% improvement |
| **Risk Reduction** | Confidence +30-50% | No change or decreased |
| **Estimation Convergence** | Story estimates align | Estimates diverge |

**Reframing "Failure":** A spike that proves an approach doesn't work is SUCCESS if it prevents wasted development time.

## Integration with Feature Workflow

### During /explore
If exploration identifies need for spike:
1. Note in PRD: "Requires spike: [topic]"
2. Agent suggests `/spike` before `/plan`

### During /blueprint
Agent checks for spike indicators:
- High-risk technical decisions
- Multiple viable approaches unclear
- Third-party integration uncertainty

If detected, agent suggests: "This appears to have high uncertainty. Consider `/spike [topic]` before planning implementation."

### After /blueprint
Agent reads existing research docs:
```bash
ls docs/features/FEAT-XXX/research-*.md
```
If spike research exists, incorporate learnings into plan.

### During /build
Spike code is **reference only**, not copy-paste:
- Understand patterns from spike
- Implement properly with tests, error handling, documentation
- Spike proved concept; implementation makes it production-ready

## Functional Spikes (Non-Technical)

Use for non-code investigations:
- User behavior and interaction patterns
- Business requirement clarification
- Domain/industry best practices
- Competitive analysis

Same structure, but:
- Validate with users/stakeholders instead of code
- Document findings as written analysis
- Examples: mockups, user interviews, competitor comparison

## Researcher Agent Integration

If spike reveals open questions requiring deeper research:

```
Task(
  subagent_type="researcher",
  description="Research post-spike questions for FEAT-XXX",
  prompt="Based on spike findings in spikes/spike-[topic]-[timestamp]/, research:
  1. [Question raised by spike]
  2. [Question raised by spike]

  Context from spike:
  - What we validated: [summary]
  - Key discovery: [main finding]
  - Open questions: [what spike couldn't answer]

  Feature folder: docs/features/FEAT-XXX_[name]/
  Create: research-spike-[topic]-[timestamp].md"
)
```

## Validation Checklist

Before proceeding from spike:

- [ ] FINDINGS.md created and continuously updated
- [ ] Success/failure criteria defined in README.md
- [ ] Research doc created in feature folder
- [ ] Research doc follows template structure
- [ ] Feature README.md links to research doc
- [ ] Handover.md references key findings (if applicable)
- [ ] PRD updated with validated decisions (if applicable)
- [ ] No orphaned spikes (all have research docs)

## Anti-Patterns

### Spike Trap (Scope Creep)
```
Initial: "Does npm workspaces work with Wrangler?"
Discovery: "Yes, but config is tricky"
New Question: "How do we handle env-specific configs?"
...time expires with 20% complete
```
**Prevention:** Treat new questions as separate spike candidates. Use time-box as forcing function.

### Documentation Inertia
Spike completes, documentation happens "later" (never).
**Prevention:** Research doc creation is gate for proceeding.

### Spike as Procrastination
Vague question, repeatedly extended time-box.
**Prevention:** Require testable success criteria upfront.

### Copy-Paste Implementation
Spike code copied directly into feature.
**Prevention:** Spike is reference only. Reimplement with tests.

### Spike Accumulation
Spikes never cleaned up, become technical debt.
**Prevention:** Cleanup when feature ships.

## Examples

### Example 1: Technology Validation
```
Topic: npm-workspaces-wrangler
Question: Do npm workspaces work with Wrangler bundling?
Time box: 6 hours
Outcome: Success
Research doc: research-spike-npm-workspaces-20260125.md
Cleanup: After FEAT-013 ships
```

### Example 2: Performance Validation
```
Topic: d1-query-performance
Question: Can D1 handle 10k concurrent reads with <200ms?
Time box: 4 hours
Outcome: Partial - found limits, documented workarounds
Research doc: research-spike-d1-performance-20260201.md
Cleanup: After FEAT-014 ships
```

### Example 3: Failed Validation
```
Topic: webrtc-workers
Question: Can Workers handle WebRTC signaling?
Time box: 4 hours
Outcome: Failed - Workers can't maintain persistent connections
Recommendation: Use Durable Objects instead
Cleanup: Immediate (after research doc created)
```

## Resources

- `references/findings-template.md` - FINDINGS.md template
- `references/readme-template.md` - Spike README.md template
