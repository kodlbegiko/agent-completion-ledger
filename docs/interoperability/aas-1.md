# AAS-1 mapping

Status: **experimental mapping to the public AAS-1 draft; not an audit opinion, conformance claim, or certification**.

## Scope difference

AAS-1 models audit-grade evidence about autonomous-agent activity, including action records, agent/principal references, policy references, hashes, signatures, timestamps, engagement context, and auditor determinations. ACL evaluates whether repository and CI evidence supports a coding-task completion claim.

## Candidate references

| ACL concept | Possible AAS-1 use | Limitation |
|---|---|---|
| Repository task claim | Action subject or evidence description | ACL task IDs are local identifiers, not AAS-1 event identities |
| Repository commit and contract digest | Evidence hash/reference | Does not establish who controlled the repository or contract |
| Assertion outcomes | Technical evidence supporting an auditor procedure | ACL assertions are not the AAS-1 assertion catalogue |
| Result digest | Integrity reference to the ACL report | Not a signature or independent timestamp |
| Tool version and execution mode | Tool/provenance metadata | Does not identify the coding agent, principal, or delegated authority |
| Overall ledger status | Input to a broader determination | Must not be relabeled as an AAS-1 Class D auditor finding |

## Missing AAS-1 semantics

ACL does not provide agent identity binding, principal authority, cryptographic signatures, independent timestamping, complete action populations, audit engagement scope, materiality, sampling, or auditor identity. It also does not establish that an action occurred merely because repository evidence exists.

## Recommended integration

Attach the complete ACL report or attested report artifact as one evidence reference in an AAS-1-oriented record. Preserve its native predicate type and limitations. An auditor or integrating system must separately evaluate identity, completeness, authority, accuracy, and the other applicable audit assertions.

## Information loss

Flattening AAS-1 records into ACL would discard agent identity, action chronology, engagement context, signatures, and auditor findings. Flattening ACL into an AAS-1 status would discard the four-state acceptance semantics and repository-specific assertion detail. Use references rather than a one-to-one conversion.
