# Source extraction and verification

## Frozen sources

Each input record contains an upstream path and immutable Git blob SHA-1. The public repository is `SWE-bench/experiments`.

## Schema adapters

Two source shapes were observed:

- **Legacy expanded:** contains an explicit `generated` list. Unique generated IDs are authoritative because the GPT-4 file has duplicate entries in `no_generation`.
- **Compact:** contains `no_generation`, `no_logs`, and `resolved`; generated count is `500 - unique(no_generation)`.

`src/agent_completion_ledger/extract.py` implements these rules and rejects overlapping or impossible status sets. `scripts/extract_source_counts.py` compares downloaded raw blobs with the frozen derived counts.

## Independent re-extraction

On a normal network:

```bash
python scripts/fetch_public_results.py
PYTHONPATH=src python scripts/extract_source_counts.py
```

The fetcher uses each Git blob SHA rather than a moving branch path. Full upstream files are not committed because the upstream experiments repository had no root `LICENSE` file when checked; this is a conservative redistribution decision, not a claim that the numerical facts are copyrighted.

## Known source anomaly

The legacy GPT-4 result file contains 30 raw `no_generation` entries but 472 unique generated predictions in a 500-slot benchmark, so only 28 no-claim slots are possible. The two-entry discrepancy is preserved in the published CSV instead of silently forcing agreement.
