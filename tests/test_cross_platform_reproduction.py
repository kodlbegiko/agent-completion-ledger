from pathlib import Path

from agent_completion_ledger.io import sha256_normalized_text_file


def test_normalized_text_hash_matches_lf_and_crlf(tmp_path: Path) -> None:
    lf = tmp_path / "lf.json"
    crlf = tmp_path / "crlf.json"
    lf.write_bytes(b'{\n  "value": 1\n}\n')
    crlf.write_bytes(b'{\r\n  "value": 1\r\n}\r\n')
    assert sha256_normalized_text_file(lf) == sha256_normalized_text_file(crlf)


def test_write_text_explicit_lf_is_byte_stable(tmp_path: Path) -> None:
    path = tmp_path / "output.json"
    path.write_text('{\n  "value": 1\n}\n', encoding="utf-8", newline="\n")
    assert b"\r\n" not in path.read_bytes()
