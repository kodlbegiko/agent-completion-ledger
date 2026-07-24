# Red-team and falsification review

## Twelve required challenges

| Challenge | Evidence or additional test | Disposition |
|---|---|---|
| 1. The problem is unimportant | A 20,574-session observational study reports developer costs, user correction, and growing inaccurate self-reporting. This pilot measures only evidence/reporting separation. | **Partly accepted.** Value is reduced review ambiguity, not catastrophic-risk prevention. |
| 2. The sample is severely biased | Seven purposively selected SWE-agent lineage submissions on one benchmark. | **Accepted.** No prevalence claim beyond this sample. |
| 3. Existing tools are already sufficient | AAS-1, Evidence Envelope, `agent-evidence`, Cursor Agent Trace, and other ledgers already exist. | **Accepted.** Generic ledger novelty is `DISPROVED`; retained contribution is the frozen benchmark adapter and protocol. |
| 4. The metric is wrong | Inclusive and strict rates, baseline precision, abstention, threshold sweep, and leave-one-submission-out analyses were produced. | Retained only as **oracle-unsupported completion-label rate**. |
| 5. The result is a dataset artifact | Per-submission rates range 33.20%–82.79%; every leave-one-submission-out lower bound remains above 55%. | Not driven by one submission, but still benchmark-family specific. |
| 6. The method leaks answer information | The ledger is explicitly post-verification reporting and intentionally consumes result labels. | Not applicable to predictive evaluation; it cannot be used before verification. |
| 7. The baseline is too weak | “Patch exists ⇒ completed” is deliberately naive and the primary rate equals one minus resolution precision among generated patches. | **Accepted.** This is not a competitive predictor or a new capability metric. |
| 8. Statistics or arithmetic are wrong | Count identities, source-schema tests, Wilson tests, CSV/JSON cross-checks, 79 automated tests, and deterministic reruns were executed. | No numerical discrepancy found; one upstream duplicate anomaly is retained. |
| 9. The result cannot generalize | Tasks repeat across submissions; attempts are not independent; one framework lineage is used. | **Accepted.** Wilson intervals describe aggregate records, not a randomized population. |
| 10. Maintenance costs exceed value | Standard-library CLI, two small adapters, four states, no service or database. | Current frozen benchmark cost is low; live multi-platform adapters remain untested. |
| 11. Native AI will replace the method | A model may emit the format, but it cannot independently certify its own outcome without an external evidence source. | Format may be absorbed by platforms; evidence/oracle separation remains relevant. |
| 12. Others have no adoption incentive | CI and PR systems already expose checks and exit codes, but no user adoption experiment was run. | Adoption value remains `UNKNOWN`. |

## Executed falsification tests

Machine-readable output: `results/published/red-team-sensitivity.json`.

1. **No-log sensitivity:** excluding all six no-log claims changes 60.67% to 60.60%.
2. **Threshold sweep:** the preregistered rule remains supported through a 50% threshold; at 60%, only four of seven submissions exceed the threshold and the rule fails.
3. **Leave-one-submission-out:** aggregate rates range 57.18%–65.47%; every descriptive Wilson lower bound remains above 55%.
4. **Oracle false-negative break-even:** 1,369 of 2,041 unsupported claims—67.07%—would need to be reclassified as acceptable despite the oracle to reduce the rate to 20%.
5. **Determinism:** output hashes match under `PYTHONHASHSEED=0` and `321`.
6. **Source anomaly preservation:** duplicate `no_generation` entries remain visible as a discrepancy field.

## Criticisms that changed the conclusion

- Replace “agents lied” with “the imposed patch-exists reporting policy was unsupported by the available oracle.”
- Replace “new completion metric” with “the arithmetic complement of benchmark support, represented as an explicit evidence contract.”
- Replace “ledger solves completion” with “ledger makes status semantics consistent with supplied evidence.”
- Treat benchmark resolution as scoped evidence, not truth about user intent.
- Reject any claim that this project invented generic agent evidence ledgers.
