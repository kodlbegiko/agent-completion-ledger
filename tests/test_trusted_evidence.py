import hashlib
import json
import sys
from importlib.resources import files
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from agent_completion_ledger.cli import main
from agent_completion_ledger.contract import (
    ContractError,
    contract_from_mapping,
    contract_sha256,
    normalize_expected_sha256,
)
from agent_completion_ledger.model import EvidenceState
from agent_completion_ledger.reporting import in_toto_statement, render_json, render_markdown
from agent_completion_ledger.verification import (
    contract_hash_mismatch_report,
    report_exit_code,
    verify_contract,
)


def _mapping(command: list[str] | None = None) -> dict[str, object]:
    evidence: list[dict[str, object]] = [
        {"id": "readme", "type": "file-exists", "path": "README.md"}
    ]
    if command is not None:
        evidence.append(
            {
                "id": "tests",
                "type": "test-command",
                "command": command,
                "timeoutSeconds": 10,
            }
        )
    return {
        "schemaVersion": "1",
        "policy": {"allowedExecutables": [sys.executable]},
        "tasks": [
            {
                "id": "trusted-task",
                "claim": {"status": "completed"},
                "evidence": evidence,
            }
        ],
    }


def test_contract_sha256_hashes_exact_bytes(tmp_path: Path) -> None:
    contract = tmp_path / "completion-ledger.yml"
    payload = b"schemaVersion: '1'\r\n"
    contract.write_bytes(payload)
    assert contract_sha256(contract) == hashlib.sha256(payload).hexdigest()


def test_expected_sha256_validation() -> None:
    assert normalize_expected_sha256(" A" * 0 + "A" * 64 + "\n") == "a" * 64
    with pytest.raises(ContractError, match="64 hexadecimal"):
        normalize_expected_sha256("not-a-digest")


def test_static_only_does_not_execute_commands(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("fixture", encoding="utf-8")
    marker = tmp_path / "command-ran.txt"
    command = [
        sys.executable,
        "-c",
        "from pathlib import Path; Path('command-ran.txt').write_text('ran')",
    ]
    report = verify_contract(
        contract_from_mapping(_mapping(command)),
        tmp_path,
        contract_path=tmp_path / "completion-ledger.yml",
        contract_sha256="a" * 64,
        no_exec=True,
    )

    assert not marker.exists()
    assert report.execution_mode == "static-only"
    assert report.tasks[0].assertions[0].outcome.value == "PASS"
    assert report.tasks[0].assertions[1].outcome.value == "UNVERIFIABLE"
    assert report.tasks[0].ledger_status is EvidenceState.UNVERIFIABLE
    assert report_exit_code(report) == 2


def test_contract_mismatch_is_integrity_only_and_deterministic(tmp_path: Path) -> None:
    contract = tmp_path / "completion-ledger.yml"
    contract.write_text("untrusted: content\n", encoding="utf-8")
    first = contract_hash_mismatch_report(
        tmp_path,
        contract,
        actual_sha256="a" * 64,
        expected_sha256="b" * 64,
    )
    second = contract_hash_mismatch_report(
        tmp_path,
        contract,
        actual_sha256="a" * 64,
        expected_sha256="b" * 64,
    )

    assert first.trusted_mode is True
    assert first.contract_digest_matched is False
    assert first.execution_mode == "integrity-only"
    assert first.overall_status is EvidenceState.UNVERIFIABLE
    assert first.result_digest == second.result_digest
    assert report_exit_code(first) == 2


def test_trusted_match_records_provenance_and_digest(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("fixture", encoding="utf-8")
    report = verify_contract(
        contract_from_mapping(_mapping()),
        tmp_path,
        contract_path=tmp_path / "completion-ledger.yml",
        contract_sha256="a" * 64,
        expected_contract_sha256="a" * 64,
        trusted_mode=True,
        contract_digest_matched=True,
    )
    raw = json.loads(render_json(report))

    assert raw["schemaVersion"] == "2"
    assert raw["provenance"]["trustedMode"] is True
    assert raw["provenance"]["contractDigestMatched"] is True
    assert raw["provenance"]["evidenceAssertionIds"] == ["readme"]
    assert len(raw["resultDigest"]) == 64
    assert render_json(report) == render_json(report)
    assert "## Provenance" in render_markdown(report)


def test_in_toto_predicate_validates_against_packaged_schema(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("fixture", encoding="utf-8")
    report = verify_contract(
        contract_from_mapping(_mapping()),
        tmp_path,
        contract_path=tmp_path / "completion-ledger.yml",
        contract_sha256="a" * 64,
        expected_contract_sha256="a" * 64,
        trusted_mode=True,
        contract_digest_matched=True,
    )
    statement = in_toto_statement(report)
    schema_path = files("agent_completion_ledger").joinpath(
        "schemas/completion-evidence-predicate.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(statement["predicate"])
    assert statement["_type"] == "https://in-toto.io/Statement/v1"
    assert statement["predicateType"].endswith("/completion-evidence/v1")
    assert statement["predicate"]["scope"]["limitations"]


def test_cli_contract_tampering_returns_unverifiable_without_parsing(tmp_path: Path) -> None:
    contract = tmp_path / "completion-ledger.yml"
    contract.write_text("this is not a valid contract\n", encoding="utf-8")
    output = tmp_path / "report.json"

    exit_code = main(
        [
            "verify",
            "--contract",
            str(contract),
            "--repo-root",
            str(tmp_path),
            "--expected-contract-sha256",
            "0" * 64,
            "--format",
            "json",
            "--output",
            str(output),
        ]
    )
    raw = json.loads(output.read_text(encoding="utf-8"))

    assert exit_code == 2
    assert raw["overallStatus"] == "UNVERIFIABLE"
    assert raw["provenance"]["contractDigestMatched"] is False
    assert raw["provenance"]["executionMode"] == "integrity-only"


def test_reports_do_not_include_command_stdout_or_stderr(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("fixture", encoding="utf-8")
    secret = "DO_NOT_LEAK_THIS_VALUE"
    command = [
        sys.executable,
        "-c",
        f"import sys; print('{secret}'); print('{secret}', file=sys.stderr)",
    ]
    report = verify_contract(
        contract_from_mapping(_mapping(command)),
        tmp_path,
        contract_path=tmp_path / "completion-ledger.yml",
        contract_sha256="a" * 64,
    )

    assert report.overall_status is EvidenceState.SUPPORTED
    assert secret not in render_json(report)
    assert secret not in render_markdown(report)
