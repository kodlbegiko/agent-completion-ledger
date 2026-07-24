import pytest

from agent_completion_ledger.metrics import (
    analyze_record,
    analyze_records,
    safe_rate,
    wilson_interval,
)
from agent_completion_ledger.model import SourceRecord


def record(
    name: str = "a",
    generated: int = 100,
    resolved: int = 30,
    no_logs: int = 5,
) -> SourceRecord:
    return SourceRecord(
        submission=name,
        source_path="x",
        source_blob_sha="b" * 40,
        benchmark_size=120,
        generated=generated,
        resolved=resolved,
        no_logs=no_logs,
        no_generation_raw=120 - generated,
        inferred_no_claim=120 - generated,
        source_format="compact",
        example_failed_instance="x__x-1",
    )


def test_safe_rate_regular() -> None:
    assert safe_rate(1, 4) == 0.25


def test_safe_rate_zero_denominator() -> None:
    assert safe_rate(1, 0) == 0.0


def test_wilson_zero_trials() -> None:
    assert wilson_interval(0, 0).lower == 0.0


def test_wilson_all_successes() -> None:
    interval = wilson_interval(10, 10)
    assert 0.72 < interval.lower < 1
    assert interval.upper == pytest.approx(1.0)


def test_wilson_rejects_invalid_successes() -> None:
    with pytest.raises(ValueError):
        wilson_interval(11, 10)


def test_analyze_record_rates() -> None:
    item = analyze_record(record())
    assert item.false_completion_rate == 0.70
    assert item.strict_false_completion_rate == pytest.approx(65 / 95)


def test_baseline_precision() -> None:
    assert analyze_record(record()).baseline_completion_precision == 0.30


def test_ledger_precision_is_one_with_supported_items() -> None:
    assert analyze_record(record()).ledger_completion_precision == 1.0


def test_ledger_precision_zero_without_supported_items() -> None:
    assert analyze_record(record(resolved=0)).ledger_completion_precision == 0.0


def test_aggregate_counts(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records)
    assert aggregate.generated == 3364
    assert aggregate.resolved == 1323
    assert aggregate.failed == 2035
    assert aggregate.unverifiable == 6


def test_aggregate_rate(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records)
    assert aggregate.false_completion_rate == pytest.approx(2041 / 3364)


def test_strict_sensitivity(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records)
    assert aggregate.strict_false_completion_rate == pytest.approx(2035 / 3358)


def test_preregistered_stopping_rule(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records)
    assert aggregate.stopping_rule_met is True
    assert aggregate.h1_supported is True
    assert aggregate.submissions_above_threshold == 7


def test_h1_fails_when_minimum_too_high(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records, stopping_minimum_claims=4000)
    assert aggregate.h1_supported is False


def test_h1_fails_when_threshold_too_high(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records, threshold=0.90)
    assert aggregate.h1_supported is False


def test_empty_records_rejected() -> None:
    with pytest.raises(ValueError, match="at least one"):
        analyze_records([])


def test_duplicate_submission_rejected() -> None:
    item = record()
    with pytest.raises(ValueError, match="unique"):
        analyze_records([item, item])


def test_each_real_submission_above_twenty_percent(
    records: list[SourceRecord],
) -> None:
    items, _ = analyze_records(records)
    assert all(item.false_completion_rate > 0.20 for item in items)


def test_aggregate_wilson_lower_bound(records: list[SourceRecord]) -> None:
    _, aggregate = analyze_records(records)
    assert aggregate.false_completion_interval.lower > 0.59
