#!/usr/bin/env bash
# leak_gate.sh - blocking confidentiality gate for the public template.
#
# Scans the WORKING TREE (tracked + untracked-not-ignored files; or every file
# under a path argument) for private tokens. Nothing is excluded except the
# active patterns file (it is gitignored by design): .gitignore, .github/*.txt
# and this script's own comments are scanned too, because enforcement
# artifacts are where leaks hide (CLAUDE.md hard-won rules 9 and 10).
#
# Usage:
#   scripts/leak_gate.sh [--patterns FILE] [--require-patterns] [--report] [--history BASE] [PATH]
#     --history BASE     also scan the ADDED lines (+) of `git log -p BASE..HEAD`, so a token that was
#                        committed and later removed is still caught (content only; masked output)
#     PATH               tree to scan (default: the repo this script lives in)
#     --patterns FILE    one ERE per line, '#' comments and blank lines ignored
#                        (default: <PATH>/.github/pii-patterns.txt)
#     --require-patterns missing patterns file => exit 2 (else NOTICE, path rules only)
#     --report           group hits by pattern, with the matched line (token masked)
#
# Checks, all case-insensitive: (1) file CONTENTS, (2) file and DIRECTORY NAMES,
# (3) inside *.docx *.pptx *.xlsx *.zip (unzipped to a temp dir), (4) path
# rules: handover.md, *.bak, agent.db*, .env*, _archive, workspace/, demos/,
# raster images outside docs/**/images/ and assets/.
#
# Output never shows a raw matched value: patterns are reported by their line
# number in the patterns file and matched text is masked as ***.
# Waivers: --waivers FILE (repeatable); defaults <PATH>/.github/leak-waivers.txt
# (tracked, GENERIC patterns only, never a private value) and
# <PATH>/.github/release-waivers.txt (gitignored, private). Lines `path:key # reason`
# (key = the pattern text, `path:<pattern>` for filename hits, or a rule id
# such as filetype:image). Every applied waiver is printed on every run.
# Exit: 0 = zero un-waived hits, 1 = hits, 2 = usage/config error.

set -uo pipefail
# macOS `cut`/`sort` abort with "Illegal byte sequence" on UTF-8 input under a UTF-8 locale, which
# silently emptied --report; matching is byte-wise and case-insensitive either way.
export LC_ALL=C

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TREE="$(cd "$SCRIPT_DIR/.." && pwd)"
PATTERNS="" REQUIRE=0 REPORT=0 HIST="" WAIVER_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --patterns) [ $# -ge 2 ] || { echo "error: --patterns needs a file" >&2; exit 2; }
                PATTERNS="$2"; shift 2 ;;
    --waivers) [ $# -ge 2 ] || { echo "error: --waivers needs a file" >&2; exit 2; }
               WAIVER_ARGS+=("$2"); shift 2 ;;
    --require-patterns) REQUIRE=1; shift ;;
    --report) REPORT=1; shift ;;
    --history) [ $# -ge 2 ] || { echo "error: --history needs a base ref" >&2; exit 2; }
               HIST="$2"; shift 2 ;;
    -h|--help) sed -n '2,32p' "$0"; exit 0 ;;
    -*) echo "error: unknown option $1" >&2; exit 2 ;;
    *) [ -d "$1" ] || { echo "error: '$1' is not a directory" >&2; exit 2; }
       TREE="$(cd "$1" && pwd)"; shift ;;
  esac
done
cd "$TREE" || exit 2
[ -n "$PATTERNS" ] || PATTERNS=".github/pii-patterns.txt"
WAIVER_FILES=()
if [ "${#WAIVER_ARGS[@]}" -gt 0 ]; then WAIVER_FILES=("${WAIVER_ARGS[@]}")
else WAIVER_FILES=("$TREE/.github/leak-waivers.txt" "$TREE/.github/release-waivers.txt"); fi
TMP="$(mktemp -d "${TMPDIR:-/tmp}/leakgate.XXXXXX")" || exit 2
trap 'rm -rf "$TMP"' EXIT
HITS="$TMP/hits"; : > "$HITS"
UNWAIVED=0; WAIVED=0

