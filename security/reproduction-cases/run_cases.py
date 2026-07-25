from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from contextlib import suppress
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = REPOSITORY_ROOT / "security/reproduction-cases/contracts"
FIXTURE_ROOT = REPOSITORY_ROOT / "security/reproduction-cases/repository"
MARKER = "ACL_BENIGN_OUTPUT_MARKER_DO_NOT_REPORT"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_status(path: Path) -> str | None:
    try:
        return str(json.loads(path.read_text(encoding="utf-8"))["overallStatus"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _run_case(
    name: str,
    contract_name: str,
    output_dir: Path,
    *,
    expected_exit: int,
    expected_status: str,
    expected_digest: str | None = None,
    no_exec: bool = False,
) -> dict[str, Any]:
    contract = CONTRACT_ROOT / contract_name
    report = output_dir / f"{name}.json"
    command = [
        "agent-completion-ledger",
        "verify",
        "--contract",
        str(contract),
        "--repo-root",
        str(FIXTURE_ROOT),
        "--format",
        "json",
        "--output",
        str(report),
    ]
    if expected_digest is not None:
        command.extend(["--expected-contract-sha256", expected_digest])
    if no_exec:
        command.append("--no-exec")

    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=15,
    )
    elapsed = time.monotonic() - started
    observed_status = _load_status(report)
    passed = completed.returncode == expected_exit and observed_status == expected_status
    return {
        "case": name,
        "contract": contract.relative_to(REPOSITORY_ROOT).as_posix(),
        "expectedExitCode": expected_exit,
        "observedExitCode": completed.returncode,
        "expectedStatus": expected_status,
        "observedStatus": observed_status,
        "elapsedSeconds": elapsed,
        "passed": passed,
        "diagnostic": (completed.stderr or completed.stdout).strip()[:1000],
    }


def run_cases(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    static_contract = CONTRACT_ROOT / "static-safe.yml"
    cases = [
        _run_case(
            "static-safe",
            "static-safe.yml",
            output_dir,
            expected_exit=0,
            expected_status="SUPPORTED",
            expected_digest=_digest(static_contract),
            no_exec=True,
        ),
        _run_case(
            "digest-mismatch",
            "static-safe.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
            expected_digest="0" * 64,
        ),
        _run_case(
            "interpreter-disabled",
            "interpreter-disabled.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
            no_exec=True,
        ),
        _run_case(
            "path-traversal",
            "path-traversal.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
            no_exec=True,
        ),
        _run_case(
            "windows-absolute",
            "windows-absolute.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
            no_exec=True,
        ),
        _run_case(
            "remote-url",
            "remote-url.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
        ),
        _run_case(
            "timeout",
            "timeout.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
        ),
        _run_case(
            "report-nondisclosure",
            "report-nondisclosure.yml",
            output_dir,
            expected_exit=0,
            expected_status="SUPPORTED",
        ),
    ]

    timeout_case = next(item for item in cases if item["case"] == "timeout")
    timeout_case["elapsedBoundSeconds"] = 1.5
    timeout_case["passed"] = bool(timeout_case["passed"] and timeout_case["elapsedSeconds"] < 1.5)

    nondisclosure_report = output_dir / "report-nondisclosure.json"
    marker_absent = nondisclosure_report.exists() and MARKER not in nondisclosure_report.read_text(
        encoding="utf-8"
    )
    nondisclosure_case = next(item for item in cases if item["case"] == "report-nondisclosure")
    nondisclosure_case["markerAbsentFromReport"] = marker_absent
    nondisclosure_case["passed"] = bool(nondisclosure_case["passed"] and marker_absent)

    link = FIXTURE_ROOT / "link.txt"
    try:
        link.symlink_to("public.txt")
        symlink_case = _run_case(
            "symlink",
            "symlink.yml",
            output_dir,
            expected_exit=2,
            expected_status="UNVERIFIABLE",
            no_exec=True,
        )
    except (OSError, NotImplementedError) as exc:
        symlink_case = {
            "case": "symlink",
            "expectedStatus": "UNVERIFIABLE",
            "observedStatus": None,
            "passed": False,
            "diagnostic": f"symlink case unavailable: {exc}",
        }
    finally:
        with suppress(OSError):
            link.unlink()
    cases.append(symlink_case)

    intoto_report = output_dir / "static-safe.intoto.json"
    intoto_command = [
        "agent-completion-ledger",
        "verify",
        "--contract",
        str(static_contract),
        "--repo-root",
        str(FIXTURE_ROOT),
        "--expected-contract-sha256",
        _digest(static_contract),
        "--no-exec",
        "--format",
        "in-toto",
        "--output",
        str(intoto_report),
    ]
    completed = subprocess.run(
        intoto_command,
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=15,
    )
    try:
        statement = json.loads(intoto_report.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        statement = {}
    intoto_passed = (
        completed.returncode == 0
        and statement.get("_type") == "https://in-toto.io/Statement/v1"
        and statement.get("predicateType")
        == "https://github.com/kodlbegiko/agent-completion-ledger/predicate/completion-evidence/v1"
    )
    cases.append(
        {
            "case": "in-toto-interpretation",
            "expectedExitCode": 0,
            "observedExitCode": completed.returncode,
            "expectedType": "https://in-toto.io/Statement/v1",
            "observedType": statement.get("_type"),
            "passed": intoto_passed,
            "interpretation": "unsigned structured evidence; not a signature or correctness proof",
            "diagnostic": (completed.stderr or completed.stdout).strip()[:1000],
        }
    )

    summary = {
        "schemaVersion": "1",
        "status": "PASS" if all(bool(item["passed"]) for item in cases) else "FAIL",
        "environment": {
            "platform": os.name,
            "repositoryRoot": str(REPOSITORY_ROOT),
        },
        "cases": cases,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = run_cases(args.output_dir)
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
