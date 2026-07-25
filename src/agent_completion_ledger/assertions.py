from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PureWindowsPath
from typing import Any

from .contract import AssertionSpec


class AssertionOutcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNVERIFIABLE = "UNVERIFIABLE"


@dataclass(frozen=True, slots=True)
class AssertionResult:
    id: str
    type: str
    outcome: AssertionOutcome
    message: str
    blocking: bool
    duration_ms: int | None = None
    actual_exit_code: int | None = None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "id": self.id,
            "type": self.type,
            "outcome": self.outcome.value,
            "message": self.message,
            "blocking": self.blocking,
        }
        if self.duration_ms is not None:
            result["durationMs"] = self.duration_ms
        if self.actual_exit_code is not None:
            result["actualExitCode"] = self.actual_exit_code
        return result


class UnsafePathError(ValueError):
    """Raised when a contract path escapes or ambiguously crosses repository root."""


def _is_windows_absolute(value: str) -> bool:
    path = PureWindowsPath(value)
    return path.is_absolute() or bool(path.drive)


def resolve_repo_path(root: Path, value: str, *, require_exists: bool = False) -> Path:
    if not value or Path(value).is_absolute() or _is_windows_absolute(value):
        raise UnsafePathError(f"path must be repository-relative: {value!r}")
    if ".." in Path(value).parts:
        raise UnsafePathError(f"path traversal is not allowed: {value!r}")

    root_resolved = root.resolve(strict=True)
    candidate = root_resolved / value
    current = root_resolved
    for part in Path(value).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            raise UnsafePathError(f"symbolic links are not allowed in evidence paths: {value!r}")
    resolved = candidate.resolve(strict=require_exists)
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise UnsafePathError(f"path leaves repository root: {value!r}") from exc
    return resolved


def _result(
    spec: AssertionSpec,
    outcome: AssertionOutcome,
    message: str,
    *,
    duration_ms: int | None = None,
    actual_exit_code: int | None = None,
) -> AssertionResult:
    return AssertionResult(
        id=spec.id,
        type=spec.type,
        outcome=outcome,
        message=message,
        blocking=spec.blocking,
        duration_ms=duration_ms,
        actual_exit_code=actual_exit_code,
    )


def _path_assertion(spec: AssertionSpec, root: Path) -> AssertionResult:
    if spec.path is None:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, "assertion path is missing")
    try:
        path = resolve_repo_path(root, spec.path)
    except (OSError, UnsafePathError) as exc:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, str(exc))

    if spec.type == "file-exists":
        passed = path.is_file()
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            f"{spec.path} {'exists' if passed else 'does not exist'}",
        )
    if spec.type == "file-not-exists":
        passed = not path.exists()
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            f"{spec.path} {'is absent' if passed else 'exists'}",
        )
    if spec.type == "file-not-empty":
        if not path.is_file():
            return _result(spec, AssertionOutcome.FAIL, f"{spec.path} is not a file")
        passed = path.stat().st_size > 0
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            f"{spec.path} {'is not empty' if passed else 'is empty'}",
        )
    if spec.type == "file-sha256":
        if not path.is_file():
            return _result(spec, AssertionOutcome.FAIL, f"{spec.path} is not a file")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        passed = digest == spec.sha256
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            f"sha256 {'matches' if passed else f'mismatch: {digest}'}",
        )
    if spec.type == "text-contains":
        if not path.is_file():
            return _result(spec, AssertionOutcome.FAIL, f"{spec.path} is not a file")
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return _result(spec, AssertionOutcome.UNVERIFIABLE, f"cannot read text: {exc}")
        passed = spec.text is not None and spec.text in content
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            "required text found" if passed else "required text not found",
        )
    if spec.type == "json-path":
        if not path.is_file():
            return _result(spec, AssertionOutcome.FAIL, f"{spec.path} is not a file")
        try:
            value: Any = json.loads(path.read_text(encoding="utf-8"))
            for segment in (spec.json_path or "").split("."):
                if not segment:
                    continue
                if isinstance(value, list):
                    value = value[int(segment)]
                elif isinstance(value, dict):
                    value = value[segment]
                else:
                    raise KeyError(segment)
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            KeyError,
            IndexError,
            ValueError,
        ) as exc:
            return _result(spec, AssertionOutcome.UNVERIFIABLE, f"cannot resolve json path: {exc}")
        passed = value == spec.expected
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            "json value matches" if passed else f"json value mismatch: {value!r}",
        )
    raise AssertionError("unreachable path assertion")


