"""scripts/recall.py: redacted text-only transcript reader. Stub at the boundary: a fake HOME."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "recall.py"
TOKEN = "ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4"


def _line(role, content):
    return json.dumps({"type": role, "message": {"role": role, "content": content}})


def _setup(tmp_path):
    proj = tmp_path / "work" / "app"
    proj.mkdir(parents=True)
    d = tmp_path / "home" / ".claude" / "projects" / str(proj.resolve()).replace("/", "-")
    d.mkdir(parents=True)
    return proj, d


def _run(tmp_path, proj, *args):
    env = {**os.environ, "HOME": str(tmp_path / "home")}
    env.pop("CLAUDE_PROJECT_DIR", None)
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=proj, env=env, capture_output=True, text=True)


def _session(d, name, lines, mtime):
    p = d / name
    p.write_text("\n".join(lines) + "\n")
    os.utime(p, (mtime, mtime))
    return p


def test_text_only_masked_and_tools_dropped(tmp_path):
    proj, d = _setup(tmp_path)
    _session(d, "s1.jsonl", [
        _line("user", f"deploy with {TOKEN} please"),
        _line("assistant", [
            {"type": "text", "text": "running it"},
            {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "TOOLUSE_MARKER"}},
        ]),
        _line("user", [{"type": "tool_result", "tool_use_id": "t1", "content": "TOOLRESULT_MARKER"}]),
        _line("user", [{"type": "text", "text": "thanks"}]),
    ], 1000)
    r = _run(tmp_path, proj)
    assert r.returncode == 0, r.stderr
    assert TOKEN not in r.stdout
    assert "TOOLRESULT_MARKER" not in r.stdout and "TOOLUSE_MARKER" not in r.stdout
    assert r.stdout.splitlines() == ["U: deploy with [REDACTED GH TOKEN] please", "A: running it", "U: thanks"]


def test_default_is_newest_top_level_non_subagent(tmp_path):
    proj, d = _setup(tmp_path)
    _session(d, "old.jsonl", [_line("user", "OLD")], 1000)
    _session(d, "main.jsonl", [_line("user", "MAIN")], 2000)
    _session(d, "agent-abc.jsonl", [_line("user", "SUBAGENT")], 3000)
    (d / "main" / "subagents").mkdir(parents=True)
    _session(d / "main" / "subagents", "x.jsonl", [_line("user", "NESTED")], 4000)
    assert _run(tmp_path, proj).stdout.strip() == "U: MAIN"
    assert _run(tmp_path, proj, "old").stdout.strip() == "U: OLD"


def test_grep_filters_lines(tmp_path):
    proj, d = _setup(tmp_path)
    _session(d, "s.jsonl", [_line("user", "alpha"), _line("assistant", "beta")], 1000)
    assert _run(tmp_path, proj, "--grep", "bet").stdout.strip() == "A: beta"


def test_missing_dir_fails_clearly(tmp_path):
    proj = tmp_path / "nowhere"
    proj.mkdir()
    (tmp_path / "home").mkdir()
    r = _run(tmp_path, proj)
    assert r.returncode != 0 and "no transcript" in r.stderr.lower()
