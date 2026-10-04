"""Layer 0: .claude/settings.json is internally consistent: sets no permission mode; allow list read-only;
denies only secret stores, Claude Code private state and irreversible remote actions."""
import fnmatch
import json
import py_compile
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SETTINGS = ROOT / ".claude" / "settings.json"
HOOKS = ROOT / ".claude" / "hooks"

KNOWN_EVENTS = {
    "PreToolUse", "PostToolUse", "PostToolUseFailure", "PermissionRequest", "PermissionDenied",
    "UserPromptSubmit", "Notification", "Stop", "StopFailure", "SubagentStart", "SubagentStop",
    "PreCompact", "PostCompact", "SessionStart", "SessionEnd", "Setup", "TeammateIdle", "TaskCreated",
    "TaskCompleted", "Elicitation", "ElicitationResult", "ConfigChange", "InstructionsLoaded",
    "WorktreeCreate", "WorktreeRemove", "CwdChanged", "FileChanged",
}
REAL_TOOLS = {"Bash", "Read", "Edit", "Write", "MultiEdit", "Task", "Agent", "Glob", "Grep", "WebFetch",
              "WebSearch", "NotebookEdit", "TodoWrite", "*"}
# Allow-list entries starting with any of these execute, write, push or post: never pre-approved.
DENY_PREFIXES = [
    "git add", "git commit", "git push", "python3", "python ", "uv ", "node ", "bash", "sh ", "curl", "wget",
    "sqlite3", "awk", "sed", "find", "ps", "rm",
    "gh issue create", "gh issue edit", "gh issue comment", "gh issue close",
    "gh pr create", "gh pr merge", "gh pr edit", "gh api", "gh gist",
]
FORBIDDEN_TOP_KEYS = {"security", "logging"}  # not Claude Code settings keys


@pytest.fixture(scope="module")
def settings():
    return json.loads(SETTINGS.read_text())


def _hook_entries(settings):
    for event, groups in settings["hooks"].items():
        for g in groups:
            for h in g["hooks"]:
                yield event, g.get("matcher"), h


def test_events_known(settings):
    assert set(settings["hooks"]) <= KNOWN_EVENTS


def test_every_hook_command_resolves_to_existing_file(settings):
    for event, _, h in _hook_entries(settings):
        assert h["type"] == "command"
        m = re.search(r'\.claude/hooks/([\w.-]+\.py)', h["command"])
        assert m, "%s: command does not reference .claude/hooks/*.py: %s" % (event, h["command"])
        assert (HOOKS / m.group(1)).is_file(), "%s: missing hook file %s" % (event, m.group(1))
        assert h["command"].startswith('python3 "$CLAUDE_PROJECT_DIR/')


def test_every_hook_file_compiles(tmp_path):
    for f in sorted(HOOKS.glob("*.py")):
        py_compile.compile(str(f), cfile=str(tmp_path / (f.name + "c")), doraise=True)


def test_matchers_name_real_tools(settings):
    for event, matcher, _ in _hook_entries(settings):
        if event in ("PreToolUse", "PostToolUse") and matcher:
            assert set(matcher.split("|")) <= REAL_TOOLS, (event, matcher)


def test_security_hook_wired_on_bash_only(settings):
    # the hook checks Bash commands; Read-tool protection lives in permissions.deny
    groups = [g for g in settings["hooks"]["PreToolUse"]
              if any("pre_tool_use.py" in h["command"] for h in g["hooks"])]
    assert [g["matcher"] for g in groups] == ["Bash"]


def test_settings_leave_permission_mode_to_user(settings):
    """Any project value overrides the user's choice; the project sets no mode at all."""
    assert not ({"defaultMode", "disableBypassPermissionsMode"} & set(settings["permissions"]))


def test_no_write_or_exec_verb_pre_approved(settings):
    for entry in settings["permissions"]["allow"]:
        m = re.match(r'^Bash\((.*)\)$', entry)
        cmd = m.group(1) if m else entry
        for p in DENY_PREFIXES:
            assert not cmd.startswith(p), "pre-approved write/exec verb: %s" % entry
        assert not entry.startswith(("Write", "Edit", "WebFetch")), entry


def test_allow_list_has_no_bare_wildcard(settings):
    for entry in settings["permissions"]["allow"]:
        assert entry not in ("Bash", "Bash(*)", "Bash(:*)", "*"), entry
        assert not entry.startswith("Bash(cat"), "cat can read credentials: " + entry


