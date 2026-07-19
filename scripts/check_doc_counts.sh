#!/usr/bin/env bash
# check_doc_counts.sh — warn when hand-written agent/command/skill counts in
# docs drift from the real directories. Non-blocking by design (exit 0 always;
# pass --strict to exit 1 on drift, e.g. for a release pre-check).
#
# Motivation: the v2.0.0 release (2026-07-19) corrected the same counts three
# times across five files. Counts asserted in prose rot; directories don't.
#
# Convention (matches how the docs have historically counted):
#   agents   = .claude/agents/*.md minus README.md and TEMPLATE.md
#   commands = .claude/commands/*.md   (public-facing docs exclude demo.md)
#   skills   = .claude/skills/*/ dirs containing a SKILL.md, minus the
#              personal/brand skills listed in .github/public-exclude.txt
#              (public-facing docs count only shipped skills)

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

agents=$(find .claude/agents -maxdepth 1 -name '*.md' ! -name 'README.md' ! -name 'TEMPLATE.md' | wc -l | tr -d ' ')
commands_all=$(find .claude/commands -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
commands_public=$commands_all
[[ -f .claude/commands/demo.md ]] && commands_public=$((commands_all - 1))

skills_public=0
for d in .claude/skills/*/; do
  name="${d#.claude/skills/}"; name="${name%/}"
  [[ -f "$d/SKILL.md" ]] || continue
  if grep -qx "\.claude/skills/$name" .github/public-exclude.txt 2>/dev/null; then
    continue
  fi
  skills_public=$((skills_public + 1))
done

echo "actual: agents=$agents commands(public)=$commands_public skills(public)=$skills_public"

DRIFT=0
check() {
  # check <file> <regex-with-COUNT-placeholder> <expected> <label>
  local file="$1" regex="$2" expected="$3" label="$4"
  [[ -f "$file" ]] || return 0
  local found
  found=$(grep -oE "$regex" "$file" | grep -oE '[0-9]+' | head -1)
  [[ -z "$found" ]] && return 0
  if [[ "$found" != "$expected" ]]; then
    echo "DRIFT: $file says $found $label, actual is $expected"
    DRIFT=1
  fi
}

for f in README.md PROJECT.md CHANGELOG.md docs/guides/skills-reference.md; do
  check "$f" '[0-9]+ skills' "$skills_public" "skills"
done
for f in README.md PROJECT.md docs/guides/commands-reference.md; do
  check "$f" '[0-9]+ (workflow )?commands' "$commands_public" "commands"
done
for f in README.md PROJECT.md docs/system/connections.md; do
  check "$f" '[0-9]+ (specialized )?agents' "$agents" "agents"
done

if [[ "$DRIFT" -eq 0 ]]; then
  echo "OK: doc counts match the directories."
else
  echo "note: fix the docs or update this script's conventions if counting rules changed."
  $STRICT && exit 1
fi
exit 0
