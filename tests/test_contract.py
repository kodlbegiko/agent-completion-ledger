import json
from pathlib import Path

import pytest
import yaml

from agent_completion_ledger.contract import (
    ContractError,
    contract_from_mapping,
    default_contract,
    load_contract,
)


def test_default_contract_is_valid() -> None:
    contract = contract_from_mapping(default_contract())
    assert contract.schema_version == "1"
    assert contract.tasks[0].id == "example-task"


def test_load_yaml_contract(tmp_path: Path) -> None:
    path = tmp_path / "contract.yml"
    path.write_text(yaml.safe_dump(default_contract()), encoding="utf-8")
    assert load_contract(path).allowed_executables == ("python",)


def test_load_json_contract(tmp_path: Path) -> None:
    path = tmp_path / "contract.json"
    path.write_text(json.dumps(default_contract()), encoding="utf-8")
    assert len(load_contract(path).tasks) == 1


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value.pop("schemaVersion"),
        lambda value: value.update(schemaVersion="2"),
        lambda value: value.update(extra=True),
        lambda value: value.update(tasks=[]),
        lambda value: value["tasks"][0]["claim"].update(status="maybe"),
        lambda value: value["tasks"][0]["evidence"][0].pop("path"),
        lambda value: value["tasks"][0]["evidence"][1].update(command="pytest"),
    ],
)
def test_schema_rejects_invalid_contract(mutation: object) -> None:
    value = default_contract()
    mutation(value)  # type: ignore[operator]
    with pytest.raises(ContractError):
        contract_from_mapping(value)


def test_duplicate_task_ids_rejected() -> None:
    value = default_contract()
    value["tasks"].append(value["tasks"][0].copy())
    with pytest.raises(ContractError, match="unique"):
        contract_from_mapping(value)


def test_non_object_contract_rejected() -> None:
    with pytest.raises(ContractError, match="object"):
        contract_from_mapping([])


def test_malformed_yaml_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad.yml"
    path.write_text("tasks: [", encoding="utf-8")
    with pytest.raises(ContractError, match="parse"):
        load_contract(path)


def test_missing_contract_rejected(tmp_path: Path) -> None:
    with pytest.raises(ContractError, match="read"):
        load_contract(tmp_path / "missing.yml")
