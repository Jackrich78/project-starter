#!/usr/bin/env python3
"""PreToolUse security guard for Bash / Read / Edit / Write / MultiEdit.

Exit 2 + one-line stderr reason = block. Anything else (including any internal
error) = exit 0, no output (fail open: a broken guard must not brick the session).
Stdlib only, no network, never prints the command (it may carry a secret).

Scan scope: the WHOLE Bash command string is tokenised, heredoc bodies included.
A commit message that literally contains a blocked command can trip the guard;
use `git commit -F <file>` to keep message text off the scanned surface.

Pure functions for tests: check_command(cmd), check_path(path), check_stateful(cmd, root).
Each returns (verdict, reason) with verdict in {"allow", "caution", "block"}.
This is a speed bump for mistakes and prompt injection, not a sandbox.
"""
import datetime
import json
import os
import re
import shlex
import subprocess
import sys
import time

ALLOW, CAUTION, BLOCK, ASK = "allow", "caution", "block", "ask"
MAIN = {"main", "master"}

READERS = set(
    "cat head tail less more nl tac strings xxd od hexdump base64 grep egrep fgrep rg ag awk sed "
    "python perl ruby node bun deno jq dd cp mv scp rsync open source . bat vi vim nano emacs code "
    "pbcopy diff cmp sort uniq cut tr paste column fold rev tee tar zip gzip zcat curl wget nc ncat "
    "netcat socat ssh sftp xargs openssl".split())
GIT_READ_SUBS = {"show", "diff", "log", "blame", "grep", "cat-file", "archive", "bundle"}
WRAPPERS = {"command", "nohup", "time", "exec", "builtin", "nice", "ionice", "caffeinate", "stdbuf", "chrt",
            "taskset", "busybox", "watch", "timeout", "script", "unbuffer", "setsid"}
# Wrapper flags that take a value (so the value is not mistaken for the command).
_WRAP_VAL = {"nice": {"-n", "--adjustment"}, "ionice": {"-c", "-n", "-p", "--class", "--classdata"},
             "timeout": {"-s", "--signal", "-k", "--kill-after"}, "watch": {"-n", "--interval", "-d"},
             "stdbuf": {"-i", "-o", "-e"}, "taskset": {"-c", "--cpu-list"}, "chrt": {"-p"}}
# Shell syntax words that precede the real command inside a segment.
_SYNTAX = {"{", "}", "!", "do", "then", "else", "elif", "if", "while", "until", "fi", "done", "esac"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "ash", "fish", "csh", "tcsh"}
CODE_EXT = (".py", ".md", ".js", ".ts", ".tsx", ".jsx", ".sh", ".rst", ".html")
GH_GROUPS = {"issue", "pr", "repo", "release", "label", "secret", "variable", "workflow", "run",
             "gist", "ruleset", "cache", "project", "ssh-key", "gpg-key", "codespace"}
GH_WRITE = {"create", "edit", "comment", "close", "reopen", "merge", "delete", "develop", "review",
            "lock", "unlock", "transfer", "pin", "unpin", "ready", "fork", "rename", "archive", "set",
            "upload", "run", "cancel", "rerun", "add", "remove", "sync", "enable", "disable", "publish"}
CURL_DATA = {"-d", "-F", "--data", "--data-binary", "--data-raw", "--data-urlencode", "--data-ascii",
             "--form", "--form-string", "--json"}
_SECRET_VAR = (r'\$\{?(?:[A-Za-z0-9]+_)*(?:TOKEN|SECRET|KEY|PASSWORD|PASSWD|CREDENTIALS?|AUTH)'
               r'(?:_[A-Za-z0-9]+)*(?![A-Za-z0-9_])')
_SECRET_NAME = r'(?:[A-Za-z0-9]+_)*(?:TOKEN|SECRET|KEY|PASSWORD|PASSWD|CREDENTIALS?|AUTH)(?:_[A-Za-z0-9]+)*'
# Pure file/content readers whose arguments must be literal (no glob / variable / substitution).
NET_CMDS = {"curl", "wget", "nc", "ncat", "netcat", "socat", "ssh", "scp", "sftp", "rsync", "gh"}
INTERPRETERS = {"python", "node", "perl", "ruby", "deno", "bun", "php", "lua", "osascript"}
_INLINE_CODE = re.compile(r'^(?:-c|-e|-p|-r|-E|--eval|-pe|-ne|-le|-lane)$')
_CODE_CRED = re.compile(r'\.env\b|\.(?:ssh|aws|kube|gnupg)\b|\.netrc|\.npmrc|\.pypirc|\.config/gh|\.docker/config'
                        r'|id_rsa|\.pem\b|\.key\b|credentials|\.claude/projects|\.claude/history|pii-patterns', re.I)
_CODE_EXEC = re.compile(r'os\.environ|\benviron\b|process\.env|\bENV\b|os\.system|subprocess|socket|urllib|requests'
                        r'|http|child_process|\bnet\b|fetch\(|exec|file_get_contents|shell_exec|popen|system\s*\('
                        r'|io\.open|os\.execute|do shell script|readfile|spawn')
_XARGS_VAL = {"-I", "-n", "-P", "-L", "-s", "-E", "-d", "-a", "-J"}
# Harness files an agent must not rewrite from a shell (the Edit tool prompts; a redirect does not).
_PROTECTED = re.compile(r'(^|/)(?:\.claude/(?:settings(?:\.local)?\.json$|hooks(?:/|$))'
                        r'|\.github/(?:pii-patterns\.txt|release-waivers\.txt|leak-waivers\.txt)$'
                        r'|\.git/(?:hooks(?:/|$)|config$)|\.mcp\.json$)')
