# Feature freeze and version policy

Effective date: **2026-07-25 UTC**

Status:

```text
FEATURE FREEZE
```

Agent Completion Ledger v0.3.x is engineering-complete within its documented scope. The current verified security and packaging patch is v0.3.1. Until external value is supported, work must prioritize distribution, reproduction, independent security review, recruitment, real measurements, and maintenance.

## Core verifier changes allowed only for

- a security vulnerability;
- a reproducible reproduction failure;
- a packaging failure;
- a cross-platform regression;
- a blocking usability problem observed in an external pilot;
- an explicit external requirement supported by reproducible evidence.

Every exception must link the triggering evidence, identify affected versions, include a regression test when applicable, and state whether the external protocol or participant materials are affected.

## v0.3.x patch scope

Permitted patch work is limited to:

- packaging metadata;
- PyPI Trusted Publishing preparation or publication;
- wheel, sdist, checksum, or GitHub Release asset fixes;
- security fixes;
- reproduction fixes;
- external-pilot blocking usability fixes;
- documentation and metadata corrections.

v0.3.1 used this exception only for the mixed-case remote-URL validation correction and packaging/distribution work. Its release does not authorize unrelated feature expansion.

## Prohibited before external value is supported

- v0.4.0;
- dashboards or SaaS;
- new assertion types without external evidence;
- additional framework adapters without external evidence;
- repeated benchmark variants presented as new impact evidence;
- synthetic or model-generated participants;
- feature work performed only to create activity.

## Release gate for v0.4.0

A v0.4.0 branch, tag, release note, or package version must not be created until the project records `EXTERNAL VALUE SUPPORTED` using the preregistered decision rule.

At minimum that requires five non-author participants, three non-author repositories, ten real tasks, at least one H1 threshold, a changed review decision, a newly identified blocking-evidence omission, median contract authoring time no greater than 30 minutes, one external maintainer willing to retain the contract, and no unresolved high-risk security finding.
