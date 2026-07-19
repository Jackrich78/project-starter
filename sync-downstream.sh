#!/bin/bash
# Sync template infrastructure to a downstream project.
#
# Usage: ./sync-downstream.sh /path/to/downstream-project
#
# What it syncs:
#   .claude/hooks/              — full replace (template is source of truth)
#   .claude/commands/           — overwrite shared, preserve project-specific
#   .claude/agents/             — manifest-controlled: only files listed in
#                                 .claude/agents/.template-manifest are copied;
#                                 user *-specialist.md files are NEVER touched
#                                 (no --delete)
#   .claude/settings.template.json — reference file; diff against your live
#                                 settings.json and adopt manually
#
# What it NEVER syncs:
#   CLAUDE.md                   — always project-specific; update manually
#   .claude/settings.json       — never overwritten; adopt settings.template.json
#   .claude/settings.local.json — never synced (keep secrets there)
#   .claude/logs/               — project data, not template infra
#   docs/guides/                — not synced in v2.0; reach via re-clone / /setup
#
# Model-tier policy lives in CLAUDE.md (not synced). See CLAUDE.md § Model Defaults.
set -e

TARGET="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST="$SCRIPT_DIR/.claude/agents/.template-manifest"

if [ -z "$TARGET" ]; then
    echo "Usage: $0 /path/to/downstream-project"
    echo ""
    echo "Syncs template infrastructure from this template repo:"
    echo "  hooks/             → full replace"
    echo "  commands/          → overwrite shared, preserve project-specific"
    echo "  agents/            → manifest-controlled (no --delete)"
    echo "  settings.template.json → reference copy (settings.json never touched)"
    echo ""
    echo "CLAUDE.md, settings.json, settings.local.json, and docs/guides/ are NOT synced."
    exit 1
fi

if [ ! -d "$TARGET/.claude" ]; then
    echo "Error: $TARGET/.claude does not exist — is this a Claude Code project?"
    exit 1
fi

if [ ! -f "$MANIFEST" ]; then
    echo "Error: manifest not found at $MANIFEST"
    echo "Run 'python3 scripts/validate_manifest.py' to diagnose."
    exit 1
fi

# Check if target is a git repo (needed for review gate)
IS_GIT_REPO=false
if git -C "$TARGET" rev-parse --git-dir >/dev/null 2>&1; then
    IS_GIT_REPO=true
fi

echo "Syncing template infrastructure → $TARGET"

# Surface the template-version header so downstream users know which version
# updated their agents (satisfies AC-035-030)
TEMPLATE_VERSION=$(grep "^# template-version:" "$MANIFEST" | head -1)
if [ -n "$TEMPLATE_VERSION" ]; then
    echo "  $TEMPLATE_VERSION"
fi
echo ""

# ── Step 1: Hooks — full replace, no review needed (template is source of truth)
echo "→ .claude/hooks/ (full replace)"
rsync -av --delete --exclude='__pycache__' "$SCRIPT_DIR/.claude/hooks/" "$TARGET/.claude/hooks/"
echo ""

# ── Step 2: Commands — overwrite shared files, preserve project-specific
echo "→ .claude/commands/ (overwrite shared, preserve project-specific)"
rsync -av "$SCRIPT_DIR/.claude/commands/" "$TARGET/.claude/commands/"
echo ""

# ── Step 3: Agents — manifest-controlled copy (no --delete, preserves user agents)
echo "→ .claude/agents/ (manifest-controlled, no --delete)"
mkdir -p "$TARGET/.claude/agents"

# Copy the manifest itself so the downstream repo can run validate_manifest.py
cp "$MANIFEST" "$TARGET/.claude/agents/.template-manifest"

