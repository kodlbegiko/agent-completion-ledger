# Research report

## Abstract

This exploratory benchmark asks whether output production is a reliable completion signal for coding agents. Seven public SWE-agent submissions to SWE-bench Verified were fixed before aggregate analysis. A generated candidate patch is the baseline completion claim; the public executable result is treated as scoped evidence: `resolved` supports completion, `no_logs` is unverifiable, and remaining generated attempts fail under the available oracle. Across 3,364 generated claims, 1,323 were supported, 2,035 failed, and 6 were unverifiable. The inclusive oracle-unsupported completion-label rate was 60.67% (95% Wilson interval 59.01%–62.31%); excluding no-log cases produced 60.60%. All seven submissions exceeded the preregistered 20% threshold. An evidence-gated ledger prevents unsupported `COMPLETED` labels relative to the supplied oracle, but it does not improve patches, repair weak tests, or measure natural-language honesty. Verdict: `SUPPORTED` within this narrow reporting scope.

## Background

Coding-agent generation and executable verification are distinct stages. The public SWE-bench experiments repository stores predictions, execution logs, and result artifacts separately. Real-world observational work also identifies inaccurate self-reporting and developer correction costs. However, UTBoost, SWE-Bench+, and STING show that benchmark tests can be weak or under-constrained. The defensible target is therefore not “true task completion,” but whether a status label accurately reflects the evidence currently available.

## Evidence-state audit

| Statement | Status | Basis |
|---|---|---|
| Public SWE-bench submissions separate predictions from executable result artifacts | `KNOWN` | Official repository structure and submission requirements |
| The seven pinned records contain 3,364 generated attempts and 1,323 resolved attempts | `KNOWN` | Immutable source blobs and deterministic extraction rules |
| A patch-exists policy is a plausible proxy for premature completion reporting | `INFERRED` | Workflow framing plus real-world inaccurate self-reporting evidence |
| The exact 60.67% rate generalizes to coding agents in practice | `UNKNOWN` | No random real-world sample |
| This project invented generic agent evidence ledgers | `DISPROVED` | Multiple public standards and tools already exist |
| Natural-language completion claims can be labeled from these benchmark files | `UNTESTABLE HERE` | The selected result files do not provide a ground-truthed claim corpus |

## Research question

Across the fixed public sample, how often is a patch-exists completion label unsupported by the SWE-bench executable oracle, and can a four-state ledger make completion status faithful to that evidence?

## Related work

SWE-bench supplies repository issues and execution-based evaluation. The experiments repository publishes predictions, logs, trajectories, and result records. UTBoost, SWE-Bench+, and STING document weaknesses in test-based oracles. AAS-1, Evidence Envelope, `agent-evidence`, and Cursor Agent Trace demonstrate active work on auditable agent evidence and provenance. Consequently, the narrower contribution here is a deterministic SWE-bench result adapter, a frozen reporting-fidelity pilot, machine-readable evidence states, and a falsification record—not a generic evidence-ledger invention. Full references are in `docs/references.md`.

## Methods

The preregistration is in `docs/methodology-preregistered.md`. The fixed sample contains seven named historical submissions. Legacy files expose an explicit `generated` list; compact files expose `no_generation`, `no_logs`, and `resolved`, with a 500-slot denominator. Sources are pinned by Git blob SHA.

Baseline policy: every generated patch is labeled `COMPLETED`. Ledger policy: `SUPPORTED`, `FAILED`, `UNVERIFIABLE`, or `NO_CLAIM`; only `SUPPORTED` maps to completion. Rates are micro-averaged and accompanied by descriptive 95% Wilson intervals. Because tasks recur across submissions, those intervals are not treated as population-level causal uncertainty.

## Data

The dataset contains 3,500 benchmark slots and 3,364 generated claims across seven submissions. Committed data are derived counts rather than full upstream files because no root license file was found in the experiments repository at inspection time. Paths, blob SHAs, extraction formats, discrepancies, and the two directly identifiable legacy failed cases are in `data/frozen/submission-summaries.json`. The fetch and extraction scripts permit independent rechecking on a normal network.

## Results

