import json
import sys
from pathlib import Path

from agent_completion_ledger.contract import contract_from_mapping
from agent_completion_ledger.model import EvidenceState
from agent_completion_ledger.reporting import render_json, render_markdown, render_terminal
from agent_completion_ledger.verification import report_exit_code, verify_contract


def _contract(task: dict[str, object]) -> object:
    return contract_from_mapping(
        {
            "schemaVersion": "1",
            "policy": {"allowedExecutables": [sys.executable]},
            "tasks": [task],
        }
    )


def test_supported_task(tmp_path: Path) -> None:
    (tmp_path / "ok").write_text("ok", encoding="utf-8")
    contract = _contract(
        {
            "id": "supported",
            "claim": {"status": "completed"},
            "evidence": [{"id": "file", "type": "file-exists", "path": "ok"}],
        }
    )
    report = verify_contract(contract, tmp_path)  # type: ignore[arg-type]
    assert report.tasks[0].ledger_status is EvidenceState.SUPPORTED
    assert report_exit_code(report) == 0


def test_failed_task(tmp_path: Path) -> None:
    contract = _contract(
        {
            "id": "failed",
            "claim": {"status": "completed"},
            "evidence": [{"id": "file", "type": "file-exists", "path": "missing"}],
        }
    )
    report = verify_contract(contract, tmp_path)  # type: ignore[arg-type]
    assert report.tasks[0].ledger_status is EvidenceState.FAILED
    assert report_exit_code(report) == 1


def test_unverifiable_task_without_evidence(tmp_path: Path) -> None:
    contract = _contract(
        {"id": "unknown", "claim": {"status": "completed"}, "evidence": []}
    )
    report = verify_contract(contract, tmp_path)  # type: ignore[arg-type]
    assert report.tasks[0].ledger_status is EvidenceState.UNVERIFIABLE
    assert report_exit_code(report) == 2


def test_no_claim_task(tmp_path: Path) -> None:
    contract = _contract(
        {"id": "none", "claim": {"status": "none"}, "evidence": []}
    )
    report = verify_contract(contract, tmp_path)  # type: ignore[arg-type]
    assert report.tasks[0].ledger_status is EvidenceState.NO_CLAIM
    assert report_exit_code(report) == 0


def test_nonblocking_failure_does_not_fail_task(tmp_path: Path) -> None:
    (tmp_path / "ok").write_text("ok", encoding="utf-8")
    contract = _contract(
        {
            "id": "supported",
            "claim": {"status": "completed"},
            "evidence": [
                {"id": "required", "type": "file-exists", "path": "ok"},
                {
                    "id": "optional",
                    "type": "file-exists",
                    "path": "missing",
                    "blocking": False,
                },
            ],
        }
    )
    report = verify_contract(contract, tmp_path)  # type: ignore[arg-type]
    assert report.tasks[0].ledger_status is EvidenceState.SUPPORTED


def test_task_filter(tmp_path: Path) -> None:
    value = {
        "schemaVersion": "1",
        "tasks": [
            {"id": "one", "claim": {"status": "none"}, "evidence": []},
            {"id": "two", "claim": {"status": "none"}, "evidence": []},
        ],
    }
    report = verify_contract(contract_from_mapping(value), tmp_path, task_id="two")
    assert [item.task_id for item in report.tasks] == ["two"]


def test_unknown_task_rejected(tmp_path: Path) -> None:
    value = {
        "schemaVersion": "1",
        "tasks": [{"id": "one", "claim": {"status": "none"}, "evidence": []}],
    }
    try:
        verify_contract(contract_from_mapping(value), tmp_path, task_id="missing")
    except ValueError as exc:
        assert "unknown task" in str(exc)
    else:
        raise AssertionError("missing task should fail")


def test_reports_are_deterministic(tmp_path: Path) -> None:
    contract = _contract(
        {"id": "none", "claim": {"status": "none"}, "evidence": []}
    )
    report = verify_contract(contract, tmp_path)  # type: ignore[arg-type]
    assert render_terminal(report) == render_terminal(report)
    assert "NO_CLAIM" in render_markdown(report)
    assert json.loads(render_json(report))["counts"]["NO_CLAIM"] == 1


def test_report_symbols_cover_pass_fail_unknown(tmp_path: Path) -> None:
    (tmp_path / "ok").write_text("ok", encoding="utf-8")
    value = {
        "schemaVersion": "1",
        "tasks": [
            {
                "id": "mixed",
                "claim": {"status": "completed"},
                "evidence": [
                    {"id": "pass", "type": "file-exists", "path": "ok"},
                    {
                        "id": "fail",
                        "type": "file-exists",
                        "path": "missing",
                        "blocking": False,
                    },
                    {
                        "id": "unknown",
                        "type": "command",
                        "command": ["missing"],
                        "blocking": False,
                    },
                ],
            }
        ],
    }
    report = verify_contract(contract_from_mapping(value), tmp_path)
    rendered = render_terminal(report)
    assert "✓ pass" in rendered
    assert "✗ fail" in rendered
    assert "? unknown" in rendered


def test_markdown_escapes_pipe(tmp_path: Path) -> None:
    value = {
        "schemaVersion": "1",
        "tasks": [
            {
                "id": "pipe",
                "claim": {"status": "completed"},
                "evidence": [
                    {"id": "text", "type": "file-exists", "path": "a|b"}
                ],
            }
        ],
    }
    report = verify_contract(contract_from_mapping(value), tmp_path)
    assert "a\\|b" in render_markdown(report)


def test_write_or_print_writes_file(tmp_path: Path) -> None:
    from agent_completion_ledger.reporting import write_or_print

    output = tmp_path / "nested" / "report.txt"
    write_or_print("text\n", output)
    assert output.read_text(encoding="utf-8") == "text\n"
