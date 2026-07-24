from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from agent_completion_ledger.contract import load_contract
from agent_completion_ledger.model import EvidenceState
from agent_completion_ledger.verification import verify_contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    contract = load_contract(args.contract)
    started = time.monotonic_ns()
    report = verify_contract(contract, args.repo_root, include_timing=True)
    elapsed_ms = int((time.monotonic_ns() - started) / 1_000_000)
    expected_suffixes = {
        "success": EvidenceState.SUPPORTED,
        "failure": EvidenceState.FAILED,
        "unverifiable": EvidenceState.UNVERIFIABLE,
    }
    observed = {item.task_id.rsplit("-", 1)[-1]: item.ledger_status for item in report.tasks}
    expected_matched = all(observed.get(key) is value for key, value in expected_suffixes.items())
    assertion_count = sum(len(task.evidence) for task in contract.tasks)
    output = {
        "schemaVersion": "1",
        "repository": args.name,
        "contractPath": str(args.contract),
        "contractLines": len(args.contract.read_text(encoding="utf-8").splitlines()),
        "assertionCount": assertion_count,
        "executionMilliseconds": elapsed_ms,
        "tasks": [item.to_dict() for item in report.tasks],
        "expectedControlledStatesMatched": expected_matched,
        "controlledFalsePositives": 0 if expected_matched else None,
        "controlledFalseNegatives": 0 if expected_matched else None,
        "completedClaimsCorrected": sum(
            item.ledger_status in {EvidenceState.FAILED, EvidenceState.UNVERIFIABLE}
            for item in report.tasks
        ),
        "manualSteps": [
            "Check out the public repository",
            "Install its documented development dependencies",
            "Run the evidence contract",
        ],
        "humanAdjudicationItems": [
            "Whether passing repository tests fully represents product-value completion"
        ],
        "limitations": [
            "Controlled failure and unverifiable cases test reporting semantics, not naturally occurring defects",
            "Elapsed time includes repository-native tests and varies by runner",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if expected_matched else 1


if __name__ == "__main__":
    raise SystemExit(main())
