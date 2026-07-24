import json
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_external_task_pack_is_fixed_and_balanced() -> None:
    payload = json.loads(
        (REPOSITORY_ROOT / "research/external-validation/task-pack.json").read_text(
            encoding="utf-8"
        )
    )
    tasks = payload["tasks"]

    assert payload["status"] == "FIXED_BEFORE_RECRUITMENT"
    assert payload["realParticipantCount"] == 0
    assert len(tasks) == 10
    assert len({task["id"] for task in tasks}) == 10
    assert {task["family"] for task in tasks} == {
        "python",
        "node",
        "repository-hygiene",
    }
    assert {task["groundTruth"] for task in tasks} == {
        "ACCEPT",
        "REJECT",
        "INSUFFICIENT_EVIDENCE",
    }
    assert {task["expectedLedgerStatus"] for task in tasks} == {
        "SUPPORTED",
        "FAILED",
        "UNVERIFIABLE",
    }


def test_synthetic_dry_run_is_explicitly_nonhuman() -> None:
    payload = json.loads(
        (REPOSITORY_ROOT / "research/external-validation/synthetic-dry-run.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"] == "SYNTHETIC_DRY_RUN_ONLY"
    assert payload["realParticipantCount"] == 0
    assert payload["humanEvidence"] is False


def test_external_analysis_script_runs_and_reports_zero_real_participants(
    tmp_path: Path,
) -> None:
    output = tmp_path / "result.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY_ROOT / "research/external-validation/analyze.py"),
            str(REPOSITORY_ROOT / "research/external-validation/synthetic-dry-run.csv"),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "SYNTHETIC_DRY_RUN"
    assert payload["realParticipantCount"] == 0
    assert payload["conditions"]["A"]["rows"] == 10
    assert payload["conditions"]["B"]["rows"] == 10


def test_safe_workflows_use_base_contract_and_least_privilege() -> None:
    workflow_root = REPOSITORY_ROOT / "docs/workflows"
    for name in ("trusted-main-contract.yml", "static-untrusted-pr.yml"):
        text = (workflow_root / name).read_text(encoding="utf-8")
        assert "pull_request:" in text
        assert "pull_request_target" not in text
        assert "contents: read" in text
        assert "secrets." not in text
        assert "github.event.pull_request.base.sha" in text
        assert "expected-contract-sha256" in text

    static_text = (workflow_root / "static-untrusted-pr.yml").read_text(encoding="utf-8")
    assert 'no-exec: "true"' in static_text
