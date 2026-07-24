#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, median

from agent_completion_ledger.io import load_records
from agent_completion_ledger.metrics import analyze_records


def main() -> int:
    records = load_records(Path("data/frozen/submission-summaries.json"))
    items, aggregate = analyze_records(records)

    thresholds = [0.20, 1 / 3, 0.40, 0.50, 0.60]
    threshold_sweep = []
    for threshold in thresholds:
        _, result = analyze_records(records, threshold=threshold)
        threshold_sweep.append(
            {
                "threshold": threshold,
                "submissions_above": result.submissions_above_threshold,
                "h1_rule_supported": result.h1_supported,
            }
        )

    leave_one_out = []
    for omitted in records:
        subset = [record for record in records if record.submission != omitted.submission]
        _, result = analyze_records(subset, stopping_minimum_claims=1)
        leave_one_out.append(
            {
                "omitted": omitted.submission,
                "generated": result.generated,
                "false_completion_rate": result.false_completion_rate,
                "wilson_lower": result.false_completion_interval.lower,
                "wilson_upper": result.false_completion_interval.upper,
            }
        )

    unsupported = aggregate.generated - aggregate.resolved
    maximum_unsupported_for_twenty_percent = int(aggregate.generated * 0.20)
    reclassifications_needed = unsupported - maximum_unsupported_for_twenty_percent

    output = {
        "schema_version": "0.1.0",
        "macro_submission_rate_mean": mean(
            item.false_completion_rate for item in items
        ),
        "macro_submission_rate_median": median(
            item.false_completion_rate for item in items
        ),
        "threshold_sweep": threshold_sweep,
        "leave_one_submission_out": leave_one_out,
        "oracle_false_negative_break_even": {
            "unsupported_claims": unsupported,
            "reclassifications_needed_to_reach_at_most_20_percent": (
                reclassifications_needed
            ),
            "share_of_unsupported_requiring_reclassification": (
                reclassifications_needed / unsupported
            ),
            "interpretation": (
                "At least this many currently unsupported claims would need to be "
                "acceptable despite the oracle to reduce the observed rate to 20%."
            ),
        },
        "accepted_novelty_criticism": (
            "The primary rate is the arithmetic complement of benchmark resolution "
            "among generated patches; the reusable contribution is the evidence-state "
            "adapter, frozen extraction record, and reporting protocol, not a new "
            "agent-capability metric."
        ),
    }
    target = Path("results/published/red-team-sensitivity.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
