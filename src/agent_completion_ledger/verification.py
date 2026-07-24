from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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

    @property
    def counts(self) -> dict[str, int]:
        return {
            state.value: sum(item.ledger_status is state for item in self.tasks)
            for state in EvidenceState
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": self.schema_version,
            "contractSchemaVersion": self.contract_schema_version,
            "counts": self.counts,
            "tasks": [item.to_dict() for item in self.tasks],
        }


def _task_status(task: TaskSpec, results: tuple[AssertionResult, ...]) -> EvidenceState:
    if task.claim_status == "none":
        return EvidenceState.NO_CLAIM
    blocking = [item for item in results if item.blocking]
    if any(item.outcome is AssertionOutcome.FAIL for item in blocking):
        return EvidenceState.FAILED
    if not blocking or any(
        item.outcome is AssertionOutcome.UNVERIFIABLE for item in blocking
    ):
        return EvidenceState.UNVERIFIABLE
    return EvidenceState.SUPPORTED


def verify_contract(
    contract: CompletionContract,
    repo_root: Path,
    *,
    task_id: str | None = None,
    include_timing: bool = False,
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
    return VerificationReport(
        schema_version="1",
        contract_schema_version=contract.schema_version,
        tasks=tuple(task_results),
    )


def report_exit_code(report: VerificationReport) -> int:
    states = {item.ledger_status for item in report.tasks}
    if EvidenceState.UNVERIFIABLE in states:
        return 2
    if EvidenceState.FAILED in states:
        return 1
    return 0
