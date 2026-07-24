#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from agent_completion_ledger.extract import extract_counts


def main() -> int:
    frozen_path = Path("data/frozen/submission-summaries.json")
    raw_dir = Path("data/raw-upstream")
    frozen: list[dict[str, Any]] = json.loads(frozen_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    extracted: list[dict[str, object]] = []

    for expected in frozen:
        source = raw_dir / f"{expected['submission']}.json"
        if not source.exists():
            errors.append(f"missing raw source: {source}")
            continue
        payload: dict[str, Any] = json.loads(source.read_text(encoding="utf-8"))
        actual = asdict(extract_counts(payload, benchmark_size=int(expected["benchmark_size"])))
        for key in (
            "benchmark_size",
            "generated",
            "resolved",
            "no_logs",
            "no_generation_raw",
            "inferred_no_claim",
        ):
            if actual[key] != expected[key]:
                errors.append(
                    f"{expected['submission']}: {key} expected "
                    f"{expected[key]!r}, got {actual[key]!r}"
                )
        extracted.append({"submission": expected["submission"], **actual})

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(json.dumps(extracted, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