# Directory targets a copy/move/sync into which lands a file beside the hooks or settings.
_PROTECTED_DIR = re.compile(r'(^|/)\.claude$')
_HOME = (r'(?:~|\$home|\$\{home\}|/users/[^/]+|/home/[^/]+|/root|'
         + re.escape(os.path.expanduser("~").lower().rstrip("/")) + ')')
_CFG = os.environ.get("CLAUDE_CONFIG_DIR", "").lower().rstrip("/")
_CLAUDE_DIR = '(?:' + _HOME + r'/\.claude' + (('|' + re.escape(_CFG)) if _CFG else '') + ')'
_HOME_CLAUDE = re.compile('^' + _CLAUDE_DIR + '/')
_HOME_CLAUDE_SENSITIVE = re.compile('^' + _CLAUDE_DIR + r'/(?:history\.jsonl|\.credentials\.json|settings(?:\.local)?\.json'
                                    r'|sessions/|shell-snapshots/|paste-cache/|file-history/|debug/|session-env/)')
_HOME_CLAUDE_JSON = re.compile('^' + _HOME + r'/\.claude\.json$')
_HOME_ROOT = re.compile('^' + _HOME + r'(?:/|/\.(?:config|claude|local|cache)/?)?$|^/$')
_WRITERS = {"tee", "cp", "mv", "install", "ln", "chmod", "chown", "chgrp", "truncate", "rm", "unlink", "shred",
            "rsync", "patch"}
# Producers whose output names only tracked or already-matched files: safe to feed a reader through xargs.
_SAFE_PRODUCER = re.compile(r'^\s*(?:git\s+ls-files(?![^|]*(?:\s-o\b|--others|\s-i\b|--ignored))|git\s+grep\s+-l'
                            r'|git\s+(?:diff|show)\s+--name-only|rg\s+(?:-l|--files-with-matches)\b|grep\s+-[a-zA-Z]*l)')
# Code and prose extensions only: config-shaped files (json, yaml, txt, ini) are where secrets live.
_SAFE_GLOB_EXT = re.compile(r'\.(?:py|md|js|mjs|cjs|ts|tsx|jsx|sh|rst|html?|css|go|rs|java|rb|c|h|cpp|svg)$', re.I)
_PUSH_LONG = ("--mirror", "--all", "--delete", "--prune", "--force", "--force-with-lease", "--force-if-includes")
_GIT_CONFIG_EXEC = re.compile(
    r'(?i)^(?:alias\.|core\.(?:sshcommand|hookspath|pager|editor|fsmonitor|askpass|gitproxy|attributesfile|excludesfile)'
    r'|diff\.(?:external$|.*\.(?:textconv|command))|difftool\..*\.cmd|merge\..*\.driver|mergetool\..*\.cmd'
    r'|filter\..*\.(?:clean|smudge|process)|credential\.|include(?:if)?\.|remote\..*\.(?:mirror|push|url|pushurl|proxy)'
    r'|push\.|url\..*\.(?:push)?insteadof|sequence\.editor|uploadpack\.|receive\.|gpg\.program|http\.(?:proxy|sslcainfo|sslverify)'
    r'|safe\.directory|sendemail\.|protocol\.)')
_GIT_CONFIG_READ = {"--get", "--get-all", "--get-regexp", "-l", "--list", "--show-origin", "--get-urlmatch", "--show-scope"}
INDIRECT_READERS = READERS - {"curl", "wget", "nc", "ncat", "netcat", "socat", "ssh", "sftp", "xargs",
                              "openssl", "tee"}
_EXEC_ENV = re.compile(r'^(?:GIT_PAGER|PAGER|EDITOR|VISUAL|GIT_EDITOR|GIT_SEQUENCE_EDITOR|LESSOPEN|LESSCLOSE|'
                       r'GIT_EXTERNAL_DIFF|GIT_SSH_COMMAND|GIT_ASKPASS|GIT_CONFIG_COUNT|GIT_CONFIG_PARAMETERS|'
                       r'GIT_CONFIG_KEY_\d+|GIT_CONFIG_VALUE_\d+)=')
_SAFE_BASES = ("$CLAUDE_PROJECT_DIR/", "${CLAUDE_PROJECT_DIR}/", "$PWD/", "$HOME/")
_SED_EXEC = re.compile(r'(?:^|[;{}\n]|[\d$/!])\s*[we]\s+\S|s(.)(?:(?!\1).)*\1(?:(?!\1).)*\1[gpiImM0-9]*[ew]')
_DANGER_RM = re.compile(r'^(/|/\*|~/?|~/\*|\.|\./|\./\*|\.\.|\.\./?|\*|\$\{?HOME\}?/?|\.?/?\.git/?)$')

