from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class EvidenceState(StrEnum):
    """A completion-reporting state, not a prediction of user satisfaction."""

    SUPPORTED = "SUPPORTED"
    FAILED = "FAILED"
    UNVERIFIABLE = "UNVERIFIABLE"
    NO_CLAIM = "NO_CLAIM"


@dataclass(frozen=True, slots=True)
class SourceRecord:
    submission: str
    source_path: str
    source_blob_sha: str
    benchmark_size: int
    generated: int
    resolved: int
    no_logs: int
    no_generation_raw: int
    inferred_no_claim: int
    source_format: str
    example_failed_instance: str | None

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> SourceRecord:
        required = {
            "submission",
            "source_path",
            "source_blob_sha",
            "benchmark_size",
            "generated",
            "resolved",
            "no_logs",
            "no_generation_raw",
            "inferred_no_claim",
            "source_format",
            "example_failed_instance",
        }
        missing = required - value.keys()
        if missing:
            raise ValueError(f"missing fields: {', '.join(sorted(missing))}")
        record = cls(
            submission=value["submission"],
            source_path=value["source_path"],
            source_blob_sha=value["source_blob_sha"],
            benchmark_size=value["benchmark_size"],
            generated=value["generated"],
            resolved=value["resolved"],
            no_logs=value["no_logs"],
            no_generation_raw=value["no_generation_raw"],
            inferred_no_claim=value["inferred_no_claim"],
            source_format=value["source_format"],
            example_failed_instance=value["example_failed_instance"],
        )
        record.validate()
        return record

    def validate(self) -> None:
        if not self.submission or not self.source_path or not self.source_blob_sha:
            raise ValueError("submission, source_path, and source_blob_sha must be non-empty")
        numeric = (
            self.benchmark_size,
            self.generated,
            self.resolved,
            self.no_logs,
            self.no_generation_raw,
            self.inferred_no_claim,
        )
        if any(not isinstance(item, int) for item in numeric):
            raise TypeError("count fields must be integers")
        if any(item < 0 for item in numeric):
            raise ValueError("count fields cannot be negative")
        if self.benchmark_size <= 0:
            raise ValueError("benchmark_size must be positive")
        if self.generated > self.benchmark_size:
            raise ValueError("generated cannot exceed benchmark_size")
        if self.resolved > self.generated:
            raise ValueError("resolved cannot exceed generated")
        if self.no_logs > self.generated - self.resolved:
            raise ValueError("no_logs cannot exceed unresolved generated claims")
        if self.inferred_no_claim != self.benchmark_size - self.generated:
            raise ValueError("inferred_no_claim must equal benchmark_size - generated")
        valid_sha = len(self.source_blob_sha) == 40 and all(
            char in "0123456789abcdef" for char in self.source_blob_sha
        )
        if not valid_sha:
            raise ValueError("source_blob_sha must be a lowercase 40-character Git blob SHA-1")

    @property
    def failed(self) -> int:
        return self.generated - self.resolved - self.no_logs

    @property
    def unsupported_inclusive(self) -> int:
        return self.generated - self.resolved

    @property
    def no_generation_discrepancy(self) -> int:
        return self.no_generation_raw - self.inferred_no_claim