AGENT_COUNT=0
while IFS= read -r line; do
    # skip blank lines and comments
    [[ -z "$line" || "$line" == \#* ]] && continue
    SRC="$SCRIPT_DIR/.claude/agents/$line"
    if [ -f "$SRC" ]; then
        cp "$SRC" "$TARGET/.claude/agents/$line"
        echo "  copied: $line"
        AGENT_COUNT=$((AGENT_COUNT + 1))
    else
        echo "  WARNING: manifest lists '$line' but source file not found — skipping"
    fi
done < "$MANIFEST"
echo "  $AGENT_COUNT agent(s) synced from manifest"
echo ""

# ── Step 4: settings.template.json — reference copy (NEVER overwrite settings.json)
echo "→ .claude/settings.template.json (reference copy)"
cp "$SCRIPT_DIR/.claude/settings.template.json" "$TARGET/.claude/settings.template.json"
echo "  Diff against your live settings.json and adopt manually:"
echo "  diff $TARGET/.claude/settings.template.json $TARGET/.claude/settings.json"
echo ""

# ── Step 5: Review gate
# Scope: agents/ + settings.template.json + hooks/ (excludes docs/guides/ per D6)
if [ "$IS_GIT_REPO" = true ]; then
    AGENTS_DIFF=$(git -C "$TARGET" diff --stat .claude/agents/ 2>/dev/null || true)
    SETTINGS_TEMPLATE_DIFF=$(git -C "$TARGET" diff --stat .claude/settings.template.json 2>/dev/null || true)
    HOOKS_DIFF=$(git -C "$TARGET" diff --stat .claude/hooks/ 2>/dev/null || true)
    COMMANDS_DIFF=$(git -C "$TARGET" diff --stat .claude/commands/ 2>/dev/null || true)

    HAS_CHANGES=false
    if [ -n "$AGENTS_DIFF" ] || [ -n "$SETTINGS_TEMPLATE_DIFF" ] || \
       [ -n "$HOOKS_DIFF" ] || [ -n "$COMMANDS_DIFF" ]; then
        HAS_CHANGES=true
    fi

    if [ "$HAS_CHANGES" = true ]; then
        echo "=== CHANGES DETECTED ==="
        echo ""

        if [ -n "$AGENTS_DIFF" ]; then
            echo "--- .claude/agents/ (manifest-controlled) ---"
            echo "$AGENTS_DIFF"
            echo ""
        fi

        if [ -n "$SETTINGS_TEMPLATE_DIFF" ]; then
            echo "--- .claude/settings.template.json (reference) ---"
            echo "$SETTINGS_TEMPLATE_DIFF"
            echo ""
        fi

        if [ -n "$HOOKS_DIFF" ]; then
            echo "--- .claude/hooks/ ---"
            echo "$HOOKS_DIFF"
            echo ""
        fi

        if [ -n "$COMMANDS_DIFF" ]; then
            echo "--- .claude/commands/ ---"
            echo "$COMMANDS_DIFF"
            echo ""
        fi

        echo "Review commands:"
        echo "  cd $TARGET"
        echo "  git diff .claude/agents/ .claude/settings.template.json .claude/hooks/ .claude/commands/"
        echo ""
        echo "Reject a specific file:"
        echo "  git checkout -- .claude/agents/<file>"
        echo "  git checkout -- .claude/hooks/<file>"
        echo "  git checkout -- .claude/commands/<file>"
        echo ""
        read -p "Press Enter to continue (or Ctrl-C to abort) " </dev/tty
    fi

    echo ""
    echo "Sync complete."
    echo ""

    if [ "$HAS_CHANGES" = true ]; then
        echo "Next steps:"
        echo "  cd $TARGET"
        echo "  git diff .claude/   # full review"
        echo "  diff .claude/settings.template.json .claude/settings.json  # adopt new settings"
        echo "  git add .claude/ && git commit -m 'chore: sync template v2.0 hooks, agents, and settings'"
    else
        echo "No changes — target is already up to date."
    fi
else
    echo "WARNING: Target is not a git repo — no diff available."
    echo "         Files were synced but there is no undo. Verify manually."
    echo ""
    echo "Sync complete."
fi
