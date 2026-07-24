from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from .assertions import AssertionOutcome
from .verification import VerificationReport

ReportFormat = Literal["terminal", "json", "markdown"]


def render_json(report: VerificationReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _symbol(outcome: AssertionOutcome) -> str:
    if outcome is AssertionOutcome.PASS:
        return "✓"
    if outcome is AssertionOutcome.FAIL:
        return "✗"
    return "?"


def render_terminal(report: VerificationReport) -> str:
    lines: list[str] = []
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
        "Summary: "
        + ", ".join(f"{state}={count}" for state, count in sorted(counts.items()))
    )
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(report: VerificationReport) -> str:
    lines = ["# Completion evidence report", ""]
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
    return "\n".join(lines).rstrip() + "\n"


def render_report(report: VerificationReport, format_name: ReportFormat) -> str:
    if format_name == "json":
        return render_json(report)
    if format_name == "markdown":
        return render_markdown(report)
    return render_terminal(report)


def write_or_print(content: str, output: Path | None) -> None:
    if output is None:
        print(content, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
