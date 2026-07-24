from agent_completion_ledger.io import load_records
from agent_completion_ledger.metrics import analyze_records
from agent_completion_ledger.model import SourceRecord


def test_leave_one_out_stays_above_twenty_percent(
    records: list[SourceRecord],
) -> None:
    for omitted in records:
        subset = [record for record in records if record != omitted]
        _, aggregate = analyze_records(subset, stopping_minimum_claims=1)
        assert aggregate.false_completion_interval.lower > 0.20


def test_five_of_seven_still_exceed_forty_percent(
    records: list[SourceRecord],
) -> None:
    _, aggregate = analyze_records(records, threshold=0.40)
    assert aggregate.submissions_above_threshold == 5
    assert aggregate.h1_supported is True


def test_sixty_percent_threshold_fails_five_of_seven_rule(
    records: list[SourceRecord],
) -> None:
    _, aggregate = analyze_records(records, threshold=0.60)
    assert aggregate.submissions_above_threshold == 4
    assert aggregate.h1_supported is False


def test_break_even_requires_large_oracle_reclassification(
    records: list[SourceRecord],
) -> None:
    _, aggregate = analyze_records(records)
    unsupported = aggregate.generated - aggregate.resolved
    allowed = int(aggregate.generated * 0.20)
    share = (unsupported - allowed) / unsupported
    assert share > 0.67
