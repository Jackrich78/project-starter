# Contributing to Project Starter

Thanks for your interest in contributing! This template uses its own workflow commands for development.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/jackrich78/project-starter.git
   cd project-starter
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

This template is designed for AI-assisted development with Claude Code. Use the built-in commands:

```bash
/explore [topic]    # Discover and plan a new feature
/blueprint FEAT-XXX  # Create implementation plan
/build FEAT-XXX     # Implement with TDD
/commit             # Git workflow with conventional commits
```

### For Template Improvements

1. **New agents** - Add to `.claude/agents/` following `TEMPLATE.md`
2. **New commands** - Add to `.claude/commands/`
3. **Documentation** - Update relevant files in `docs/`

## Code Style

This template is stack-agnostic. When contributing:

- Follow existing patterns in the codebase
- Keep markdown files under 500 lines where possible
- Use conventional commits (see below)

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new /status command
fix: correct file path in researcher agent
docs: update architecture documentation
chore: update .gitignore patterns
```

## Pull Request Process

1. Ensure your changes work with the template workflow
2. Update documentation if adding new features
3. Keep PRs focused on a single change
4. Fill out the PR template with a clear description

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about contributing

---

Thank you for helping improve Project Starter!
