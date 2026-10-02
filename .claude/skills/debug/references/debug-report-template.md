# Debug close-out template

Post this as the closing comment on the bug's issue (`gh issue comment N --body-file <file>`), or in the commit body when no issue exists. Keep it under one screen. A bug fix without a regression test is not closed.

```markdown
## Debug close-out

**Symptom:** <what the user saw, expected vs actual>
**Type / severity:** <logic | integration | performance | test failure> / <P0-P4>

**Root cause:** <file:line and why; one or two sentences>
**Why it slipped through:** <missing test, wrong assumption, untested path>
**Blast radius:** <other callers or features checked, and the result>

**Fix:** <what changed, in one or two sentences; commit link>
**Regression test:** `<path>::<name>`, seen red before the fix
**Validation:** <suite result, smoke test, perf before/after, qa-reviewer verdict if run>

**Docs updated:** <paths, or "none, behaviour unchanged">
**Learned:** <one line a future debugger would want>
```

## Filled example

```markdown
## Debug close-out

**Symptom:** Reorder showed total 81 instead of 90 after a 10% promo.
**Type / severity:** logic / P2

**Root cause:** `checkout.py:88` re-applied the promo to the already discounted stored price.
**Why it slipped through:** reorder had no test; the promo test covered first orders only.
**Blast radius:** `calc_total` has two callers; the cart path is correct.

**Fix:** apply promo to list price only (commit abc1234).
**Regression test:** `tests/unit/orders/test_totals.py::test_reorder_discount_applied_once`, seen red (81 != 90)
**Validation:** full suite green; manual reorder shows 90.

**Docs updated:** none, behaviour unchanged.
**Learned:** stored prices are post-discount; derive totals from list price.
```
