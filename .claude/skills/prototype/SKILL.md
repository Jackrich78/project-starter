---
name: prototype
description: "Build a throwaway clickable prototype to answer one logic or concept question. Use on \"prototype this\", \"let me click through it\", \"does this state machine handle X then Y\", \"feel out this workflow or pricing model before we build it\". Single-file HTML, no install."
type: skill
disable-model-invocation: true
---

Adapted from Matt Pocock's `prototype` skill, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# Prototype

## Context

A prototype is **throwaway code that answers a question**. This skill covers the logic shape only: a single-file HTML demo where someone presses buttons and watches a state model change. Use it for business logic, state transitions or data shape that looks fine on paper. Visual UI exploration is out of scope. For broader technical unknowns use `spike`.

## Pattern

1. **State the question** in a visible intro on the page (not just a comment): which state model, which question. A prototype answering the wrong question is pure waste.
2. **Isolate the logic in a pure module** inside one `<script>`: a reducer `(state, action) => state`, a state machine, a set of pure functions, or a class with a clear method surface. No DOM inside it; the page calls in, never the reverse.
3. **Build one shareable HTML file**: plain HTML/CSS/JS, everything inline, opens by double-click. Domain language on every label, for a non-developer. Layout top to bottom:
   - title and one-line question;
   - current state as a labelled panel, re-rendered after every click, with what just changed called out;
   - free-play buttons, one per action, always available;
   - guided walkthroughs, one per tab: scenario description plus ordered buttons to press; start resets to a known state. Pick the awkward cases: happy path, tricky edge, something that should be illegal.
   - restrained styling, one accent colour, no animation.
4. **Hand it over** and wait. "Wait, that shouldn't be possible" is a bug in the idea, which is the point. Add actions or scenarios on request.
5. **Capture the answer.** Lift the validated pure module into the real code. Record the verdict and the question it settled in `docs/decisions.md` (or on the issue). Park the HTML on a throwaway branch with a pointer, or delete it; the working branch keeps only the decision.

Ground rules: name and place the file so it reads as a prototype; state lives in memory (persistence is what you would be checking, not depending on); no tests, no error handling beyond runnable.

## Example

Question: "Can a subscription be paused after cancellation is scheduled?" Reducer with states `active | cancelling | paused | ended`; buttons Pause, Cancel, Resume, Tick month; tab "Cancel then pause" shows the illegal move being refused. Reviewer clicks it, says "pause should extend the end date", decision logged, reducer lifted into `billing/`.

## Anti-patterns

- Adding tests: a prototype needing tests is no longer a prototype.
- Wiring to the real database: use memory unless persistence is the question.
- Generalising ("what if we later support X"): one question only.
- Letting the logic reference the DOM: it stops being liftable.
- A framework, bundler or server: defeats "double-click and share".
- Shipping the HTML shell to production: the logic module is the keeper.
