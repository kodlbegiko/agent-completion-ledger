import json
from pathlib import Path


def _candidates() -> list[dict[str, object]]:
    root = Path("data/design")
    index = json.loads((root / "candidates.json").read_text(encoding="utf-8"))
    candidates: list[dict[str, object]] = []
    for filename in index["files"]:
        candidates.extend(json.loads((root / filename).read_text(encoding="utf-8")))
    assert index["count"] == len(candidates)
    return candidates


def test_candidate_count_at_least_twenty() -> None:
    assert len(_candidates()) >= 20


def test_candidate_scores_match_components() -> None:
    data = _candidates()
    assert all(
        item["total_score"] == sum(item["scores"].values())  # type: ignore[union-attr]
        for item in data
    )


def test_selected_candidate_is_top_ranked() -> None:
    data = _candidates()
    assert data[0]["slug"] == "agent-completion-ledger"
    assert data[0]["total_score"] == max(item["total_score"] for item in data)


def test_every_candidate_has_required_fields() -> None:
    root = Path("data/design")
    index = json.loads((root / "candidates.json").read_text(encoding="utf-8"))
    required = set(index["required_fields"])
    assert all(required.issubset(item) for item in _candidates())


def test_manifest_exists() -> None:
    assert Path("research-manifest.yml").exists()


def test_required_repository_files_exist() -> None:
    required = {
        "README.md",
        "RESEARCH.md",
        "research-manifest.yml",
        "LICENSE",
        "CITATION.cff",
        "CHANGELOG.md",
        "SECURITY.md",
        "CONTRIBUTING.md",
        ".github/workflows/ci.yml",
    }
    assert all(Path(path).exists() for path in required)


def test_no_absolute_work_path_in_source() -> None:
    for path in Path("src").rglob("*.py"):
        assert "/mnt/data" not in path.read_text(encoding="utf-8")
