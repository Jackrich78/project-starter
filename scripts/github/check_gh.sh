#!/usr/bin/env bash
# Probe the gh capabilities the issue flow needs (docs/system/issue-flow.md).
# Usage: bash scripts/github/check_gh.sh [--quiet]   exit 1 on any FAIL
QUIET=0; [ "$1" = "--quiet" ] && QUIET=1
FAILS=0
report() { # status label
  [ "$1" = FAIL ] && FAILS=$((FAILS+1))
  if [ "$QUIET" = 0 ] || [ "$1" = FAIL ]; then echo "$1  $2"; fi
}
check() { # label cmd...
  label=$1; shift
  if "$@" >/dev/null 2>&1; then report ok "$label"; else report FAIL "$label"; fi
}
has_flag() { gh issue create --help 2>&1 | grep -q -- "$1"; }

if ! command -v gh >/dev/null 2>&1; then echo "FAIL  gh installed"; exit 1; fi

ver=$(gh --version 2>/dev/null | head -1 | sed -E 's/^gh version ([0-9]+)\.([0-9]+).*/\1 \2/')
set -- $ver
if [ -n "$1" ] && { [ "$1" -gt 2 ] || { [ "$1" -eq 2 ] && [ "$2" -ge 96 ]; }; }; then
  report ok "gh version >= 2.96 ($1.$2)"
else
  report FAIL "gh version >= 2.96 (found ${1:-?}.${2:-?}; upgrade gh; no in-session fallback)"
fi
check "gh auth status" gh auth status
check "gh issue create --parent" has_flag --parent
check "gh issue create --blocked-by" has_flag --blocked-by
if git remote get-url origin >/dev/null 2>&1; then
  check "gh issue list --json parent,blockedBy,subIssuesSummary" \
    gh issue list --json parent,blockedBy,subIssuesSummary --limit 1
else
  [ "$QUIET" = 0 ] && echo "skip  issue list fields (no git remote)"
fi
exit $((FAILS > 0))
