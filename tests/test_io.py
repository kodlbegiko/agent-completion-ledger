import json
from pathlib import Path

import pytest

from agent_completion_ledger.io import (
    canonical_json,
    ledger_rows,
    load_records,
    sha256_file,
    validate_ledger,
    write_outputs,
)
from agent_completion_ledger.metrics import analyze_records
from agent_completion_ledger.model import SourceRecord


def test_canonical_json_key_order() -> None:
    assert canonical_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'


def test_load_records_requires_array(tmp_path: Path) -> None:
    path = tmp_path / "x.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="array"):
        load_records(path)


def test_load_records_requires_objects(tmp_path: Path) -> None:
    path = tmp_path / "x.json"
    path.write_text("[1]", encoding="utf-8")
    with pytest.raises(ValueError, match="object"):
        load_records(path)


def test_ledger_has_four_rows_per_submission(records: list[SourceRecord]) -> None:
    assert len(ledger_rows(records)) == 28


def test_ledger_counts_sum_to_slots(records: list[SourceRecord]) -> None:
    rows = ledger_rows(records)
    assert sum(int(row["count"]) for row in rows) == 3500


def test_write_outputs(records: list[SourceRecord], tmp_path: Path) -> None:
    items, aggregate = analyze_records(records)
    hashes = write_outputs(tmp_path, records, items, aggregate)
    assert set(hashes) == {
        "summary.json",
        "submission-metrics.csv",
        "ledger.jsonl",
        "sensitivity.json",
    }
    assert (tmp_path / "output-hashes.json").exists()


def test_summary_verdict_supported(
    records: list[SourceRecord],
    tmp_path: Path,
) -> None:
    items, aggregate = analyze_records(records)
    write_outputs(tmp_path, records, items, aggregate)
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert summary["verdict"] == "SUPPORTED"


def test_hash_is_deterministic(tmp_path: Path) -> None:
    path = tmp_path / "x"
    path.write_bytes(b"abc")
    assert sha256_file(path) == ("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")


def test_valid_ledger(records: list[SourceRecord], tmp_path: Path) -> None:
    items, aggregate = analyze_records(records)
    write_outputs(tmp_path, records, items, aggregate)
    assert validate_ledger(tmp_path / "ledger.jsonl") == []


def test_invalid_json_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger"
    path.write_text("not-json\n", encoding="utf-8")
    assert "invalid JSON" in validate_ledger(path)[0]


def test_non_object_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger"
    path.write_text("[]\n", encoding="utf-8")
    assert "record must be an object" in validate_ledger(path)[0]


def test_unknown_state_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger"
    row = {
        "evidence_state": "MAYBE",
        "count": 1,
        "evidence": {"source_blob_sha": "a"},
    }
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    assert any("unknown evidence_state" in error for error in validate_ledger(path))


def test_negative_count_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger"
    row = {
        "evidence_state": "FAILED",
        "count": -1,
        "evidence": {"source_blob_sha": "a"},
    }
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    assert any("non-negative" in error for error in validate_ledger(path))


def test_missing_evidence_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger"
    row = {"evidence_state": "FAILED", "count": 1}
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    assert any("source is missing" in error for error in validate_ledger(path))


def test_blank_line_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger"
    path.write_text("\n", encoding="utf-8")
    assert validate_ledger(path) == ["line 1: blank line"]
