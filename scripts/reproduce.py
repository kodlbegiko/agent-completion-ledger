#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from agent_completion_ledger.io import load_records, write_outputs
from agent_completion_ledger.metrics import analyze_records


def main() -> int:
    records = load_records(Path("data/frozen/submission-summaries.json"))
    per_submission, aggregate = analyze_records(records)
    write_outputs(Path("results/reproduced"), records, per_submission, aggregate)
    print("SUPPORTED" if aggregate.h1_supported else "NOT SUPPORTED")
    return 0 if aggregate.h1_supported else 1


if __name__ == "__main__":
    raise SystemExit(main())
