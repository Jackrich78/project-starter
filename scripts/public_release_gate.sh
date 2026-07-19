#!/usr/bin/env bash
# public_release_gate.sh — blocking PII / personal-content gate for public releases.
#
# Run against the FILTERED export tree produced by the two-remote-sync release
# process (docs/guides/two-remote-sync.md), i.e. after git archive + the
# public-exclude.txt pass, and BEFORE pushing to the public remote.
#
# Usage:
#   scripts/public_release_gate.sh <path-to-filtered-tree>
#
# Checks:
#   1. Content patterns from .github/pii-patterns.txt (grep -rInE, one regex
#      per line).
#   2. File-type/path rules: handover.md, *.bak, agent.db*, .env*, _archive
#      paths, workspace/, demos/, and raster images outside approved dirs.
#
# Every hit must be waived in .github/release-waivers.txt (format:
# `path:pattern-or-rule # reason`) or the script exits non-zero. There is no
# bypass flag — waivers are the only way through, and every applied waiver is
# printed on every run so suppressions stay visible.
#
# Exit 0 + one-line OK summary only when there are zero un-waived hits.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PATTERNS_FILE="$REPO_ROOT/.github/pii-patterns.txt"
WAIVERS_FILE="$REPO_ROOT/.github/release-waivers.txt"

# Raster images are only expected in these dirs (relative to tree root).
# Adjust if the repo's diagram/asset conventions change.
APPROVED_IMAGE_DIRS=(
  "docs/system/diagrams/"
)

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <path-to-filtered-tree>" >&2
  exit 2
fi

TREE="${1%/}"
if [[ ! -d "$TREE" ]]; then
  echo "error: '$TREE' is not a directory" >&2
  exit 2
fi
if [[ ! -f "$PATTERNS_FILE" ]]; then
  echo "error: patterns file not found: $PATTERNS_FILE" >&2
  echo "       copy .github/pii-patterns.example.txt to .github/pii-patterns.txt and fill in your own tokens (it is maintainer-private and excluded from the public snapshot)." >&2
  exit 2
fi

UNWAIVED_COUNT=0
WAIVED_COUNT=0

# is_waived <relpath> <pattern-or-rule-id>
# Prints the waiver line (with reason) and returns 0 if waived; returns 1
# otherwise. Waiver matching is exact: relpath and pattern-or-rule-id must
# match the waiver line's path/key exactly (split on the first ':').
is_waived() {
  local relpath="$1" key="$2"
  [[ -f "$WAIVERS_FILE" ]] || return 1
  local line wline wkey_and_reason wkey reason
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    # Split off trailing "# reason" comment.
    reason="${line#*#}"
    wline="${line%%#*}"
    wline="$(echo -n "$wline" | sed -e 's/[[:space:]]*$//')"
    [[ "$wline" != *:* ]] && continue
    wpath="${wline%%:*}"
    wkey="${wline#*:}"
    wkey="$(echo -n "$wkey" | sed -e 's/[[:space:]]*$//')"
    if [[ "$wpath" == "$relpath" && "$wkey" == "$key" ]]; then
      echo "  WAIVED: $relpath :: $key ::${reason}"
      return 0
    fi
  done < "$WAIVERS_FILE"
  return 1
}

echo "== public_release_gate: scanning $TREE =="
echo

# ---------------------------------------------------------------------------
# 1. Content pattern grep gate
# ---------------------------------------------------------------------------
echo "-- content patterns (.github/pii-patterns.txt) --"
while IFS= read -r pattern || [[ -n "$pattern" ]]; do
  [[ -z "$pattern" || "$pattern" =~ ^[[:space:]]*# ]] && continue

  # Each match line: <tree-relative-path-with-tree-prefix>:<lineno>:<content>
  # -i: personal tokens must not slip through on capitalization.
  matches="$(grep -rIinE -- "$pattern" "$TREE" 2>/dev/null || true)"
  [[ -z "$matches" ]] && continue

  while IFS= read -r match || [[ -n "$match" ]]; do
    [[ -z "$match" ]] && continue
    filepath="${match%%:*}"
    rest="${match#*:}"
    lineno="${rest%%:*}"
    relpath="${filepath#"$TREE"/}"

    if is_waived "$relpath" "$pattern"; then
      WAIVED_COUNT=$((WAIVED_COUNT + 1))
    else
      echo "  HIT: $relpath:$lineno  (pattern: $pattern)"
      UNWAIVED_COUNT=$((UNWAIVED_COUNT + 1))
    fi
  done <<< "$matches"

  # File PATHS can leak tokens too (e.g. a venture name in a filename) —
  # scan the path list with the same pattern, case-insensitively.
  path_matches="$(find "$TREE" -type f | sed "s|^$TREE/||" | grep -iE -- "$pattern" || true)"
  while IFS= read -r p || [[ -n "$p" ]]; do
    [[ -z "$p" ]] && continue
    if is_waived "$p" "path:$pattern"; then
      WAIVED_COUNT=$((WAIVED_COUNT + 1))
    else
      echo "  HIT: $p  (filename matches pattern: $pattern)"
      UNWAIVED_COUNT=$((UNWAIVED_COUNT + 1))
    fi
  done <<< "$path_matches"
done < "$PATTERNS_FILE"

# ---------------------------------------------------------------------------
# 2. File-type / path rules
# ---------------------------------------------------------------------------
echo
echo "-- file-type / path rules --"

check_rule() {
  # check_rule <rule-id> <relpath>
  local rule="$1" relpath="$2"
  if is_waived "$relpath" "$rule"; then
    WAIVED_COUNT=$((WAIVED_COUNT + 1))
  else
    echo "  HIT: $relpath  (rule: $rule)"
    UNWAIVED_COUNT=$((UNWAIVED_COUNT + 1))
  fi
}

while IFS= read -r -d '' f; do
  relpath="${f#"$TREE"/}"
  base="$(basename "$f")"

  case "$base" in
    handover.md) check_rule "filetype:handover" "$relpath" ;;
  esac
  case "$base" in
    *.bak) check_rule "filetype:bak" "$relpath" ;;
  esac
  case "$base" in
    agent.db*) check_rule "filetype:agentdb" "$relpath" ;;
  esac
  case "$base" in
    .env*) check_rule "filetype:env" "$relpath" ;;
  esac
  case "/$relpath" in
    */_archive/*|*/_archive) check_rule "filetype:archive" "$relpath" ;;
  esac
  case "/$relpath" in
    */workspace/*) check_rule "filetype:workspace" "$relpath" ;;
  esac
  case "/$relpath" in
    */demos/*) check_rule "filetype:demos" "$relpath" ;;
  esac

  case "$base" in
    *.png|*.jpg|*.jpeg|*.gif|*.webp|*.PNG|*.JPG|*.JPEG|*.GIF|*.WEBP)
      approved=false
      for dir in "${APPROVED_IMAGE_DIRS[@]}"; do
        case "/$relpath" in
          "/${dir}"*) approved=true ;;
        esac
      done
      if [[ "$approved" == false ]]; then
        check_rule "filetype:image" "$relpath"
      fi
      ;;
  esac
done < <(find "$TREE" -type f -print0)

echo
if [[ "$UNWAIVED_COUNT" -eq 0 ]]; then
  echo "OK: public_release_gate passed — 0 un-waived hits ($WAIVED_COUNT waived)."
  exit 0
else
  echo "FAIL: public_release_gate found $UNWAIVED_COUNT un-waived hit(s) ($WAIVED_COUNT waived). Fix or waive before pushing." >&2
  exit 1
fi
