"""Tests for scripts/leak_gate.sh and scripts/coupling_lint.sh.

Both scripts run as subprocesses against a throwaway git repo (tmp_path).
Fixture tokens are fake: johndoe, example.com, acme.
"""
import subprocess
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts" / "leak_gate.sh"
LINT = ROOT / "scripts" / "coupling_lint.sh"


def git(repo, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
        cwd=repo, check=True, capture_output=True,
    )


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q")
    (r / "README.md").write_text("clean readme\n")
    (r / "src.txt").write_text("nothing here\n")
    git(r, "add", "-A")
    git(r, "commit", "-qm", "init")
    return r


@pytest.fixture
def patterns(tmp_path):
    p = tmp_path / "patterns.txt"
    p.write_text("# comment\n\njohndoe\n")
    return p


def run(script, repo, *args):
    return subprocess.run(
        ["bash", str(script), *args, str(repo)], capture_output=True, text=True
    )


def gate(repo, patterns, *args):
    return run(GATE, repo, "--patterns", str(patterns), *args)


def test_clean_repo_passes(repo, patterns):
    r = gate(repo, patterns)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK" in r.stdout


def test_content_hit_case_insensitive(repo, patterns):
    (repo / "notes.md").write_text("owner is JOHNDOE here\n")
    r = gate(repo, patterns)
    assert r.returncode == 1
    assert "notes.md:1" in r.stdout


def test_filename_hit(repo, patterns):
    (repo / "notes-johndoe.md").write_text("")
    r = gate(repo, patterns)
    assert r.returncode == 1
    assert "notes-" in r.stdout


def test_directory_name_hit(repo, patterns):
    (repo / "JohnDoe-stuff").mkdir()
    (repo / "JohnDoe-stuff" / "a.md").write_text("x\n")
    assert gate(repo, patterns).returncode == 1


def test_hit_inside_docx(repo, patterns):
    with zipfile.ZipFile(repo / "deck.docx", "w") as z:
        z.writestr("word/document.xml", "<w:t>contact johndoe</w:t>")
    r = gate(repo, patterns)
    assert r.returncode == 1
    assert "deck.docx!word/document.xml" in r.stdout


def test_hit_in_gitignore(repo, patterns):
    (repo / ".gitignore").write_text("# johndoe private dir\nbuild/\n")
    r = gate(repo, patterns)
    assert r.returncode == 1
    assert ".gitignore:1" in r.stdout


def test_waived_hit_is_printed_and_passes(repo, patterns):
    (repo / "CONTRIBUTING.md").write_text("git clone example.com/johndoe/tpl\n")
    (repo / ".github").mkdir()
    (repo / ".github" / "release-waivers.txt").write_text(
        "CONTRIBUTING.md:johndoe # public clone url\n"
        ".github/release-waivers.txt:johndoe # waiver names the token\n"
    )
    r = gate(repo, patterns)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "WAIVED: CONTRIBUTING.md :: pattern #" in r.stdout
    assert "public clone url" in r.stdout
    # the waiver line names the pattern by index: the gate never prints what it protects
    assert ":: johndoe ::" not in r.stdout


def test_output_never_contains_raw_token(repo, patterns):
    (repo / "notes.md").write_text("the JohnDoe account\n")
    (repo / "x-johndoe.md").write_text("")
    for extra in ([], ["--report"]):
        r = gate(repo, patterns, *extra)
        out = (r.stdout + r.stderr).lower()
        assert r.returncode == 1
        assert "johndoe" not in out
        assert "***" in out


def test_report_groups_by_pattern(repo, patterns):
    (repo / "notes.md").write_text("johndoe\n")
    r = gate(repo, patterns, "--report")
    assert "-- pattern #3 --" in r.stdout
    assert "notes.md:1" in r.stdout


def test_no_patterns_file_notice_exit_0(repo, tmp_path):
    missing = tmp_path / "nope.txt"
    r = gate(repo, missing)
    assert r.returncode == 0
    assert "NOTICE" in r.stdout


def test_require_patterns_exit_2(repo, tmp_path):
    r = gate(repo, tmp_path / "nope.txt", "--require-patterns")
    assert r.returncode == 2


