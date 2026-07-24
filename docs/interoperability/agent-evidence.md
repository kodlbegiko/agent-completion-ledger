# Agent Evidence mapping

Status: **experimental documentation mapping; no official integration or equivalence claim**.

## Scope difference

Agent Evidence describes portable evidence objects and bundles for agent/service operations, with operation, policy, provenance, evidence, validation, hashes, verification, and offline-review concepts. ACL is narrower: one or more coding-task completion claims evaluated against repository acceptance assertions.

## Candidate mapping

| ACL field | Agent Evidence-oriented field | Caveat |
|---|---|---|
| Task claim | Operation subject or operation description | ACL does not record the full operation lifecycle |
| Contract path/digest | Policy reference and integrity hash | The contract is acceptance policy, not every runtime policy |
| Repository commit | Subject/provenance reference | Commit identity does not prove runtime inputs were complete |
| Assertion results | Evidence and validation results | ACL assertion types are repository-specific |
| Tool version | Validator metadata | ACL does not identify all runtime actors or frameworks |
| Result digest | Evidence object hash/reference | Digest alone is not a signed manifest or detached anchor |
| Attested report | External evidence bundle member | Signing and bundle verification remain external to ACL |

## Missing semantics

ACL does not maintain an append-only operation event store, hash chain, framework callbacks, actor identity, signed manifest, detached anchor, or offline bundle format. Agent Evidence does not automatically supply ACL's explicit four-state acceptance decision for a coding-task contract.

## Recommended integration

An Agent Evidence exporter may include an ACL JSON report or in-toto statement as a referenced evidence artifact, recording its SHA-256 and predicate type. The Agent Evidence validator should not reinterpret `SUPPORTED` as proof that the entire operation was correct, authorized, or complete.

## Information loss

Converting an operation bundle into ACL loses runtime sequence and actor context. Converting ACL into a generic operation record can obscure blocking/nonblocking assertion semantics and `UNVERIFIABLE`. Keep the native ACL artifact and link it by digest.
