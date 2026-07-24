# External validation protocol

Status: **READY FOR EXTERNAL VALIDATION**

Real participant count: **0**

The preregistered hypotheses, thresholds, task pack, consent notice, collection template, and analysis script are under `research/external-validation/`.

## Materials freeze

Before the first participant:

1. record the commit SHA containing the protocol and task pack;
2. export SHA-256 digests for `preregistration.md`, `task-pack.json`, `data-template.csv`, and `analyze.py`;
3. do not change primary metrics, exclusions, or thresholds after outcome data are inspected;
4. log any operational correction with date, reason, affected participants, and whether re-consent is required.

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

## Data quality checks

- exactly ten completed task rows per included participant;
- five rows in each condition;
- no duplicate participant/task pair;
- decision and ground truth use allowed values;
- review time is positive;
- confidence and ambiguity are integers 1–5;
- exclusions contain a written reason;
- synthetic IDs beginning `SYNTH-` are never merged with real participant results.

## Analysis

```bash
python research/external-validation/analyze.py \
  research/external-validation/collected-data.csv \
  --output research/external-validation/analysis-result.json
```

The script reports both conditions and every preregistered threshold. It does not claim causal attribution beyond the prepared comparison, and it cannot resolve H2 without additional specification-only controls.

## Recruitment state

No participant has been recruited or completed the protocol. The repository issues track recruitment, reproduction, interoperability feedback, and security review. Until real evidence meets the stated thresholds, the project status remains:

```text
EXTERNAL VALIDATION PENDING
```
