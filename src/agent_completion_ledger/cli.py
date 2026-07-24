from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from .io import load_records, validate_ledger, write_outputs
from .metrics import analyze_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-completion-ledger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser(
        "analyze",
        help="Analyze frozen submission summaries",
    )
    analyze.add_argument("source", type=Path)
    analyze.add_argument("--output-dir", type=Path, required=True)
    analyze.add_argument("--threshold", type=float, default=0.20)
    analyze.add_argument("--minimum-claims", type=int, default=3000)

    benchmark = subparsers.add_parser(
        "benchmark",
        help="Reproduce the committed pilot",
    )
    benchmark.add_argument("--output-dir", type=Path, required=True)
    benchmark.add_argument(
        "--source",
        type=Path,
        default=Path("data/frozen/submission-summaries.json"),
    )

    validate = subparsers.add_parser(
        "validate-ledger",
        help="Validate a JSONL evidence ledger",
    )
    validate.add_argument("ledger", type=Path)
    return parser


def _analyze(
    source: Path,
    output_dir: Path,
    threshold: float,
    minimum_claims: int,
) -> int:
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
                "verdict": ("SUPPORTED" if aggregate.h1_supported else "NOT SUPPORTED"),
                "generated": aggregate.generated,
                "false_completion_rate": aggregate.false_completion_rate,
                "hashes": hashes,
            },
            sort_keys=True,
        )
    )
    return 0 if aggregate.h1_supported else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        return _analyze(
            args.source,
            args.output_dir,
            args.threshold,
            args.minimum_claims,
        )
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
    raise AssertionError("unreachable")
