"""scripts/validate_agent_memory.py: entry format, cap, exit codes, roster."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "validate_agent_memory.py"

GOOD = "- 2026-10-01 · re-run the failing test alone first · source: tests/x.py:12\n"
HEAD = "# A Memory\n\n<!-- format comment -->\n"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def mem(tmp_path: Path, name: str, content: str) -> Path:
    d = tmp_path / "mem" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "MEMORY.md").write_text(content, encoding="utf-8")
    return tmp_path / "mem"


def test_valid_file_passes(tmp_path):
    m = mem(tmp_path, "a", HEAD + GOOD + "- 2026-10-02 · b · source: commit:abc1234\n"
            "- 2026-10-02 · c · source: https://example.com/x\n- 2026-10-02 · d · source: session:ab12\n")
    assert run("--memory-dir", str(m)).returncode == 0


def test_empty_template_passes(tmp_path):
    assert run("--memory-dir", str(mem(tmp_path, "a", HEAD))).returncode == 0


def test_multiline_comment_skipped(tmp_path):
    m = mem(tmp_path, "a", "# A\n<!--\n- not an entry\nprose here\n-->\n" + GOOD)
    assert run("--memory-dir", str(m)).returncode == 0


def test_bad_date_fails(tmp_path):
    m = mem(tmp_path, "a", HEAD + "- 2026-13-45 · x · source: a.py:1\n")
    r = run("--memory-dir", str(m))
    assert r.returncode == 1 and "invalid date" in r.stdout


def test_missing_source_fails(tmp_path):
    m = mem(tmp_path, "a", HEAD + "- 2026-10-01 · a method with no source\n")
    r = run("--memory-dir", str(m))
    assert r.returncode == 1 and "MEMORY.md:4" in r.stdout


def test_bad_source_kind_fails(tmp_path):
    m = mem(tmp_path, "a", HEAD + "- 2026-10-01 · x · source: somewhere\n")
    assert run("--memory-dir", str(m)).returncode == 1


def test_prose_paragraph_fails(tmp_path):
    m = mem(tmp_path, "a", HEAD + "This session I learned many things about the codebase.\n")
    r = run("--memory-dir", str(m))
    assert r.returncode == 1 and "prose" in r.stdout


def test_151_lines_fail_150_pass(tmp_path):
    ok = mem(tmp_path, "a", "# A\n" + GOOD * 149)  # 150 lines
    assert run("--memory-dir", str(ok)).returncode == 0
    over = mem(tmp_path / "o", "a", "# A\n" + GOOD * 150)  # 151 lines
    r = run("--memory-dir", str(over))
    assert r.returncode == 1 and "151 lines" in r.stdout


def test_usage_errors_exit_2(tmp_path):
    assert run("--memory-dir", str(tmp_path / "nope")).returncode == 2
    m = mem(tmp_path, "a", HEAD)
    assert run("--memory-dir", str(m), "--agent", "ghost").returncode == 2


def test_agent_filter_only_checks_that_agent(tmp_path):
    m = mem(tmp_path, "good", HEAD)
    mem(tmp_path, "bad", HEAD + "prose\n")
    assert run("--memory-dir", str(m), "--agent", "good").returncode == 0
    assert run("--memory-dir", str(m), "--agent", "bad").returncode == 1


def _roster(tmp_path: Path, agents: list[str], dirs: list[str]):
    ad = tmp_path / "agents"
    ad.mkdir()
    for a in agents:
        (ad / f"{a}.md").write_text("---\nname: x\n---\n")
    (ad / "TEMPLATE.md").write_text("t")
    (ad / "README.md").write_text("r")
    md = tmp_path / "mem"
    md.mkdir()
    for d in dirs:
        (md / d).mkdir()
        (md / d / "MEMORY.md").write_text(HEAD)
    return ["--check-roster", "--agents-dir", str(ad), "--memory-dir", str(md)]


def test_roster_match_passes(tmp_path):
    assert run(*_roster(tmp_path, ["a", "b"], ["a", "b"])).returncode == 0


def test_roster_agent_without_memory_dir_fails(tmp_path):
    r = run(*_roster(tmp_path, ["a", "b"], ["a"]))
    assert r.returncode == 1 and "missing memory dir for agent 'b'" in r.stdout


def test_roster_memory_dir_without_agent_fails(tmp_path):
    r = run(*_roster(tmp_path, ["a"], ["a", "ghost"]))
    assert r.returncode == 1 and "no agent file 'ghost.md'" in r.stdout


def test_repo_memory_files_are_valid():
    assert run().returncode == 0
