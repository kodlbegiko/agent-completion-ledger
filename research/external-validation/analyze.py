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


def _metrics(items: list[dict[str, str]]) -> dict[str, float | int | None]:
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
    return {
        "rows": len(items),
        "medianReviewTimeSeconds": statistics.median(review_times),
        "meanAmbiguity": statistics.fmean(ambiguity),
        "meanConfidence": statistics.fmean(confidence),
        "medianFirstBlockerTimeSeconds": (
            statistics.median(blocker_times) if blocker_times else None
        ),
        "falseAcceptanceRate": sum(false_acceptance) / len(false_acceptance),
        "falseRejectionRate": sum(false_rejection) / len(false_rejection),
    }


def _participant_balanced_summary(
    participant_metrics: list[dict[str, Any]],
) -> dict[str, float | int | None]:
    blocker_medians = [
        float(item["medianFirstBlockerTimeSeconds"])
        for item in participant_metrics
        if item["medianFirstBlockerTimeSeconds"] is not None
    ]
    return {
        "participants": len(participant_metrics),
        "medianReviewTimeSeconds": statistics.median(
            float(item["medianReviewTimeSeconds"]) for item in participant_metrics
        ),
        "meanAmbiguity": statistics.fmean(
            float(item["meanAmbiguity"]) for item in participant_metrics
        ),
        "meanConfidence": statistics.fmean(
            float(item["meanConfidence"]) for item in participant_metrics
        ),
        "medianFirstBlockerTimeSeconds": (
            statistics.median(blocker_medians) if blocker_medians else None
        ),
        "falseAcceptanceRate": statistics.fmean(
            float(item["falseAcceptanceRate"]) for item in participant_metrics
        ),
        "falseRejectionRate": statistics.fmean(
            float(item["falseRejectionRate"]) for item in participant_metrics
        ),
    }


def _condition_effects(
    baseline: dict[str, float | int | None],
    treatment: dict[str, float | int | None],
) -> dict[str, float | None]:
    false_acceptance_reduction = _relative_reduction(
        float(baseline["falseAcceptanceRate"]),
        float(treatment["falseAcceptanceRate"]),
    )
    ambiguity_reduction = _relative_reduction(
        float(baseline["meanAmbiguity"]),
        float(treatment["meanAmbiguity"]),
    )
    blocker_reduction = None
    if (
        baseline["medianFirstBlockerTimeSeconds"] is not None
        and treatment["medianFirstBlockerTimeSeconds"] is not None
    ):
        blocker_reduction = _relative_reduction(
            float(baseline["medianFirstBlockerTimeSeconds"]),
            float(treatment["medianFirstBlockerTimeSeconds"]),
        )
    review_time_change = (
        float(treatment["medianReviewTimeSeconds"])
        - float(baseline["medianReviewTimeSeconds"])
    ) / float(baseline["medianReviewTimeSeconds"])
    return {
        "falseAcceptanceRelativeReduction": false_acceptance_reduction,
        "ambiguityRelativeReduction": ambiguity_reduction,
        "firstBlockerTimeRelativeReduction": blocker_reduction,
        "medianReviewTimeRelativeChange": review_time_change,
    }


def summarize(rows: list[dict[str, str]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        condition = row["condition"].strip()
        if condition not in {"A", "B"}:
            raise ValueError(f"unknown condition: {condition!r}")
        grouped[condition].append(row)
    if set(grouped) != {"A", "B"}:
        raise ValueError("both conditions A and B are required")

    pooled_conditions: dict[str, dict[str, float | int | None]] = {}
    participant_records: list[dict[str, Any]] = []
    participant_balanced_conditions: dict[str, dict[str, float | int | None]] = {}

    for condition, items in sorted(grouped.items()):
        pooled = _metrics(items)
        pooled["participants"] = len({item["participant_id"] for item in items})
        pooled_conditions[condition] = pooled

        by_participant: dict[str, list[dict[str, str]]] = defaultdict(list)
        for item in items:
            by_participant[item["participant_id"]].append(item)
        condition_participant_metrics: list[dict[str, Any]] = []
        for participant_id, participant_items in sorted(by_participant.items()):
            metrics = {
                "participantId": participant_id,
                "condition": condition,
                **_metrics(participant_items),
            }
            participant_records.append(metrics)
            condition_participant_metrics.append(metrics)
        participant_balanced_conditions[condition] = _participant_balanced_summary(
            condition_participant_metrics
        )

    primary_effects = _condition_effects(
        participant_balanced_conditions["A"], participant_balanced_conditions["B"]
    )
    pooled_effects = _condition_effects(pooled_conditions["A"], pooled_conditions["B"])

    threshold_results = {
        "falseAcceptanceReductionAtLeast25Percent": (
            primary_effects["falseAcceptanceRelativeReduction"] is not None
            and primary_effects["falseAcceptanceRelativeReduction"] >= 0.25
        ),
        "ambiguityReductionAtLeast20Percent": (
            primary_effects["ambiguityRelativeReduction"] is not None
            and primary_effects["ambiguityRelativeReduction"] >= 0.20
        ),
        "firstBlockerTimeReductionAtLeast20Percent": (
            primary_effects["firstBlockerTimeRelativeReduction"] is not None
            and primary_effects["firstBlockerTimeRelativeReduction"] >= 0.20
        ),
        "medianReviewTimeMoreThan20PercentSlower": (
            primary_effects["medianReviewTimeRelativeChange"] is not None
            and primary_effects["medianReviewTimeRelativeChange"] > 0.20
        ),
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
        "schemaVersion": "2",
        "status": "SYNTHETIC_DRY_RUN" if synthetic else "EXTERNAL_DATA_ANALYSIS",
        "realParticipantCount": real_participant_count,
        "primaryAnalysisBasis": "participant-balanced condition summaries",
        "participantMetrics": participant_records,
        "participantBalancedConditions": participant_balanced_conditions,
        "pooledConditions": pooled_conditions,
        "primaryEffects": primary_effects,
        "pooledSensitivityEffects": pooled_effects,
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
