"""Evidence-gated status accounting for coding-agent benchmark submissions."""

from .metrics import AggregateMetrics, SubmissionMetrics, analyze_records
from .model import EvidenceState, SourceRecord

__all__ = [
    "AggregateMetrics",
    "EvidenceState",
    "SourceRecord",
    "SubmissionMetrics",
    "analyze_records",
]

__version__ = "0.1.0"
