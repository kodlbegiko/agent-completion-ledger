from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ExtractedCounts:
    benchmark_size: int
    generated: int
    resolved: int
    no_logs: int
    no_generation_raw: int
    inferred_no_claim: int
    source_format: str


def _string_list(value: Any, key: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a list of strings")
    return value


def extract_counts(
    payload: dict[str, Any],
    *,
    benchmark_size: int = 500,
) -> ExtractedCounts:
    """Extract auditable aggregate counts from known SWE-bench result schemas."""

    if benchmark_size <= 0:
        raise ValueError("benchmark_size must be positive")

    no_generation = _string_list(payload.get("no_generation"), "no_generation")
    no_logs = set(_string_list(payload.get("no_logs"), "no_logs"))
    resolved = set(_string_list(payload.get("resolved"), "resolved"))
    if no_logs & resolved:
        raise ValueError("no_logs and resolved must be disjoint")

    if "generated" in payload:
        generated_ids = set(_string_list(payload.get("generated"), "generated"))
        if resolved - generated_ids:
            raise ValueError("resolved contains an instance absent from generated")
        if no_logs - generated_ids:
            raise ValueError("no_logs contains an instance absent from generated")
        generated = len(generated_ids)
        source_format = "legacy-expanded"
    else:
        absent_ids = set(no_generation)
        if absent_ids & resolved:
            raise ValueError("no_generation and resolved must be disjoint")
        if absent_ids & no_logs:
            raise ValueError("no_generation and no_logs must be disjoint")
        generated = benchmark_size - len(absent_ids)
        source_format = "compact"

    if generated < 0 or generated > benchmark_size:
        raise ValueError("derived generated count is outside benchmark bounds")
    if len(resolved) + len(no_logs) > generated:
        raise ValueError("resolved plus no_logs cannot exceed generated")

    return ExtractedCounts(
        benchmark_size=benchmark_size,
        generated=generated,
        resolved=len(resolved),
        no_logs=len(no_logs),
        no_generation_raw=len(no_generation),
        inferred_no_claim=benchmark_size - generated,
        source_format=source_format,
    )
