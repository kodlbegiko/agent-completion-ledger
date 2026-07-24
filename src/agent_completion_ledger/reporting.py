from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from .assertions import AssertionOutcome
from .verification import VerificationReport

ReportFormat = Literal["terminal", "json", "markdown", "in-toto"]
PREDICATE_TYPE = (
    "https://github.com/kodlbegiko/agent-completion-ledger/"
    "predicate/completion-evidence/v1"
)


def render_json(report: VerificationReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _symbol(outcome: AssertionOutcome) -> str:
    if outcome is AssertionOutcome.PASS:
        return "✓"
    if outcome is AssertionOutcome.FAIL:
        return "✗"
    return "?"


def render_terminal(report: VerificationReport) -> str:
    lines: list[str] = [
        f"Tool version: {report.tool_version}",
        f"Repository commit: {report.repository_commit_sha}",
        f"Contract SHA-256: {report.contract_sha256 or 'UNKNOWN'}",
        f"Trusted mode: {'yes' if report.trusted_mode else 'no'}",
        f"Execution mode: {report.execution_mode}",
        "",
    ]
    for task in report.tasks:
        lines.extend(
            [
                f"Task: {task.task_id}",
                f"Claimed status: {task.claimed_status}",
                f"Ledger status: {task.ledger_status.value}",
                "Evidence:",
            ]
        )
        if not task.assertions:
            lines.append("? no evidence assertions")
        for assertion in task.assertions:
            lines.append(f"{_symbol(assertion.outcome)} {assertion.id}: {assertion.message}")
        lines.append("")
    counts = report.counts
    lines.append(
        "Summary: " + ", ".join(f"{state}={count}" for state, count in sorted(counts.items()))
    )
    lines.append(f"Result digest: {report.result_digest}")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(report: VerificationReport) -> str:
    digest_match = (
        "not pinned"
        if report.contract_digest_matched is None
        else ("matched" if report.contract_digest_matched else "mismatched")
    )
    lines = [
        "# Completion evidence report",
        "",
        "## Provenance",
        "",
        f"- Tool version: `{report.tool_version}`",
        f"- Repository commit SHA: `{report.repository_commit_sha}`",
        f"- Repository root identity: `{report.repository_root_identity}`",
        f"- Contract path: `{report.contract_path}`",
        f"- Contract SHA-256: `{report.contract_sha256 or 'UNKNOWN'}`",
        f"- Trusted mode: `{'true' if report.trusted_mode else 'false'}`",
        f"- Contract digest: `{digest_match}`",
        f"- Execution mode: `{report.execution_mode}`",
        f"- Report schema version: `{report.schema_version}`",
        f"- Result digest: `{report.result_digest}`",
        "",
    ]
    for task in report.tasks:
        lines.extend(
            [
                f"## `{task.task_id}`",
                "",
                f"- Claimed status: `{task.claimed_status}`",
                f"- Ledger status: **`{task.ledger_status.value}`**",
                "",
                "| Evidence | Type | Blocking | Outcome | Detail |",
                "|---|---|---:|---|---|",
            ]
        )
        if not task.assertions:
            lines.append("| — | — | — | `UNVERIFIABLE` | No evidence assertions |")
        for assertion in task.assertions:
            detail = assertion.message.replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| `{assertion.id}` | `{assertion.type}` | "
                f"{'yes' if assertion.blocking else 'no'} | "
                f"`{assertion.outcome.value}` | {detail} |"
            )
        lines.append("")
    lines.extend(["## Summary", "", "| State | Count |", "|---|---:|"])
    for state, count in sorted(report.counts.items()):
        lines.append(f"| `{state}` | {count} |")
    lines.extend(
        [
            "",
            "> This report is repository-level acceptance evidence. It is not a sandbox, "
            "security certification, semantic-correctness proof, or product-value assessment.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def in_toto_statement(report: VerificationReport) -> dict[str, object]:
    assertion_summary = [
        {
            "id": assertion.id,
            "type": assertion.type,
            "outcome": assertion.outcome.value,
            "blocking": assertion.blocking,
        }
        for task in report.tasks
        for assertion in task.assertions
    ]
    task_claims = [
        {
            "taskId": task.task_id,
            "claimedStatus": task.claimed_status,
            "ledgerStatus": task.ledger_status.value,
        }
        for task in report.tasks
    ]
    predicate: dict[str, object] = {
        "schemaVersion": "1",
        "taskClaims": task_claims,
        "ledgerStatus": {
            "overall": report.overall_status.value,
            "counts": report.counts,
        },
        "contractDigest": {"sha256": report.contract_sha256},
        "repository": {
            "identity": report.repository_root_identity,
            "commit": report.repository_commit_sha,
        },
        "assertionSummary": assertion_summary,
        "evidenceReportDigest": {"sha256": report.result_digest},
        "tool": {"name": "agent-completion-ledger", "version": report.tool_version},
        "scope": {
            "kind": "repository-level coding-agent acceptance evidence",
            "trustedMode": report.trusted_mode,
            "executionMode": report.execution_mode,
            "limitations": [
                "describes verification results only",
                "does not prove software security",
                "does not prove semantic correctness",
                "does not establish regulatory compliance",
                "is not a signed attestation unless signed by an external attestation system",
            ],
        },
    }
    if report.expected_contract_sha256 is not None:
        predicate["expectedContractDigest"] = {
            "sha256": report.expected_contract_sha256,
            "matched": report.contract_digest_matched,
        }
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {
                "name": report.repository_root_identity,
                "digest": {"gitCommit": report.repository_commit_sha},
            }
        ],
        "predicateType": PREDICATE_TYPE,
        "predicate": predicate,
    }


def render_in_toto(report: VerificationReport) -> str:
    return json.dumps(in_toto_statement(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_report(report: VerificationReport, format_name: ReportFormat) -> str:
    if format_name == "json":
        return render_json(report)
    if format_name == "markdown":
        return render_markdown(report)
    if format_name == "in-toto":
        return render_in_toto(report)
    return render_terminal(report)


def write_or_print(content: str, output: Path | None) -> None:
    if output is None:
        print(content, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")
