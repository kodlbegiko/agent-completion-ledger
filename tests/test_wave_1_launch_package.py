import csv
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "external-validation"


def test_recruitment_matrix_preserves_legacy_and_wave_one_schema() -> None:
    path = RESEARCH / "recruitment-targets.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames

    assert fields == [
        "rank",
        "fit",
        "repository",
        "maintainer_type",
        "public_contact_channel",
        "why_fit",
        "reasonable_pilot_task",
        "estimated_integration_friction",
        "security_notes",
        "do_not_contact_reason",
        "activity_evidence",
        "current_status",
        "launch_audit_date",
        "audit_head_sha",
        "repository_state",
        "tests_or_build",
        "contribution_or_issue_policy",
        "contact_gate",
        "wave_1_role",
    ]
    assert len(rows) == 30
    assert len({row["repository"] for row in rows}) == 30
    assert {row["fit"] for row in rows} <= {
        "HIGH FIT",
        "MEDIUM FIT",
        "LOW FIT",
        "EXCLUDE",
    }
    assert {row["current_status"] for row in rows} <= {
        "CURRENT HIGH FIT",
        "CURRENT MEDIUM FIT",
        "CURRENT LOW FIT",
        "NO LONGER SUITABLE",
        "DO NOT CONTACT",
    }

    mandatory = {
        "rank",
        "fit",
        "repository",
        "current_status",
        "launch_audit_date",
        "audit_head_sha",
        "repository_state",
        "tests_or_build",
        "contribution_or_issue_policy",
        "contact_gate",
    }
    assert all(row[field].strip() for row in rows for field in mandatory)


def test_wave_one_roles_and_status_are_fixed_and_unsent() -> None:
    roles_path = RESEARCH / "wave-1-target-roles.csv"
    with roles_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 9
    assert len({row["wave_id"] for row in rows}) == 9
    assert len({row["repository"] for row in rows}) == 9
    roles = [row["role"] for row in rows]
    assert roles.count("MAINTAINER_PILOT") == 5
    assert roles.count("INDEPENDENT_REPRODUCTION") == 2
    assert roles.count("INDEPENDENT_SECURITY_REVIEW") == 2
    assert {row["status"] for row in rows} == {"NOT_SENT"}

    status_path = RESEARCH / "wave-1-status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    assert status["schemaVersion"] == "1"
    assert status["decision"] == "READY FOR OWNER OUTREACH"
    assert status["wave1"] == {
        "maintainerPilotTargets": 5,
        "reproductionTargets": 2,
        "securityReviewTargets": 2,
        "messagesSent": 0,
        "ownerReviewRequired": True,
    }
    assert all(value == 0 for value in status["externalEvidence"].values())


def test_historical_prospective_dogfood_contract_is_unchanged() -> None:
    path = (
        ROOT
        / "research"
        / "prospective-dogfood"
        / "acl-external-validation-operations"
        / "completion-ledger.yml"
    )
    text = path.read_text(encoding="utf-8")
    contract = yaml.safe_load(text)
    evidence = contract["tasks"][0]["evidence"]
    noncomment_lines = [
        line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")
    ]

    assert len(evidence) == 12
    assert len(noncomment_lines) == 74
    assert "READY FOR RECRUITMENT" in text
    assert "Real participant count: **0**" in text
    assert "Non-author repository count: **0**" in text


def test_nested_invitation_fences_keep_complete_messages() -> None:
    path = ROOT / "docs" / "outreach" / "WAVE-1-READY-TO-SEND.md"
    text = path.read_text(encoding="utf-8")
    for section_id in ("W1-R1", "W1-R2", "W1-S1", "W1-S2"):
        section_start = text.index(f"## {section_id}")
        next_section = text.find("\n## ", section_start + 1)
        section = text[section_start : next_section if next_section != -1 else None]
        assert "````markdown\n" in section
        assert "\n````\n" in section
        assert section.count("```bash\n") == 1

    r1_start = text.index("## W1-R1")
    r1_end = text.index("\n## W1-R2", r1_start)
    r1 = text[r1_start:r1_end]
    assert "Expected result:" in r1
    assert "Please do not provide private project data" in r1


def test_security_instructions_separate_main_from_v031_execution() -> None:
    path = ROOT / "docs" / "INDEPENDENT-SECURITY-REVIEW.md"
    text = path.read_text(encoding="utf-8")
    main_index = text.index("git switch main")
    worktree_index = text.index("git worktree add ../acl-v0.3.1 v0.3.1")

    assert main_index < worktree_index
    assert 'python -m pip install -e ".[dev]"' in text
    assert "ACL is **not a sandbox**" in text
    assert "never third-party targets or real secrets" in text
    assert not (ROOT / ".github" / "workflows" / "wave-1-test-diagnostic.yml").exists()
