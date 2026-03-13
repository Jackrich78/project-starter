# Feature Documentation

Per-feature documentation lives here. Each feature gets its own subdirectory.

## Structure

```
docs/features/
└── FEAT-001_your-feature-name/
    ├── README.md      — Feature overview, status, acceptance criteria links
    ├── prd.md         — Product requirements (problem, goals, scope)
    └── plan.md        — Implementation plan (tasks, dependencies, approach)
```

## Creating a Feature

```bash
/explore [topic]          # Discover and define → creates prd.md
/blueprint FEAT-001       # Technical plan → creates plan.md
/build FEAT-001           # TDD implementation
```

## Naming Convention

`FEAT-XXX_short-description/` where `XXX` is a zero-padded number (001, 002, ...).

Features are created and managed by the `/explore`, `/blueprint`, and `/build` commands.
