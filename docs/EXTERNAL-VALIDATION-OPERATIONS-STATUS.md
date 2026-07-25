# External validation operations status

Status date: **2026-07-25 UTC**

Decision:

```text
EXTERNAL VALIDATION IN PROGRESS
```

The v0.3.1 security and packaging patch remains released and verified. The owner manually sent the first compliant Wave 1 invitation through the approved public channel. No response, consent, enrollment, completed task, reproduction, or security review is claimed from that send.

## Current qualifying counts

```text
Real participants: 0
Non-author repositories: 0
Real external tasks: 0
Independent reproductions: 0
Independent security reviewers: 0
Targeted outreach sent: 1
Responses: 0
```

Only a verified `NON-AUTHOR HUMAN` may increment a participant or external-evidence count. An invitation, owner comment, CI result, model review, bot response, synthetic row, or author-owned dogfood task does not count.

## First public outreach record

```text
Wave ID: W1-M1
Target: tmux-python/tmuxp
Role: MAINTAINER_PILOT
Channel: GitHub Discussions / General
State: SENT — AWAITING RESPONSE
Public URL: https://github.com/tmux-python/tmuxp/discussions/1078
```

The owner manually posted the approved invitation and supplied the public URL. The connected GitHub actions do not expose Discussion creation metadata, so the outreach log records the owner-confirmation time and states that limitation explicitly.

The remaining eight Wave 1 messages are still `NOT_SENT` and each requires its own same-day policy check and owner approval. No cross-channel duplicate contact or follow-up has been sent.

## Release and feature-freeze gate

- Core verifier: `FEATURE FREEZE`.
- v0.3.0 remains immutable and documented as affected by the mixed-case remote-URL rejection defect.
- v0.3.1 is the verified security and packaging patch.
- Release/tag commit: `703d63d6fb9a4329327634d5ae6e21030e13075e`.
- Release assets include wheel, sdist, and `SHA256SUMS`.
- Exact checksum validation and released-wheel smoke verification passed.
- Runtime and package metadata remain `0.3.1`.
- PyPI remains unpublished and is not a Wave 1 prerequisite.
- No v0.4.0 development is authorized before the external-value gate is met.

## Security boundary

v0.3.1 rejects lower-, upper-, and mixed-case HTTP/HTTPS command arguments before an allow-listed executable receives them. This correction does not make ACL a sandbox.

Remaining material risks include:

- allow-listed interpreters, tests, build systems, plugins, imports, lifecycle hooks, dependencies, and repository code execute with runner permissions;
- timeouts are not CPU, memory, process-tree, network, syscall, or filesystem isolation;
- reports can reveal repository identity, paths, task/assertion IDs, and messages;
- a valid in-toto envelope or signed artifact does not prove correctness or safe execution;
- independent security reviewer count remains zero.

## Fixed external study

The preregistered research question, H1/H0/H2, task pack, counterbalancing, exclusions, consent requirements, effect thresholds, and participant-balanced primary analysis remain unchanged.

### H1

No result. There are no eligible human outcome rows.

### H0

No result. One sent invitation and zero responses do not demonstrate that all effect thresholds fail.

### H2

No result. There are no human outcomes from which to separate ACL-format effects from specification quality, added tests/build commands, domain knowledge, ordering, or learning.

### Protocol deviations

- Human-study deviations: none; no participant has consented or enrolled.
- The first message was manually sent by the owner after a same-day target and channel check.
- Recording a sent invitation changes operational status, not external-value evidence.
- Synthetic dry-run data remain analysis-pipeline plumbing only.

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

## Follow-up and stop rules

- W1-M1 remains `SENT — AWAITING RESPONSE`.
- Do not treat silence, a reaction, a star, a bot acknowledgment, or ordinary repository activity as participation.
- At most one follow-up is permitted, only on or after the existing Day 10 rule and only if the target policy still allows it.
- A decline, removal, lock, or request to stop permanently ends contact.
- After 30 compliant targeted contacts with no non-author participation, or when another preregistered STOP condition is met, stop expansion and evaluate:

```text
RESEARCH COMPLETE — MAINTENANCE MODE
```

Do not change thresholds or add features to avoid a negative result.

## Honest impact statement

### Actually achieved

- verified v0.3.1 security and packaging release;
- fixed research protocol, measurement templates, consent, and analysis pipeline;
- one compliant owner-sent public Wave 1 invitation with an auditable link;
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

## Historical contract compatibility record

The immutable prospective-dogfood contract remains unchanged. The following literals are retained only so the historical 12-assertion, 74-non-comment-line record can still be verified. They are not the current operational decision or current count labels.

```text
READY FOR RECRUITMENT
```

- Real participant count: **0**
- Non-author repository count: **0**

Current operational decision is `EXTERNAL VALIDATION IN PROGRESS`; current qualifying counts are the values recorded at the top of this document.
