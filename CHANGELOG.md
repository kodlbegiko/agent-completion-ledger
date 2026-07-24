# Changelog

## 0.2.0 — Unreleased

- Added Completion Evidence Contract schema v1 and 14 assertion types.
- Added four-state task verification with deterministic terminal, JSON, and Markdown reports.
- Added `init`, `validate-contract`, `verify`, `report`, `reproduce`, and `generalization` commands.
- Added repository-root path confinement, Windows-path rejection, symlink checks, executable allowlists, argv-only commands, and timeouts.
- Added canonical tracked-text hashing and explicit LF output so reproduction hashes remain stable across Windows, macOS, and Linux checkouts.
- Added a composite GitHub Action, cross-platform CI, wheel smoke tests, and deterministic fixture integration.
- Added measured Shipcheck and CSV Snapshot dogfood results with controlled success, failure, and unverifiable cases.
- Added third-party reproduction documentation and GitHub issue forms; external validation remains pending.
- Added a preregistered Multi-SWE-bench Go/MagentLess second-source study and machine-readable result.
- Increased the automated suite from 79 to 177 tests. Final CI coverage: 95.39% lines, 90.81% branches, 94.37% combined branch-aware coverage.

## 0.1.0 — 2026-07-24

- Added preregistered seven-submission SWE-agent/SWE-bench Verified pilot.
- Added evidence-state schema, deterministic CLI, CSV/JSON/JSONL outputs, sensitivity analysis, and source hashes.
- Added 21-candidate selection record, full research report, red-team review, CI, packaging, and tests.
- Initial verdict: `SUPPORTED` within the documented executable-oracle reporting scope.