def _command_assertion(
    spec: AssertionSpec,
    root: Path,
    allowed_executables: tuple[str, ...],
    include_timing: bool,
) -> AssertionResult:
    if not spec.command:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, "command argument array is missing")
    executable = spec.command[0]
    if executable not in allowed_executables:
        return _result(
            spec,
            AssertionOutcome.UNVERIFIABLE,
            f"executable is not allow-listed: {executable}",
        )
    if any(argument.lower().startswith(("http://", "https://")) for argument in spec.command):
        return _result(
            spec,
            AssertionOutcome.UNVERIFIABLE,
            "remote URL arguments are not allowed",
        )
    try:
        working_directory = resolve_repo_path(root, spec.working_directory, require_exists=True)
    except (OSError, UnsafePathError) as exc:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, str(exc))
    if not working_directory.is_dir():
        return _result(spec, AssertionOutcome.UNVERIFIABLE, "workingDirectory is not a directory")

    started = time.monotonic_ns()
    try:
        completed = subprocess.run(
            list(spec.command),
            cwd=working_directory,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            timeout=spec.timeout_seconds,
            check=False,
        )
    except FileNotFoundError:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, f"executable not found: {executable}")
    except subprocess.TimeoutExpired:
        duration = int((time.monotonic_ns() - started) / 1_000_000) if include_timing else None
        return _result(
            spec,
            AssertionOutcome.UNVERIFIABLE,
            f"command timed out after {spec.timeout_seconds:g} seconds",
            duration_ms=duration,
        )
    except OSError as exc:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, f"command could not run: {exc}")

    duration = int((time.monotonic_ns() - started) / 1_000_000) if include_timing else None
    passed = completed.returncode == spec.expected_exit_code
    return _result(
        spec,
        AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
        (
            f"command exited with expected code {completed.returncode}"
            if passed
            else f"expected exit code {spec.expected_exit_code}, got {completed.returncode}"
        ),
        duration_ms=duration,
        actual_exit_code=completed.returncode,
    )


def _git_assertion(spec: AssertionSpec, root: Path) -> AssertionResult:
    command = ["git", "status", "--porcelain=v1"]
    if spec.type == "git-diff-contains":
        command = ["git", "diff", "--no-ext-diff", "--"]
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, f"git evidence unavailable: {exc}")
    if completed.returncode != 0:
        return _result(
            spec,
            AssertionOutcome.UNVERIFIABLE,
            f"git exited with code {completed.returncode}",
        )
    if spec.type == "git-working-tree-clean":
        passed = completed.stdout.strip() == ""
        return _result(
            spec,
            AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
            "working tree is clean" if passed else "working tree has changes",
        )
    passed = spec.text is not None and spec.text in completed.stdout
    return _result(
        spec,
        AssertionOutcome.PASS if passed else AssertionOutcome.FAIL,
        "git diff contains required text" if passed else "git diff does not contain required text",
    )


def _multi_path_assertion(spec: AssertionSpec, root: Path) -> AssertionResult:
    failures: list[str] = []
    unverifiable: list[str] = []
    for value in spec.paths:
        try:
            path = resolve_repo_path(root, value)
        except (OSError, UnsafePathError) as exc:
            unverifiable.append(str(exc))
            continue
        if spec.type == "required-files" and not path.is_file():
            failures.append(value)
        if spec.type == "forbidden-files" and path.exists():
            failures.append(value)
    if unverifiable:
        return _result(spec, AssertionOutcome.UNVERIFIABLE, "; ".join(unverifiable))
    if failures:
        label = "missing" if spec.type == "required-files" else "present"
        return _result(spec, AssertionOutcome.FAIL, f"{label}: {', '.join(failures)}")
    return _result(spec, AssertionOutcome.PASS, "all path requirements satisfied")


def evaluate_assertion(
    spec: AssertionSpec,
    root: Path,
    allowed_executables: tuple[str, ...],
    *,
    include_timing: bool = False,
    no_exec: bool = False,
) -> AssertionResult:
    path_types = {
        "file-exists",
        "file-not-exists",
        "file-not-empty",
        "file-sha256",
        "text-contains",
        "json-path",
    }
    command_types = {"command", "test-command", "build-command", "exit-code"}
    if spec.type in path_types:
        return _path_assertion(spec, root)
    if spec.type in command_types:
        if no_exec:
            return _result(
                spec,
                AssertionOutcome.UNVERIFIABLE,
                "command evidence disabled by static-only mode",
            )
        return _command_assertion(spec, root, allowed_executables, include_timing)
    if spec.type in {"git-diff-contains", "git-working-tree-clean"}:
        return _git_assertion(spec, root)
    if spec.type in {"required-files", "forbidden-files"}:
        return _multi_path_assertion(spec, root)
    return _result(spec, AssertionOutcome.UNVERIFIABLE, f"unsupported assertion type: {spec.type}")
