import json
from pathlib import Path

import yaml

from agent_completion_ledger.cli import main
from agent_completion_ledger.reproduction import reproduce


def test_reproduce_matches_published_hashes(tmp_path: Path) -> None:
    result = reproduce(Path("research-manifest.yml"), tmp_path)
    assert result.exit_code == 0
    assert result.status == "REPRODUCED"
    assert (tmp_path / "reproduction-report.json").is_file()
    assert (tmp_path / "reproduction-summary.md").is_file()


def test_reproduce_detects_expected_hash_mismatch(tmp_path: Path) -> None:
    manifest = yaml.safe_load(Path("research-manifest.yml").read_text(encoding="utf-8"))
    manifest["expected_outputs"]["summary.json"] = "0" * 64
    manifest_path = tmp_path / "manifest.yml"
    manifest_path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    result = reproduce(manifest_path, tmp_path / "out")
    assert result.exit_code == 1
    assert "summary.json" in result.mismatched


def test_reproduce_missing_source_is_environment_error(tmp_path: Path) -> None:
    result = reproduce(
        Path("research-manifest.yml"),
        tmp_path / "out",
        source_override=tmp_path / "missing.json",
    )
    assert result.exit_code == 2


def test_cli_reproduce_success(tmp_path: Path) -> None:
    assert main(["reproduce", "--output-dir", str(tmp_path)]) == 0


def test_cli_init_validate_and_no_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "completion-ledger.yml"
    assert main(["init", "--output", str(path)]) == 0
    assert main(["validate-contract", str(path)]) == 0
    assert main(["init", "--output", str(path)]) == 2
    assert main(["init", "--output", str(path), "--force"]) == 0


def test_cli_verify_json_and_report(tmp_path: Path) -> None:
    contract = tmp_path / "contract.yml"
    contract.write_text(
        "schemaVersion: '1'\ntasks:\n  - id: no-claim\n    claim:\n      status: none\n    evidence: []\n",
        encoding="utf-8",
    )
    report = tmp_path / "report.json"
    assert (
        main(
            [
                "verify",
                "--contract",
                str(contract),
                "--repo-root",
                str(tmp_path),
                "--format",
                "json",
                "--output",
                str(report),
            ]
        )
        == 0
    )
    assert json.loads(report.read_text(encoding="utf-8"))["counts"]["NO_CLAIM"] == 1
    markdown = tmp_path / "report.md"
    assert main(["report", str(report), "--format", "markdown", "--output", str(markdown)]) == 0
    assert "NO_CLAIM" in markdown.read_text(encoding="utf-8")


def test_reproduce_bad_manifest_is_environment_error(tmp_path: Path) -> None:
    path = tmp_path / "bad.yml"
    path.write_text("[]\n", encoding="utf-8")
    result = reproduce(path, tmp_path / "out")
    assert result.exit_code == 2


def test_cli_invalid_contract(tmp_path: Path) -> None:
    path = tmp_path / "bad.yml"
    path.write_text("schemaVersion: '1'\ntasks: []\n", encoding="utf-8")
    assert main(["validate-contract", str(path)]) == 1


def test_cli_verify_missing_contract(tmp_path: Path) -> None:
    assert main(["verify", "--contract", str(tmp_path / "missing.yml")]) == 2


def test_cli_report_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    assert main(["report", str(path)]) == 2


def test_cli_generalization_missing_source(tmp_path: Path) -> None:
    assert (
        main(
            [
                "generalization",
                "--source",
                str(tmp_path / "missing.json"),
                "--output",
                str(tmp_path / "out.json"),
            ]
        )
        == 2
    )
