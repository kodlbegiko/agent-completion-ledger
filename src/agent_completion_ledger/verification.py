from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path

from . import __version__
from .assertions import AssertionOutcome, AssertionResult, evaluate_assertion
from .contract import CompletionContract, TaskSpec
from .model import EvidenceState


@dataclass(frozen=True, slots=True)
class TaskVerification:
    task_id: str
    description: str
    claimed_status: str
    ledger_status: EvidenceState
    assertions: tuple[AssertionResult, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "taskId": self.task_id,
            "description": self.description,
            "claimedStatus": self.claimed_status,
            "ledgerStatus": self.ledger_status.value,
            "assertions": [item.to_dict() for item in self.assertions],
        }


@dataclass(frozen=True, slots=True)
class VerificationReport:
    schema_version: str
    contract_schema_version: str
    tasks: tuple[TaskVerification, ...]
    tool_version: str = __version__
    repository_commit_sha: str = "UNKNOWN"
    contract_path: str = "UNKNOWN"
    contract_sha256: str = ""
    expected_contract_sha256: str | None = None
    repository_root_identity: str = "UNKNOWN"
    trusted_mode: bool = False
    contract_digest_matched: bool | None = None
    execution_mode: str = "full"
    result_digest: str = ""

    @property
    def counts(self) -> dict[str, int]:
        return {
            state.value: sum(item.ledger_status is state for item in self.tasks)
            for state in EvidenceState
        }

    @property
    def assertion_ids(self) -> tuple[str, ...]:
        return tuple(
            assertion.id for task in self.tasks for assertion in task.assertions
        )

    @property
    def overall_status(self) -> EvidenceState:
        states = {item.ledger_status for item in self.tasks}
        if EvidenceState.UNVERIFIABLE in states:
            return EvidenceState.UNVERIFIABLE
        if EvidenceState.FAILED in states:
            return EvidenceState.FAILED
        if EvidenceState.SUPPORTED in states:
            return EvidenceState.SUPPORTED
        return EvidenceState.NO_CLAIM

    def _base_dict(self) -> dict[str, object]:
        provenance: dict[str, object] = {
            "toolVersion": self.tool_version,
            "repositoryCommitSha": self.repository_commit_sha,
            "contractPath": self.contract_path,
            "contractSha256": self.contract_sha256,
            "repositoryRootIdentity": self.repository_root_identity,
            "taskIds": [item.task_id for item in self.tasks],
            "evidenceAssertionIds": list(self.assertion_ids),
            "reportSchemaVersion": self.schema_version,
            "trustedMode": self.trusted_mode,
            "executionMode": self.execution_mode,
        }
        if self.expected_contract_sha256 is not None:
            provenance["expectedContractSha256"] = self.expected_contract_sha256
        if self.contract_digest_matched is not None:
            provenance["contractDigestMatched"] = self.contract_digest_matched
        return {
            "schemaVersion": self.schema_version,
            "contractSchemaVersion": self.contract_schema_version,
            "counts": self.counts,
            "overallStatus": self.overall_status.value,
            "provenance": provenance,
            "tasks": [item.to_dict() for item in self.tasks],
        }

    def to_dict(self) -> dict[str, object]:
        result = self._base_dict()
        result["resultDigest"] = self.result_digest
        return result


def _task_status(task: TaskSpec, results: tuple[AssertionResult, ...]) -> EvidenceState:
    if task.claim_status == "none":
        return EvidenceState.NO_CLAIM
    blocking = [item for item in results if item.blocking]
    if any(item.outcome is AssertionOutcome.FAIL for item in blocking):
        return EvidenceState.FAILED
    if not blocking or any(item.outcome is AssertionOutcome.UNVERIFIABLE for item in blocking):
        return EvidenceState.UNVERIFIABLE
    return EvidenceState.SUPPORTED


