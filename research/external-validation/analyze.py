from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "participant_id",
    "task_id",
    "condition",
    "ground_truth",
    "decision",
    "review_time_seconds",
    "confidence_1_to_5",
    "ambiguity_1_to_5",
    "first_blocker_time_seconds",
    "false_acceptance",
    "false_rejection",
}


def _as_float(value: str) -> float | None:
    stripped = value.strip()
    return float(stripped) if stripped else None


def _as_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"expected true/false, got {value!r}")
    return normalized == "true"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("input has no CSV header")
        missing = REQUIRED_FIELDS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
        rows = [dict(row) for row in reader]

    usable = [
        row
        for row in rows
        if row.get("notes", "") != "TEMPLATE_ROW_DO_NOT_ANALYZE"
        and not row.get("exclusion_reason", "").strip()
    ]
    if not usable:
        raise ValueError("input contains no analyzable rows")
    return usable


def _relative_reduction(baseline: float, treatment: float) -> float | None:
    if baseline == 0:
        return None
    return (baseline - treatment) / baseline


def summarize(rows: list[dict[str, str]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        condition = row["condition"].strip()
        if condition not in {"A", "B"}:
            raise ValueError(f"unknown condition: {condition!r}")
        grouped[condition].append(row)
    if set(grouped) != {"A", "B"}:
        raise ValueError("both conditions A and B are required")

    condition_metrics: dict[str, dict[str, Any]] = {}
    for condition, items in sorted(grouped.items()):
        review_times = [float(item["review_time_seconds"]) for item in items]
        ambiguity = [float(item["ambiguity_1_to_5"]) for item in items]
        confidence = [float(item["confidence_1_to_5"]) for item in items]
        blocker_times = [
            value
            for item in items
            if (value := _as_float(item["first_blocker_time_seconds"])) is not None
        ]
        false_acceptance = [_as_bool(item["false_acceptance"]) for item in items]
        false_rejection = [_as_bool(item["false_rejection"]) for item in items]
        condition_metrics[condition] = {
            "rows": len(items),
            "participants": len({item["participant_id"] for item in items}),
            "medianReviewTimeSeconds": statistics.median(review_times),
            "meanAmbiguity": statistics.fmean(ambiguity),
            "meanConfidence": statistics.fmean(confidence),
            "medianFirstBlockerTimeSeconds": (
                statistics.median(blocker_times) if blocker_times else None
            ),
            "falseAcceptanceRate": sum(false_acceptance) / len(false_acceptance),
            "falseRejectionRate": sum(false_rejection) / len(false_rejection),
        }

    baseline = condition_metrics["A"]
    treatment = condition_metrics["B"]
    false_acceptance_reduction = _relative_reduction(
        baseline["falseAcceptanceRate"], treatment["falseAcceptanceRate"]
    )
    ambiguity_reduction = _relative_reduction(baseline["meanAmbiguity"], treatment["meanAmbiguity"])
    blocker_reduction = None
    if (
        baseline["medianFirstBlockerTimeSeconds"] is not None
        and treatment["medianFirstBlockerTimeSeconds"] is not None
    ):
        blocker_reduction = _relative_reduction(
            baseline["medianFirstBlockerTimeSeconds"],
            treatment["medianFirstBlockerTimeSeconds"],
        )
    review_time_change = (
        treatment["medianReviewTimeSeconds"] - baseline["medianReviewTimeSeconds"]
    ) / baseline["medianReviewTimeSeconds"]

    threshold_results = {
        "falseAcceptanceReductionAtLeast25Percent": (
            false_acceptance_reduction is not None and false_acceptance_reduction >= 0.25
        ),
        "ambiguityReductionAtLeast20Percent": (
            ambiguity_reduction is not None and ambiguity_reduction >= 0.20
        ),
        "firstBlockerTimeReductionAtLeast20Percent": (
            blocker_reduction is not None and blocker_reduction >= 0.20
        ),
        "medianReviewTimeMoreThan20PercentSlower": review_time_change > 0.20,
    }
    primary_effect = any(
        threshold_results[key]
        for key in (
            "falseAcceptanceReductionAtLeast25Percent",
            "ambiguityReductionAtLeast20Percent",
            "firstBlockerTimeReductionAtLeast20Percent",
        )
    )
    offset_by_cost = (
        threshold_results["medianReviewTimeMoreThan20PercentSlower"]
        and not threshold_results["falseAcceptanceReductionAtLeast25Percent"]
    )

    synthetic = any(item["participant_id"].startswith("SYNTH-") for item in rows)
    real_participant_count = len(
        {item["participant_id"] for item in rows if not item["participant_id"].startswith("SYNTH-")}
    )
    computed_threshold_result = primary_effect and not offset_by_cost

    return {
        "schemaVersion": "1",
        "status": "SYNTHETIC_DRY_RUN" if synthetic else "EXTERNAL_DATA_ANALYSIS",
        "realParticipantCount": real_participant_count,
        "conditions": condition_metrics,
        "effects": {
            "falseAcceptanceRelativeReduction": false_acceptance_reduction,
            "ambiguityRelativeReduction": ambiguity_reduction,
            "firstBlockerTimeRelativeReduction": blocker_reduction,
            "medianReviewTimeRelativeChange": review_time_change,
        },
        "thresholds": threshold_results,
        "preregisteredH1MaterialThresholdMet": None if synthetic else computed_threshold_result,
        "syntheticThresholdExercise": computed_threshold_result if synthetic else None,
        "interpretationWarning": (
            "Synthetic rows validate analysis plumbing only. Their metrics and threshold "
            "exercise are not human evidence and cannot support H1, adoption, or impact."
            if synthetic
            else "External data still require protocol, exclusion, and provenance review."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = summarize(load_rows(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
