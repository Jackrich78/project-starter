# Customizing CI Workflows

## Current Workflows

- `validate.yml` - Base validation (markdown, YAML, Python hooks)
- `stack-cloudflare.yml` - Stack-specific tests (path-filtered)

## To Add Language-Specific Validation

Edit `validate.yml` and add after line 60 (marked with `# CUSTOMIZATION:`):

```yaml
# TypeScript type checking
- name: TypeScript Check
  run: npx tsc --noEmit

# ESLint
- name: Lint TypeScript
  run: npx eslint .
```

## Use ci-validation Skill

Run locally before pushing:

```bash
# Validates workflows, runs checks locally
actionlint .github/workflows/*.yml
```

See `.claude/skills/ci-validation/` for full guide.