# Whole-string patterns (cannot be tokenised: pipes, fork bombs, device redirects).
WHOLE = [
    (r':\s*\(\s*\)\s*\{', "fork bomb"),
    (r'>\s*/dev/(?:sd|hd|nvme|disk)', "write to disk device"),
    (r'\b(?:curl|wget)\b[^\n;&]*\|\s*(?:sudo\s+)?(?:env\s+\S+\s+)?(?:ba|z|da|k)?sh\b', "pipe download to shell"),
    (r'\b(?:ba|z|da)?sh\s+<\(\s*(?:curl|wget)|\bsource\s+<\(\s*(?:curl|wget)', "run downloaded script"),
    (r'\$\{\s*' + _SECRET_NAME + r'\s*:[-=?]', "secret in parameter-expansion default"),
    # a shell or interpreter whose program text arrives on stdin: the hook cannot see what runs
    (r'\|\s*(?:env\s+\S+\s+)?(?:ba|z|da|k|a|fi)?sh\b(?:\s+-[A-Za-z]+)*\s*(?:$|[|;&)\n])', "shell reads commands from a pipe"),
    (r'(?:^|[|;&(\s])(?:ba|z|da|k|a|fi)?sh\s+(?:-[A-Za-z]+\s+)*(?:<<<|<\()', "shell reads commands from a here-string/process substitution"),
    (r'\|\s*(?:python[\d.]*|node|perl|ruby|php|lua|deno|bun)(?:\s+-)?\s*(?:$|[|;&)\n])', "interpreter reads code from a pipe"),
]


def _is_cred_path(p):
    """Reason string if `p` names a credential file, else None. `..`/`.` segments are resolved lexically."""
    p = (p or "").strip().strip("\"'")
    if not p or p.startswith("-"):
        return None
    if "/." in p or p.startswith("."):
        n = os.path.normpath(p)
        p = ("~/" + n.lstrip("/")) if p.startswith("~/") and not n.startswith("~/") else n
    low = p.lower().rstrip("/")
    base = low.rsplit("/", 1)[-1]
    if re.match(r'^\.env($|[.*?\[])', base) and not re.match(r'^\.env\.(example|sample|template|dist|defaults?)$', base):
        return "env file"
    if base == ".dev.vars" or base in (".netrc", ".npmrc", ".pypirc", ".git-credentials"):
        return "credential file"
    if re.search(r'\.(pem|key|p12|pfx|ppk|jks|keystore)$', base) or re.match(r'^id_(rsa|dsa|ecdsa|ed25519)', base):
        return "private key"
    if re.search(r'(^|/)\.(ssh|aws|kube|gnupg)(/|$)|(^|/)\.config/gh(/|$)|(^|/)\.docker/config\.json$'
                 r'|(^|/)\.claude/projects/(.*\.jsonl$|.*/subagents(/|$))', low):
        return "credential directory"
    if re.search(r'(^|/)\.claude/projects(/|$)', low) and "/memory/" not in low and not low.endswith("/memory"):
        return "transcript directory (use scripts/recall.py)"
    if _HOME_CLAUDE_SENSITIVE.match(low):
        return "Claude Code home state (history, sessions, settings)"
    if re.search(r'(^|/)\.github/(pii-patterns|release-waivers)\.txt$|(^|/)\.claude/settings\.local\.json$', low):
        return "private harness file (patterns, waivers, local settings)"
    if re.match(r'^/proc/(self|\d+)/environ$', low):
        return "process environment"
    if re.search(r'credentials|secret', base) and ("." in base or "/" in low) and not base.endswith(CODE_EXT):
        return "credentials/secret file"
    return None


def _norm(p):
    """Lower-case, unquoted, `..`/`.` segments resolved lexically (never touches the filesystem), no trailing /."""
    p = (p or "").strip().strip("\"'")
    if not p:
        return ""
    keep_tilde = p.startswith("~/")
    n = os.path.normpath(p)
    if keep_tilde and not n.startswith("~/"):
        n = "~/" + n.lstrip("/")
    return n.lower().rstrip("/")


def _is_protected(p, as_dir=False):
    """True if `p` is a harness file a shell must not rewrite, or anything under ~/.claude.
    as_dir: also treat `.claude` itself as protected (a copy INTO it lands beside the hooks)."""
    low = _norm(p)
    if not low:
        return False
    return (bool(_PROTECTED.search(low)) or bool(_HOME_CLAUDE.match(low)) or bool(_HOME_CLAUDE_JSON.match(low))
            or (as_dir and bool(_PROTECTED_DIR.search(low))))


def _safe_glob(a):
    """A reader glob that cannot reach a credential file: literal directory, basename with a code/doc extension."""
    if re.search(r'[$`\\]', a):
        return False
    d, _, b = a.rpartition("/")
    if re.search(r'[*?\[]', d) or (d and _is_cred_path(d + "/x")) or _HOME_ROOT.match(d.lower() + "/"):
        return False
    return bool(re.match(r'^[A-Za-z0-9_*?][A-Za-z0-9_.*?-]*$', b)) and bool(_SAFE_GLOB_EXT.search(b))


def _raw_segments(cmd):
    """Quote-aware split on ; & | newline ( ). Returns (segments, ansi_c_quote_seen).
    Quotes are kept in the segment text so callers can tell what the shell expands."""
    segs, cur, q, i, ansi = [], [], None, 0, False
    while i < len(cmd):
        c = cmd[i]
        if q == "'":
            cur.append(c)
            q = None if c == "'" else q
        elif q == '"':
            if c == "\\" and i + 1 < len(cmd):
                cur.append(c + cmd[i + 1])
                i += 1
            else:
                cur.append(c)
                q = None if c == '"' else q
        elif c == "\\" and i + 1 < len(cmd):
            cur.append(c + cmd[i + 1])
            i += 1
        elif c in "'\"":
            q = c
            cur.append(c)
        elif c == "$" and cmd[i + 1:i + 2] == "'":
            ansi = True
            cur.append(c)
        elif c == "$" and cmd[i + 1:i + 2] == "(":
            cur.append("$(")
            segs.append("".join(cur))
            cur = []
            i += 1
        elif c == "`":
            cur.append(c)
        elif c in ";&|\n()":
            segs.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    segs.append("".join(cur))
    return segs, ansi


