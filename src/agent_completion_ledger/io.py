from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .metrics import AggregateMetrics, SubmissionMetrics
from .model import EvidenceState, SourceRecord


def canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_normalized_text_file(path: Path) -> str:
    """Hash UTF-8 text after universal-newline normalization.

    Git may materialize tracked text with CRLF on Windows. Research inputs are
    content-equivalent across checkouts, so their manifest hash uses canonical LF.
    Generated research outputs are written with explicit LF and use byte hashes.
    """

    text = path.read_text(encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_records(path: Path) -> list[SourceRecord]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("source file must contain a JSON array")
    records: list[SourceRecord] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("each source record must be a JSON object")
        records.append(SourceRecord.from_mapping(item))
    return records


def ledger_rows(records: Iterable[SourceRecord]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in records:
        counts = (
            (EvidenceState.SUPPORTED, record.resolved),
            (EvidenceState.FAILED, record.failed),
            (EvidenceState.UNVERIFIABLE, record.no_logs),
            (EvidenceState.NO_CLAIM, record.inferred_no_claim),
        )
        for state, count in counts:
            rows.append(
                {
                    "schema_version": "0.1.0",
                    "submission": record.submission,
                    "evidence_state": state.value,
                    "count": count,
                    "evidence": {
                        "kind": "swe-bench-results-json",
                        "source_path": record.source_path,
                        "source_blob_sha": record.source_blob_sha,
                    },
                    "scope_note": (
                        "SWE-bench executable-oracle support; not user-satisfaction ground truth"
                    ),
                }
            )
    return rows


def _write_lf(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def write_outputs(
    output_dir: Path,
    records: list[SourceRecord],
    per_submission: list[SubmissionMetrics],
    aggregate: AggregateMetrics,
) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "schema_version": "0.1.0",
        "verdict": "SUPPORTED" if aggregate.h1_supported else "NOT SUPPORTED",
        "aggregate": aggregate.to_dict(),
        "submissions": [item.to_dict() for item in per_submission],
    }
    summary_path = output_dir / "summary.json"
    _write_lf(
        summary_path,
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )

    csv_path = output_dir / "submission-metrics.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "submission",
            "generated",
            "resolved",
            "failed",
            "unverifiable",
            "no_claim",
            "false_completion_rate",
            "strict_false_completion_rate",
            "baseline_completion_precision",
            "no_generation_discrepancy",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in per_submission:
            row = asdict(item)
            writer.writerow({key: row[key] for key in fieldnames})

    ledger_path = output_dir / "ledger.jsonl"
    _write_lf(
        ledger_path,
        "".join(canonical_json(row) + "\n" for row in ledger_rows(records)),
    )

    sensitivity = {
        "inclusive": {
            "numerator": aggregate.generated - aggregate.resolved,
            "denominator": aggregate.generated,
            "rate": aggregate.false_completion_rate,
            "wilson_95": asdict(aggregate.false_completion_interval),
            "treatment_of_no_logs": "counted as not supported",
        },
        "strict": {
            "numerator": aggregate.failed,
            "denominator": aggregate.generated - aggregate.unverifiable,
            "rate": aggregate.strict_false_completion_rate,
            "wilson_95": asdict(aggregate.strict_false_completion_interval),
            "treatment_of_no_logs": "excluded",
        },
        "difference": (aggregate.false_completion_rate - aggregate.strict_false_completion_rate),
    }
    sensitivity_path = output_dir / "sensitivity.json"
    _write_lf(
        sensitivity_path,
        json.dumps(sensitivity, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )

    output_paths = (summary_path, csv_path, ledger_path, sensitivity_path)
    hashes = {path.name: sha256_file(path) for path in output_paths}
    hash_path = output_dir / "output-hashes.json"
    _write_lf(hash_path, json.dumps(hashes, indent=2, sort_keys=True) + "\n")
    return hashes


def validate_ledger(path: Path) -> list[str]:
    errors: list[str] = []
    allowed = {state.value for state in EvidenceState}
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            errors.append(f"line {line_number}: blank line")
            continue
        try:
            row: Any = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_number}: record must be an object")
            continue
        if row.get("evidence_state") not in allowed:
            errors.append(f"line {line_number}: unknown evidence_state")
        if not isinstance(row.get("count"), int) or row.get("count", -1) < 0:
            errors.append(f"line {line_number}: count must be a non-negative integer")
        evidence = row.get("evidence")
        if not isinstance(evidence, dict) or not evidence.get("source_blob_sha"):
            errors.append(f"line {line_number}: evidence source is missing")
    return errors
