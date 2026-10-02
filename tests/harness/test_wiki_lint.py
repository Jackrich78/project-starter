"""scripts/wiki_lint.py against a tmp_path fixture wiki."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("yaml")
SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "wiki_lint.py"


def page(type_="guide", extra="", body="# T\n"):
    return f"---\ntype: {type_}\n{extra}---\n\n{body}"


@pytest.fixture
def wiki(tmp_path):
    docs = tmp_path / "docs"
    (docs / "guides").mkdir(parents=True)
    (docs / "index.md").write_text("# index\n\n- [a](guides/a.md)\n")
    (docs / "log.md").write_text("# log\n")
    (docs / "guides" / "a.md").write_text(page())
    return tmp_path


def lint(root, *flags):
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--all", "--json", *flags],
                       capture_output=True, text=True)
    return r.returncode, json.loads(r.stdout)


def has(report, level, needle):
    return any(f["level"] == level and needle in f["message"] for f in report["findings"])


def test_clean_wiki_passes(wiki):
    code, rep = lint(wiki)
    assert code == 0 and rep["errors"] == 0 and rep["warnings"] == 0


def test_missing_frontmatter_is_error(wiki):
    (wiki / "docs/guides/a.md").write_text("# no frontmatter\n")
    code, rep = lint(wiki)
    assert code == 1 and has(rep, "ERROR", "missing frontmatter")


def test_unknown_type_is_error(wiki):
    (wiki / "docs/guides/a.md").write_text(page("banana"))
    code, rep = lint(wiki)
    assert code == 1 and has(rep, "ERROR", "unknown type")


def test_unknown_decay_tier_is_error(wiki):
    (wiki / "docs/guides/a.md").write_text(page(extra="decay_tier: soonish\n"))
    code, rep = lint(wiki)
    assert code == 1 and has(rep, "ERROR", "decay_tier")


def test_over_cap_is_error_and_split_deferred_downgrades(wiki):
    p = wiki / "docs/guides/a.md"
    p.write_text(page(body="x\n" * 300))
    code, rep = lint(wiki)
    assert code == 1 and has(rep, "ERROR", "300-line cap")
    p.write_text(page(body="# SPLIT-DEFERRED too big for now\n" + "x\n" * 299))
    code, rep = lint(wiki)
    assert code == 0 and has(rep, "WARNING", "SPLIT-DEFERRED")


def test_broken_link_is_warning(wiki):
    (wiki / "docs/guides/a.md").write_text(page(body="[x](nope.md)\n"))
    code, rep = lint(wiki)
    assert code == 0 and has(rep, "WARNING", "broken link")


def test_link_inside_code_fence_ignored(wiki):
    (wiki / "docs/guides/a.md").write_text(page(body="```\n[x](nope.md)\n```\n"))
    _, rep = lint(wiki)
    assert not has(rep, "WARNING", "broken link")


def test_unindexed_page_is_warning(wiki):
    (wiki / "docs/guides/b.md").write_text(page())
    code, rep = lint(wiki)
    assert code == 0 and has(rep, "WARNING", "not indexed")


def test_supersedes_missing_target_is_error(wiki):
    (wiki / "docs/guides/a.md").write_text(page(extra="supersedes: gone.md\n"))
    code, rep = lint(wiki)
    assert code == 1 and has(rep, "ERROR", "supersedes")


def test_supersedes_existing_target_ok(wiki):
    (wiki / "docs/guides/a.md").write_text(page(extra="supersedes: ../index.md\n"))
    code, _ = lint(wiki)
    assert code == 0


def test_stale_after_past_is_warning(wiki):
    (wiki / "docs/guides/a.md").write_text(page(extra="stale_after: 2020-01-01\n"))
    code, rep = lint(wiki)
    assert code == 0 and has(rep, "WARNING", "stale")


def test_decay_tier_derived_from_updated(wiki):
    (wiki / "docs/guides/a.md").write_text(page(extra="decay_tier: figures\nupdated: 2020-01-01\n"))
    _, rep = lint(wiki)
    assert has(rep, "WARNING", "decay_tier 'figures'")


def test_strict_promotes_warnings(wiki):
    (wiki / "docs/guides/a.md").write_text(page(body="[x](nope.md)\n"))
    assert lint(wiki)[0] == 0
    code, rep = lint(wiki, "--strict")
    assert code == 1 and has(rep, "ERROR", "broken link")


def test_reserved_names_skip_type_check(wiki):
    (wiki / "docs/index.md").write_text("# index, no frontmatter\n\n- [a](guides/a.md)\n")
    code, rep = lint(wiki)
    assert code == 0 and not has(rep, "ERROR", "frontmatter")


def test_skill_md_scanned_without_index(wiki):
    s = wiki / ".claude/skills/x"
    s.mkdir(parents=True)
    (s / "SKILL.md").write_text("---\nname: x\n---\n")
    code, rep = lint(wiki)
    assert code == 1 and has(rep, "ERROR", "type")


def test_archive_excluded(wiki):
    (wiki / "docs/archive").mkdir()
    (wiki / "docs/archive/old.md").write_text("no frontmatter\n")
    code, _ = lint(wiki)
    assert code == 0


def test_summary_line_and_text_format(wiki):
    (wiki / "docs/guides/a.md").write_text("# x\n")
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(wiki), "--all"], capture_output=True, text=True)
    assert "docs/guides/a.md:1 ERROR" in r.stdout
    assert r.stdout.strip().splitlines()[-1] == "wiki_lint: 1 errors, 0 warnings over 3 files"
