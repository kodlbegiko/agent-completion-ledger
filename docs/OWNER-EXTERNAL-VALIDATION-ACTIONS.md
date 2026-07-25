# Owner actions: external validation mission

Status: **OWNER REVIEW REQUIRED**

No external message has been sent. No participant, integration, reproduction, or independent security review is counted until a non-author supplies qualifying evidence.

## 1. Review and merge the operations PR

Confirm that the PR:

- changes no core verifier behavior;
- creates no v0.4.0 material;
- leaves the fixed research question, H1/H0/H2 thresholds, exclusions, and participant-balanced analysis unchanged;
- labels all author-owned dogfood separately;
- contains no private email addresses or automated outreach action;
- passes the normal CI, workflow-lint, security-case, and prospective-dogfood jobs.

## 2. Complete distribution setup

Follow `docs/OWNER-PYPI-PUBLISH-ACTIONS.md`.

Owner-only steps include:

- enabling PyPI/TestPyPI account security;
- creating protected `testpypi`, `pypi`, and `release-artifacts` environments;
- registering pending Trusted Publishers;
- preparing packaging-only v0.3.1 metadata/version changes;
- approving TestPyPI, production PyPI, and GitHub Release artifact deployments;
- independently smoke-testing `pip install agent-completion-ledger==0.3.1` before changing README installation guidance.

Do not claim PyPI publication or use the short installation command until verified.

## 3. Approve outreach one target at a time

For each candidate selected from `recruitment-targets.csv`:

1. re-check that the repository is active and public;
2. read its contribution guide, issue templates, code of conduct, and support policy;
3. confirm the public channel permits a research/pilot request;
4. verify the message is individualized and the task can be completed without secrets/private code;
5. search `outreach-log.csv` to ensure there was no prior contact;
6. approve the exact message and channel;
7. send manually;
8. immediately record attempt number, target, date, channel, and response state.

Do not batch-send, tag maintainers, scrape email, or create external issues/PRs automatically.

## 4. Recruitment order

Recommended initial order:

1. invite two HIGH FIT maintainers to inspect the reproduction-only path;
2. invite two different HIGH FIT maintainers to inspect the fixed ten-task review study;
3. invite one HIGH FIT maintainer to consider one real repository integration;
4. separately invite at least one security reviewer.

Do not contact the same maintainer through multiple channels. A decline ends contact. A non-response is not consent.

## 5. Participant enrollment

Before a session:

- confirm inclusion criteria and consent;
- assign a pseudonymous ID;
- keep identity/contact data separate from responses;
- freeze and record protocol/task/data hashes;
- assign counterbalance schedule and random seed;
- explain `ACCEPT`, `REJECT`, and `INSUFFICIENT_EVIDENCE`;
- disclose expected duration and withdrawal rights;
- confirm no private code, secrets, confidential employer data, or sensitive personal information will be submitted.

## 6. Real repository integration

For every non-author integration:

- ensure the contract is written before reviewing the agent completion claim;
- record all fields in `adoption-integration-template.csv`;
- measure installation, authoring, CI baseline, and CI-with-ACL time rather than estimating;
- preserve the original agent summary and pre-ledger decision;
- obtain fixed ground truth from the maintainer or an agreed test/review oracle;
- record all author assistance and subjective conditions;
- do not merge a change solely because ACL reports `SUPPORTED`.

## 7. Independent reproduction

A qualifying reproduction must identify version/commit, environment, command, expected/observed result, and public evidence or a reviewable report. Record it under Issue #4 only after confirming the reproducer is not a project author.

## 8. Independent security review

Send only the reviewed draft in `docs/outreach/security-review-request.md`. Direct reviewers to `docs/INDEPENDENT-SECURITY-REVIEW.md` and private security reporting for high-risk findings.

If a credible high-risk issue appears:

- pause outreach for the affected surface;
- do not publish exploit details;
- use the feature-freeze security exception;
- add a regression test and patch release;
- update the security review issue only after safe disclosure.

## 9. Analysis gate

Do not run confirmatory human analysis until at least five eligible participants complete the fixed study. Before analysis:

- validate consent and data schema;
- remove template, synthetic, author-owned, model-only, duplicate, and excluded rows;
- document missing data and deviations;
- use participant-balanced summaries as primary;
- keep pooled row-level metrics as sensitivity only;
- report all favorable and unfavorable thresholds;
- keep exploratory integration findings separate.

## 10. Decision gate

Select `EXTERNAL VALUE SUPPORTED` only when every GO condition is met. Select `PIVOT REQUIRED` only from concrete external evidence. Evaluate `RESEARCH COMPLETE — MAINTENANCE MODE` after a STOP rule, including 30 targeted attempts without participation.

Until then, the public operational status remains:

```text
READY FOR RECRUITMENT
```
