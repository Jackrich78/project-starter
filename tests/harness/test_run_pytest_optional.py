"""`npm test` is two lanes with one degrade rule, and CI runs what the docs say it runs.

Lanes (`scripts/run_pytest_optional.mjs`): `harness` runs tests/harness under python3 -m pytest;
`project` runs tests/unit + tests/integration under `uv run --frozen pytest`. A lane whose runtime
or suite is missing prints one NOTICE and exits 0, so a Node-only cloner never sees red.
The runner derives its root from its own location, so each case copies it into a bare tmp tree.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "run_pytest_optional.mjs"
WORKFLOWS = ROOT / ".github" / "workflows"


def _run(tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    (tmp_path / "scripts").mkdir()
    runner = tmp_path / "scripts" / RUNNER.name
    shutil.copy(RUNNER, runner)
    return subprocess.run(["node", str(runner), *args], cwd=tmp_path, capture_output=True, text=True, timeout=60)


def test_project_lane_degrades_without_pyproject(tmp_path):
    r = _run(tmp_path, "project")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "NOTICE: project tests skipped - add pyproject.toml and run uv sync once" in r.stdout


def test_harness_lane_degrades_without_suite_dir(tmp_path):
    r = _run(tmp_path, "harness")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "NOTICE: tests/harness not found" in r.stdout


def test_default_runs_harness_then_project(tmp_path):
    r = _run(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.index("tests/harness not found") < r.stdout.index("project tests skipped")


def _steps(workflow: str) -> list[dict]:
    data = yaml.safe_load((WORKFLOWS / workflow).read_text(encoding="utf-8"))
    return [s for job in data["jobs"].values() for s in job["steps"]]


def _python_versions(workflow: str) -> list[str]:
    return [str(s["with"]["python-version"]) for s in _steps(workflow) if "setup-python" in s.get("uses", "")]


def test_ci_python_is_312():
    for wf in ("validate.yml", "harness-health.yml"):
        versions = _python_versions(wf)
        assert versions, f"{wf}: no setup-python step"
        assert versions == ["3.12"] * len(versions), f"{wf}: python-version {versions}"


def test_validate_has_project_tests_guarded_by_pyproject():
    guarded = [s for s in _steps("validate.yml") if "pyproject.toml" in str(s.get("if", ""))]
    assert guarded, "validate.yml: no step guarded by `if: hashFiles('pyproject.toml') != ''`"
    assert any("uv run --frozen pytest" in str(s.get("run", "")) for s in guarded)


def test_package_json_has_project_lane():
    scripts = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"]
    assert "test:project" in scripts
    assert "test:py" in scripts
    assert "project" in scripts["test:project"]