| Submission | Generated | Supported | Unsupported incl. unknown | Rate |
|---|---:|---:|---:|---:|
| Claude 3 Opus (2024-04-02) | 459 | 79 | 380 | 82.79% |
| GPT-4 (2024-04-02) | 472 | 112 | 360 | 76.27% |
| Claude 3.5 Sonnet (2024-06-20) | 489 | 168 | 321 | 65.64% |
| GPT-4o (2024-07-28) | 450 | 116 | 334 | 74.22% |
| Claude 3.7 Sonnet (2025-02-25) | 498 | 313 | 185 | 37.15% |
| LM 32B (2025-05-11) | 496 | 201 | 295 | 59.48% |
| Claude 4 Sonnet (2025-05-22) | 500 | 334 | 166 | 33.20% |
| **Total** | **3,364** | **1,323** | **2,041** | **60.67%** |

The aggregate Wilson lower bound was 59.01%, seven of seven submissions exceeded 20%, and the 3,000-claim stopping minimum was met. Baseline completion-label precision relative to the oracle was 39.33%. Ledger precision is 100% relative to that same oracle by construction because it refuses to label failed or unverifiable records complete; this is a consistency property, not model improvement.

## Error analysis

The 2024 GPT-4 source contains 30 raw `no_generation` entries but 472 unique generated predictions, implying 28 no-claim slots. Duplicate no-generation IDs explain the discrepancy. The adapter preserves raw and inferred values and uses the explicit generated list. `astropy__astropy-12907` in the Claude 3 Opus source and `django__django-16454` in the GPT-4 source are generated but absent from the corresponding resolved lists, providing direct failed examples. Compact files support aggregate failed counts but not exact failed identifiers without the full benchmark universe, so no fabricated identifiers are reported for them.

## Sensitivity analysis

Counting six no-log claims as unsupported yields 60.67%; excluding them yields 60.60%, a 0.07 percentage-point difference. Leave-one-submission-out rates range 57.18%–65.47%. The five-of-seven rule remains supported at thresholds through 50% and fails at 60%. To drive the observed rate down to 20%, at least 1,369 currently unsupported claims—67.07% of them—would need to be acceptable despite the supplied oracle.

## Red-team and alternative explanations

The primary rate is exactly the complement of oracle-supported precision among generated patches. This is not a novel agent-capability statistic, and the baseline is intentionally weak. The useful artifact is the explicit status contract and reproducible extraction/falsification workflow. The strongest remaining threat is criterion validity: weak tests can overstate support, while incomplete or benchmark-mismatched tests can reject patches that users might accept. Twelve adversarial challenges and their dispositions are in `docs/red-team.md`.

## Threats to validity

- **Construct:** generated patch is a behavioral proxy, not a natural-language completion statement.
- **Internal:** source schemas changed; adapters and count identities are tested.
- **Criterion:** SWE-bench resolution is evidence, not ground truth about user intent.
- **Sampling:** the historical sample is purposive and limited to one framework lineage.
- **Independence:** the same benchmark tasks recur across submissions.
- **Instrumentation:** compact files lack exact failed-instance lists; only counts are inferred.

## Limitations

This is an exploratory benchmark, not a prevalence study or intervention trial. It does not compare against a sophisticated confidence estimator, observe actual product messages, measure reviewer time, validate adoption, or strengthen the benchmark oracle. The generic ledger concept is already occupied by emerging standards. The current CLI supports two observed SWE-bench result schemas, not arbitrary agent platforms.

## Ethical and safety considerations

Only public aggregate benchmark records are analyzed. No personal data, secrets, private prompts, or hidden reasoning are collected. Third-party patches are not executed in this environment. Results must not be used to accuse named vendors or models of dishonesty because the “completion claim” is an operational baseline imposed by this study.

## Negative results

1. Generic agent-evidence ledger novelty is `DISPROVED`.
2. No patch-quality improvement occurs; status gating changes semantics only.
3. Natural-language false completion claims are `UNTESTABLE HERE` from these records.
4. Adoption benefit remains `UNKNOWN` because no user study was conducted.
5. The primary rate is derivable from existing resolved counts; the incremental contribution is packaging, evidence states, extraction checks, and falsification—not discovery of a hidden benchmark statistic.

## Conclusion

**SUPPORTED — The pilot evidence supports the stated hypothesis within the documented scope and limitations.** Under the imposed patch-exists baseline, 60.67% of generated attempts lacked support from the available executable oracle. Evidence gating makes the report faithful to that oracle. It does not establish that real-world agents make false statements at this rate, and it does not establish true task completion.

## Future work

Replicate across other agent frameworks; pair natural-language self-reports with verifier outcomes; reassess supported cases using strengthened tests; and run a preregistered reviewer study measuring time-to-verification, correction rate, and adoption friction.
