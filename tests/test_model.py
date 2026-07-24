from typing import Any

import pytest

from agent_completion_ledger.model import EvidenceState, SourceRecord


def valid_mapping() -> dict[str, Any]:
    return {
        "submission": "demo",
        "source_path": "results.json",
        "source_blob_sha": "a" * 40,
        "benchmark_size": 10,
        "generated": 8,
        "resolved": 3,
        "no_logs": 1,
        "no_generation_raw": 2,
        "inferred_no_claim": 2,
        "source_format": "compact",
        "example_failed_instance": "x__x-1",
    }


def test_evidence_states_are_stable() -> None:
    assert [state.value for state in EvidenceState] == [
        "SUPPORTED",
        "FAILED",
        "UNVERIFIABLE",
        "NO_CLAIM",
    ]


def test_record_from_mapping() -> None:
    record = SourceRecord.from_mapping(valid_mapping())
    assert record.generated == 8


def test_failed_property() -> None:
    record = SourceRecord.from_mapping(valid_mapping())
    assert record.failed == 4


def test_unsupported_inclusive_property() -> None:
    record = SourceRecord.from_mapping(valid_mapping())
    assert record.unsupported_inclusive == 5


def test_discrepancy_property() -> None:
    value = valid_mapping()
    value["no_generation_raw"] = 4
    record = SourceRecord.from_mapping(value)
    assert record.no_generation_discrepancy == 2


def test_missing_field_rejected() -> None:
    value = valid_mapping()
    value.pop("resolved")
    with pytest.raises(ValueError, match="missing fields"):
        SourceRecord.from_mapping(value)


@pytest.mark.parametrize(
    "field",
    [
        "benchmark_size",
        "generated",
        "resolved",
        "no_logs",
        "no_generation_raw",
        "inferred_no_claim",
    ],
)
def test_negative_count_rejected(field: str) -> None:
    value = valid_mapping()
    value[field] = -1
    with pytest.raises(ValueError):
        SourceRecord.from_mapping(value)


def test_non_integer_count_rejected() -> None:
    value = valid_mapping()
    value["generated"] = 8.0
    with pytest.raises(TypeError):
        SourceRecord.from_mapping(value)


def test_generated_over_benchmark_rejected() -> None:
    value = valid_mapping()
    value["generated"] = 11
    value["inferred_no_claim"] = -1
    with pytest.raises(ValueError):
        SourceRecord.from_mapping(value)


def test_resolved_over_generated_rejected() -> None:
    value = valid_mapping()
    value["resolved"] = 9
    with pytest.raises(ValueError):
        SourceRecord.from_mapping(value)


def test_no_logs_over_unresolved_rejected() -> None:
    value = valid_mapping()
    value["no_logs"] = 6
    with pytest.raises(ValueError):
        SourceRecord.from_mapping(value)


def test_inferred_no_claim_mismatch_rejected() -> None:
    value = valid_mapping()
    value["inferred_no_claim"] = 3
    with pytest.raises(ValueError, match="inferred_no_claim"):
        SourceRecord.from_mapping(value)


def test_bad_sha_rejected() -> None:
    value = valid_mapping()
    value["source_blob_sha"] = "xyz"
    with pytest.raises(ValueError, match="blob SHA"):
        SourceRecord.from_mapping(value)
