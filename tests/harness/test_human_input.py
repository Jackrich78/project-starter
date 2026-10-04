"""scripts/github/human_input.py: the human's input since the assistant's last signed comment.

Exercised through the CLI as a subprocess. gh is a fake binary on PATH.
"""
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "github" / "human_input.py"
SIG = "> *Posted by the assistant.*"
NOW = "2026-10-04T12:00:00Z"


def claude_md(tmp_path, sig=f"`{SIG}`"):
    p = tmp_path / "CLAUDE.md"
    p.write_text(
        "# Proj\n\n## Workflow\n\n- Integration mode: `direct`\n"
        f"- Agent signature on issues and comments: {sig} <!-- \"\" to disable -->\n"
        "- Areas (labels): `area:core`\n\n## Other\n\n- Agent signature: `bogus`\n"
    )
    return p


def comment(body, at, signed=False):
    return {
        "author": {"login": "owner"},
        "authorAssociation": "OWNER",
        # production shape: the signature is the first line (issue-flow.md § Agent signature)
        "body": (f"{SIG}\n\n" if signed else "") + body,
        "createdAt": at,
    }


def issue(n, title="T", state="OPEN", created="2026-10-01T09:00:00Z", closed=None,
          updated="2026-10-03T09:00:00Z", body="body", comments=(), labels=()):
    return {
        "number": n, "title": title, "state": state, "createdAt": created,
        "closedAt": closed, "updatedAt": updated, "body": body, "comments": list(comments),
        # gh shape: a list of label objects
        "labels": [{"id": f"L{i}", "name": l, "description": "", "color": "ffffff"}
                   for i, l in enumerate(labels)],
    }


def run(tmp_path, issues, md=None, extra=(), env=None):
    j = tmp_path / "issues.json"
    j.write_text(json.dumps(issues))
    md = md or claude_md(tmp_path)
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--from-json", str(j), "--claude-md", str(md),
         "--now", NOW, *extra],
        capture_output=True, text=True, env=env,
    )


def sections(out):
    """Map section header prefix -> list of '#N title' lines under it."""
    res, cur = {}, None
    for line in out.splitlines():
        if line.startswith("#"):
            assert cur is not None, f"issue line before any header: {line!r}"
            res[cur].append(line.strip())
        elif line.strip():
            cur = line.strip().rstrip(":")
            res.setdefault(cur, [])
    return res


def listed(out, header):
    for k, v in sections(out).items():
        if k.startswith(header):
            return v
    return []


def nums(lines):
    return [int(l.split()[0].lstrip("#")) for l in lines]