# --- patterns -------------------------------------------------------------
PAT_N=(); PAT_RE=()
HAVE_PATTERNS=0
if [ -f "$PATTERNS" ]; then
  HAVE_PATTERNS=1
  PAT_ABS="$(cd "$(dirname "$PATTERNS")" && pwd)/$(basename "$PATTERNS")"
  n=0
  while IFS= read -r p || [ -n "$p" ]; do
    n=$((n + 1)); p="${p%$'\r'}"
    case "$p" in ''|[[:space:]]*'#'*|'#'*) continue ;; esac
    [ -n "${p//[[:space:]]/}" ] || continue
    # an invalid ERE would silently disable the pattern (grep exit 2 was discarded): fail closed instead
    printf '' | grep -qiE -e "$p" 2>/dev/null; rc=$?
    [ "$rc" -eq 2 ] && { echo "error: invalid pattern at $PATTERNS line $n" >&2; exit 2; }
    PAT_N+=("$n"); PAT_RE+=("$p")
  done < "$PATTERNS"
elif [ "$REQUIRE" -eq 1 ]; then
  echo "error: patterns file not found: $PATTERNS (--require-patterns)" >&2
  echo "       copy .github/pii-patterns.example.txt to .github/pii-patterns.txt and fill it in." >&2
  exit 2
else
  PAT_ABS=""
  echo "NOTICE: no patterns file ($PATTERNS) - content/filename scan SKIPPED, path rules only. Not a full leak check."
fi

# --- file list (NUL separated, relative paths) -----------------------------
LIST="$TMP/list"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ "$(git rev-parse --show-toplevel)" = "$(pwd -P)" ]; then
  { git ls-files -z; git ls-files -z -o --exclude-standard; } > "$TMP/raw"
else
  find . -path ./.git -prune -o -type f -print0 > "$TMP/raw"
fi
: > "$LIST"
while IFS= read -r -d '' f; do
  f="${f#./}"
  [ -f "$f" ] || continue
  [ -n "$PAT_ABS" ] && [ "$TREE/$f" = "$PAT_ABS" ] && continue
  case "$f" in -*) f="./$f" ;; esac   # a leading dash must never parse as an option
  printf '%s\0' "$f" >> "$LIST"
done < "$TMP/raw"

# --- helpers --------------------------------------------------------------
is_waived() { # <path> <key> <label>  (prints the label, never the raw pattern text)
  local wf line w wp wk reason
  for wf in "${WAIVER_FILES[@]}"; do
  [ -f "$wf" ] || continue
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|[[:space:]]*'#'*|'#'*) continue ;; esac
    reason="${line#*#}"; [ "$reason" = "$line" ] && reason=""
    w="${line%%#*}"; w="${w%"${w##*[![:space:]]}"}"
    case "$w" in *:*) ;; *) continue ;; esac
    wp="${w%%:*}"; wk="${w#*:}"
    if [ "$wp" = "$1" ] && [ "$wk" = "$2" ]; then
      echo "  WAIVED: $(mask "$1" "$2") :: $3 ::${reason}"; return 0
    fi
  done < "$wf"
  done
  return 1
}

mask() { # <text> <ere> -> text with every match replaced by ***
  local out="$1" tok
  # longest match first, so a shorter overlapping match cannot leave a tail of a longer one visible
  while IFS= read -r tok; do
    [ -n "$tok" ] && out="${out//"$tok"/***}"
  done < <(printf '%s\n' "$1" | grep -oiE -- "$2" 2>/dev/null | sort -u | awk '{ print length($0) "\t" $0 }' | sort -rn | cut -f2-)
  printf '%s' "$out"
}

