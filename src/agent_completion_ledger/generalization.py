from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .metrics import Interval, wilson_interval


@dataclass(frozen=True, slots=True)
class MultiSweBenchRecord:
    source_repository: str
    source_commit: str
    source_path: str
    source_blob_sha: str
    total_instances: int
    submitted_instances: int
    completed_instances: int
    resolved_instances: int
    unresolved_instances: int
    empty_error_patch_instances: int
    unstopped_instances: int

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> MultiSweBenchRecord:
        record = cls(**value)
        record.validate()
        return record

    def validate(self) -> None:
        counts = (
            self.total_instances,
            self.submitted_instances,
            self.completed_instances,
            self.resolved_instances,
            self.unresolved_instances,
            self.empty_error_patch_instances,
            self.unstopped_instances,
        )
        if any(not isinstance(item, int) for item in counts):
            raise TypeError("generalization counts must be integers")
        if any(item < 0 for item in counts):
            raise ValueError("generalization counts cannot be negative")
        if self.completed_instances != self.submitted_instances:
            raise ValueError("completed_instances must equal submitted_instances")
        if self.resolved_instances + self.unresolved_instances != self.completed_instances:
            raise ValueError("resolved + unresolved must equal completed")
        if self.completed_instances > self.total_instances:
            raise ValueError("completed cannot exceed total")
        if len(self.source_blob_sha) != 40 or any(
            item not in "0123456789abcdef" for item in self.source_blob_sha
        ):
            raise ValueError("source_blob_sha must be a lowercase Git blob SHA-1")


@dataclass(frozen=True, slots=True)
class GeneralizationResult:
    verdict: str
    unsupported_rate: float
    wilson_95: Interval
    baseline_precision: float
    incomplete_rate: float
    excluding_empty_error_rate: float | None
    reclassifications_to_20_percent: int
    share_unsupported_reclassified: float
    record: MultiSweBenchRecord

    def to_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": "1",
            "study": "multi-swe-bench-go-magentless-confirmatory",
            "verdict": self.verdict,
            "record": asdict(self.record),
            "metrics": {
                "unsupportedRate": self.unsupported_rate,
                "wilson95": asdict(self.wilson_95),
                "baselineCompletionPrecision": self.baseline_precision,
                "incompleteRate": self.incomplete_rate,
                "excludingEmptyErrorRate": self.excluding_empty_error_rate,
                "reclassificationsToReachAtMost20Percent": (self.reclassifications_to_20_percent),
                "shareUnsupportedRequiringReclassification": (self.share_unsupported_reclassified),
            },
            "policyB": "UNTESTABLE HERE",
            "scopeNote": (
                "Executable benchmark evidence, not user satisfaction or semantic correctness"
            ),
        }


def analyze_generalization(record: MultiSweBenchRecord) -> GeneralizationResult:
    completed = record.completed_instances
    unsupported = record.unresolved_instances
    rate = unsupported / completed
    interval = wilson_interval(unsupported, completed)
    incomplete_rate = record.unstopped_instances / completed
    h1 = completed >= 50 and incomplete_rate <= 0.10 and rate > 0.20 and interval.lower > 0.20

    denominator_without_empty = completed - record.empty_error_patch_instances
    numerator_without_empty = unsupported - record.empty_error_patch_instances
    excluding_empty: float | None = None
    if denominator_without_empty > 0 and numerator_without_empty >= 0:
        excluding_empty = numerator_without_empty / denominator_without_empty

    maximum_at_20 = math.floor(completed * 0.20)
    reclassifications = max(0, unsupported - maximum_at_20)
    share = reclassifications / unsupported if unsupported else 0.0
    return GeneralizationResult(
        verdict="SUPPORTED" if h1 else "NOT SUPPORTED",
        unsupported_rate=rate,
        wilson_95=interval,
        baseline_precision=record.resolved_instances / completed,
        incomplete_rate=incomplete_rate,
        excluding_empty_error_rate=excluding_empty,
        reclassifications_to_20_percent=reclassifications,
        share_unsupported_reclassified=share,
        record=record,
    )


def load_generalization_record(path: Path) -> MultiSweBenchRecord:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("generalization source must be an object")
    return MultiSweBenchRecord.from_mapping(value)


def write_generalization_result(source: Path, output: Path) -> GeneralizationResult:
    result = analyze_generalization(load_generalization_record(source))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result
