#!/usr/bin/env python3
"""Fetch immutable Git blobs for independent source-count verification.

The pilot does not redistribute the full upstream files because the experiments
repository had no root LICENSE file when observed on 2026-07-24. This helper
lets reproducers fetch the exact public blobs directly from GitHub.
"""

from __future__ import annotations

import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPOSITORY = "SWE-bench/experiments"


def main() -> int:
    source = Path("data/frozen/submission-summaries.json")
    target = Path("data/raw-upstream")
    target.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = json.loads(source.read_text(encoding="utf-8"))
    for record in records:
        sha = record["source_blob_sha"]
        request = urllib.request.Request(
            f"https://api.github.com/repos/{REPOSITORY}/git/blobs/{sha}",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "agent-completion-ledger/0.1",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload: dict[str, Any] = json.load(response)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"fetch failed for {sha}: {exc}", file=sys.stderr)
            return 2
        content = base64.b64decode(payload["content"])
        destination = target / f"{record['submission']}.json"
        destination.write_bytes(content)
        print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