def _unquote_for_scan(a):
    """Drop what the shell does not expand: single-quoted text, and glob chars inside double quotes."""
    a = re.sub(r"'[^']*'", "", a)
    return re.sub(r'"([^"]*)"', lambda m: re.sub(r'[*?\[]', '', m.group(1)), a)


def _strip_heredocs(cmd):
    """Remove heredoc BODY lines (keep the command lines): the reader-argument rule scans the command's
    own arguments only. The WHOLE patterns and token checks still see the full text."""
    out, delim = [], None
    for line in cmd.split("\n"):
        if delim is not None:
            if line.strip() == delim:
                delim = None
            continue
        out.append(line)
        m = re.search(r'<<-?\s*[\'"]?([A-Za-z_]\w*)[\'"]?', line)
        if m:
            delim = m.group(1)
    return "\n".join(out)


def _raw_check(cmd):
    """Obfuscation / indirection checks on the RAW string, before tokenising."""
    cmd = _strip_heredocs(cmd)
    if "\\\n" in cmd:
        return BLOCK, "backslash-newline line continuation"
    segs, ansi = _raw_segments(cmd)
    if ansi:
        return BLOCK, "ANSI-C quoting $'...'"
    for seg in segs:
        try:
            toks = shlex.split(seg, posix=False)
        except ValueError:
            toks = seg.split()
        if not toks:
            continue
        i, name = _command(toks)
        pre = toks[:i] + (toks[i + 1:] if name in ("export", "declare", "typeset", "local", "readonly") else [])
        for t in pre:
            m = re.match(r'^[A-Za-z_]\w*=(.*)$', t)
            if m and _is_cred_path(m.group(1)):
                return BLOCK, "variable assigned a credential path"
        net = name in NET_CMDS or (name == "git" and "push" in toks[i + 1:])
        if net and any(re.search(r'\$\(|\$\{|`', re.sub(r"'[^']*'", "", a)) for a in toks[i + 1:]):
            return BLOCK, "command substitution/expansion in a network command argument"
        if name not in INDIRECT_READERS:
            continue
        for a in toks[i + 1:]:
            bare = a.strip('"')
            base = next((b for b in _SAFE_BASES if bare.startswith(b)), None)
            if base:
                rest = bare[len(base):]
                if not re.search(r'[$*?\[`\\]', rest) and not _is_cred_path(rest):
                    continue
            if re.search(r'[*?\[$`]', _unquote_for_scan(a)) and not _safe_glob(bare):
                return BLOCK, "glob/variable/substitution in a reader argument"
    return None


def check_path(path, tool="Read"):
    """Any tool: a credential path blocks (private pattern/waiver files and settings.local.json included).
    Write/Edit: a repo harness file (hooks, settings.json, tracked waivers, .mcp.json) and a global Claude
    file such as ~/.claude/CLAUDE.md or ~/.claude.json ask; ~/.claude settings, hooks, plugins and session
    state block; ~/.claude auto-memory and plans allow; .git internals block. Paths are normalised first."""
    reason = _is_cred_path(_norm(path)) or _is_cred_path(path)
    if reason:
        return BLOCK, "credential file path: " + reason
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit") and _is_protected(path):
        low = _norm(path)
        if _HOME_CLAUDE_JSON.match(low):
            return ASK, "edit of ~/.claude.json (MCP servers, global state): confirm"
        if _HOME_CLAUDE.match(low):
            rest = low[_HOME_CLAUDE.match(low).end():]
            # Claude Code's own auto-memory and plan files are written through these tools: allow
            if re.match(r'projects/[^/]+/memory(/|$)|plans/', rest):
                return ALLOW, None
            # global permissions, hooks, plugins and credentials: never from inside a project
            if re.match(r'settings|hooks/|plugins/|\.credentials|history\.jsonl|sessions/|shell-snapshots/'
                        r'|session-env/|file-history/|paste-cache/|debug/', rest):
                return BLOCK, "write to Claude Code home state"
            return ASK, "edit of a global Claude Code file (" + rest + "): confirm"
        if re.search(r'(^|/)\.git/', low):
            return BLOCK, "write to .git internals"
        return ASK, "edit of a harness file (hook, settings or leak-gate input): confirm"
    return ALLOW, None


def _cands(tok):
    out = {tok, tok.lstrip("@<"), tok.rsplit("=", 1)[-1].lstrip("@"), tok.rsplit(":", 1)[-1]}
    if "@" in tok:
        out.add(tok.split("@", 1)[1])
    return out


def _cred_in(tokens):
    for t in tokens:
        for c in _cands(t):
            r = _is_cred_path(c)
            if r:
                return r
    return None


