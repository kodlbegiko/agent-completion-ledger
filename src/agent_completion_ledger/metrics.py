from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from math import sqrt

from .model import SourceRecord


@dataclass(frozen=True, slots=True)
class Interval:
    lower: float
    upper: float


@dataclass(frozen=True, slots=True)
class SubmissionMetrics:
    submission: str
    generated: int
    resolved: int
    failed: int
    unverifiable: int
    no_claim: int
    false_completion_rate: float
    strict_false_completion_rate: float
    baseline_completion_precision: float
    ledger_completion_precision: float
    false_completion_interval: Interval
    no_generation_discrepancy: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AggregateMetrics:
    submissions: int
    benchmark_slots: int
    generated: int
    resolved: int
    failed: int
    unverifiable: int
    no_claim: int
    false_completion_rate: float
    strict_false_completion_rate: float
    baseline_completion_precision: float
    ledger_completion_precision: float
    false_completion_interval: Interval
    strict_false_completion_interval: Interval
    submissions_above_threshold: int
    threshold: float
    stopping_minimum_claims: int
    stopping_rule_met: bool
    h1_supported: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def safe_rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def wilson_interval(
    successes: int,
    trials: int,
    z: float = 1.959963984540054,
) -> Interval:
    if trials <= 0:
        return Interval(0.0, 0.0)
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between zero and trials")
    proportion = successes / trials
    denominator = 1 + z * z / trials
    center = (proportion + z * z / (2 * trials)) / denominator
    margin = z * sqrt(
        proportion * (1 - proportion) / trials + z * z / (4 * trials * trials)
    )
    margin /= denominator
    return Interval(max(0.0, center - margin), min(1.0, center + margin))


def analyze_record(record: SourceRecord) -> SubmissionMetrics:
    inclusive = record.unsupported_inclusive
    strict_trials = record.generated - record.no_logs
    return SubmissionMetrics(
        submission=record.submission,
        generated=record.generated,
        resolved=record.resolved,
        failed=record.failed,
        unverifiable=record.no_logs,
        no_claim=record.inferred_no_claim,
        false_completion_rate=safe_rate(inclusive, record.generated),
        strict_false_completion_rate=safe_rate(record.failed, strict_trials),
        baseline_completion_precision=safe_rate(record.resolved, record.generated),
        ledger_completion_precision=1.0 if record.resolved else 0.0,
        false_completion_interval=wilson_interval(inclusive, record.generated),
        no_generation_discrepancy=record.no_generation_discrepancy,
    )


def analyze_records(
    records: Iterable[SourceRecord],
    *,
    threshold: float = 0.20,
    stopping_minimum_claims: int = 3000,
) -> tuple[list[SubmissionMetrics], AggregateMetrics]:
    materialized = list(records)
    if not materialized:
        raise ValueError("at least one source record is required")
    names = [record.submission for record in materialized]
    if len(names) != len(set(names)):
        raise ValueError("submission names must be unique")

    per_submission = [analyze_record(record) for record in materialized]
    benchmark_slots = sum(record.benchmark_size for record in materialized)
    generated = sum(record.generated for record in materialized)
    resolved = sum(record.resolved for record in materialized)
    failed = sum(record.failed for record in materialized)
    unverifiable = sum(record.no_logs for record in materialized)
    no_claim = sum(record.inferred_no_claim for record in materialized)
    inclusive = generated - resolved
    strict_trials = generated - unverifiable
    above = sum(item.false_completion_rate > threshold for item in per_submission)
    inclusive_interval = wilson_interval(inclusive, generated)
    strict_interval = wilson_interval(failed, strict_trials)
    stopping_met = generated >= stopping_minimum_claims
    h1_supported = stopping_met and inclusive_interval.lower > threshold and above >= 5

    aggregate = AggregateMetrics(
        submissions=len(materialized),
        benchmark_slots=benchmark_slots,
        generated=generated,
        resolved=resolved,
        failed=failed,
        unverifiable=unverifiable,
        no_claim=no_claim,
        false_completion_rate=safe_rate(inclusive, generated),
        strict_false_completion_rate=safe_rate(failed, strict_trials),
        baseline_completion_precision=safe_rate(resolved, generated),
        ledger_completion_precision=1.0 if resolved else 0.0,
        false_completion_interval=inclusive_interval,
        strict_false_completion_interval=strict_interval,
        submissions_above_threshold=above,
        threshold=threshold,
        stopping_minimum_claims=stopping_minimum_claims,
        stopping_rule_met=stopping_met,
        h1_supported=h1_supported,
    )
    return per_submission, aggregate
