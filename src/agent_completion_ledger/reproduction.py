from __future__ import annotations

import json
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .io import (
    load_records,
    sha256_file,
    sha256_normalized_text_file,
    validate_ledger,
    write_outputs,
)
from .metrics import analyze_records


@dataclass(frozen=True, slots=True)
class ReproductionResult:
    status: str
    exit_code: int
    output_dir: str
    matched: tuple[str, ...]
    mismatched: tuple[str, ...]
    errors: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schemaVersion": "1",
            "status": self.status,
            "exitCode": self.exit_code,
            "environment": {
                "python": platform.python_version(),
                "implementation": platform.python_implementation(),
                "platform": platform.system(),
            },
            "outputDirectory": self.output_dir,
            "matchedOutputs": list(self.matched),
            "mismatchedOutputs": list(self.mismatched),
            "errors": list(self.errors),
        }


def _load_manifest(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("research manifest must be an object")
    return value


def _markdown(result: ReproductionResult) -> str:
    lines = [
        "# Reproduction report",
        "",
        f"- Status: **`{result.status}`**",
        f"- Exit code: `{result.exit_code}`",
        f"- Python: `{platform.python_version()}`",
        f"- Platform: `{platform.system()}`",
        f"- Output directory: `{result.output_dir}`",
        "",
        "## Hash verification",
        "",
    ]
    if result.matched:
        lines.append("Matched: " + ", ".join(f"`{item}`" for item in result.matched))
    if result.mismatched:
        lines.append("Mismatched: " + ", ".join(f"`{item}`" for item in result.mismatched))
    if result.errors:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in result.errors)
    return "\n".join(lines).rstrip() + "\n"


def reproduce(
    manifest_path: Path,
    output_dir: Path,
    *,
    source_override: Path | None = None,
) -> ReproductionResult:
    errors: list[str] = []
    if sys.version_info < (3, 11):
        errors.append("Python 3.11 or newer is required")
    try:
        manifest = _load_manifest(manifest_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return ReproductionResult("ERROR", 2, str(output_dir), (), (), (str(exc),))

    source = source_override or Path(
        manifest.get("dataset_sources", {}).get(
            "records_file", "data/frozen/submission-summaries.json"
        )
    )
    expected_source_hash = manifest.get("dataset_sources", {}).get("records_sha256")
    if not source.is_file():
        errors.append(f"required source file is missing: {source}")
    elif expected_source_hash and sha256_normalized_text_file(source) != expected_source_hash:
        errors.append(f"source hash mismatch: {source}")
    if errors:
        return ReproductionResult("ERROR", 2, str(output_dir), (), (), tuple(errors))

    try:
        records = load_records(source)
        per_submission, aggregate = analyze_records(
            records,
            threshold=0.20,
            stopping_minimum_claims=3000,
        )
        write_outputs(output_dir, records, per_submission, aggregate)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return ReproductionResult("ERROR", 2, str(output_dir), (), (), (str(exc),))

    ledger_errors = validate_ledger(output_dir / "ledger.jsonl")
    if ledger_errors:
        errors.extend(ledger_errors)

    expected = manifest.get("expected_outputs", {})
    matched: list[str] = []
    mismatched: list[str] = []
    for filename in (
        "summary.json",
        "submission-metrics.csv",
        "ledger.jsonl",
        "sensitivity.json",
    ):
        output = output_dir / filename
        expected_hash = expected.get(filename)
        if not output.is_file() or not expected_hash or sha256_file(output) != expected_hash:
            mismatched.append(filename)
        else:
            matched.append(filename)

    exit_code = 2 if errors else (1 if mismatched else 0)
    status = "ERROR" if errors else ("MISMATCH" if mismatched else "REPRODUCED")
    result = ReproductionResult(
        status,
        exit_code,
        str(output_dir),
        tuple(matched),
        tuple(mismatched),
        tuple(errors),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "reproduction-report.json").write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output_dir / "reproduction-summary.md").write_text(
        _markdown(result),
        encoding="utf-8",
        newline="\n",
    )
    return result