def _segments(cmd):
    """Token lists per simple command. Quote-aware; falls back to naive split (heredocs)."""
    cmd = cmd.replace("`", " ; ")
    try:
        lex = shlex.shlex(cmd.replace("\n", " ; "), posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        segs, cur = [], []
        for t in lex:
            if t == "$":
                continue
            if t and all(c in ";&|()" for c in t):
                segs.append(cur)
                cur = []
            else:
                cur.append(t)
        segs.append(cur)
    except ValueError:
        segs = []
        for s in re.split(r'&&|\|\||[;|&\n()]', cmd):
            try:
                segs.append(shlex.split(s))
            except ValueError:
                segs.append([w.strip("\"'") for w in s.split()])
    return [s for s in segs if s]


def _command(tokens):
    """(index, normalised name) of the real command after env assignments and wrappers."""
    i = 0
    while i < len(tokens):
        t = tokens[i]
        b = os.path.basename(t)
        if re.match(r'^[A-Za-z_]\w*=', t) or t in _SYNTAX or re.match(r'^\w+\(\)$', t):
            i += 1
        elif t == "function":
            i += 2
        elif b in WRAPPERS:
            i += 1
            vals = _WRAP_VAL.get(b, set())
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 2 if tokens[i] in vals else 1
            if b == "timeout" and i < len(tokens) and re.match(r'^\d+(?:\.\d+)?[smhd]?$', tokens[i]):
                i += 1
            if b == "script" and i < len(tokens) and ("/" in tokens[i] or tokens[i].endswith(".txt")):
                i += 1
        elif b == "env":
            j = i + 1
            while j < len(tokens) and (tokens[j].startswith("-") or "=" in tokens[j]):
                j += 1
            if j >= len(tokens):
                return i, "env"
            i = j
        else:
            return i, ("python" if re.match(r'^python[\d.]*$', b) else b)
    return len(tokens), ""


def _git(tokens):
    i, name = _command(tokens)
    if name != "git":
        return None
    a, j = tokens[i + 1:], 0
    while j < len(a) and a[j].startswith("-"):
        j += 2 if a[j] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace") else 1
    return (a[j], a[j + 1:]) if j < len(a) else None


def _push_check(args, direct=False):
    pos = [a for a in args if not a.startswith("-")]
    flags = [a for a in args if a.startswith("-")]
    for f in flags:
        base = f.split("=", 1)[0]
        # git accepts any unique abbreviation of a long option (--mirro, --delet, --al)
        if base.startswith("--") and len(base) >= 4 and any(o.startswith(base) for o in _PUSH_LONG):
            return BLOCK, "force/delete/all/mirror/prune push"
        if re.match(r'^-[a-zA-Z]*[fd][a-zA-Z]*$', f):
            return BLOCK, "force/delete/all/mirror/prune push"
    if any(f.startswith("--repo") for f in flags):
        return BLOCK, "push to explicit repo/URL"
    if pos and not re.match(r'^[\w.-]+$', pos[0]):
        return BLOCK, "push to URL/path instead of a named remote"
    for ref in pos[1:]:
        dst = ref.split(":")[-1].lstrip("+")
        if ref.startswith("+") or ref.startswith(":"):
            return BLOCK, "forced or delete refspec"
        if re.sub(r'^(?:refs/)?heads/', "", dst) in MAIN:
            if direct:
                return CAUTION, "direct-mode push to main/master"
            return BLOCK, "push to main/master"
    return CAUTION, "git push"


def _gh_check(tokens, i, whole_cmd):
    args = tokens[i + 1:]
    if args and args[0] == "api":
        rest = args[1:]
        for k, a in enumerate(rest):
            m = re.match(r'^(?:-X|--method)(?:=|\s*)(\w*)$', a) or re.match(r'^-X(\w+)$', a)
            val = (m.group(1) or (rest[k + 1] if k + 1 < len(rest) else "")) if m else ""
            if val.upper() in ("POST", "PUT", "PATCH", "DELETE"):
                return BLOCK, "gh api write method"
            if a in ("-f", "-F", "--field", "--raw-field", "--input") or a.startswith("--input="):
                return BLOCK, "gh api request body (implicit POST)"
        if "graphql" in rest and re.search(r'\bmutation\b', whole_cmd, re.I):
            return BLOCK, "gh api graphql mutation"
        return ALLOW, None
    group = next((k for k, a in enumerate(args) if a in GH_GROUPS), None)
    if group is None:
        if args[:2] == ["auth", "token"] or args[:2] == ["auth", "refresh"]:
            return BLOCK, "gh auth token access"
        if args[:2] == ["auth", "status"] and any(a == "--show-token" or re.match(r'^-[a-z]*t[a-z]*$', a)
                                                  for a in args[2:]):
            return BLOCK, "gh auth status --show-token"
        return ALLOW, None
    g = args[group]
    verb = next((a for a in args[group + 1:] if not a.startswith("-")), "")
    if verb not in GH_WRITE:
        return ALLOW, None
    repo_flag = any(re.match(r'^(-R|--repo)([=\w./-]*)$', a) for a in args)
    if g == "gist" or (g == "repo" and verb == "delete") or g in ("secret", "variable") \
            or (g == "release" and verb in ("create", "publish", "delete")):
        return BLOCK, "gh %s %s" % (g, verb)
    if repo_flag or re.search(r'\bGH_REPO=', whole_cmd):
        return BLOCK, "gh write verb targeting an explicit repo"
    return CAUTION, "gh %s %s" % (g, verb)


def _check_segment(tokens, whole_cmd, direct=False):
    # `< file` redirect of a credential file, for any command.
    for k, t in enumerate(tokens):
        if (t == "<" and k + 1 < len(tokens)) or (t.startswith("<") and not t.startswith("<<") and len(t) > 1):
            tgt = tokens[k + 1] if t == "<" else t[1:]
            if _is_cred_path(tgt):
                return BLOCK, "redirect from credential file"
    # `> file` / `>> file` / `&> file` aimed at a harness file, for any command.
    for k, t in enumerate(tokens):
        tgt = None
        if t in (">", ">>", ">|", "&>", "&>>") and k + 1 < len(tokens):
            tgt = tokens[k + 1]
        else:
            m = re.match(r'^(?:\d?>>?|&>>?|>\|)(.+)$', t)
            tgt = m.group(1) if m else None
        if tgt and _is_protected(tgt):
            return BLOCK, "shell redirect into a protected harness file (use the Edit tool)"
    i, name = _command(tokens)
    if not name:
        return None
    args = tokens[i + 1:]
    g = _git(tokens)
    if name in _WRITERS or (name in ("sed", "gsed", "perl") and any(re.match(r'^-[a-zA-Z]*i', a) for a in args)) \
            or (name == "dd"):
        targets = [a[3:] if a.startswith("of=") else a for a in args if not a.startswith("-") or a.startswith("of=")]
        into_dir = name in ("cp", "mv", "install", "ln", "rsync")
        if any(_is_protected(a, as_dir=into_dir) for a in targets):
            return BLOCK, "shell write/chmod/delete of a protected harness file (use the Edit tool)"
    if name in ("grep", "egrep", "fgrep", "rg", "ag"):
        rec = name in ("rg", "ag") or any(re.match(r'^-[a-zA-Z]*[rR]|^--(?:dereference-)?recursive$', a) for a in args)
        if rec and any(_HOME_ROOT.match(a.lower()) for a in [x for x in args if not x.startswith("-")][1:]):
            return BLOCK, "recursive read over a home or root directory"
    for t in tokens[:i] + (args if name in ("export", "env") else []):
        if _EXEC_ENV.match(t):
            return BLOCK, "pager/editor/config env hook"
    if name in ("rg", "grep", "egrep", "fgrep", "ag") and any(a == "--pre" or a.startswith("--pre=") for a in args):
        return BLOCK, "preprocessor command execution (--pre)"
    if name == "find" and any(a in ("-exec", "-execdir", "-ok", "-okdir", "-delete") for a in args):
        return BLOCK, "find executes or deletes"
    if name == "git":
        j = 0
        while j < len(args) and args[j].startswith("-"):
            if args[j] == "-c" or args[j].startswith("--config-env"):
                return BLOCK, "git -c config injection"
            j += 2 if args[j] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace") else 1
    if name == "less" and any("!" in a or "|" in a for a in args):
        return BLOCK, "less shell escape"
    if name in ("vim", "nvim", "vi", "view") and any(re.match(r'^(?:-c|--cmd|-S$|\+)', a) for a in args):
        return BLOCK, "editor command execution"
    if name in ("awk", "gawk", "mawk", "nawk") and re.search(r'system\s*\(|\|&|\|\s*getline', " ".join(args)):
        return BLOCK, "awk executes commands"
    if name in ("sed", "gsed") and any(not a.startswith("-") and _SED_EXEC.search(a) for a in args):
        return BLOCK, "sed w/e command"
    if name in READERS or (g and g[0] in GIT_READ_SUBS):
        r = _cred_in(args)
        if r:
            return BLOCK, "read of " + r
    if name == "export" and (not [a for a in args if not a.startswith("-")] or "-p" in args):
        return BLOCK, "environment dump"
    if name in ("declare", "typeset") and any(re.match(r'^-[a-zA-Z]*[xp]', a) for a in args) \
            and not any("=" in a for a in args):
        return BLOCK, "environment dump"
    if name == "set" and not args:
        return BLOCK, "environment dump"
    if name == "xargs":
        k = 0
        while k < len(args) and args[k].startswith("-"):
            k += 2 if args[k] in _XARGS_VAL else 1
        if k < len(args):
            inner = _command(args[k:])
            if inner[1] in SHELLS or inner[1] in INTERPRETERS:
                return BLOCK, "xargs into a shell/interpreter"
            if inner[1] in READERS:
                # the file names arrive on stdin: only a producer that names tracked/matched files is safe
                m = re.search(r'([^|\n;&]*)\|\s*xargs\b', whole_cmd)
                if not (m and _SAFE_PRODUCER.match(m.group(1))):
                    return BLOCK, "reader fed by xargs from an unbounded producer"
            v = _check_segment(args[k:], whole_cmd, direct)
            if v and v[0] == BLOCK:
                return v
    if name == "env" or (name == "printenv" and not [a for a in args if not a.startswith("-")]):
        return BLOCK, "environment dump"
    if name == "printenv" and any(re.fullmatch(_SECRET_NAME, a, re.I) for a in args):
        return BLOCK, "printenv of secret variable"
    if name == "ps" and any(re.match(r'^(-?[A-Za-z]*(ew+|we)[A-Za-z]*|-E|-?[aux]+e)$', a) for a in args):
        return BLOCK, "ps with environment output"
    if name in ("echo", "printf") and re.search(_SECRET_VAR, " ".join(args), re.I):
        return BLOCK, "secret variable expanded into output"
    if name == "security" and any(a in ("find-generic-password", "find-internet-password") for a in args):
        return BLOCK, "keychain read"
    if name in ("nc", "ncat", "netcat", "socat"):
        return BLOCK, "raw network client"
    if name == "curl":
        for k, a in enumerate(args):
            if a in ("-T", "--upload-file") or a.startswith("--upload-file=") or re.match(r'^-(?!-)[A-Za-z]*T', a):
                return BLOCK, "curl upload"
            val = None
            if a in CURL_DATA:
                val = args[k + 1] if k + 1 < len(args) else ""
            elif re.match(r'^--[\w-]+=', a) and a.split("=", 1)[0] in CURL_DATA:
                val = a.split("=", 1)[1]
            elif re.match(r'^-[dF].', a):
                val = a[2:]
            if val is not None and re.match(r'^(?:[^=]*=)?@', val):
                return BLOCK, "curl sends a local file"
    if name == "wget" and any(a.startswith(("--post-file", "--body-file")) for a in args):
        return BLOCK, "wget uploads a local file"
    if name in ("rsync", "scp") and any("@" in a for a in args):
        return BLOCK, "remote file copy"
    if name == "gh":
        v = _gh_check(tokens, i, whole_cmd)
        if v[0] != ALLOW:
            return v
    if name == "git" and g:
        sub, a = g
        if sub == "push":
            return _push_check(a, direct)
        if sub in ("diff", "log", "show", "format-patch") and any(
                x == "--output" or x.startswith("--output=") for x in a):
            return BLOCK, "git --output writes a file"
        if sub == "config" and any(re.match(r'(?i)^(?:remote\..*\.(?:push)?url|url\..*\.(?:push)?insteadof)', x)
                                   for x in a):
            return BLOCK, "git config push-target redirection"
        if sub == "config" and not (set(a) & _GIT_CONFIG_READ) and any(_GIT_CONFIG_EXEC.match(x) for x in a):
            return BLOCK, "git config of an exec-capable or push-altering key"
        if sub == "stash" and a[:1] == ["clear"]:
            return BLOCK, "git stash clear"
        if sub == "stash" and a[:1] == ["drop"] and not any(re.match(r'^stash@\{\d+\}$', x) for x in a[1:]):
            return BLOCK, "git stash drop without an explicit stash@{N}"
        if sub in ("checkout", "restore") and any(_is_protected(x) for x in a):
            return BLOCK, "git checkout/restore of a protected harness file (use the Edit tool)"
        if sub == "reflog" and a[:1] and a[0] in ("expire", "delete"):
            return BLOCK, "git reflog expire/delete"
        if sub == "gc" and any(x.startswith("--prune") for x in a):
            return BLOCK, "git gc --prune"
        if sub in ("filter-branch", "filter-repo", "replace", "prune"):
            return BLOCK, "git history rewrite/prune"
        if sub == "update-ref" and any(x in ("-d", "--delete") for x in a):
            return BLOCK, "git update-ref delete"
        if sub == "worktree" and a[:1] == ["remove"] and any(x in ("--force", "-f") for x in a):
            return BLOCK, "git worktree remove --force"
        if sub == "reset" and "--hard" in a:
            return BLOCK, "git reset --hard"
        if sub == "clean" and any(x == "--force" or re.match(r'^-[a-z]*f', x) for x in a):
            return BLOCK, "git clean -f"
        if sub in ("checkout", "restore") and (a[-1:] == ["."] or ("--" in a and "." in a)):
            return BLOCK, "discard all working-tree changes"
        if sub == "branch":
            pos = [x for x in a if not x.startswith("-")]
            if any(re.match(r'^-[A-Za-z]*[dD]|^--delete$', x) for x in a if x.startswith("-")) and MAIN & set(a):
                return BLOCK, "delete main/master branch"
            if any(re.match(r'^-[A-Za-z]*[fmM]|^--(?:force|move)$', x) for x in a if x.startswith("-")) \
                    and pos[:1] and pos[0] in MAIN:
                return BLOCK, "move/force main/master branch"
        if sub == "remote" and a[:1] and a[0] in ("add", "set-url", "remove"):
            return BLOCK, "git remote mutation"
        if sub == "credential":
            return BLOCK, "git credential helper access"
    if name == "rm":
        fl = [a for a in args if a.startswith("-")]
        rec = any(a in ("--recursive",) or re.match(r'^-[A-Za-z]*[rR]', a) for a in fl)
        if rec and any(_DANGER_RM.match(a) for a in args if not a.startswith("-")):
            return BLOCK, "recursive delete of a root/home/cwd target"
    if name in ("sudo", "doas") or name.startswith("mkfs"):
        return BLOCK, name
    if name == "chmod" and "777" in args:
        return BLOCK, "chmod 777"
    if name == "dd" and any(a.startswith("if=") for a in args):
        return BLOCK, "dd if="
    if name == "eval":
        return BLOCK, "eval"
    if name in SHELLS and any(re.match(r'^-[a-z]*c[a-z]*$', a) for a in args):
        return BLOCK, "shell -c"
    if name in INTERPRETERS:
        positional = [a for a in args if not a.startswith("-")]
        inline = any(_INLINE_CODE.match(a) for a in args)
        stdin_code = "-" in args or (not positional and "<<" in whole_cmd)
        code = " ".join(args) if inline else (whole_cmd if stdin_code else "")
        if code and _CODE_CRED.search(code):
            return BLOCK, "inline interpreter code touching credential paths"
        if code and _CODE_EXEC.search(code):
            return BLOCK, "inline interpreter code with exec/network"
    if name in ("npm", "npx", "pnpm", "yarn", "bun"):
        # npm parses config flags anywhere before `--`; these ones execute code or point npm at another tree
        before = args[:args.index("--")] if "--" in args else args
        if any(re.match(r'^(?:--node-options|--script-shell|--prefix|--userconfig|--globalconfig|-C|--cwd|--ignore-scripts=false)(?:=|$)', a)
               for a in before):
            return BLOCK, "npm config flag that executes code or relocates the run"
    if name == "gh":
        for k, a in enumerate(args):
            val = None
            if a in ("--jq", "-q") and k + 1 < len(args):
                val = args[k + 1]
            elif a.startswith("--jq="):
                val = a[5:]
            elif a.startswith("-q") and len(a) > 2:
                val = a[2:]
            if val is not None and re.search(r'(?<![\w.])(?:env|\$ENV|\$__loc__|input_filename)\b', val):
                return BLOCK, "jq expression reads the process environment"
    if name in ("npm", "pnpm", "yarn") and "publish" in args:
        return CAUTION, "package publish"
    if "pip" in tokens[:i + 2] + [name] and "install" in args and any("://" in a or a.startswith("git+") for a in args):
        return CAUTION, "pip install from URL"
    if name in ("docker", "docker-compose", "podman"):
        return CAUTION, "docker"
    return None


def check_command(cmd, direct=False):
    """Pure verdict for a Bash command string. direct=True (CLAUDE.md integration mode) lets a plain
    non-force push to main/master through; force/URL/mirror/all pushes stay blocked."""
    if not cmd or not cmd.strip():
        return ALLOW, None
    for pat, why in WHOLE:
        if re.search(pat, cmd, re.I):
            return BLOCK, why
    raw = _raw_check(cmd)
    if raw:
        return raw
    caution = None
    for seg in _segments(cmd):
        v = _check_segment(seg, cmd, direct)
        if v and v[0] == BLOCK:
            return v
        if v and v[0] == CAUTION and not caution:
            caution = v
    return caution or (ALLOW, None)


def _current_branch(root):
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, capture_output=True,
                           text=True, timeout=3)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def _direct_mode(root):
    """True only when CLAUDE.md in root has a line `- Integration mode: `direct``. Re-read every call."""
    try:
        with open(os.path.join(root, "CLAUDE.md"), encoding="utf-8") as f:
            return re.search(r'^- Integration mode: `direct`', f.read(), re.M) is not None
    except Exception:
        return False


