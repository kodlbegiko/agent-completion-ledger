# External validation operations status

Status date: **2026-07-25 UTC**

Decision:

```text
READY FOR OWNER OUTREACH
```

The v0.3.1 security and packaging patch is released and verified. Wave 1 targets, exact messages, dispatch order, logging fields, consent handling, and follow-up rules are prepared. No external message has been sent.

## Qualifying counts

```text
Real participants: 0
Non-author repositories: 0
Real external tasks: 0
Independent reproductions: 0
Independent security reviewers: 0
Targeted outreach sent: 0
Responses: 0
```

Only a verified `NON-AUTHOR HUMAN` may increment an external count. Author comments, CI, release jobs, model reviews, automated replies, synthetic data, and author-owned dogfood do not count.

## Release and distribution gate

- Core verifier: `FEATURE FREEZE`.
- v0.3.0: immutable and affected by the documented mixed-case remote-URL rejection defect.
- v0.3.1: verified security and packaging patch.
- Release/tag commit: `703d63d6fb9a4329327634d5ae6e21030e13075e`.
- Release: `v0.3.1 — Security and Packaging Patch`; not draft; not prerelease.
- Assets: wheel, sdist, and `SHA256SUMS` present.
- Exact checksum-entry and SHA-256 validation: passed.
- Released-wheel clean-environment smoke test: passed.
- Runtime and package metadata: `0.3.1`.
- Human evidence: `docs/v0.3.1-release-verification.md`.
- Machine evidence: `docs/v0.3.1-release-verification.json`.
- PyPI: not published.

The verified GitHub tag and assets are sufficient for Wave 1. PyPI is optional adoption-friction reduction, not a recruitment prerequisite.

## Security boundary

v0.3.1 rejects lower-, upper-, and mixed-case HTTP/HTTPS command arguments before an allow-listed executable receives them. This correction does not make ACL a sandbox.

Remaining material risks include:

- allow-listed interpreters, tests, build systems, plugins, imports, lifecycle hooks, dependencies, and repository code execute with runner permissions;
- timeouts are not CPU, memory, process-tree, network, syscall, or filesystem isolation;
- reports can reveal repository identity, paths, task/assertion IDs, and messages;
- a valid in-toto envelope or signed artifact does not prove correctness or safe execution;
- independent security reviewer count remains zero.

The security review package and benign cases now target v0.3.1.

## Wave 1 readiness

Prepared and not sent:

- current-status re-audit of the original 30 candidates;
- five maintainer-pilot targets;
- two independent-reproduction targets;
- two independent-security-review targets;
- nine personalized ready-to-send messages;
- Day 1/3/5 dispatch order;
- Day 10-or-later single-follow-up rule;
- expanded manual outreach log;
- consent, pseudonymization, privacy, and analysis handling.

Normative launch files:

- `docs/outreach/WAVE-1-TARGETS.md`;
- `docs/outreach/WAVE-1-READY-TO-SEND.md`;
- `docs/OWNER-EXTERNAL-VALIDATION-ACTIONS.md`;
- `research/external-validation/outreach-log.csv`.

No issue, PR, email, social post, maintainer tag, or follow-up was sent by repository automation or by this preparation work.

## Author-owned prospective dogfood

```text
AUTHOR-OWNED PROSPECTIVE DOGFOOD
```

The prior operations task recorded 12 assertions, 74 non-comment contract lines, a final verification runtime of 0.174295465 seconds, and `SUPPORTED`. It did not change the merge decision or discover the mixed-case URL defect. Contract authoring time was not reliably timed and remains `null`. It provides no external-validation credit.

## Fixed external study

The research question, H1/H0/H2, task pack, counterbalancing, exclusions, consent, effect thresholds, and participant-balanced primary analysis remain unchanged.

### H1

No result. There are no eligible human rows.

### H0

No result. Zero recruitment outcomes are not evidence that all effect thresholds fail.

### H2

No result. There are no human outcomes from which to separate ACL-format effects from specification quality, added tests/build commands, domain knowledge, ordering, or learning.

### Protocol deviations

- Human-study deviations: none; enrollment has not begun.
- Wave 1 target selection and outreach operations are pre-recruitment preparation.
- The v0.3.1 security/reproduction documentation correction does not alter hypotheses, thresholds, tasks, exclusions, or analysis.
- Synthetic dry-run data remain pipeline plumbing only.

## GO-gate status

| Requirement | Current evidence |
|---|---|
| 5 non-author participants | 0 — not met |
| 3 non-author repositories | 0 — not met |
| 10 real/fixed coding tasks | 0 external completions — not met |
| At least one H1 threshold | no result |
| One changed reviewer decision | not demonstrated |
| One missing blocking evidence found | not demonstrated |
| Median contract authoring time <=30 min | no external measurements |
| One external maintainer willing to retain contract | 0 |
| No unresolved high-risk security issue | no known unresolved issue; independent review still absent |

`EXTERNAL VALUE SUPPORTED`, `PIVOT REQUIRED`, and `RESEARCH COMPLETE — MAINTENANCE MODE` cannot be selected from current outcome evidence.

## Stop rule

After 30 compliant targeted contacts with no non-author participation, or when the other preregistered STOP conditions are met, stop feature expansion and evaluate:

```text
RESEARCH COMPLETE — MAINTENANCE MODE
```

Do not change thresholds or add features to avoid a negative result.

## Honest impact statement

### Actually achieved

- verified v0.3.1 security/packaging release and low-friction GitHub-tag installation path;
- fixed research protocol, measurement templates, consent, and analysis pipeline;
- manual Wave 1 launch package with no automated outreach;
- bounded independent-reproduction and security-review instructions.

### Reasonable potential

ACL may help maintainers notice missing test/build/file evidence or distinguish insufficient evidence from failed implementation.

### Not demonstrated

- reviewer time savings;
- false-acceptance or false-rejection improvement;
- changed real review decisions;
- willingness to maintain contracts;
- independent security adequacy;
- adoption, public benefit, or broad social impact.

Until a real non-author human consents and enrolls, the operational decision remains:

```text
READY FOR OWNER OUTREACH
```

## Historical contract compatibility record

The immutable prospective-dogfood contract remains unchanged. The following literals are retained only so the historical 12-assertion, 74-non-comment-line record can still be verified against the repository. They are not the current launch decision or current count labels.

```text
READY FOR RECRUITMENT
```

- Real participant count: **0**
- Non-author repository count: **0**

Current operational status remains `READY FOR OWNER OUTREACH`, and the current qualifying counts remain those recorded above.
