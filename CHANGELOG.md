# Changelog

## 0.3.1 — 2026-07-25

- Fixed remote URL argument rejection so mixed-case `HTTP://` and `HTTPS://` schemes are rejected before an allow-listed executable receives them.
- Added parameterized lower- and uppercase regression tests plus an end-to-end benign reproduction case for the affected trust boundary.
- Preserved the v0.3.0 tag as immutable and documented that v0.3.0 remains affected; external executable-mode integration should use v0.3.1 or later and still treat ACL as not being a sandbox.
- Added owner-dispatched, immutable-tag PyPI Trusted Publishing preparation using OIDC, protected environments, TestPyPI-first approval, and no long-lived registry token.
- Added reproducible wheel and sdist build validation, `twine check`, clean wheel installation smoke testing, SHA-256 checksums, and GitHub Release artifact upload preparation.
- Expanded package metadata with project URLs, keywords, supported Python classifiers, audience, license, operating-system, and quality-assurance classifiers.
- Added external-validation recruitment, distribution, independent-security-review, and prospective-dogfood operations without changing the preregistered research question or claiming external value.
- Kept the project under `FEATURE FREEZE`; no new assertion type, framework adapter, dashboard, SaaS feature, or v0.4.0 work was added.

## 0.3.0 — 2026-07-24

- Narrowed the product position to repository-level acceptance evidence contracts for coding-agent tasks.
- Added trusted contract SHA-256 pinning before contract parsing; mismatches produce integrity-only `UNVERIFIABLE` reports and exit code 2.
- Added deterministic report provenance: tool version, repository identity/commit, contract path/digest, task and assertion identifiers, execution mode, schema version, and result digest.
- Added `--no-exec` static-only mode; blocking command evidence becomes `UNVERIFIABLE` and is never treated as passed.
- Added experimental in-toto Statement v1 output and a versioned completion evidence predicate schema.
- Added a GitHub Artifact Attestation integration example without reimplementing signing or claiming correctness certification.
- Added explicit interoperability mappings for OpenTelemetry GenAI, AAS-1, Agent Evidence, GitHub Artifact Attestations, SLSA/in-toto, Cortex Loop, and ordinary CI.
- Added safe pull-request workflow examples using read-only permissions, base-branch contracts, no secrets, and no `pull_request_target` execution.
- Added minimal, Node.js, and Python adoption examples plus a 15-minute maintainer quickstart and removal instructions.
- Preregistered a ten-task, three-family external reviewability study with consent/privacy materials, collection template, analysis script, and clearly labeled synthetic plumbing dry run.
- Added v0.3.0 red-team analysis and expanded security documentation around interpreter risk, report confidentiality, and non-goals.
- External validation remains pending; real participant and non-author integration counts remain zero at release preparation.

## 0.2.0 — 2026-07-24

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
