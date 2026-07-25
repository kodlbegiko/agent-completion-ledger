from __future__ import annotations

import tomllib
from pathlib import Path

from agent_completion_ledger import __version__


def test_runtime_version_matches_project_metadata() -> None:
    project = tomllib.loads(
        (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert __version__ == project["project"]["version"]