def _git_text(root: Path, *arguments: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def _repository_commit(root: Path) -> str:
    return _git_text(root, "rev-parse", "HEAD") or "UNKNOWN"


def _repository_identity(root: Path) -> str:
    remote = _git_text(root, "config", "--get", "remote.origin.url")
    if remote:
        sanitized = re.sub(r"(https?://)[^/@]+@", r"\1", remote)
        return f"git:{sanitized}"
    return f"directory:{root.name}"


def _contract_path_identity(root: Path, contract_path: Path | None) -> str:
    if contract_path is None:
        return "UNKNOWN"
    try:
        resolved = contract_path.resolve(strict=True)
        return resolved.relative_to(root).as_posix()
    except (OSError, ValueError):
        return f"external:{contract_path.name}"


def _finalize_report(report: VerificationReport) -> VerificationReport:
    canonical = json.dumps(
        report._base_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return replace(report, result_digest=hashlib.sha256(canonical).hexdigest())


def contract_hash_mismatch_report(
    repo_root: Path,
    contract_path: Path,
    *,
    actual_sha256: str,
    expected_sha256: str,
) -> VerificationReport:
    """Return an integrity-only report without trusting a mismatched contract body."""

    root = repo_root.resolve(strict=True)
    assertion = AssertionResult(
        id="contract-sha256-pin",
        type="contract-sha256-pin",
        outcome=AssertionOutcome.UNVERIFIABLE,
        message="contract SHA-256 does not match the pinned trusted digest",
        blocking=True,
    )
    task = TaskVerification(
        task_id="contract-integrity",
        description="Trusted contract digest validation",
        claimed_status="completed",
        ledger_status=EvidenceState.UNVERIFIABLE,
        assertions=(assertion,),
    )
    return _finalize_report(
        VerificationReport(
            schema_version="2",
            contract_schema_version="UNKNOWN",
            tasks=(task,),
            repository_commit_sha=_repository_commit(root),
            contract_path=_contract_path_identity(root, contract_path),
            contract_sha256=actual_sha256,
            expected_contract_sha256=expected_sha256,
            repository_root_identity=_repository_identity(root),
            trusted_mode=True,
            contract_digest_matched=False,
            execution_mode="integrity-only",
        )
    )


def verify_contract(
    contract: CompletionContract,
    repo_root: Path,
    *,
    task_id: str | None = None,
    include_timing: bool = False,
    contract_path: Path | None = None,
    contract_sha256: str = "",
    expected_contract_sha256: str | None = None,
    trusted_mode: bool = False,
    contract_digest_matched: bool | None = None,
    no_exec: bool = False,
) -> VerificationReport:
    root = repo_root.resolve(strict=True)
    selected = [task for task in contract.tasks if task_id is None or task.id == task_id]
    if task_id is not None and not selected:
        raise ValueError(f"unknown task id: {task_id}")

    task_results: list[TaskVerification] = []
    for task in selected:
        assertions = tuple(
            evaluate_assertion(
                assertion,
                root,
                contract.allowed_executables,
                include_timing=include_timing,
                no_exec=no_exec,
            )
            for assertion in task.evidence
        )
        task_results.append(
            TaskVerification(
                task_id=task.id,
                description=task.description,
                claimed_status=task.claim_status,
                ledger_status=_task_status(task, assertions),
                assertions=assertions,
            )
        )
    return _finalize_report(
        VerificationReport(
            schema_version="2",
            contract_schema_version=contract.schema_version,
            tasks=tuple(task_results),
            repository_commit_sha=_repository_commit(root),
            contract_path=_contract_path_identity(root, contract_path),
            contract_sha256=contract_sha256,
            expected_contract_sha256=expected_contract_sha256,
            repository_root_identity=_repository_identity(root),
            trusted_mode=trusted_mode,
            contract_digest_matched=contract_digest_matched,
            execution_mode="static-only" if no_exec else "full",
        )
    )


def report_exit_code(report: VerificationReport) -> int:
    states = {item.ledger_status for item in report.tasks}
    if EvidenceState.UNVERIFIABLE in states:
        return 2
    if EvidenceState.FAILED in states:
        return 1
    return 0