record() { # <idx|rule> <waiver-path> <waiver-key> <display-loc> <text>
  if is_waived "$2" "$3" "$1"; then WAIVED=$((WAIVED + 1)); return; fi
  UNWAIVED=$((UNWAIVED + 1))
  printf '%s\t%s\t%s\n' "$1" "$4" "$5" >> "$HITS"
}

# scan_tree <listfile> <display-prefix> <strip-prefix>
scan_tree() {
  local lf="$1" dp="$2" sp="$3" i=-1 pat idx out f rel rest ln text
  [ -s "$lf" ] || return 0
  while [ $((i + 1)) -lt "${#PAT_RE[@]}" ]; do
    i=$((i + 1))
    pat="${PAT_RE[$i]}"; idx="${PAT_N[$i]}"
    # content
    xargs -0 grep -HnIiE -e "$pat" -- < "$lf" > "$TMP/out" 2>/dev/null
    while IFS= read -r out || [ -n "$out" ]; do
      f="${out%%:*}"; rest="${out#*:}"; ln="${rest%%:*}"; text="${rest#*:}"
      rel="${f#"$sp"}"; rel="${rel#./}"
      text="$(mask "$text" "$pat")"
      record "pattern #$idx" "$dp$rel" "$pat" "$(mask "$dp$rel:$ln" "$pat")" "$(printf '%.160s' "$text")"
    done < "$TMP/out"
    # file and directory names
    tr '\0' '\n' < "$lf" | grep -iE -- "$pat" > "$TMP/out" 2>/dev/null
    while IFS= read -r f || [ -n "$f" ]; do
      rel="${f#"$sp"}"; rel="${rel#./}"
      record "pattern #$idx" "$dp$rel" "path:$pat" "$(mask "$dp$rel" "$pat")" "(file/dir name)"
    done < "$TMP/out"
  done
}

# --- 1. patterns: tree, then inside zip/OOXML -----------------------------
if [ "$HAVE_PATTERNS" -eq 1 ]; then
  scan_tree "$LIST" "" ""
  z=0
  while IFS= read -r -d '' f; do
    case "$f" in *.docx|*.pptx|*.xlsx|*.zip|*.DOCX|*.PPTX|*.XLSX|*.ZIP) ;; *) continue ;; esac
    z=$((z + 1)); d="$TMP/z$z"; mkdir -p "$d"
    if ! unzip -qq -o "$f" -d "$d" </dev/null >/dev/null 2>&1; then
      record "rule" "$f" "unzip:failed" "$f" "(archive could not be unzipped - cannot verify)"
      continue
    fi
    (cd "$d" && find . -type f -print0) | while IFS= read -r -d '' g; do g="${g#./}"; case "$g" in -*) g="./$g" ;; esac; printf '%s\0' "$g"; done > "$TMP/zl"
    # scan_tree greps relative to cwd, so run it from the extraction dir
    cd "$d" && scan_tree "$TMP/zl" "$f!" ""; cd "$TREE"
  done < "$LIST"
fi

