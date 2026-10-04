"""Runtime tests for the non-security hooks (stdlib + pytest only)."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

HOOKS = Path(__file__).resolve().parents[2] / ".claude" / "hooks"
sys.path.insert(0, str(HOOKS))
from pre_compact import redact  # noqa: E402

ALL_HOOKS = ["pre_compact.py", "session_start_reprime.py", "session_prime.py", "stop.py", "post_tool_use.py"]


def run(hook, stdin, project, extra_env=None):
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(project)
    env.update(extra_env or {})
    return subprocess.run(
        [sys.executable, str(HOOKS / hook)], input=stdin, capture_output=True,
        text=True, env=env, cwd=str(project), timeout=30,
    )


SECRETS = [
    ("API_KEY=abc123456789", "abc123456789"),
    ("OPENAI_API_KEY=sk-live-0123456789", "sk-live-0123456789"),
    ("MY_SECRET=hunter2hunter2", "hunter2hunter2"),
    ("DB_PASSWORD=correcthorse", "correcthorse"),
    ("GITHUB_TOKEN=abcdef123456", "abcdef123456"),
    ('{"password": "s3cretvalue"}', "s3cretvalue"),
    ("api_key: yamlsecret99", "yamlsecret99"),
    ("auth-key = tskey-abc123456", "tskey-abc123456"),
    ("token: 'quotedtoken123'", "quotedtoken123"),
    ("ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2", "A1b2C3d4E5f6G7h8I9j0K1l2"),
    ("github_pat_" + "11ABCDEFG0123456789_abcdefghij", "11ABCDEFG0123456789_abcdefghij"),
    ("xoxb-1234567890-abcdefghij", "1234567890-abcdefghij"),
    ("AKIAIOSFODNN7EXAMPLE", "AKIAIOSFODNN7EXAMPLE"),
    ("aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY", "wJalrXUtnFEMI"),
    ("Authorization: Bearer abcdefgh12345678", "abcdefgh12345678"),
    ("https://user:p4ssw0rd@example.com/x", "p4ssw0rd"),
    ("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.sig_nature-1", "eyJzdWIi"),
    ("-----BEGIN RSA PRIVATE KEY-----\nMIIEabc\n-----END RSA PRIVATE KEY-----", "MIIEabc"),
    # audit round 3 (2026-10-02): shapes the first redactor let through
    ("-----BEGIN PGP PRIVATE KEY BLOCK-----\nlQdGBF\n-----END PGP PRIVATE KEY BLOCK-----", "lQdGBF"),
    ("ASIAIOSFODNN7EXAMPLE", "ASIAIOSFODNN7EXAMPLE"),
    ("xapp-1-A0123456789-abcdefghij", "A0123456789-abcdefghij"),
    ("glpat-" + "abcdefghij1234567890", "abcdefghij1234567890"),
    ("hf_" + "abcdefghij1234567890", "abcdefghij1234567890"),
    ("npm_" + "abcdefghij1234567890", "abcdefghij1234567890"),
    ("sk_live_" + "abcdefghij1234567890", "abcdefghij1234567890"),
    ("AIza" + "SyA0123456789abcdefghijklmnopqrstu", "SyA0123456789abcdefghijklmnopqrstu"),
    ("SG." + "abcdefghij1234567890" + "." + "zyxwvutsrq0987654321", "zyxwvutsrq0987654321"),
    ("Authorization: Basic dXNlcjpwYXNzd29yZA==", "dXNlcjpwYXNzd29yZA=="),
    ("Authorization: token abcdefgh12345678", "abcdefgh12345678"),
    ("curl -u alice:hunter2x https://example.com", "hunter2x"),
    ("mysql -phunter2x db", "hunter2x"),
    ("tool --token abcdefgh12345678", "abcdefgh12345678"),
    ("tool --password=abcdefgh12345678", "abcdefgh12345678"),
    ("https://abcdefgh1234567890@example.com/x", "abcdefgh1234567890"),
    ("https://example.com/x?key=abcdefgh12345678", "abcdefgh12345678"),
    ("Cookie: session=abcdefgh12345678; csrftoken=zyxw9876", "abcdefgh12345678"),
    ("SECRET_KEY=abcdefgh12345678", "abcdefgh12345678"),
    ("DB_PASS=abcdefgh12345678", "abcdefgh12345678"),
    ("MYSQL_PWD=abcdefgh12345678", "abcdefgh12345678"),
    ("private_key=abcdefgh12345678", "abcdefgh12345678"),
    ("passphrase: abcdefgh12345678", "abcdefgh12345678"),
    ("AUTH=abcdefgh12345678", "abcdefgh12345678"),
    ("password=abcde", "abcde"),
    ('{\\"api_key\\": \\"abcdefgh12345678\\"}', "abcdefgh12345678"),
    ("CLIENT_SECRET_V2 = abcdefgh12345678", "abcdefgh12345678"),
]


def test_redact_before_truncate_keeps_no_key_prefix():
    key = "sk-ant-api03-" + "A" * 40
    text = "x" * 110 + " " + key
    out = redact(" ".join(text.split()))[:120]
    assert "sk-ant-api03-A" not in out


@pytest.mark.parametrize("text,secret", SECRETS)
def test_redact_replaces_secret(text, secret):
    out = redact(text)
    assert secret not in out
    assert out != text


@pytest.mark.parametrize("text,key", [
    ("API_KEY=abc123456789", "API_KEY="),
    ('{"password": "s3cretvalue"}', '"password": "'),
    ("Bearer abcdefgh12345678", "Bearer "),
    ("https://user:p4ssw0rd@example.com", "https://user:"),
])
def test_redact_keeps_key(text, key):
    out = redact(text)
    assert key in out and "***" in out


@pytest.mark.parametrize("text", [
    "hello world", "ls -la /tmp", "token count is low", "def f(x): return x + 1",
    "https://example.com/path?a=1", "password: ok",
])
def test_redact_benign_unchanged(text):
    assert redact(text) == text


@pytest.mark.parametrize("text", ["tokenizer=bert-base", "bypass=true", "mkdir -p build/out", "cp -p a b",
                                  "the password field is required", "git log --oneline -5", "ls -la docs/"])
def test_redact_benign_round3(text):
    assert redact(text) == text





def _transcript(tmp_path):
    def u(t):
        return {"type": "user", "message": {"role": "user", "content": t}}
    lines = [u(f"message {i} " + "x" * 500) for i in range(7)]
    lines.append({"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "text", "text": "done with it"},
        {"type": "tool_use", "name": "Edit", "input": {"file_path": "/p/src/a.py"}},
        {"type": "tool_use", "name": "Bash", "input": {"command": "curl -H 'x' API_KEY=abc123456789 host"}},
        {"type": "tool_use", "name": "Task", "input": {"subagent_type": "researcher", "description": "dig"}},
        {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
    ]}})
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(json.dumps(x) for x in lines) + "\nnot json\n")
    return p


def test_pre_compact_writes_salvage(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    t = _transcript(tmp_path)
    r = run("pre_compact.py", json.dumps({"session_id": "abc-1", "transcript_path": str(t)}), proj)
    assert r.returncode == 0 and r.stdout == ""
    files = list((proj / ".claude" / "salvage").glob("salvage-abc-1-*.md"))
    assert len(files) == 1
    text = files[0].read_text()
    for section in ("## Last user messages", "## Last assistant text", "## Files edited",
                    "## Commands run", "## Agents / skills dispatched"):
        assert section in text
    assert "/p/src/a.py" in text and "researcher: dig" in text and "skill commit" in text
    assert "message 6" in text and "message 1 " not in text  # last 5 only
    assert "abc123456789" not in text
    assert len(text.encode()) <= 6 * 1024
    assert (proj / ".claude" / "session-state.json").exists()


def test_pre_compact_keeps_newest_10(tmp_path):
    proj = tmp_path / "proj"
    sd = proj / ".claude" / "salvage"
    sd.mkdir(parents=True)
    for i in range(12):
        f = sd / f"salvage-old{i}-20200101T0000{i:02d}.md"
        f.write_text("x")
        os.utime(f, (1000 + i, 1000 + i))
    run("pre_compact.py", json.dumps({"session_id": "new", "transcript_path": str(_transcript(tmp_path))}), proj)
    assert len(list(sd.glob("salvage-*.md"))) == 10


def _salvage(proj, sid, body, age_s=0):
    sd = proj / ".claude" / "salvage"
    sd.mkdir(parents=True, exist_ok=True)
    f = sd / f"salvage-{sid}-20260101T000000.md"
    f.write_text(body)
    t = time.time() - age_s
    os.utime(f, (t, t))


def test_reprime_matching_session(tmp_path):
    _salvage(tmp_path, "sess-A", "SALVAGE-A", age_s=99999)
    r = run("session_start_reprime.py", json.dumps({"source": "compact", "session_id": "sess-A"}), tmp_path)
    out = json.loads(r.stdout)["hookSpecificOutput"]
    assert out["hookEventName"] == "SessionStart" and out["additionalContext"] == "SALVAGE-A"


def test_reprime_stale_mismatch_silent(tmp_path):
    _salvage(tmp_path, "sess-A", "SALVAGE-A", age_s=99999)
    r = run("session_start_reprime.py", json.dumps({"source": "compact", "session_id": "sess-B"}), tmp_path)
    assert r.returncode == 0 and r.stdout == ""


def test_reprime_fresh_fallback_and_startup_ignored(tmp_path):
    _salvage(tmp_path, "sess-A", "SALVAGE-A", age_s=10)
    r = run("session_start_reprime.py", json.dumps({"source": "resume", "session_id": "sess-B"}), tmp_path)
    assert "SALVAGE-A" in r.stdout
    r = run("session_start_reprime.py", json.dumps({"source": "startup", "session_id": "sess-A"}), tmp_path)
    assert r.stdout == ""


def test_session_prime_priorities(tmp_path):
    (tmp_path / "docs" / "system").mkdir(parents=True)
    (tmp_path / "docs" / "system" / "current-priorities.md").write_text(
        "---\nupdated: 2020-01-01\n---\nShip it.\n")
    r = run("session_prime.py", "{}", tmp_path)
    ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "PRIORITIES MAY BE STALE (updated: 2020-01-01)" in ctx and "Ship it" in ctx


def test_post_tool_use_index_nudge(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("- known.md\n")
    ev = lambda f: json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / f)}})
    assert "new.md" in run("post_tool_use.py", ev("docs/new.md"), tmp_path).stdout
    assert run("post_tool_use.py", ev("docs/known.md"), tmp_path).stdout == ""
    assert run("post_tool_use.py", ev("src/x.py"), tmp_path).stdout == ""


def test_stop_dirty_tree(tmp_path):
    g = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)
    g("init", "-q")
    assert run("stop.py", "{}", tmp_path).stdout == ""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "decisions.md").write_text("x\n")
    out = json.loads(run("stop.py", "{}", tmp_path).stdout)["systemMessage"]
    assert "uncommitted changes" in out and "REJECTED" in out


@pytest.mark.parametrize("hook", ALL_HOOKS)
@pytest.mark.parametrize("stdin", ["{}", "garbage \x00 {{{", ""])
def test_every_hook_fails_open_and_silent(hook, stdin, tmp_path):
    r = run(hook, stdin, tmp_path)
    assert r.returncode == 0 and r.stdout == ""