STALE_VERDICT_SECS = 24 * 3600


def check_stateful(cmd, root=None):
    """QA gate + bare push on main. Reads repo state; tests monkeypatch _current_branch."""
    root = root or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    subs = [g for g in (_git(s) for s in _segments(cmd)) if g and g[0] in ("commit", "push")]
    if not subs:
        return ALLOW, None
    branch = _current_branch(root)
    if not branch or branch == "HEAD":
        return ALLOW, None
    if any(s == "push" and len([x for x in a if not x.startswith("-")]) <= 1 for s, a in subs) and branch in MAIN \
            and not _direct_mode(root):
        return BLOCK, "push of main/master (current branch)"
    safe = re.sub(r'[^\w.@+-]', "_", branch.replace("/", "__"))
    try:
        vpath = os.path.join(root, ".claude", "qa", "verdict-" + safe)
        with open(vpath, encoding="utf-8") as f:
            first = f.readline()
        stale = time.time() - os.path.getmtime(vpath) > STALE_VERDICT_SECS
    except OSError:
        return ALLOW, None
    if stale:
        return CAUTION, "stale QA verdict (>24h) ignored; re-run /qa"
    if "BLOCKED SECURITY" in first:
        return BLOCK, "QA verdict BLOCKED SECURITY on this branch; resolve findings, re-run /qa --issue N"
    return ALLOW, None


