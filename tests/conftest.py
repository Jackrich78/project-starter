"""Root pytest fixtures for the whole tree (harness and project lanes).

`Bash(npm test -- *)` is pre-approved in `.claude/settings.json`, so anything pytest collects
runs without a permission prompt. This fixture makes sure a collected test can never spend an
API budget or call out: every environment variable whose name ends in KEY, TOKEN, SECRET or
PASSWORD is removed, and in-process sockets are disabled, for every test in every lane.
Live checks are explicit script calls outside pytest, which prompt.

Scope: in-process only. A test that shells out starts a child with the parent environment and
a working network, so tests must not subprocess anything that reads keys or opens a socket
(`.claude/rules/testing.md`). Spawning local tools (node, python3, git) is fine.
"""

import os
import re
import socket

import pytest

SECRET_NAME = re.compile(r"(KEY|TOKEN|SECRET|PASSWORD)$")


def _network_disabled(*_args, **_kwargs):
    raise RuntimeError("network is disabled under pytest")


@pytest.fixture(autouse=True)
def _no_keys_no_network(monkeypatch):
    for name in [n for n in os.environ if SECRET_NAME.search(n)]:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(socket, "socket", _network_disabled)
    monkeypatch.setattr(socket, "create_connection", _network_disabled)
    yield
