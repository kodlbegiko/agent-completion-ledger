from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class ContractError(ValueError):
    """Raised when a completion evidence contract is invalid."""


@dataclass(frozen=True, slots=True)
class AssertionSpec:
    id: str
    type: str
    blocking: bool = True
    path: str | None = None
    sha256: str | None = None
    text: str | None = None
    json_path: str | None = None
    expected: Any = None
    command: tuple[str, ...] = ()
    expected_exit_code: int = 0
    timeout_seconds: float = 300.0
    working_directory: str = "."
    paths: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TaskSpec:
    id: str
    description: str
    claim_status: str
    agent: str | None
    recorded_at: str | None
    evidence: tuple[AssertionSpec, ...]


@dataclass(frozen=True, slots=True)
class CompletionContract:
    schema_version: str
    allowed_executables: tuple[str, ...]
    tasks: tuple[TaskSpec, ...]


def _schema() -> dict[str, Any]:
    resource = files("agent_completion_ledger").joinpath(
        "schemas/completion-contract.schema.json"
    )
    value = json.loads(resource.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError("packaged contract schema is not a JSON object")
    return value


def load_contract(path: Path) -> CompletionContract:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractError(f"cannot read contract: {exc}") from exc

    try:
        if path.suffix.lower() == ".json":
            raw: Any = json.loads(text)
        else:
            raw = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ContractError(f"cannot parse contract: {exc}") from exc
    return contract_from_mapping(raw)


def contract_from_mapping(raw: Any) -> CompletionContract:
    if not isinstance(raw, dict):
        raise ContractError("contract must be an object")

    validator = Draft202012Validator(_schema())
    errors = sorted(validator.iter_errors(raw), key=lambda item: list(item.absolute_path))
    if errors:
        formatted: list[str] = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "$"
            formatted.append(f"{location}: {error.message}")
        raise ContractError("contract schema validation failed: " + "; ".join(formatted))

    policy = raw.get("policy", {})
    allowed = tuple(str(item) for item in policy.get("allowedExecutables", []))
    tasks: list[TaskSpec] = []
    for raw_task in raw["tasks"]:
        assertions: list[AssertionSpec] = []
        for item in raw_task.get("evidence", []):
            assertions.append(
                AssertionSpec(
                    id=item["id"],
                    type=item["type"],
                    blocking=item.get("blocking", True),
                    path=item.get("path"),
                    sha256=item.get("sha256"),
                    text=item.get("text"),
                    json_path=item.get("jsonPath"),
                    expected=item.get("expected"),
                    command=tuple(item.get("command", [])),
                    expected_exit_code=item.get("expectedExitCode", 0),
                    timeout_seconds=float(item.get("timeoutSeconds", 300)),
                    working_directory=item.get("workingDirectory", "."),
                    paths=tuple(item.get("paths", [])),
                )
            )
        claim = raw_task["claim"]
        tasks.append(
            TaskSpec(
                id=raw_task["id"],
                description=raw_task.get("description", ""),
                claim_status=claim["status"],
                agent=claim.get("agent"),
                recorded_at=claim.get("recordedAt"),
                evidence=tuple(assertions),
            )
        )

    identifiers = [task.id for task in tasks]
    if len(identifiers) != len(set(identifiers)):
        raise ContractError("task ids must be unique")
    return CompletionContract(
        schema_version=raw["schemaVersion"],
        allowed_executables=allowed,
        tasks=tuple(tasks),
    )


def default_contract() -> dict[str, Any]:
    return {
        "schemaVersion": "1",
        "policy": {"allowedExecutables": ["python"]},
        "tasks": [
            {
                "id": "example-task",
                "description": "Replace this task with a concrete completion claim.",
                "claim": {"status": "completed", "agent": "unknown"},
                "evidence": [
                    {
                        "id": "readme-exists",
                        "type": "file-exists",
                        "path": "README.md",
                    },
                    {
                        "id": "tests-pass",
                        "type": "test-command",
                        "command": ["python", "-m", "pytest"],
                        "expectedExitCode": 0,
                        "timeoutSeconds": 300,
                    },
                ],
            }
        ],
    }