_REDACT = [
    (r'(?i)\b([\w-]*(?:token|secret|passw(?:or)?d|api_?key|auth\w*|credential\w*)["\']?\s*[:=]\s*)["\']?[^\s"\']+', r'\1[REDACTED]'),
    (r'(?i)(bearer\s+)[\w.~+/=-]+', r'\1[REDACTED]'),
    (r'\b(?:gh[pousr]_|github_pat_|xox[abp]-|sk-|AKIA)[\w-]{8,}', '[REDACTED]'),
    (r'eyJ[\w-]{10,}\.eyJ[\w-]{10,}[\w.-]*', '[REDACTED]'),
    (r'(://[^/\s:@]+:)[^@\s]+@', r'\1[REDACTED]@'),
    (r'(?i)(\s-u\s+[^\s:]+:)\S+', r'\1[REDACTED]'),
]


def _log(action, cmd, reason, root):
    try:
        for pat, rep in _REDACT:
            cmd = re.sub(pat, rep, cmd)
        path = os.environ.get("CLAUDE_SECURITY_LOG") or os.path.join(root, ".claude", "logs", "security.log")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                "action": action, "reason": reason, "command": cmd[:200]}) + "\n")
    except Exception:
        pass


def main():
    try:
        data = json.load(sys.stdin)
        tool, ti = data.get("tool_name", ""), data.get("tool_input") or {}
        root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        if tool == "Bash":
            cmd = ti.get("command", "")
            v, why = check_command(cmd, _direct_mode(root))
            if v != BLOCK:
                sv, swhy = check_stateful(cmd, root)
                if sv == BLOCK or (sv == CAUTION and v == ALLOW):
                    v, why = sv, swhy
        elif tool in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit"):
            cmd = ti.get("file_path") or ti.get("notebook_path") or ""
            v, why = check_path(cmd, tool)
        else:
            return
        if v == BLOCK:
            _log("blocked", cmd, why, root)
            sys.stderr.write("Security hook: blocked - %s\n" % why)
            sys.exit(2)
        if v == ASK:
            _log("ask", cmd, why, root)
            sys.stdout.write(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "ask",
                "permissionDecisionReason": "Security hook: " + why}}) + "\n")
            return
        if v == CAUTION:
            _log("caution", cmd, why, root)
    except Exception:
        return


if __name__ == "__main__":
    main()
