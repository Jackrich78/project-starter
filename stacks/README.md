# Stacks

Pre-configured scaffolding for specific deployment targets. Each stack extends the base harness with platform-specific agents, configuration, and boilerplate.

## Available Stacks

| Stack | Description | Status |
|-------|-------------|--------|
| [cloudflare](cloudflare/) | Cloudflare Workers, D1, R2, KV, Queues | Complete |

## How to Use a Stack

There are two workflows depending on what you need:

### Option A: Full Harness + Stack (Recommended)

Get the complete AI workflow (commands, agents, hooks) plus the stack:

```bash
# 1. Clone entire repo (trailing dot copies hidden files)
mkdir my-project
cp -r /path/to/project-starter/. my-project/
cd my-project

# 2. Merge stack to root
cp -r stacks/cloudflare/* .
cp -r stacks/cloudflare/.claude/agents/* .claude/agents/
cp stacks/cloudflare/.gitignore .
cp stacks/cloudflare/.dev.vars.example .

# 3. Clean up (REQUIRED - prevents duplicate tests)
rm -rf stacks/ spikes/

# 4. Fresh install
rm -rf node_modules package-lock.json
npm install

# 5. Verify
npm test  # 59 tests should pass
```

### Option B: Stack Only

Just the worker code without the AI harness:

```bash
mkdir my-project && cd my-project
cp -r /path/to/project-starter/stacks/cloudflare/* .
cp -r /path/to/project-starter/stacks/cloudflare/.* . 2>/dev/null
npm install
npm test
```

> **Note:** Each stack includes its own detailed README with setup instructions.

### Future: GitHub Templates

We plan to publish separate GitHub templates:
- `project-starter` - Base harness only
- `project-starter-cloudflare` - Base + Cloudflare stack

This will allow one-click project creation.

## Contributing a Stack

Want to add support for another platform? Follow this pattern:

### Directory Structure

```
stacks/your-stack/
├── README.md              # Setup instructions
├── .claude/
│   └── agents/
│       └── your-stack-specialist.md  # Domain expert agent
├── src/                   # Boilerplate code
├── package.json           # Stack dependencies (if applicable)
└── [config files]         # Platform-specific config
```

### Requirements

1. **README.md** — Clear setup instructions
2. **Specialist Agent** — Domain expert for the platform (`.claude/agents/your-stack-specialist.md`)
3. **Minimal Boilerplate** — Just enough to get started, not a full application
4. **Config Templates** — Platform configuration with sensible defaults
5. **Merge-safe structure** — Your directory layout must mirror the project root. When a user runs `cp -r stacks/your-stack/* .`, files must land in the correct locations. For example, `.claude/agents/` inside your stack merges into the project's `.claude/agents/`.

### Contribution Process

1. Fork the repository
2. Create your stack in `stacks/your-stack/`
3. **Verify the merge:** from the project root, run `cp -r stacks/your-stack/* .` and confirm files land correctly (agents in `.claude/agents/`, config at root, src in `src/`)
4. Test the full workflow: merge, `rm -rf stacks/`, `npm install`, `npm test`
5. Submit a PR with description of what the stack provides

## Design Rationale

### Why merge-to-root?

We evaluated five patterns for managing deployment variants alongside a shared base harness: separate repos, git branches, git submodules, a CLI scaffolder, and a monorepo with variant directories. (Full analysis: [template-structure-research](../docs/research/template-structure-research.md), [sync strategies](../docs/research/template-sync-strategies-2026-02-06.md).)

The **merge-to-root** pattern was chosen:

1. **Monorepo-inspired, simplified.** Like Create-T3-App and Turborepo, everything lives in one repo. But instead of keeping `base/` and `stacks/` side-by-side permanently, users merge the stack into the root and discard the rest. One clone, one merge, done.

2. **No path indirection.** The harness (agents, commands, hooks, skills) uses relative paths extensively — `../../docs/templates/`, `../agents/README.md`, etc. Nesting the harness inside a `base/` subdirectory would break every relative path in every agent, command, and skill file. Keeping the harness at the project root avoids this entirely.

3. **Stacks are additive, not compositional.** A stack adds platform-specific files (specialist agents, config, boilerplate src/) without modifying any core harness file. After merging, the stack files coexist with the harness. No conflicts, no overrides.

4. **Delete after merge.** Once merged, `stacks/` serves no purpose and its test files would conflict with the project's own tests. The `rm -rf stacks/` step is required cleanup, not optional tidying.

### Properties of a well-designed stack

- **Self-contained** — all files needed in one directory
- **Minimal** — just enough to get started, not a full application
- **Well-documented** — clear setup instructions and platform guidance
- **Additive** — no modifications to base harness files required
- **Merge-safe** — file structure mirrors the project root so `cp -r stacks/your-stack/* .` lands files in the correct locations
