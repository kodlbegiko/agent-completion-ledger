from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .contract import ContractError, default_contract, load_contract
from .generalization import write_generalization_result
from .io import load_records, validate_ledger, write_outputs
from .metrics import analyze_records
from .reporting import ReportFormat, render_report, write_or_print
from .reproduction import reproduce
from .verification import VerificationReport, report_exit_code, verify_contract


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-completion-ledger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze frozen submission summaries")
    analyze.add_argument("source", type=Path)
    analyze.add_argument("--output-dir", type=Path, required=True)
    analyze.add_argument("--threshold", type=float, default=0.20)
    analyze.add_argument("--minimum-claims", type=int, default=3000)

    benchmark = subparsers.add_parser("benchmark", help="Reproduce the committed pilot")
    benchmark.add_argument("--output-dir", type=Path, required=True)
    benchmark.add_argument(
        "--source",
        type=Path,
        default=Path("data/frozen/submission-summaries.json"),
    )

    validate = subparsers.add_parser(
        "validate-ledger", help="Validate a JSONL aggregate evidence ledger"
    )
    validate.add_argument("ledger", type=Path)

    init = subparsers.add_parser("init", help="Create a starter completion evidence contract")
    init.add_argument("--output", type=Path, default=Path("completion-ledger.yml"))
    init.add_argument("--force", action="store_true")

    validate_contract = subparsers.add_parser(
        "validate-contract", help="Validate a completion evidence contract"
    )
    validate_contract.add_argument(
        "contract", type=Path, nargs="?", default=Path("completion-ledger.yml")
    )

    verify = subparsers.add_parser("verify", help="Execute evidence assertions")
    verify.add_argument(
        "--contract", type=Path, default=Path("completion-ledger.yml")
    )
    verify.add_argument("--repo-root", type=Path, default=Path("."))
    verify.add_argument("--task")
    verify.add_argument(
        "--format", choices=("terminal", "json", "markdown"), default="terminal"
    )
    verify.add_argument("--output", type=Path)
    verify.add_argument("--include-timing", action="store_true")

    report = subparsers.add_parser(
        "report", help="Render a previously generated verification JSON report"
    )
    report.add_argument("input", type=Path)
    report.add_argument(
        "--format", choices=("terminal", "json", "markdown"), default="terminal"
    )
    report.add_argument("--output", type=Path)

    reproduce_parser = subparsers.add_parser(
        "reproduce", help="Run and hash-check the committed v0.1.0 pilot"
    )
    reproduce_parser.add_argument(
        "--manifest", type=Path, default=Path("research-manifest.yml")
    )
    reproduce_parser.add_argument(
        "--output-dir", type=Path, default=Path("reproduced-results")
    )
    reproduce_parser.add_argument("--source", type=Path)

    generalization = subparsers.add_parser(
        "generalization", help="Analyze the preregistered second benchmark source"
    )
    generalization.add_argument(
        "--source",
        type=Path,
        default=Path("data/generalization/multi-swe-bench-go-magentless-summary.json"),
    )
    generalization.add_argument(
        "--output",
        type=Path,
        default=Path("results/v0.2.0/generalization-result.json"),
    )
    return parser


def _analyze(source: Path, output_dir: Path, threshold: float, minimum_claims: int) -> int:
    if not 0 <= threshold < 1:
        print("threshold must be in [0, 1)", file=sys.stderr)
        return 2
    if minimum_claims <= 0:
        print("minimum-claims must be positive", file=sys.stderr)
        return 2
    try:
        records = load_records(source)
        per_submission, aggregate = analyze_records(
            records,
            threshold=threshold,
            stopping_minimum_claims=minimum_claims,
        )
        hashes = write_outputs(output_dir, records, per_submission, aggregate)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"analysis failed: {exc}", file=sys.stderr)
        return 2

    print(
        json.dumps(
            {
                "verdict": "SUPPORTED" if aggregate.h1_supported else "NOT SUPPORTED",
                "generated": aggregate.generated,
                "false_completion_rate": aggregate.false_completion_rate,
                "hashes": hashes,
            },
            sort_keys=True,
        )
    )
    return 0 if aggregate.h1_supported else 1


def _init_contract(output: Path, force: bool) -> int:
    if output.exists() and not force:
        print(f"contract already exists: {output}; use --force to replace", file=sys.stderr)
        return 2
    try:
        import yaml

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            yaml.safe_dump(default_contract(), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"cannot write contract: {exc}", file=sys.stderr)
        return 2
    print(f"created {output}")
    return 0


def _verify(args: argparse.Namespace) -> int:
    try:
        contract = load_contract(args.contract)
        report = verify_contract(
            contract,
            args.repo_root,
            task_id=args.task,
            include_timing=args.include_timing,
        )
        content = render_report(report, cast(ReportFormat, args.format))
        write_or_print(content, args.output)
    except (ContractError, OSError, ValueError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 2
    return report_exit_code(report)


def _load_report(path: Path) -> VerificationReport:
    from .assertions import AssertionOutcome, AssertionResult
    from .model import EvidenceState
    from .verification import TaskVerification

    raw = json.loads(path.read_text(encoding="utf-8"))
    tasks: list[TaskVerification] = []
    for item in raw["tasks"]:
        assertions = tuple(
            AssertionResult(
                id=result["id"],
                type=result["type"],
                outcome=AssertionOutcome(result["outcome"]),
                message=result["message"],
                blocking=result["blocking"],
                duration_ms=result.get("durationMs"),
                actual_exit_code=result.get("actualExitCode"),
            )
            for result in item["assertions"]
        )
        tasks.append(
            TaskVerification(
                task_id=item["taskId"],
                description=item.get("description", ""),
                claimed_status=item["claimedStatus"],
                ledger_status=EvidenceState(item["ledgerStatus"]),
                assertions=assertions,
            )
        )
    return VerificationReport(
        schema_version=raw["schemaVersion"],
        contract_schema_version=raw["contractSchemaVersion"],
        tasks=tuple(tasks),
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        return _analyze(args.source, args.output_dir, args.threshold, args.minimum_claims)
    if args.command == "benchmark":
        return _analyze(args.source, args.output_dir, 0.20, 3000)
    if args.command == "validate-ledger":
        try:
            errors = validate_ledger(args.ledger)
        except OSError as exc:
            print(f"validation failed: {exc}", file=sys.stderr)
            return 2
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("ledger valid")
        return 0
    if args.command == "init":
        return _init_contract(args.output, args.force)
    if args.command == "validate-contract":
        try:
            contract = load_contract(args.contract)
        except ContractError as exc:
            print(f"contract invalid: {exc}", file=sys.stderr)
            return 1
        print(f"contract valid: {len(contract.tasks)} task(s)")
        return 0
    if args.command == "verify":
        return _verify(args)
    if args.command == "report":
        try:
            report = _load_report(args.input)
            write_or_print(render_report(report, cast(ReportFormat, args.format)), args.output)
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            print(f"report failed: {exc}", file=sys.stderr)
            return 2
        return 0
    if args.command == "reproduce":
        result = reproduce(args.manifest, args.output_dir, source_override=args.source)
        print(json.dumps(result.to_dict(), sort_keys=True))
        return result.exit_code
    if args.command == "generalization":
        try:
            result = write_generalization_result(args.source, args.output)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            print(f"generalization analysis failed: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result.to_dict(), sort_keys=True))
        return 0 if result.verdict == "SUPPORTED" else 1
    raise AssertionError("unreachable")
