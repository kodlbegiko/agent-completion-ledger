import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from agent_completion_ledger.assertions import (
    AssertionOutcome,
    UnsafePathError,
    evaluate_assertion,
    resolve_repo_path,
)
from agent_completion_ledger.contract import AssertionSpec


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("hello marker\n", encoding="utf-8")
    (tmp_path / "empty.txt").write_text("", encoding="utf-8")
    (tmp_path / "data.json").write_text(
        json.dumps({"version": "1.0", "nested": {"enabled": True}, "items": [3]}),
        encoding="utf-8",
    )
    return tmp_path


@pytest.mark.parametrize("value", ["../secret", "a/../../secret", "/etc/passwd", "C:\\secret", "C:/secret"])
def test_unsafe_paths_rejected(repo: Path, value: str) -> None:
    with pytest.raises(UnsafePathError):
        resolve_repo_path(repo, value)


def test_safe_path_resolves(repo: Path) -> None:
    assert resolve_repo_path(repo, "README.md") == repo / "README.md"


def test_symlink_rejected(repo: Path) -> None:
    target = repo / "README.md"
    link = repo / "link.md"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable")
    with pytest.raises(UnsafePathError, match="symbolic"):
        resolve_repo_path(repo, "link.md")


@pytest.mark.parametrize(
    ("spec", "outcome"),
    [
        (AssertionSpec("a", "file-exists", path="README.md"), AssertionOutcome.PASS),
        (AssertionSpec("a", "file-exists", path="missing"), AssertionOutcome.FAIL),
        (AssertionSpec("a", "file-not-exists", path="missing"), AssertionOutcome.PASS),
        (AssertionSpec("a", "file-not-exists", path="README.md"), AssertionOutcome.FAIL),
        (AssertionSpec("a", "file-not-empty", path="README.md"), AssertionOutcome.PASS),
        (AssertionSpec("a", "file-not-empty", path="empty.txt"), AssertionOutcome.FAIL),
        (AssertionSpec("a", "text-contains", path="README.md", text="marker"), AssertionOutcome.PASS),
        (AssertionSpec("a", "text-contains", path="README.md", text="absent"), AssertionOutcome.FAIL),
        (
            AssertionSpec("a", "json-path", path="data.json", json_path="nested.enabled", expected=True),
            AssertionOutcome.PASS,
        ),
        (
            AssertionSpec("a", "json-path", path="data.json", json_path="items.0", expected=3),
            AssertionOutcome.PASS,
        ),
        (
            AssertionSpec("a", "json-path", path="data.json", json_path="version", expected="2"),
            AssertionOutcome.FAIL,
        ),
        (
            AssertionSpec("a", "required-files", paths=("README.md", "data.json")),
            AssertionOutcome.PASS,
        ),
        (
            AssertionSpec("a", "required-files", paths=("README.md", "missing")),
            AssertionOutcome.FAIL,
        ),
        (
            AssertionSpec("a", "forbidden-files", paths=("missing",)),
            AssertionOutcome.PASS,
        ),
        (
            AssertionSpec("a", "forbidden-files", paths=("README.md",)),
            AssertionOutcome.FAIL,
        ),
    ],
)
def test_file_assertions(repo: Path, spec: AssertionSpec, outcome: AssertionOutcome) -> None:
    assert evaluate_assertion(spec, repo, ()).outcome is outcome


def test_sha256_passes(repo: Path) -> None:
    digest = hashlib.sha256((repo / "README.md").read_bytes()).hexdigest()
    result = evaluate_assertion(
        AssertionSpec("sha", "file-sha256", path="README.md", sha256=digest), repo, ()
    )
    assert result.outcome is AssertionOutcome.PASS


def test_sha256_fails(repo: Path) -> None:
    result = evaluate_assertion(
        AssertionSpec("sha", "file-sha256", path="README.md", sha256="0" * 64), repo, ()
    )
    assert result.outcome is AssertionOutcome.FAIL


def test_json_path_missing_is_unverifiable(repo: Path) -> None:
    result = evaluate_assertion(
        AssertionSpec("json", "json-path", path="data.json", json_path="missing", expected=1),
        repo,
        (),
    )
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_command_passes(repo: Path) -> None:
    spec = AssertionSpec(
        "command",
        "command",
        command=(sys.executable, "-c", "raise SystemExit(0)"),
        timeout_seconds=10,
    )
    result = evaluate_assertion(spec, repo, (sys.executable,))
    assert result.outcome is AssertionOutcome.PASS
    assert result.actual_exit_code == 0


def test_command_failure(repo: Path) -> None:
    spec = AssertionSpec(
        "command",
        "test-command",
        command=(sys.executable, "-c", "raise SystemExit(3)"),
        timeout_seconds=10,
    )
    result = evaluate_assertion(spec, repo, (sys.executable,))
    assert result.outcome is AssertionOutcome.FAIL
    assert result.actual_exit_code == 3


def test_expected_nonzero_exit_code(repo: Path) -> None:
    spec = AssertionSpec(
        "command",
        "exit-code",
        command=(sys.executable, "-c", "raise SystemExit(3)"),
        expected_exit_code=3,
        timeout_seconds=10,
    )
    assert evaluate_assertion(spec, repo, (sys.executable,)).outcome is AssertionOutcome.PASS