def test_credential_reads_denied(settings):
    deny = set(settings["permissions"]["deny"])
    for need in ("Read(./.env)", "Read(~/.ssh/**)", "Read(~/.aws/**)", "Read(~/.netrc)", "Read(~/.config/gh/**)",
                 "Bash(sudo *)", "Bash(git push --force*)", "Bash(git push --mirror*)",
                 "Bash(gh repo delete*)", "Bash(gh gist create*)", "Bash(gh secret *)"):
        assert need in deny, need


def test_no_non_settings_keys_or_env_caps(settings):
    assert not (FORBIDDEN_TOP_KEYS & set(settings))
    assert "env" not in settings


def test_no_bare_prefix_allow_entries(settings):
    for entry in settings["permissions"]["allow"]:
        if entry == "Bash(git branch --list*)":  # explicit exception: read-only listing flag
            continue
        assert not re.search(r'[^ ]\*\)$', entry), "bare-prefix allow entry (needs a space before *): " + entry


def test_exec_vector_denies_present(settings):
    deny = set(settings["permissions"]["deny"])
    for need in ("Bash(git config remote.*)",):
        assert need in deny, need


def test_npm_allow_entries_stop_config_flags(settings):
    """`npm test *` let npm parse --node-options; only the `-- <args>` form is pre-approved."""
    allow = set(settings["permissions"]["allow"])
    assert "Bash(npm test *)" not in allow and "Bash(npm run test *)" not in allow
    assert "Bash(npm test -- *)" in allow


def test_claude_home_state_denied(settings):
    deny = set(settings["permissions"]["deny"])
    for need in ("Read(~/.claude/history.jsonl)", "Read(~/.claude/sessions/**)", "Read(~/.claude/shell-snapshots/**)",
                 "Read(~/.git-credentials)", "Read(./.claude/settings.local.json)"):
        assert need in deny, need


def test_new_denies_present_and_memory_dir_readable(settings):
    deny = settings["permissions"]["deny"]
    for need in ("Bash(gh auth status --show-token*)", "Bash(gh auth status -t*)",
                 "Read(~/.claude/projects/**/*.jsonl)", "Read(**/.dev.vars)", "Read(**/id_rsa*)"):
        assert need in deny, need
    assert "Read(~/.claude/projects/**)" not in deny
    target = "~/.claude/projects/x/memory/MEMORY.md"
    for entry in deny:
        m = re.match(r'^Read\((.*)\)$', entry)
        if m:
            pat = m.group(1).replace("**", "*")
            assert not fnmatch.fnmatch(target, pat), "deny rule matches auto-memory: " + entry


def _matching_denies(settings, call):
    """Deny entries whose pattern matches `call` (`Tool(arg)`), with `**` collapsed to `*` as above."""
    tool, _, arg = call.partition("(")
    arg = arg[:-1]
    hits = []
    for entry in settings["permissions"]["deny"]:
        m = re.match(r'^(\w+)\((.*)\)$', entry)
        if m and m.group(1) == tool and fnmatch.fnmatchcase(arg, m.group(2).replace("**", "*")):
            hits.append(entry)
    return hits


ROUTINE_CALLS = (
    "Bash(rm -rf node_modules)",
    "Bash(rm -fr dist)",
    "Bash(gh api repos/o/r/pulls)",
    "Bash(find . -name x -exec grep -l y {} +)",
    "Bash(find . -name '*.pyc' -delete)",
    "Bash(git -c color.ui=never log -1)",
    "Bash(npm install --prefix web)",
    "Read(docs/guides/credentials-setup.md)",
    "Read(tests/test_credentials.py)",
    "Read(./.env.example)",
)
DANGEROUS_CALLS = (
    "Bash(git push --force origin x)",
    "Bash(sudo ls)",
    "Bash(gh repo delete o/r)",
    "Bash(gh gist create f)",
    "Read(~/.ssh/id_rsa)",
    "Read(./.env)",
    "Read(./.env.local)",
    "Read(config/credentials.json)",
)


@pytest.mark.parametrize("call", ROUTINE_CALLS)
def test_routine_work_matches_no_deny_rule(settings, call):
    """A project deny can never be undone by the user, so only what is dangerous in every mode is denied."""
    assert _matching_denies(settings, call) == [], call


@pytest.mark.parametrize("call", DANGEROUS_CALLS)
def test_dangerous_work_still_matches_a_deny_rule(settings, call):
    assert _matching_denies(settings, call), call
