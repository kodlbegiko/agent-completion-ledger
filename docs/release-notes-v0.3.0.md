# v0.3.0 — Trusted acceptance evidence and external validation readiness

Agent Completion Ledger v0.3.0 narrows the product to **repository-level acceptance evidence contracts for coding-agent tasks** and hardens the boundary between trusted policy, untrusted repository changes, structured evidence, and external attestation.

## Added

- Exact contract SHA-256 pinning before parsing with integrity-only `UNVERIFIABLE` mismatch reports.
- Provenance-rich deterministic report schema v2.
- `--no-exec` static-only verification.
- Experimental in-toto Statement v1 output with a versioned custom predicate schema.
- Composite Action inputs for trusted digest pinning and static mode.
- GitHub Artifact Attestation integration and verification example.
- Experimental semantic mappings for OpenTelemetry GenAI, AAS-1, Agent Evidence, GitHub attestations, SLSA/in-toto, Cortex Loop, and ordinary CI.
- Read-only safe PR workflow fixtures using trusted base-branch contracts.
- Minimal, Node.js, and Python adoption examples.
- Fifteen-minute quickstart, maintainer pilot, preregistered ten-task external validation study, consent/privacy notice, collection template, analysis script, and synthetic plumbing dry run.

## Security boundary

Trusted Contract Mode checks contract bytes; it is not a sandbox. Allow-listed interpreters can still execute malicious repository code. Static-only mode disables command assertions and returns `UNVERIFIABLE` when command evidence is required. Reports omit command stdout/stderr but can reveal task IDs, paths, repository identity, and assertion messages.

The in-toto statement is unsigned structured evidence unless an external system signs it. A signature or GitHub Artifact Attestation does not prove code security, semantic correctness, contract completeness, regulatory compliance, or product value.

## Packaging

GitHub Releases provide source archives. CI builds and smoke-tests wheel and sdist packages, but v0.3.0 is not published on PyPI. Install from the GitHub tag or repository source.

## Validation status

Cross-platform tests, branch coverage, strict typing, build, wheel smoke, deterministic output, schema checks, safe workflow fixtures, composite action integration, reproduction, generalization, and existing dogfood must pass before release.

## External status

- Real external participants: **0**.
- Non-author repository integrations: **0**.
- Independent adoption, review-time improvement, changed real reviewer decisions, and realized impact: **EXTERNAL VALIDATION PENDING**.

The release prepares independent evaluation; it does not claim that evaluation has succeeded.
