---
name: codebase-design
description: "Module-boundary and interface-depth analysis. Use when designing a new module, deciding where a seam goes, judging whether a module is too shallow, or when testability of an interface is in question, typically during /blueprint."
type: skill
---

Adapted from Matt Pocock's `codebase-design` skill, MIT, https://github.com/mattpocock/skills (see `NOTICE`).

# Codebase Design

## Context

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this vocabulary exactly while designing or restructuring code: leverage for callers, locality for maintainers, testability for everyone.

## Glossary

**Module**: anything with an interface and an implementation, at any scale (function, class, package, tier-spanning slice). *Avoid*: unit, component, service.
**Interface**: everything a caller must know: signature, invariants, ordering, error modes, required config, performance. *Avoid*: API, signature (too narrow).
**Implementation**: the body inside a module. Distinct from **Adapter**: a small adapter can hide a large implementation (a database repo) and the reverse (an in-memory fake).
**Depth**: behaviour a caller can exercise per unit of interface learned. **Deep** = large behaviour, small interface; **shallow** = interface nearly as complex as the implementation.
**Seam** (Michael Feathers): a place where behaviour can change without editing there; where a module's interface lives. *Avoid*: boundary (overloaded with DDD).
**Adapter**: a concrete thing satisfying an interface at a seam; names a role, not contents.
**Leverage**: what callers get from depth. **Locality**: what maintainers get: change, bugs and verification concentrate in one place.

## Pattern

1. **Ask of any interface:** fewer methods? simpler parameters? more complexity hidden inside?
2. **Apply the deletion test.** Imagine deleting the module. Complexity vanishes: pass-through. Complexity reappears across N callers: it earns its keep.
3. **Make the interface the test surface.** Callers and tests cross the same seam; wanting to test past it means the module is the wrong shape.
4. **Design for testability.** Accept dependencies, do not create them (`process_order(order, gateway)`). Return results, not side effects. Keep the surface small.
5. **Place seams honestly.** One adapter = hypothetical seam; two (usually production plus test) = real. Internal seams stay private to the implementation.
6. **Deepen a cluster by dependency category:**
   - *In-process* (pure, in-memory): merge, test through the new interface.
   - *Local-substitutable* (fake filesystem, in-memory db): test with the stand-in; seam stays internal.
   - *Remote but owned*: define a port at the seam, production and in-memory adapters.
   - *True external* (third-party API): inject as a port, mock adapter in tests.
7. **Replace tests, do not layer them.** Delete old unit tests on the shallow modules once interface-level tests exist. Assert observable outcomes; tests must survive internal refactors.
8. **Design it twice, only when it earns its cost:** the module touches two or more external systems, or `challenger` flagged a design disagreement you cannot settle inline. Otherwise design once.
   - Frame constraints, dependencies (with category) and a rough sketch for the human; they read while agents work.
   - Spawn 3+ sub-agents in parallel with separate briefs, each a radically different interface: minimal (1-3 entry points), maximally flexible, optimised for the commonest caller, ports-and-adapters.
   - Each returns interface (with invariants and errors), usage example, what is hidden, dependency strategy, trade-offs.
   - Present sequentially, compare by depth, locality and seam placement, then give one opinionated recommendation or hybrid. Agent output is a claim, not a fact: briefs-only agents give framing agreement, not validation.

## Example

Three tiny modules `parse_header`, `validate_header`, `normalise_header` each have callers calling all three in order. Deletion test: merge them into `read_header(raw) -> Header | Error`; the ordering knowledge now lives once. Tests move to `read_header`; the three old unit tests are deleted.

## Anti-patterns

- Depth as an implementation-to-interface line ratio: it rewards padding. Depth here is leverage.
- A port with one adapter: indirection, not a seam.
- Exposing internal seams through the interface because tests use them.
- Saying "boundary", "service" or "component": inconsistent words dissolve the model.
- Running design-it-twice on every module decision.