def test_path_rules_run_without_patterns(repo, tmp_path):
    (repo / "handover.md").write_text("x\n")
    r = gate(repo, tmp_path / "nope.txt")
    assert r.returncode == 1
    assert "filetype:handover" in r.stdout


def test_image_allowed_only_in_approved_dirs(repo, patterns):
    (repo / "docs" / "guides" / "images").mkdir(parents=True)
    (repo / "docs" / "guides" / "images" / "ok.png").write_bytes(b"\x89PNG")
    assert gate(repo, patterns).returncode == 0
    (repo / "stray.png").write_bytes(b"\x89PNG")
    r = gate(repo, patterns)
    assert r.returncode == 1 and "stray.png" in r.stdout


def test_untracked_files_are_scanned_ignored_are_not(repo, patterns):
    (repo / ".gitignore").write_text("secret_dir/\n")
    git(repo, "add", ".gitignore")
    (repo / "secret_dir").mkdir()
    (repo / "secret_dir" / "a.txt").write_text("johndoe\n")
    assert gate(repo, patterns).returncode == 0
    (repo / "untracked.txt").write_text("johndoe\n")
    assert gate(repo, patterns).returncode == 1


def test_dash_named_files_do_not_disable_scan(repo, patterns):
    """A file named like a grep option must not swallow options or hide other files' hits."""
    (repo / "--exclude=*").write_text("clean\n")
    (repo / "-r").write_text("johndoe in a dash file\n")
    (repo / "leak-me.txt").write_text("johndoe\n")
    r = gate(repo, patterns)
    assert r.returncode == 1
    assert "leak-me.txt:1" in r.stdout
    assert "-r:1" in r.stdout


def test_coupling_dash_named_files(repo):
    (repo / "--exclude=*").write_text("clean\n")
    (repo / "leak-me.txt").write_text(f"{ATOM}\n")
    r = run(LINT, repo)
    assert r.returncode == 1 and "leak-me.txt:1" in r.stdout


def test_history_catches_token_added_then_removed(repo, patterns):
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    (repo / "cfg.txt").write_text("owner johndoe\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "add")
    (repo / "cfg.txt").write_text("owner redacted\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "remove")
    assert gate(repo, patterns).returncode == 0          # working tree is clean
    r = gate(repo, patterns, "--history", base)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "cfg.txt" in r.stdout and "johndoe" not in (r.stdout + r.stderr).lower()
    assert gate(repo, patterns, "--history", "HEAD").returncode == 0   # empty range


def test_history_bad_ref_is_usage_error(repo, patterns):
    assert gate(repo, patterns, "--history", "no-such-ref").returncode == 2


# --- coupling lint ---------------------------------------------------------

ATOM = "ATOM-" + "123"          # built at runtime so this file stays lint-clean
SRC_IMPORT = "from src" + ".foo import x"


def test_coupling_lint_catches_ids_and_src_imports(repo):
    (repo / "a.md").write_text(f"see {ATOM} for details\n")
    (repo / "b.py").write_text(SRC_IMPORT + "\n")
    r = run(LINT, repo)
    assert r.returncode == 1
    assert "a.md:1" in r.stdout and "b.py:1" in r.stdout


def test_coupling_lint_clean_passes(repo):
    assert run(LINT, repo).returncode == 0


def test_coupling_lint_filename_hit(repo):
    (repo / ("notes-" + "ATOM-" + "123" + ".md")).write_text("")
    assert run(LINT, repo).returncode == 1


def test_coupling_summary_counts_per_file(repo):
    (repo / "a.md").write_text(f"{ATOM}\nok\n{ATOM}\n")
    (repo / "b.py").write_text(SRC_IMPORT + "\n")
    r = run(LINT, repo, "--summary")
    assert r.returncode == 0   # report mode
    lines = r.stdout.splitlines()
    assert any(l.split()[0] == "2" and l.endswith("a.md") for l in lines)
    assert any(l.split()[0] == "1" and l.endswith("b.py") for l in lines)
    assert "TOTAL: 3" in r.stdout


def test_coupling_allow_waives(repo, tmp_path):
    (repo / "a.md").write_text(f"{ATOM}\n")
    allow = tmp_path / "allow.txt"
    allow.write_text("a.md:*  # legacy\n")
    r = run(LINT, repo, "--allow", str(allow))
    assert r.returncode == 0