def test_command_not_allowlisted(repo: Path) -> None:
    spec = AssertionSpec("command", "command", command=(sys.executable, "--version"))
    assert evaluate_assertion(spec, repo, ()).outcome is AssertionOutcome.UNVERIFIABLE


def test_remote_url_argument_rejected(repo: Path) -> None:
    spec = AssertionSpec(
        "command", "command", command=(sys.executable, "https://example.invalid/code.py")
    )
    result = evaluate_assertion(spec, repo, (sys.executable,))
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_command_timeout(repo: Path) -> None:
    spec = AssertionSpec(
        "command",
        "command",
        command=(sys.executable, "-c", "import time; time.sleep(2)"),
        timeout_seconds=0.01,
    )
    result = evaluate_assertion(spec, repo, (sys.executable,), include_timing=True)
    assert result.outcome is AssertionOutcome.UNVERIFIABLE
    assert "timed out" in result.message
    assert result.duration_ms is not None


def test_working_directory_traversal(repo: Path) -> None:
    spec = AssertionSpec(
        "command",
        "command",
        command=(sys.executable, "--version"),
        working_directory="..",
    )
    assert evaluate_assertion(spec, repo, (sys.executable,)).outcome is AssertionOutcome.UNVERIFIABLE


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def test_git_working_tree_clean_and_dirty(repo: Path) -> None:
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "fixture@example.invalid")
    _git(repo, "config", "user.name", "Fixture")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "baseline")
    spec = AssertionSpec("git", "git-working-tree-clean")
    assert evaluate_assertion(spec, repo, ()).outcome is AssertionOutcome.PASS
    (repo / "README.md").write_text("changed marker\n", encoding="utf-8")
    assert evaluate_assertion(spec, repo, ()).outcome is AssertionOutcome.FAIL


def test_git_diff_contains(repo: Path) -> None:
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "fixture@example.invalid")
    _git(repo, "config", "user.name", "Fixture")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "baseline")
    (repo / "README.md").write_text("changed evidence-marker\n", encoding="utf-8")
    spec = AssertionSpec("git", "git-diff-contains", text="evidence-marker")
    assert evaluate_assertion(spec, repo, ()).outcome is AssertionOutcome.PASS


def test_assertion_result_to_dict_with_optional_fields() -> None:
    from agent_completion_ledger.assertions import AssertionResult

    result = AssertionResult(
        id="x",
        type="command",
        outcome=AssertionOutcome.PASS,
        message="ok",
        blocking=True,
        duration_ms=4,
        actual_exit_code=0,
    )
    assert result.to_dict()["durationMs"] == 4
    assert result.to_dict()["actualExitCode"] == 0


def test_missing_path_in_direct_spec_is_unverifiable(repo: Path) -> None:
    result = evaluate_assertion(AssertionSpec("x", "file-exists"), repo, ())
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_not_empty_missing_file_fails(repo: Path) -> None:
    result = evaluate_assertion(
        AssertionSpec("x", "file-not-empty", path="missing"), repo, ()
    )
    assert result.outcome is AssertionOutcome.FAIL


def test_sha_missing_file_fails(repo: Path) -> None:
    result = evaluate_assertion(
        AssertionSpec("x", "file-sha256", path="missing", sha256="0" * 64), repo, ()
    )
    assert result.outcome is AssertionOutcome.FAIL


def test_text_missing_file_fails(repo: Path) -> None:
    result = evaluate_assertion(
        AssertionSpec("x", "text-contains", path="missing", text="x"), repo, ()
    )
    assert result.outcome is AssertionOutcome.FAIL


def test_text_invalid_utf8_is_unverifiable(repo: Path) -> None:
    (repo / "binary").write_bytes(b"\xff")
    result = evaluate_assertion(
        AssertionSpec("x", "text-contains", path="binary", text="x"), repo, ()
    )
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_json_missing_file_fails(repo: Path) -> None:
    result = evaluate_assertion(
        AssertionSpec("x", "json-path", path="missing", json_path="x", expected=1),
        repo,
        (),
    )
    assert result.outcome is AssertionOutcome.FAIL


def test_json_scalar_path_is_unverifiable(repo: Path) -> None:
    (repo / "scalar.json").write_text('"value"', encoding="utf-8")
    result = evaluate_assertion(
        AssertionSpec("x", "json-path", path="scalar.json", json_path="x", expected=1),
        repo,
        (),
    )
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_empty_direct_command_is_unverifiable(repo: Path) -> None:
    result = evaluate_assertion(AssertionSpec("x", "command"), repo, ())
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_allowlisted_missing_executable_is_unverifiable(repo: Path) -> None:
    executable = "__agent_completion_ledger_missing_executable__"
    result = evaluate_assertion(
        AssertionSpec("x", "command", command=(executable,)), repo, (executable,)
    )
    assert result.outcome is AssertionOutcome.UNVERIFIABLE


def test_working_directory_file_is_unverifiable(repo: Path) -> None:
    spec = AssertionSpec(
        "x",
        "command",
        command=(sys.executable, "--version"),
        working_directory="README.md",
    )
    assert evaluate_assertion(spec, repo, (sys.executable,)).outcome is AssertionOutcome.UNVERIFIABLE


def test_unknown_assertion_is_unverifiable(repo: Path) -> None:
    result = evaluate_assertion(AssertionSpec("x", "future-type"), repo, ())
    assert result.outcome is AssertionOutcome.UNVERIFIABLE
