# GitHub Artifact Attestations mapping

Status: **supported integration example using GitHub's maintained action; ACL is not itself an attestation service**.

## Roles

- ACL evaluates a repository acceptance contract and emits a deterministic report or experimental in-toto statement.
- GitHub Artifact Attestations can bind an artifact digest and custom predicate to a GitHub Actions workflow identity using GitHub's attestation infrastructure.
- GitHub CLI verifies the attestation against the expected repository owner/workflow identity and predicate type.

## Mapping

| ACL concept | GitHub attestation concept | Notes |
|---|---|---|
| `completion-report.json` | Attestation subject artifact | This binds the exact report bytes |
| ACL custom predicate | Custom attestation predicate | Use the versioned ACL predicate type |
| Contract digest | Predicate field | A trusted pin is meaningful only when the workflow obtains the expected digest from a trusted source |
| Repository commit | Predicate field and workflow source context | Compare both rather than assuming they are identical |
| Result digest | Predicate integrity field | The attestation subject digest remains authoritative for report-file bytes |
| Tool version/execution mode | Predicate metadata | Does not prove the tool source was reviewed unless the action/tool is immutably pinned |

## Unsupported interpretations

A valid GitHub attestation does not establish software safety, semantic correctness, contract completeness, reviewer agreement, or regulatory compliance. It establishes a signed relationship between subject/predicate data and the workflow identity represented by the attestation.

## Safe use

- Generate attestations on trusted branches, not untrusted fork pull requests.
- Grant only `contents: read`, `id-token: write`, and `attestations: write` when required.
- Pin the ACL action and other third-party actions to reviewed immutable commits for high-assurance use.
- Keep secrets out of the contract and report.
- Verify the exact downloaded report bytes and expected custom predicate type.

See `docs/attestation-integration.md` for the end-to-end example.
