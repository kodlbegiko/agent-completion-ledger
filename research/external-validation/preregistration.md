# Preregistration: external reviewability study

Status: **PREREGISTERED DESIGN — RECRUITMENT NOT STARTED**

Real participant count at registration: **0**

## Research question

Does a Completion Evidence Contract report help non-author maintainers judge whether coding-agent work has sufficient acceptance evidence faster or more consistently than an agent summary alone?

## Hypotheses

### H1

Compared with the summary-only condition, summary plus ACL report will achieve at least one of these preregistered material effects:

1. at least **25% relative reduction in false acceptance rate**; or
2. at least **20% relative reduction in reviewer ambiguity**; or
3. at least **20% reduction in median time to identify the first blocking issue**.

A qualifying effect is rejected if median total review time becomes more than 20% slower and the condition produces no compensating reduction of at least 25% in false acceptance.

### H0

The ACL condition does not meet a material threshold, or its review/authoring cost offsets the measured benefit.

### H2

Any benefit is primarily caused by a more explicit task specification rather than the ACL tool/report. This is evaluated by recording contract authoring time and asking reviewers which information changed their decision. H2 is not resolved by the primary two-condition comparison alone; it is a stated alternative explanation.

## Fixed materials

- 10 fixed coding tasks in `task-pack.json`.
- Three task families: Python, Node.js, and repository/release hygiene.
- Ground-truth classes: acceptable completion, failed completion, and insufficient evidence.
- Two review conditions:
  - **A: summary only**;
  - **B: identical summary plus ACL report**.
- The code diff, task statement, and ground truth are held constant between conditions.

## Participants

Target: at least five non-author software maintainers or experienced reviewers. No project author is counted toward the external-participant threshold. Recruitment, consent, and exclusions are recorded before analysis.

### Inclusion

- has reviewed or maintained a software repository;
- can inspect the language/task family assigned;
- is not an author of ACL or the prepared task artifacts;
- provides informed consent.

### Exclusion

- incomplete decision or timing record;
- prior access to ground truth for the assigned task;
- technical interruption that prevents viewing required materials;
- duplicate participation.

Exclusions are documented with reason and are not silently replaced after results are inspected.

## Assignment and order

Use a counterbalanced design. Each participant reviews five tasks in condition A and five in condition B. Task-condition assignment is rotated using the fixed Latin-style schedule in the protocol. Review order is randomized within each block using a recorded seed. No participant reviews the same task in both conditions.

## Outcomes

For every task collect:

- total review time in seconds;
- accept/reject/insufficient-evidence decision;
- false acceptance and false rejection against fixed ground truth;
- confidence on a 1–5 scale;
- ambiguity on a 1–5 scale;
- time to first blocking issue in seconds, or blank if none identified;
- free-text blocking issue;
- whether the report changed the initial decision;
- maintenance willingness on a 1–5 scale.

For contract preparation collect:

- authoring time in seconds;
- non-comment contract line count;
- CI overhead in seconds;
- revision count.

## Primary analysis

1. Calculate participant-level and pooled false acceptance, false rejection, ambiguity, confidence, review time, and first-blocker time by condition.
2. Report absolute and relative condition differences with bootstrap 95% confidence intervals where sample size permits.
3. Evaluate the three H1 material thresholds exactly as written above.
4. Report all thresholds, including unfavorable outcomes; do not select only the best metric.
5. Keep acceptable, failed, and insufficient-evidence ground-truth classes visible in stratified results.

## Secondary analysis

- inter-reviewer agreement by condition;
- task-family effects;
- correlation between contract length/authoring time and review outcomes;
- qualitative reasons a report did or did not change a decision;
- sensitivity analysis excluding interrupted sessions.

Secondary analysis is exploratory and cannot replace a failed primary threshold.

## Stopping rule

The first analysis occurs after at least five eligible external participants complete all assigned tasks. Recruitment may continue to 12 participants for precision, but the hypotheses, metrics, exclusions, and thresholds cannot change after any outcome data are inspected.

## Integrity and privacy

Participant identifiers are pseudonymous. The identity key is stored separately from response data. Do not collect repository secrets, private source code, or personal account credentials. Raw free text is reviewed for accidental identifiers before publication.

## Synthetic dry run

A synthetic dry run may validate schemas, counterbalancing, and analysis code. It is stored separately and labeled synthetic. It is never counted as a participant, adoption, reproduction, or evidence for H1/H0/H2.

## Current status

`READY FOR EXTERNAL VALIDATION`

This status means the protocol and collection machinery are prepared. It does not mean external validation is complete.
