import json
from pathlib import Path

import pytest

from agent_completion_ledger.generalization import (
    MultiSweBenchRecord,
    analyze_generalization,
    load_generalization_record,
    write_generalization_result,
)

SOURCE = Path("data/generalization/multi-swe-bench-go-magentless-summary.json")


def test_fixed_generalization_result_supported() -> None:
    result = analyze_generalization(load_generalization_record(SOURCE))
    assert result.verdict == "SUPPORTED"
    assert result.unsupported_rate == pytest.approx(316 / 341)
    assert result.wilson_95.lower > 0.20
    assert result.reclassifications_to_20_percent == 248


def test_generalization_result_written(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    write_generalization_result(SOURCE, output)
    value = json.loads(output.read_text(encoding="utf-8"))
    assert value["policyB"] == "UNTESTABLE HERE"
    assert value["record"]["source_blob_sha"] == "30c6d4f4242b1ce87a000edeec5a29a622678861"


@pytest.mark.parametrize(
    "field,value",
    [
        ("completed_instances", 340),
        ("resolved_instances", 24),
        ("total_instances", 300),
        ("unstopped_instances", -1),
        ("source_blob_sha", "bad"),
    ],
)
def test_generalization_invalid_counts_rejected(field: str, value: object) -> None:
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    raw[field] = value
    with pytest.raises((TypeError, ValueError)):
        MultiSweBenchRecord.from_mapping(raw)


def test_generalization_h0_when_rate_low() -> None:
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    raw["resolved_instances"] = 300
    raw["unresolved_instances"] = 41
    result = analyze_generalization(MultiSweBenchRecord.from_mapping(raw))
    assert result.verdict == "NOT SUPPORTED"


def test_generalization_h0_when_sample_small() -> None:
    raw = json.loads(SOURCE.read_text(encoding="utf-8"))
    raw.update(
        total_instances=40,
        submitted_instances=40,
        completed_instances=40,
        resolved_instances=0,
        unresolved_instances=40,
        empty_error_patch_instances=0,
    )
    result = analyze_generalization(MultiSweBenchRecord.from_mapping(raw))
    assert result.verdict == "NOT SUPPORTED"
