from __future__ import annotations

import csv
from pathlib import Path

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _read_single_csv_row(relative_path: str) -> tuple[list[str], list[str]]:
    path = REPOSITORY_ROOT / relative_path
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    assert len(rows) == 2
    return rows[0], rows[1]


def test_external_integration_template_has_aligned_columns() -> None:
    header, template = _read_single_csv_row(
        "research/external-validation/adoption-integration-template.csv"
    )
    assert len(header) == 35
    assert len(template) == len(header)
    record = dict(zip(header, template, strict=True))
    assert record["ci_runtime_overhead_seconds"] == ""
    assert record["decision_before_ledger"] == "INSUFFICIENT_EVIDENCE"
    assert record["private_code_collected"] == "false"
    assert record["secrets_collected"] == "false"
    assert record["employer_confidential_data_collected"] == "false"
    assert record["notes"]


def test_prospective_dogfood_template_has_aligned_columns() -> None:
    header, template = _read_single_csv_row("research/prospective-dogfood/collection-template.csv")
    assert len(header) == 37
    assert len(template) == len(header)
    record = dict(zip(header, template, strict=True))
    assert record["author_assistance_count"] == "0"
    assert record["subjective_conditions_not_automated"] == "Conditions requiring human judgment"
    assert record["security_or_privacy_concerns"] == "No secrets/private code"
    assert record["notes"]


def test_pypi_workflow_keeps_checksums_outside_distribution_directory() -> None:
    path = REPOSITORY_ROOT / ".github/workflows/publish-pypi.yml"
    text = path.read_text(encoding="utf-8")
    parsed = yaml.load(text, Loader=yaml.BaseLoader)
    assert isinstance(parsed, dict)
    assert "checksums/SHA256SUMS" in text
    assert "dist/SHA256SUMS" not in text
    assert "name: python-package-checksums" in text
    assert text.count("packages-dir: dist/") == 2


def test_release_artifact_workflow_is_manual_and_environment_protected() -> None:
    path = REPOSITORY_ROOT / ".github/workflows/build-release-artifacts.yml"
    text = path.read_text(encoding="utf-8")
    parsed = yaml.load(text, Loader=yaml.BaseLoader)
    assert isinstance(parsed, dict)
    assert "workflow_dispatch:" in text
    assert "environment: release-artifacts" in text
    assert "gh release upload" in text
    assert "SHA256SUMS" in text


def test_outreach_log_records_first_owner_send() -> None:
    path = REPOSITORY_ROOT / "research/external-validation/outreach-log.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    record = rows[0]
    assert record["attempt_number"] == "1"
    assert record["wave_id"] == "W1-M1"
    assert record["target_repository"] == "tmux-python/tmuxp"
    assert record["owner_approved"] == "yes"
    assert record["response_state"] == "SENT — AWAITING RESPONSE"
    assert record["responder_class"] == "UNKNOWN"
    assert record["participant_id"] == ""
    assert record["public_link"] == "https://github.com/tmux-python/tmuxp/discussions/1078"


def test_recruitment_matrix_has_exactly_thirty_unique_targets() -> None:
    path = REPOSITORY_ROOT / "research/external-validation/recruitment-targets.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 30
    assert len({row["repository"] for row in rows}) == 30
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["fit"]] = counts.get(row["fit"], 0) + 1
    assert counts == {
        "HIGH FIT": 10,
        "MEDIUM FIT": 16,
        "LOW FIT": 2,
        "EXCLUDE": 2,
    }
