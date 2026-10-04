#!/usr/bin/env bash
# coupling_lint.sh - fail on leftovers of the private product this template was
# extracted from. These are not personal data (that is leak_gate.sh); they are
# product-specific ids, contracts and integrations that must not appear here.
#
# Usage: scripts/coupling_lint.sh [--summary] [--allow FILE] [PATH]
#   --summary     print hit count per file (burn-down tracker), plus total
#   --allow FILE  waiver list, lines `path:pattern # reason`; pattern `*` waives
#                 every pattern for that path
#   PATH          tree to scan (default: repo this script lives in)
# Scans the working tree (git ls-files + untracked-not-ignored), contents AND
# file/directory names. This script is skipped (it contains the patterns).
# Exit: 0 clean (or --summary), 1 hits, 2 usage error.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TREE="$(cd "$SCRIPT_DIR/.." && pwd)"
SELF="$(basename "$0")"
SUMMARY=0 ALLOW=""
while [ $# -gt 0 ]; do
  case "$1" in
    --summary) SUMMARY=1; shift ;;
    --allow) [ $# -ge 2 ] || { echo "error: --allow needs a file" >&2; exit 2; }
             ALLOW="$2"; shift 2 ;;
    -*) echo "error: unknown option $1" >&2; exit 2 ;;
    *) [ -d "$1" ] || { echo "error: '$1' is not a directory" >&2; exit 2; }
       TREE="$(cd "$1" && pwd)"; shift ;;
  esac
done
[ -z "$ALLOW" ] || [ -f "$ALLOW" ] || { echo "error: allow file not found: $ALLOW" >&2; exit 2; }
cd "$TREE" || exit 2

PATTERNS=(
  '\b(ATOM|FEAT)-[0-9]{3}\b'
  '\bC(1[01]|[1-9]) [a-z]+-'
  'from src\.|import src\b'
  # product names (Telegram, Notion) are not structural coupling and were dropped in v3.0.1;
  # `--allow` remains for the rest
  'LaunchAgent|launchctl|pgvector'
)

TMP="$(mktemp -d "${TMPDIR:-/tmp}/coupling.XXXXXX")" || exit 2
trap 'rm -rf "$TMP"' EXIT
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ "$(git rev-parse --show-toplevel)" = "$(pwd -P)" ]; then
  { git ls-files -z; git ls-files -z -o --exclude-standard; } > "$TMP/raw"
else
  find . -path ./.git -prune -o -type f -print0 > "$TMP/raw"
fi
: > "$TMP/list"
while IFS= read -r -d '' f; do
  f="${f#./}"
  [ -f "$f" ] || continue
  [ "$f" = "scripts/$SELF" ] && continue
  case "$f" in -*) f="./$f" ;; esac   # a leading dash must never parse as an option
  printf '%s\0' "$f" >> "$TMP/list"
done < "$TMP/raw"

allowed() { # <path> <pattern>
  [ -n "$ALLOW" ] || return 1
  local line w
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|[[:space:]]*'#'*|'#'*) continue ;; esac
    w="${line%%#*}"; w="${w%"${w##*[![:space:]]}"}"
    case "$w" in *:*) ;; *) continue ;; esac
    if [ "${w%%:*}" = "$1" ] && { [ "${w#*:}" = "$2" ] || [ "${w#*:}" = "*" ]; }; then
      echo "  WAIVED: $1 :: $2 ::${line#*#}"; return 0
    fi
  done < "$ALLOW"
  return 1
}

HITS="$TMP/hits"; : > "$HITS"   # file<TAB>loc<TAB>text
COUNT=0
if [ -s "$TMP/list" ]; then
  for pat in "${PATTERNS[@]}"; do
    xargs -0 grep -HnIE -e "$pat" -- < "$TMP/list" > "$TMP/out" 2>/dev/null
    while IFS= read -r out || [ -n "$out" ]; do
      f="${out%%:*}"; rest="${out#*:}"; ln="${rest%%:*}"; f="${f#./}"
      allowed "$f" "$pat" && continue
      printf '%s\t%s:%s\t%.140s\n' "$f" "$f" "$ln" "${rest#*:}" >> "$HITS"; COUNT=$((COUNT + 1))
    done < "$TMP/out"
    tr '\0' '\n' < "$TMP/list" | grep -E -- "$pat" > "$TMP/out" 2>/dev/null
    while IFS= read -r f || [ -n "$f" ]; do
      f="${f#./}"
      allowed "$f" "$pat" && continue
      printf '%s\t%s\t(file/dir name)\n' "$f" "$f" >> "$HITS"; COUNT=$((COUNT + 1))
    done < "$TMP/out"
  done
fi

if [ "$COUNT" -eq 0 ]; then echo "OK: coupling_lint - 0 hits."; exit 0; fi
if [ "$SUMMARY" -eq 1 ]; then
  cut -f1 "$HITS" | sort | uniq -c | sort -rn | awk '{ c=$1; $1=""; sub(/^ /,""); printf "%5d  %s\n", c, $0 }'
  echo "TOTAL: $COUNT hit(s) in $(cut -f1 "$HITS" | sort -u | wc -l | tr -d ' ') file(s)."
  exit 0   # --summary is a report
else
  awk -F'\t' '{ printf "HIT: %s  %s\n", $2, $3 }' "$HITS"
  echo "FAIL: coupling_lint found $COUNT hit(s)." >&2
fi
exit 1
