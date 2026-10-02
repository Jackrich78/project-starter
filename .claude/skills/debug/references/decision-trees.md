# Debug decision trees

Read from `SKILL.md` step 1 (classification and severity) and when choosing agents.

## Bug type

```
Stack trace or error from a call to another service, API, database?  -> INTEGRATION FAILURE
Slower, more memory, more queries than before?                       -> PERFORMANCE REGRESSION
Test fails (flaky, broken assertion, environment)?                   -> TEST FAILURE
Wrong output, wrong branch, off-by-one, wrong rendering?             -> LOGIC BUG (UI bugs: "LOGIC BUG (UI)")
```

| Type | Typical root causes | Typical fix |
|---|---|---|
| Logic | wrong conditional, off-by-one, bad assumption about input | fix the logic, regression test at unit level |
| Integration | contract changed, config mismatch, expired credential, timeout | match the contract, add an integration test, document the contract |
| Performance | N+1 query, missing index, unbounded loop, leak | measure first, fix the hot spot, add a budget check |
| Test failure | shared state, timing, environment drift, stale fixture | fix the cause (inject the clock, isolate state); never just retry |

## Severity

| Level | Meaning | Example |
|---|---|---|
| P0 | production down, data loss, security breach | auth bypass |
| P1 | major function broken, users blocked | checkout fails |
| P2 | partially broken, workaround exists | wrong total on one path |
| P3 | minor or cosmetic, edge case | misaligned label |
| P4 | trivial, no user impact | typo in log |

P0 and P1 always get a `qa-reviewer` pass.

## Scope

```
Tied to one issue or feature area?  -> load that issue and its code
Cross-cutting or infrastructure?    -> load PROJECT.md and docs/system/
```

## Agent coordination

```
Unfamiliar library, cryptic error, third-party behaviour  -> researcher
Several fix approaches, or blast radius > 5 files         -> challenger
P0/P1, auth, data handling, API contract change           -> qa-reviewer
Fix changes documented behaviour or cross-references      -> librarian
Always: pick the regression test level                    -> test-strategy
```

## Regression test routing (via test-strategy)

| Bug | Level |
|---|---|
| pure logic, handler, hook | `tdd` unit |
| styling or rendering | `component-test` |
| interaction flow | `e2e` |
| API-to-DB, middleware | `integration` |
| responsive layout | `component-test` at several viewports |

## UI bug investigation checklist

For a LOGIC BUG (UI):

1. **Styling:** computed styles in DevTools; specificity conflicts (`!important`, inline); class names actually applied; utility-class conflicts; media-query breakpoints.
2. **Component:** props and state in the framework DevTools; hook dependency arrays; needless re-renders; conditional rendering; event bindings.
3. **Layout:** check 320, 768, 1024, 1920 px; viewport meta tag; relative units; flex and grid container and item properties; horizontal scroll on mobile.
4. **Evidence:** screenshot the bug and the expected state; note browser, OS, viewport. With a browser automation tool available, capture across viewports and read computed styles programmatically.
5. **Cross-browser:** Chrome, Firefox, Safari (WebKit, iOS), a mobile browser.
