# Data card

## Source

Seven `results/results.json` files from the public `SWE-bench/experiments` repository, each pinned by Git blob SHA in `data/frozen/submission-summaries.json`.

## Unit of analysis

A generated benchmark prediction/patch. Aggregate count records are committed; the upstream files can be independently fetched with `scripts/fetch_public_results.py` on a normal network.

## Extraction

For compact result files, generated = 500 − count(`no_generation`). For legacy expanded files, the explicit `generated` list is authoritative. Resolved and no-log counts come directly from named lists. The GPT-4 legacy file contains 30 raw no-generation entries but only 28 benchmark slots not generated; the two-entry discrepancy is preserved as an error-analysis field.

## Licensing and privacy

No root LICENSE file was found in the upstream experiments repository during this study. To avoid implying redistribution rights, only derived numerical facts, paths, hashes, and minimal instance identifiers are committed. No personal information or private model traces are included.

## Bias

The sample is purposive, restricted to SWE-agent lineage and SWE-bench Verified. It is not a random sample of coding agents or real development sessions.
