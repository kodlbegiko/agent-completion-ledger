# External validation operations status

Status date: **2026-07-25 UTC**

Decision:

```text
READY FOR RECRUITMENT
```

The v0.3.1 security and packaging patch is released and verified. The specific mixed-case remote-URL defect that blocked executable-mode external pilots in v0.3.0 is corrected in v0.3.1. This does not make ACL a sandbox; executable pilots still require disposable, least-privilege runners and no secrets.

## Counts

- Real participant count: **0**
- Non-author repository count: **0**
- Real external task count: **0**
- Independent reproduction count: **0**
- Independent security reviewer count: **0**
- Completed targeted outreach count: **0**
- Author-owned prospective dogfood tasks completed under this mission: **1**

## Engineering and distribution

- Core verifier: `FEATURE FREEZE`.
- v0.3.0: immutable and affected by case-sensitive mixed-case remote-URL rejection.
- v0.3.1: **VERIFIED security and packaging patch**.
- Release commit and tag target: `703d63d6fb9a4329327634d5ae6e21030e13075e`.
- Release name: `v0.3.1 — Security and Packaging Patch`.
- Release publication time: `2026-07-25T04:35:26Z`.
- Release status: not draft; not prerelease.
- Required assets: wheel, sdist, and `SHA256SUMS` present.
- Checksum verification: passed.
- Released-wheel clean-environment smoke test: passed.
- Release verification workflow: run `30144411275`.
- Machine-readable verification: `docs/v0.3.1-release-verification.json`.
- Human-readable verification: `docs/v0.3.1-release-verification.md`.
- PyPI: **not published**.
- PyPI Trusted Publishing workflow: prepared; owner-side TestPyPI/PyPI environments and pending publishers remain required.
- Primary installation remains the verified Git tag until production PyPI installation is separately verified.

## Security correction

v0.3.0 checked `http://` and `https://` command arguments case-sensitively. Mixed-case schemes such as `HTTPS://` could therefore reach an allow-listed executable.

v0.3.1 normalizes command arguments before the prefix comparison and includes lower- and uppercase regression cases. The release package, version metadata, checksums, and wheel installation were verified after publication.

Remaining material risk:

- ACL is not a sandbox.
- Allow-listed interpreters, tests, build systems, plugins, lifecycle hooks, dependencies, and repository code execute with runner permissions.
- Timeouts are not resource isolation.
- Independent security reviewer count remains zero.

## Recruitment readiness

Prepared but not sent:

- 30-candidate public recruitment matrix;
- 10 HIGH FIT individualized drafts;
- general maintainer invitation;
- independent reproduction request;
- independent security review request;
- consent/privacy and preregistered study materials.

No issue, pull request, email, social post, or maintainer tag was sent to an external target during preparation.

Owner-approved recruitment may now include:

- independent reproduction;
- fixed report-review sessions;
- `--no-exec` static workflows;
- bounded executable-mode v0.3.1 pilots on disposable, least-privilege runners without secrets;
- independent security review.

The existence of a verified patch release is not evidence that external maintainers obtain value from ACL.

## Author-owned prospective dogfood

Record class:

```text
AUTHOR-OWNED PROSPECTIVE DOGFOOD
```

Task: prepare and verify the external-validation operations package in `kodlbegiko/agent-completion-ledger`.

- Contract committed before implementation completion: yes.
- Contract assertions: 12.
- Non-comment contract lines: 74.
- Final PR verification runtime: 0.174295465 seconds on GitHub Actions.
- Ledger result: `SUPPORTED`.
- Security reproduction cases in the same final run: 10 passed, 0 failed.
- Decision before ledger: `INSUFFICIENT_EVIDENCE` because the files did not yet exist.
- Decision after ledger: eligible for human review; merge decision remained human.
- Reviewer/merge decision changed by ledger: no.
- Missing blocking evidence found by this dogfood task: no.
- Contract authoring time: not reliably timed and therefore left `null`.
- External validation credit: none.

The mixed-case URL defect was found through repository review, not by the prospective completion contract.

## External study

The fixed research question, H1, H0, H2, thresholds, task pack, counterbalancing, exclusions, and participant-balanced primary analysis remain unchanged.

### H1

No result. There are no real participants or external task rows.

### H0

No result. Absence of participants is not evidence that all effect thresholds fail.

### H2

No result. There are no human outcomes from which to distinguish ACL-format effects from specification quality, tests/build commands, domain knowledge, case order, or learning effects.

### Protocol deviations

- Human-study deviations: **none**, because recruitment has not begun.
- Pre-recruitment operational additions did not change the preregistration.
- The security correction was permitted by the documented feature-freeze exception.
- Synthetic dry-run data remain analysis plumbing only and are excluded from human evidence.

## Security review

- Independent reviewers: **0**.
- Independent public findings: none.
- Private findings: unavailable to check through the connected interface.
- Repository review finding: one mixed-case URL-scheme validation defect in v0.3.0.
- Fix status: corrected, regression-tested, released, and package-verified in v0.3.1.
- Independent security adequacy: **not demonstrated**.

## Decision-gate status

| GO requirement | Current evidence |
|---|---|
| 5 non-author participants | 0 — not met |
| 3 non-author repositories | 0 — not met |
| 10 real tasks | 0 — not met |
| At least one H1 threshold | no human result |
| One changed reviewer decision | not demonstrated externally |
| One missing blocking evidence found | not demonstrated externally |
| Median contract authoring time <=30 minutes | no external measurements |
| One maintainer willing to retain contract | 0 |
| No unresolved high-risk security issue | known v0.3.0 defect patched in v0.3.1; independent review still pending |

`EXTERNAL VALUE SUPPORTED`, `PIVOT REQUIRED`, and `RESEARCH COMPLETE — MAINTENANCE MODE` cannot yet be selected from outcome evidence.

## Stop rule

Stop feature expansion and evaluate maintenance mode when any preregistered STOP condition is met, including 30 targeted recruitment attempts with no non-author participation, median external contract authoring time above 30 minutes, no measurable review improvement, no willingness to maintain contracts, predominantly subjective tasks, ordinary CI providing equivalent value, unresolved execution risk, or complete coverage by mature alternatives.

## Honest impact statement

### Already achieved

- Published and verified v0.3.1 security and packaging patch.
- Explicit completion-claim/evidence boundary.
- Trusted contract byte pinning, static-only review, provenance-rich reports, and bounded interoperability documentation.
- Wheel, sdist, and SHA-256 release assets with passed checksum and clean-install smoke verification.
- Auditable recruitment, distribution, and security-review preparation without contacting external maintainers.

### Reasonable potential

ACL may help maintainers notice missing test/build/file evidence or distinguish insufficient evidence from a failed implementation.

### Not demonstrated

- reviewer time savings;
- lower false acceptance or false rejection;
- changed real merge decisions;
- external maintenance willingness;
- independent security adequacy;
- adoption, public benefit, or broad social impact.

### Evidence still required

At least five non-author participants, three non-author repositories, ten real tasks, participant-balanced outcomes, contract/setup cost measurements, at least one changed decision and one newly identified blocking-evidence omission, maintenance willingness, and independent security review.
