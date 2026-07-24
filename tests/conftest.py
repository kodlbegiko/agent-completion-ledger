from pathlib import Path

import pytest

from agent_completion_ledger.io import load_records
from agent_completion_ledger.model import SourceRecord


@pytest.fixture
def records() -> list[SourceRecord]:
    return load_records(Path("data/frozen/submission-summaries.json"))
