# External validation operations status

Status date: **2026-07-25 UTC**

Decision:

```text
READY FOR RECRUITMENT
```

Restriction: until a v0.3.1 patch containing the mixed-case remote-URL rejection fix is released and verified, owner-approved recruitment may use reproduction, report review, fixed-study materials, and `--no-exec` static workflows only. Do not ask an external repository to run v0.3.0 command assertions as a trusted execution boundary.

## Counts

- Real participant count: **0**
- Non-author repository count: **0**
- Real external task count: **0**
- Independent reproduction count: **0**
- Independent security reviewer count: **0**
- Completed targeted outreach count: **0**
- Author-owned prospective dogfood tasks completed under this mission: **1**

## Engineering and distribution

- v0.3.0 release: verified.
- Release-tag CI: 189 tests passed across Linux, Windows, and macOS.
- Core verifier: `FEATURE FREEZE`; one security-exception fix is under review.
- Security finding: v0.3.0 checks remote URL arguments case-sensitively, so mixed-case schemes such as `HTTPS://` can reach an allow-listed executable. PR #8 normalizes the check before execution and adds lower/uppercase regression cases.
- Release status: source fix prepared; affected v0.3.0 tag remains immutable and requires a v0.3.1 patch release. This is not yet a verified public fix.
- PyPI: not published.
- PyPI Trusted Publishing workflow: prepared as an owner-dispatched immutable-tag workflow; owner-side environments and pending publishers are required.
- GitHub Release wheel/sdist/checksum workflow: prepared, not yet run.
- Primary installation remains the Git-tag command until a production PyPI install is independently verified.

## Recruitment readiness

Prepared but not sent:

- 30-candidate public recruitment matrix;
- 10 HIGH FIT individualized drafts;
- general maintainer invitation;
- independent reproduction request;
- independent security review request;
- consent/privacy and preregistered study materials already present in the repository.

No issue, pull request, email, social post, or maintainer tag was sent to an external target during preparation.

## Author-owned prospective dogfood

Record class:

```text
AUTHOR-OWNED PROSPECTIVE DOGFOOD
```

Task: prepare and verify this external-validation operations package in `kodlbegiko/agent-completion-ledger`.

- Contract committed before implementation completion: yes.
- Contract assertions: 12.
- Non-comment contract lines: 74.
- Preliminary verification runtime: 0.178941665 seconds on GitHub Actions.
- Ledger result: `SUPPORTED`.
- Decision before ledger: `INSUFFICIENT_EVIDENCE` because the files did not yet exist.
- Decision after ledger: eligible for human review; merge decision remains human.
- Reviewer/merge decision changed by ledger: no.
- Missing blocking evidence found by this dogfood task: no.
- Contract authoring time: not reliably timed and therefore left `null` rather than estimated.
- External validation credit: none.

The same PR review did uncover a separate mixed-case URL security defect. That finding came from repository review, not from the prospective completion contract, and is reported separately.

## External study

The fixed research question and hypotheses remain unchanged.

### H1

No result. There are no real participants or external task rows.

### H0

No result. Absence of participants is not evidence that all effect thresholds fail.

### H2

No result. There are no human outcomes from which to distinguish ACL format effects from specification quality, tests/build commands, domain knowledge, case order, or learning effects.

### Protocol deviations

- Human-study deviations: **none**, because recruitment has not begun.
- Pre-recruitment operational additions: recruitment matrix, outreach drafts, distribution workflows, security review package, and author-owned prospective dogfood collection. These do not change the fixed research question, hypotheses, thresholds, task pack, exclusions, or participant-balanced primary analysis.
- A security review finding required a narrowly scoped verifier fix under the documented feature-freeze exception. It does not change research outcomes or thresholds.
- Synthetic dry run remains analysis plumbing only and is excluded from human evidence.

## Security review

- Independent reviewers: 0.
- Independent public findings: none.
- Private findings: unavailable to check through the connected interface.
- Repository PR review finding: one high-priority trust-boundary defect involving case-sensitive URL-scheme rejection.
- Fix status: source fix and parametrized regression test are present on PR #8; full CI and v0.3.1 release verification remain required.
- Remaining material risk: allow-listed interpreters and project test/build tools can execute repository code with runner permissions; ACL is not a sandbox.

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
| No unresolved high-risk security issue | public patch release pending |

`EXTERNAL VALUE SUPPORTED`, `PIVOT REQUIRED`, and `RESEARCH COMPLETE — MAINTENANCE MODE` cannot yet be selected from outcome evidence. Recruitment materials are ready, but executable-mode external integration remains gated on a verified patch release.

## Stop rule

Stop feature expansion and evaluate maintenance mode when any preregistered STOP condition is met, including 30 targeted recruitment attempts with no non-author participation, median external contract authoring time above 30 minutes, no measurable review improvement, no willingness to maintain contracts, predominantly subjective tasks, ordinary CI providing equivalent value, unresolved execution risk, or complete coverage by mature alternatives.

## Honest impact statement

### Already achieved

- Published and reproducible engineering artifact at v0.3.0.
- Explicit completion-claim/evidence boundary.
- Trusted contract byte pinning, static-only review, provenance-rich reports, and bounded interoperability documentation.
- Auditable recruitment, distribution, and security-review preparation without contacting external maintainers.
- A real security review defect was identified and a narrow source fix was prepared before external executable-mode recruitment.

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

At least five non-author participants, three non-author repositories, ten real tasks, participant-balanced outcomes, contract/setup cost measurements, at least one changed decision and one newly identified blocking-evidence omission, maintenance willingness, an independently reviewed patch release, and independent security review.
