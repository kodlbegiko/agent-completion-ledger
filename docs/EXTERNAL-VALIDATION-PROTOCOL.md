# External validation protocol

Status: **READY FOR RECRUITMENT**

Real participant count: **0**

Non-author repository count: **0**

The preregistered hypotheses, thresholds, task pack, consent notice, collection template, and analysis script are under `research/external-validation/`.

## Fixed research question

> For non-author repository maintainers, does adding an Agent Completion Ledger report to coding-agent completion review improve decision quality, missing-evidence detection, or review efficiency compared with reading the agent summary alone?

The research question, H1/H0/H2, material thresholds, exclusions, and participant-balanced primary analysis cannot be changed after human outcome data are inspected.

## Materials freeze

Before the first participant:

1. record the commit SHA containing the protocol and task pack;
2. export SHA-256 digests for `preregistration.md`, `task-pack.json`, `data-template.csv`, `adoption-integration-template.csv`, and `analyze.py`;
3. do not change primary metrics, exclusions, or thresholds after outcome data are inspected;
4. log any operational correction with date, reason, affected participants, and whether re-consent is required;
5. exclude all `SYNTH-`, template, author-owned, and model-only records from human analysis.

## Counterbalancing schedule

Use two schedules and alternate them by enrollment order:

| Schedule | Condition A tasks | Condition B tasks |
|---|---|---|
| S1 | py-01, py-03, node-01, node-03, repo-02 | py-02, py-04, node-02, repo-01, repo-03 |
| S2 | py-02, py-04, node-02, repo-01, repo-03 | py-01, py-03, node-01, node-03, repo-02 |

Randomize order within each condition block using a recorded random seed. A participant never reviews the same task in both conditions.

## Session procedure

1. Confirm eligibility and consent.
2. Assign a pseudonymous participant ID and counterbalance schedule.
3. Explain the three allowed decisions: `ACCEPT`, `REJECT`, `INSUFFICIENT_EVIDENCE`.
4. Present task statement, diff/artifacts, and identical agent summary.
5. In condition A, collect the decision without ACL report.
6. In condition B, also present the prepared ACL report.
7. Record timings without pausing for unrelated interruptions; mark interruptions explicitly.
8. Do not reveal ground truth until every task is complete.
9. Collect maintenance willingness and qualitative feedback.
10. Store identity/contact information separately from response rows.

## Fixed decision scoring

- False acceptance: reviewer chooses `ACCEPT` when ground truth is `REJECT` or `INSUFFICIENT_EVIDENCE`.
- False rejection: reviewer chooses `REJECT` or `INSUFFICIENT_EVIDENCE` when ground truth is `ACCEPT`.
- Correct insufficient-evidence decision: reviewer chooses `INSUFFICIENT_EVIDENCE` for that ground-truth class.
- First-blocker time is measured only when a blocking issue is identified; absence remains missing, not zero.

## Non-author repository integration track

A participant may also apply ACL to a real public task in a repository they maintain. This track measures adoption friction and real decision effects; it does not replace the fixed counterbalanced ten-task experiment.

For every integration, use `research/external-validation/adoption-integration-template.csv` and record:

- participant pseudonymous ID and consent state;
- repository type and public identifier, or `not disclosed` when approved by the protocol;
- programming language and task family;
- ACL version and public task/commit/PR reference;
- whether the contract existed before the review decision;
- contract authoring time, non-comment line count, and assertion count;
- installation time;
- CI runtime before ACL, with ACL, and calculated overhead;
- decision before and after the ledger and whether it changed;
- false acceptance and false rejection against fixed ground truth;
- ambiguity before and after;
- time to the first blocking evidence;
- willingness to keep the contract;
- number of times author assistance was required;
- subjective conditions not automatically verified;
- security/privacy concerns and protocol deviations.

Do not collect secrets, private code, employer-confidential information, hidden reasoning, sensitive personal data, or identity information beyond consented contact records stored separately. The template has explicit negative-control fields for prohibited data; any `true` value requires immediate review and exclusion from publication.

## Data quality checks

- exactly ten completed task rows per included fixed-study participant;
- five rows in each condition;
- no duplicate participant/task pair;
- decision and ground truth use allowed values;
- review time is positive;
- confidence and ambiguity are integers 1–5;
- exclusions contain a written reason;
- synthetic IDs beginning `SYNTH-` are never merged with real participant results;
- repeated judgments from one participant remain clustered under that participant and are not treated as independent participants;
- participant-balanced summaries are primary; pooled rows are sensitivity analysis only;
- author-owned prospective dogfood and non-author integration records remain separately labeled.

## Analysis

```bash
python research/external-validation/analyze.py \
  research/external-validation/collected-data.csv \
  --output research/external-validation/analysis-result.json
```

The script reports participant-level, participant-balanced, and pooled sensitivity results and every preregistered threshold. It does not claim causal attribution beyond the prepared comparison, and it cannot resolve H2 without additional specification-only controls and qualitative evidence.

Real integration outcomes are summarized separately before any exploratory cross-task analysis. They may establish real decision changes or adoption friction but cannot be substituted for missing fixed-study participants.

## Recruitment operations

- Candidate matrix: `research/external-validation/recruitment-targets.csv`.
- Outreach log: `research/external-validation/outreach-log.csv`.
- Drafts: `docs/outreach/`.
- No message may be sent without owner approval and a fresh repository/contact-policy check.
- One initial public message maximum per target; no automated issue, PR, email, tagging, or social posting.
- Stop and evaluate maintenance mode after 30 targeted attempts with no non-author participant.

## Recruitment state

No participant has been recruited or completed the protocol. Issues #4–#7 track reproduction, recruitment, interoperability feedback, and security review. Until real evidence meets the stated thresholds, the project status remains:

```text
READY FOR RECRUITMENT
```
