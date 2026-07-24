# Experimental in-toto completion evidence predicate

## Command

```bash
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$CONTRACT_SHA256" \
  --format in-toto \
  --output completion-evidence.intoto.json
```

The output uses the in-toto Statement v1 envelope:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [],
  "predicateType": "https://github.com/kodlbegiko/agent-completion-ledger/predicate/completion-evidence/v1",
  "predicate": {}
}
```

The predicate schema is `schemas/completion-evidence-predicate.schema.json`.

## Predicate semantics

The predicate records:

- task claims and their four-state ledger results;
- the exact contract SHA-256 and optional trusted digest pin;
- repository identity and checked-out commit;
- assertion identifiers, types, blocking status, and outcomes;
- the deterministic evidence-report digest;
- tool version and execution mode;
- explicit scope and limitations.

The `evidenceReportDigest` is the SHA-256 of the canonical report payload before the digest field is inserted. It makes accidental or deliberate report mutation detectable when the original trusted digest is retained. It is not a signature.

## Subject choice

The statement subject identifies the repository/commit evaluated by ACL. A downstream attestation system may instead attest the generated report file as the artifact subject and use this ACL predicate as the custom predicate. That approach binds the signed attestation to the exact report bytes.

## Security boundary

An unsigned Statement is structured JSON only. It does **not** establish:

- who ran the verifier;
- whether the runner was trusted;
- whether the repository was safe;
- whether the code is semantically correct;
- whether the project complies with law or policy;
- whether the statement was modified after generation.

Use an established signing or artifact-attestation system when issuer identity and tamper-evident distribution are required. ACL deliberately does not implement Sigstore, key management, transparency logs, or signature verification.

## Compatibility status

This predicate is experimental and versioned. It uses the in-toto Statement envelope but is not an in-toto, SLSA, GitHub, or standards-body certification. Consumers must match the exact `predicateType` and validate the predicate schema before relying on fields.
