import json
from pathlib import Path

from agent_completion_ledger.cli import main
from agent_completion_ledger.io import write_outputs
from agent_completion_ledger.metrics import analyze_records
from agent_completion_ledger.model import SourceRecord

SOURCE = Path("data/frozen/submission-summaries.json")


def test_cli_benchmark_supported(tmp_path: Path) -> None:
    args = ["benchmark", "--source", str(SOURCE), "--output-dir", str(tmp_path)]
    assert main(args) == 0


def test_cli_analyze_not_supported_with_high_threshold(tmp_path: Path) -> None:
    args = [
        "analyze",
        str(SOURCE),
        "--output-dir",
        str(tmp_path),
        "--threshold",
        "0.99",
    ]
    assert main(args) == 1


def test_cli_rejects_bad_threshold(tmp_path: Path) -> None:
    args = [
        "analyze",
        str(SOURCE),
        "--output-dir",
        str(tmp_path),
        "--threshold",
        "1.2",
    ]
    assert main(args) == 2


def test_cli_rejects_bad_minimum(tmp_path: Path) -> None:
    args = [
        "analyze",
        str(SOURCE),
        "--output-dir",
        str(tmp_path),
        "--minimum-claims",
        "0",
    ]
    assert main(args) == 2


def test_cli_missing_source(tmp_path: Path) -> None:
    args = ["analyze", "missing.json", "--output-dir", str(tmp_path)]
    assert main(args) == 2


def test_cli_validate_valid(
    tmp_path: Path,
    records: list[SourceRecord],
) -> None:
    items, aggregate = analyze_records(records)
    write_outputs(tmp_path, records, items, aggregate)
    assert main(["validate-ledger", str(tmp_path / "ledger.jsonl")]) == 0


def test_cli_validate_invalid(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text("{}\n", encoding="utf-8")
    assert main(["validate-ledger", str(path)]) == 1


def test_cli_validate_missing() -> None:
    assert main(["validate-ledger", "missing.jsonl"]) == 2


def test_e2e_output_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "a"
    second = tmp_path / "b"
    first_args = [
        "benchmark",
        "--source",
        str(SOURCE),
        "--output-dir",
        str(first),
    ]
    second_args = [
        "benchmark",
        "--source",
        str(SOURCE),
        "--output-dir",
        str(second),
    ]
    assert main(first_args) == 0
    assert main(second_args) == 0
    assert (first / "output-hashes.json").read_text(encoding="utf-8") == (
        second / "output-hashes.json"
    ).read_text(encoding="utf-8")
    summary = json.loads((first / "summary.json").read_text(encoding="utf-8"))
    assert summary["aggregate"]["generated"] == 3364