# --- 1b. history: added lines of BASE..HEAD ---------------------------------
if [ -n "$HIST" ]; then
  case "$HIST" in -*) echo "error: bad --history ref" >&2; exit 2 ;; esac
  git rev-parse --verify -q "$HIST^{commit}" >/dev/null 2>&1 || { echo "error: --history: unknown ref '$HIST'" >&2; exit 2; }
  if [ "$HAVE_PATTERNS" -eq 1 ]; then
    # added lines (binary diffs included via --text; merges via -m), `+++` is a header only after a `---` line
    git log -p -m --text --no-color --no-ext-diff --format='@@C %h' "$HIST..HEAD" -- 2>/dev/null | awk '
      /^@@C /  { c = $2; h = 0; next }
      /^--- /  { h = 1; next }
      /^\+\+\+ / && h { f = substr($0, 7); h = 0; next }
      { h = 0 }
      /^\+/   { printf "%s\001%s\001%s\n", c, f, substr($0, 2) }' > "$TMP/hist"
    # author, committer and message lines: the likeliest PII in history is a name or an e-mail
    # (identity lines are reported once per distinct value, under the path `commit-meta`, so a waiver
    #  `commit-meta:<pattern> # own author line` in release-waivers.txt covers the maintainer's own commits)
    git log --no-color --format='@@C %h%n%an <%ae>%n%cn <%ce>%n%B' "$HIST..HEAD" 2>/dev/null | awk '
      /^@@C /  { c = $2; next }
      NF && !seen[$0]++ { printf "%s\001commit-meta\001%s\n", c, $0 }' >> "$TMP/hist"
    # file and directory names added or renamed in history
    git log --no-color --name-only --diff-filter=AR --format='@@C %h' "$HIST..HEAD" -- 2>/dev/null | awk '
      /^@@C /  { c = $2; next }
      NF       { printf "%s\001commit-path\001%s\n", c, $0 }' >> "$TMP/hist"
    i=-1
    while [ $((i + 1)) -lt "${#PAT_RE[@]}" ]; do
      i=$((i + 1)); pat="${PAT_RE[$i]}"; idx="${PAT_N[$i]}"
      while IFS=$'\001' read -r c f text; do
        printf '%s\n' "$text" | grep -qiE -e "$pat" 2>/dev/null || continue
        record "pattern #$idx" "$f" "$pat" "$(mask "history $c:$f" "$pat")" "$(printf '%.160s' "$(mask "$text" "$pat")")"
      done < "$TMP/hist"
    done
  fi
fi

# --- 2. path / file-type rules --------------------------------------------
rule() { local p="${2#./}"; record "rule: $1" "$p" "$1" "$p" "(path rule)"; }
while IFS= read -r -d '' f; do
  b="${f##*/}"
  case "$b" in handover.md) rule filetype:handover "$f" ;; esac
  case "$b" in *.bak) rule filetype:bak "$f" ;; esac
  case "$b" in agent.db*) rule filetype:agentdb "$f" ;; esac
  case "$b" in .env*) rule filetype:env "$f" ;; esac
  case "/$f" in */_archive/*) rule filetype:archive "$f" ;; esac
  case "/$f" in */workspace/*) rule filetype:workspace "$f" ;; esac
  case "/$f" in */demos/*) rule filetype:demos "$f" ;; esac
  case "$b" in
    *.png|*.jpg|*.jpeg|*.gif|*.webp|*.PNG|*.JPG|*.JPEG|*.GIF|*.WEBP)
      case "$f" in
        assets/*|docs/images/*|docs/*/images/*|docs/*/*/images/*|docs/*/*/*/images/*) ;;
        *) rule filetype:image "$f" ;;
      esac ;;
  esac
done < "$LIST"

# --- report ----------------------------------------------------------------
echo "== leak_gate: scanned $TREE =="
if [ "$UNWAIVED" -gt 0 ]; then
  if [ "$REPORT" -eq 1 ]; then
    K="$(cut -f1 "$HITS" | sort -u | grep -c '^pattern #')"
    echo "$UNWAIVED hits across $K patterns. Waive one hit: add \"path:key # reason\" to .github/leak-waivers.txt. Change what is scanned: edit .github/pii-patterns.txt yourself (one regex per line; the agent cannot read it)."
    cut -f1 "$HITS" | sort -u | while IFS= read -r g; do
      echo "-- $g --"
      awk -F'\t' -v g="$g" '$1 == g { printf "  %s\n      %s\n", $2, $3 }' "$HITS"
    done
  else
    awk -F'\t' '{ printf "  HIT: %s  (%s)\n", $2, $1 }' "$HITS"
  fi
  echo "FAIL: leak_gate found $UNWAIVED un-waived hit(s) ($WAIVED waived)." >&2
  exit 1
fi
echo "OK: leak_gate passed - 0 un-waived hits ($WAIVED waived)."
exit 0