def test_ac_001_unsigned_after_signed_listed_as_replied(tmp_path):
    issues = [
        # human replied after assistant: listed
        issue(1, comments=[comment("a", "2026-10-02T09:00:00Z", True),
                           comment("human reply", "2026-10-03T09:00:00Z")]),
        # assistant answered the human: not listed
        issue(2, comments=[comment("a", "2026-10-02T09:00:00Z", True),
                           comment("human", "2026-10-03T09:00:00Z"),
                           comment("a2", "2026-10-03T10:00:00Z", True)]),
        # body unsigned, no comments: body is the newest unsigned entry, nothing signed: listed
        issue(3, body="human wrote this", created="2026-10-03T08:00:00Z"),
        # legacy: signature at end of body counts as signed at createdAt: not listed
        issue(4, body=f"handover text\n\n{SIG}", created="2026-10-03T08:00:00Z"),
        # legacy body signed, then human comment later: listed
        issue(5, body=f"handover\n\n{SIG}", created="2026-10-01T08:00:00Z",
              comments=[comment("human", "2026-10-02T08:00:00Z")]),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert sorted(nums(listed(r.stdout, "Human replied"))) == [1, 3, 5]
    assert "#2 " not in r.stdout and "#4 " not in r.stdout


def test_ac_002_close_without_signed_comment_listed_as_closed(tmp_path):
    closed = "2026-10-03T12:00:00Z"
    issues = [
        # no signed comment at all: listed
        issue(10, state="CLOSED", closed=closed, comments=[comment("x", "2026-10-01T10:00:00Z")]),
        # signed comment 30 s before close: within the 60 s window, not listed
        issue(11, state="CLOSED", closed=closed,
              comments=[comment("done", "2026-10-03T11:59:30Z", True)]),
        # signed comment after close: not listed
        issue(12, state="CLOSED", closed=closed,
              comments=[comment("done", "2026-10-03T12:05:00Z", True)]),
        # signed comment 5 minutes before close: outside window, listed
        issue(13, state="CLOSED", closed=closed,
              comments=[comment("early", "2026-10-03T11:55:00Z", True)]),
        # open issue is never under closed
        issue(14),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert sorted(nums(listed(r.stdout, "Human closed"))) == [10, 13]


def test_ac_003_open_ask_without_reply_listed_as_waiting(tmp_path):
    t = "2026-10-02T09:00:00Z"
    issues = [
        issue(20, comments=[comment("**Ask** which option?", t, True)]),
        issue(21, comments=[comment("Ask: which option?", t, True)]),
        # plain signed comment, no ask: not listed
        issue(22, comments=[comment("status update", t, True)]),
        # ask answered by unsigned entry: not under waiting
        issue(23, comments=[comment("**Ask** x", t, True),
                            comment("answer", "2026-10-03T09:00:00Z")]),
        # closed issue with an ask: never waiting
        issue(24, state="CLOSED", closed="2026-10-02T09:00:30Z",
              comments=[comment("**Ask** x", t, True)]),
        # ask is in an older signed entry; newest signed has none: not listed
        issue(25, comments=[comment("**Ask** x", t, True),
                            comment("resolved", "2026-10-02T10:00:00Z", True)]),
        # a sub-task bullet that starts with the verb "Ask" is not an Ask block: not listed
        issue(26, comments=[comment("- [ ] Ask Sam for the draft\n- ask Lee", t, True)]),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert sorted(nums(listed(r.stdout, "Waiting on you"))) == [20, 21]
    assert 24 not in nums(listed(r.stdout, "Waiting on you"))
    assert 23 in nums(listed(r.stdout, "Human replied"))


def test_ac_004_empty_signature_is_loud_and_nonzero(tmp_path):
    issues = [issue(1, comments=[comment("human", "2026-10-03T09:00:00Z")])]
    for md in (claude_md(tmp_path, sig="``"),):
        r = run(tmp_path, issues, md=md)
        assert r.returncode != 0
        assert "#1" not in r.stdout
        assert "signature" in (r.stdout + r.stderr).lower()
    # missing line entirely
    p = tmp_path / "NOSIG.md"
    p.write_text("# P\n\n## Workflow\n\n- Integration mode: `direct`\n")
    r = run(tmp_path, issues, md=p)
    assert r.returncode != 0
    assert "signature" in (r.stdout + r.stderr).lower()
    assert "nothing new" not in r.stdout


def test_ac_005_reads_claude_md_and_offline_json(tmp_path):
    fake = tmp_path / "bin"
    fake.mkdir()
    log = tmp_path / "gh.log"
    gh = fake / "gh"
    gh.write_text(f'#!/bin/sh\necho "$@" >> "{log}"\ncat "{tmp_path}/ghout.json"\n')
    gh.chmod(gh.stat().st_mode | stat.S_IXUSR)
    env = {**os.environ, "PATH": f"{fake}{os.pathsep}{os.environ['PATH']}"}
    data = [issue(1, comments=[comment("human", "2026-10-03T09:00:00Z")])]
    (tmp_path / "ghout.json").write_text(json.dumps(data))

    # offline: gh never called
    md = claude_md(tmp_path)
    r = run(tmp_path, data, md=md, env=env)
    assert r.returncode == 0, r.stderr
    assert not log.exists(), "gh was called despite --from-json"
    assert "Human replied" in r.stdout

    # signature read from CLAUDE.md, not hard-coded: a different signature
    other = claude_md(tmp_path, sig="`> *Other bot.*`")
    d2 = [issue(2, comments=[{**comment("x", "2026-10-02T09:00:00Z"),
                              "body": "x\n\n> *Other bot.*"},
                             comment("human", "2026-10-03T09:00:00Z")])]
    r = run(tmp_path, d2, md=other)
    assert 2 in nums(listed(r.stdout, "Human replied"))
    r = run(tmp_path, d2)  # default SIG: the Other-bot comment is unsigned
    assert r.returncode == 0

    # online: one gh issue list --state all call, updated:>= from --days
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--claude-md", str(md), "--now", NOW, "--days", "7"],
        capture_output=True, text=True, env=env,
    )
    assert r.returncode == 0, r.stderr
    calls = log.read_text().strip().splitlines()
    assert len(calls) == 1
    assert "issue list" in calls[0] and "--state all" in calls[0]
    assert "updated:>=2026-09-27" in calls[0]
    for f in ("number", "title", "state", "createdAt", "closedAt", "updatedAt", "body", "comments",
              "labels"):
        assert f in calls[0]

    # default is 14 days
    log.unlink()
    subprocess.run([sys.executable, str(SCRIPT), "--claude-md", str(md), "--now", NOW],
                   capture_output=True, text=True, env=env)
    assert "updated:>=2026-09-20" in log.read_text()


def test_ac_006_output_order_and_nothing_new_line(tmp_path):
    replied = lambda n, upd: issue(  # noqa: E731
        n, title=f"R{n}", updated=upd,
        comments=[comment("a", "2026-10-01T10:00:00Z", True),
                  comment("h", "2026-10-02T10:00:00Z")])
    issues = [
        replied(1, "2026-10-02T10:00:00Z"),
        replied(2, "2026-10-03T10:00:00Z"),
        issue(3, title="C3", state="CLOSED", closed="2026-10-03T10:00:00Z",
              updated="2026-10-03T10:00:00Z"),
        issue(4, title="W4", updated="2026-10-03T11:00:00Z",
              comments=[comment("Ask: pick", "2026-10-03T11:00:00Z", True)]),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    kinds = [("replied" if "replied" in l else "closed" if "closed" in l
              else "waiting" if "Waiting" in l else None) for l in lines if not l.startswith("#")]
    assert kinds == ["replied", "closed", "waiting"]
    assert [l for l in lines if l.startswith("#")] == ["#2 R2", "#1 R1", "#3 C3", "#4 W4"]
    assert "nothing new" not in r.stdout

    # all empty: exactly one line
    quiet = [issue(5, comments=[comment("a", "2026-10-02T10:00:00Z", True)])]
    r = run(tmp_path, quiet)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().splitlines() == ["Human input: nothing new"]


def test_live_shape_numbered_titles(tmp_path):
    """Found by the first live run: titles already carrying "#N · " printed the number twice."""
    md = claude_md(tmp_path)
    issues = [issue(7, title="#7 · Plain numbered title",
                    comments=[comment("human", "2026-10-03T09:00:00Z")]),
              issue(8, title="Plain title", comments=[comment("human", "2026-10-03T08:00:00Z")])]
    r = run(tmp_path, issues, md=md)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[0].rstrip(":") == "Human replied"
    assert "#7 · Plain numbered title" in r.stdout.splitlines()
    assert "#7 #7" not in r.stdout
    assert "#8 Plain title" in r.stdout.splitlines()


def test_ready_for_human_label_counts_as_waiting(tmp_path):
    """Asks written before the Ask block existed are invisible to the Ask-line check; the
    `ready-for-human` label still marks them (found by the first live run)."""
    t = "2026-10-02T09:00:00Z"
    issues = [
        issue(30, labels=["ready-for-human", "P1"], comments=[comment("old-style ask", t, True)]),
        # label but the human already replied: replied wins, listed once
        issue(31, labels=["ready-for-human"], comments=[comment("ask", t, True),
                                                        comment("answer", "2026-10-03T09:00:00Z")]),
        # closed with the label: never waiting
        issue(32, state="CLOSED", closed="2026-10-02T09:00:30Z", labels=["ready-for-human"],
              comments=[comment("done", t, True)]),
        # other labels only, no Ask line: not waiting
        issue(33, labels=["ready-for-agent"], comments=[comment("status", t, True)]),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert nums(listed(r.stdout, "Waiting on you")) == [30]
    assert nums(listed(r.stdout, "Human replied")) == [31]


def test_qa_reply_after_signed_close_is_listed_as_replied(tmp_path):
    """QA: the replied rule applies to closed issues too, once the close itself was signed."""
    closed = "2026-10-02T12:00:00Z"
    issues = [
        issue(40, state="CLOSED", closed=closed,
              comments=[comment("closing", "2026-10-02T12:00:10Z", True),
                        comment("actually, one more thing", "2026-10-03T09:00:00Z")]),
        # signed close, nothing after: neither list
        issue(41, state="CLOSED", closed=closed,
              comments=[comment("closing", "2026-10-02T12:00:10Z", True)]),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert nums(listed(r.stdout, "Human replied")) == [40]
    assert nums(listed(r.stdout, "Human closed")) == []


def test_qa_quote_reply_is_not_signed(tmp_path):
    """QA: a GitHub quote-reply nests the signature ("> > ...") and the human may quote it
    inline; only a line that is exactly the signature marks the assistant."""
    t = "2026-10-02T09:00:00Z"
    quoted = f"> {SIG}\n>\n> **Ask (#50 · x):** pick\n\nB please"
    inline = f"you wrote {SIG} but I disagree"
    issues = [
        issue(50, comments=[comment("**Ask (#50 · x):** pick", t, True),
                            comment(quoted, "2026-10-03T09:00:00Z")]),
        issue(51, comments=[comment("status", t, True),
                            comment(inline, "2026-10-03T09:00:00Z")]),
    ]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert sorted(nums(listed(r.stdout, "Human replied"))) == [50, 51]


def test_qa_ask_mid_line_is_not_an_ask(tmp_path):
    """QA: pins the ^ anchor on the Ask line."""
    issues = [issue(60, comments=[comment("see the **Ask** above; Ask: is answered",
                                          "2026-10-02T09:00:00Z", True)])]
    r = run(tmp_path, issues)
    assert r.returncode == 0, r.stderr
    assert nums(listed(r.stdout, "Waiting on you")) == []


def test_qa_signature_read_from_workflow_section_only(tmp_path):
    """QA: a same-prefix line outside ## Workflow is ignored."""
    p = tmp_path / "CLAUDE.md"
    p.write_text("# P\n\n## Notes\n\n- Agent signature on issues and comments: `> *Decoy.*`\n"
                 "\n## Workflow\n\n"
                 f"- Agent signature on issues and comments: `{SIG}`\n\n## Later\n")
    issues = [issue(70, comments=[comment("status", "2026-10-02T09:00:00Z", True),
                                  comment("human", "2026-10-03T09:00:00Z")])]
    r = run(tmp_path, issues, md=p)
    assert r.returncode == 0, r.stderr
    assert nums(listed(r.stdout, "Human replied")) == [70]
