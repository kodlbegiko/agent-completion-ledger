import pytest

from agent_completion_ledger.extract import extract_counts


def test_extract_compact_counts() -> None:
    payload = {
        "no_generation": ["a", "b"],
        "no_logs": ["c"],
        "resolved": ["d", "e"],
    }
    result = extract_counts(payload, benchmark_size=10)
    assert result.generated == 8
    assert result.resolved == 2
    assert result.no_logs == 1
    assert result.inferred_no_claim == 2
    assert result.source_format == "compact"


def test_extract_compact_deduplicates_absent_ids_but_preserves_raw_count() -> None:
    payload = {"no_generation": ["a", "a"], "no_logs": [], "resolved": []}
    result = extract_counts(payload, benchmark_size=10)
    assert result.generated == 9
    assert result.no_generation_raw == 2
    assert result.inferred_no_claim == 1


def test_extract_legacy_uses_generated_list() -> None:
    payload = {
        "generated": ["a", "b", "c"],
        "no_generation": ["d", "d"],
        "no_logs": ["c"],
        "resolved": ["a"],
    }
    result = extract_counts(payload, benchmark_size=5)
    assert result.generated == 3
    assert result.no_generation_raw == 2
    assert result.inferred_no_claim == 2
    assert result.source_format == "legacy-expanded"


def test_extract_rejects_overlapping_resolved_and_no_logs() -> None:
    payload = {"no_generation": [], "no_logs": ["a"], "resolved": ["a"]}
    with pytest.raises(ValueError, match="disjoint"):
        extract_counts(payload)


def test_extract_rejects_legacy_resolved_absent_from_generated() -> None:
    payload = {"generated": ["a"], "no_logs": [], "resolved": ["b"]}
    with pytest.raises(ValueError, match="absent"):
        extract_counts(payload)


def test_extract_rejects_invalid_list_type() -> None:
    with pytest.raises(ValueError, match="list of strings"):
        extract_counts({"no_generation": "a", "no_logs": [], "resolved": []})


def test_extract_rejects_nonpositive_benchmark_size() -> None:
    with pytest.raises(ValueError, match="positive"):
        extract_counts({}, benchmark_size=0)
