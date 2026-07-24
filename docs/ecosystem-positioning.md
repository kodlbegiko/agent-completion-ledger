# Ecosystem positioning

## Product position

**Repository-level acceptance evidence contracts for coding-agent tasks.**

Agent Completion Ledger (ACL) evaluates a task-level completion claim against deterministic repository and CI evidence. It is intentionally narrower than agent tracing, operation audit, supply-chain provenance, identity, or compliance systems.

中文定位：**針對 AI 程式代理任務，以 Repository 與 CI 證據驗證完成宣稱的接受契約。**

## ACL is responsible for

- explicit task completion claims;
- repository evidence such as files, hashes, JSON values, Git state, tests, and builds;
- deterministic `SUPPORTED`, `FAILED`, `UNVERIFIABLE`, and `NO_CLAIM` statuses;
- CI integration and reviewer-facing reports;
- recording the contract digest, repository commit, assertion identifiers, tool version, and result digest.

## ACL is not responsible for

- complete agent tracing or chain-of-thought retention;
- general operation auditing or agent identity;
- legal or regulatory certification;
- build-artifact provenance by itself;
- a complete execution sandbox;
- deciding whether a product is valuable to users;
- proving that software is semantically correct or secure.

## Adjacent systems

| System | Primary unit | Primary purpose | Relation to ACL | Important non-equivalence |
|---|---|---|---|---|
| Agent Completion Ledger | Repository task claim | Acceptance evidence for a coding-agent task | Produces task status and evidence report | Not a runtime trace, identity system, or signed provenance system |
| Agent Evidence | Agent/service operation and evidence bundle | Portable, auditable operation evidence, validation, hashes, and offline verification | Some operation, policy, evidence, provenance, and validation fields can reference an ACL report | ACL does not capture a full operation event stream or signed evidence bundle |
| AAS-1 | Audit-grade agent action and engagement records | Independent assurance over agent activity using record classes and audit assertions | An ACL report may be referenced as one technical evidence item in a broader audit record | ACL does not establish agent identity, authority, signature, timestamp service, audit engagement, or auditor determination |
| OpenTelemetry GenAI semantic conventions | Runtime spans, events, metrics, and logs | Observable execution telemetry for GenAI systems | Trace/span identifiers can be carried as optional external references around an ACL verification run | Telemetry describes runtime activity; ACL evaluates repository acceptance evidence after or during that activity |
| GitHub Artifact Attestations | Artifact subject plus signed attestation bundle | Bind artifact digests to workflow identity and a predicate | GitHub can attest an ACL report artifact or its experimental predicate | ACL's unsigned JSON is not an attestation and GitHub attestation does not prove program correctness |
| SLSA / in-toto | Artifact provenance and attestations | Describe how artifacts were built and provide standard statement envelopes | ACL emits an experimental in-toto Statement-compatible result; SLSA provenance may separately cover built artifacts | ACL does not claim SLSA conformance and does not replace build provenance |
| Cortex Loop | Coding-agent policy/enforcement workflow | Enforce coding-agent process constraints and review gates | A Cortex-style gate could consume an ACL exit code or report | ACL is not a general agent orchestration or enforcement platform |
| Tests and ordinary CI | Repository command/result | Execute project-specific checks | ACL calls or references these checks and records how they support a task claim | A passing test alone does not identify the task claim, contract integrity, missing evidence, or review provenance |

## Interoperability posture

Mappings in `docs/interoperability/` are **experimental documentation mappings**. They are not official endorsements, certifications, or complete semantic conversions. Exporters should be added only where the source and destination semantics are explicit enough to avoid inventing meaning.

The in-toto output is the only machine-readable interoperability surface in this release. It describes the ACL result and limitations. Signing, identity binding, transparency logs, and artifact-attestation verification are delegated to established external systems.

## Sources reviewed

- OpenTelemetry GenAI semantic conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- AAS-1 public draft: <https://aas-1.org/>
- Agent Evidence package description: <https://pypi.org/project/agent-evidence/>
- GitHub Artifact Attestations: <https://docs.github.com/en/actions/concepts/security/artifact-attestations>
- in-toto Attestation Statement v1: <https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md>
- SLSA provenance: <https://slsa.dev/spec/v1.1/provenance>
- Cortex Loop: <https://cortexloop.org/>
