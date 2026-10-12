# Scaffold Validation Tests

These tests validate the STARTER structure itself, not your code.

**Purpose:** Ensure project-starter maintains correct structure

## What's Tested

- `.github/workflows/validate.yml` exists and has required steps
- Required files exist (CLAUDE.md, PROJECT.md, etc.)
- Workflow syntax is valid (via validate-workflow.test.ts)

## For Your Project

You can extend these tests OR delete this directory entirely. If you delete it, remove `postinstall` from the root `package.json` and change `test` to `node scripts/run_pytest_optional.mjs`, or root `npm ci` / `npm test` will fail.
Your feature tests go in `/test/unit/`, not here.

## Running These Tests

From the repo root (`postinstall` installs this directory's dependencies):

```bash
npm ci && npm test
```
