from pathlib import Path

import yaml

from agent_completion_ledger.contract import load_contract


def test_public_contract_schema_copies_match() -> None:
    assert (
        Path("schemas/completion-contract.schema.json").read_bytes()
        == Path("src/agent_completion_ledger/schemas/completion-contract.schema.json").read_bytes()
    )


def test_composite_action_has_required_steps() -> None:
    value = yaml.safe_load(Path("action.yml").read_text(encoding="utf-8"))
    assert value["runs"]["using"] == "composite"
    text = Path("action.yml").read_text(encoding="utf-8")
    assert "shell: bash" in text
    assert "agent-completion-ledger" in text


def test_dogfood_contracts_define_three_states() -> None:
    for path in (
        Path("examples/real-repositories/shipcheck/completion-ledger.yml"),
        Path("examples/real-repositories/csv-snapshot/completion-ledger.yml"),
    ):
        contract = load_contract(path)
        assert len(contract.tasks) == 3
        identifiers = {task.id.rsplit("-", 1)[-1] for task in contract.tasks}
        assert identifiers == {"success", "failure", "unverifiable"}


def test_issue_forms_do_not_request_secrets() -> None:
    for path in Path(".github/ISSUE_TEMPLATE").glob("reproduction-*.yml"):
        text = path.read_text(encoding="utf-8").lower()
        assert "do not include api keys" in text or "remove secrets" in text
        assert "password" not in text


def test_preregistered_source_matches_derived_record() -> None:
    prereg = Path("docs/v0.2.0-generalization-preregistered.md").read_text(encoding="utf-8")
    source = Path("data/generalization/multi-swe-bench-go-magentless-summary.json").read_text(
        encoding="utf-8"
    )
    assert "evaluation/go/verified/20250329_MagentLess_Claude-3.7-Sonnet" in prereg
    assert "6a7d5566f62fa76f4192302cf763051b98e4facc" in prereg
    assert "6a7d5566f62fa76f4192302cf763051b98e4facc" in source
