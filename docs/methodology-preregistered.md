# Preregistered pilot protocol

Date frozen: 2026-07-24 (Asia/Taipei), before calculating aggregate results.

## Research question

In a fixed public sample of SWE-agent submissions evaluated on SWE-bench Verified, how large is the false-completion rate under a patch-exists baseline, and can evidence-gated reporting eliminate unsupported `COMPLETED` labels relative to the supplied executable oracle?

## Hypotheses

- **H1:** The micro-averaged inclusive false-completion rate exceeds 20%; its 95% Wilson lower bound exceeds 20%; and at least five of seven submissions individually exceed 20%.
- **H0:** One or more H1 conditions are not met.
- **H2:** Missing evaluation logs or benchmark-oracle weaknesses explain a material part of the apparent error.

## Operational definitions

- **Completion claim:** a submitted/generated candidate patch recorded by the public result file. This is a behavioral proxy, not a natural-language claim.
- **Supported:** instance appears in `resolved`.
- **Unverifiable:** generated instance appears in `no_logs`.
- **Failed:** generated but neither resolved nor no-logs.
- **False completion (inclusive):** generated minus resolved, divided by generated.
- **Strict false completion:** failed divided by generated minus no-logs.
- **Ledger completion precision:** resolved / all ledger records labeled completed. The ledger labels only resolved records completed, so this is an evidence-consistency property, not predictive performance.

## Dataset and fixed sample

Inclusion rule: the seven plain SWE-agent historical Verified submissions selected from the public directory: 20240402 Claude 3 Opus, 20240402 GPT-4, 20240620 Claude 3.5 Sonnet, 20240728 GPT-4o, 20250225 Claude 3.7 Sonnet, 20250511 LM 32B, and 20250522 Claude 4 Sonnet. Best-of-k, hybrid tools, and other agent frameworks are excluded. Each source is pinned by its Git blob SHA.

No personal data are stored. Full source files are not redistributed because no root upstream license was found; only factual derived counts, source paths, blob hashes, and a few instance identifiers are committed.

## Baseline and experiment

Baseline: every generated patch is reported as completed. Experimental reporting policy: only `resolved` is `SUPPORTED`; other evidence states remain explicit. The policy is evaluated for reporting fidelity, not task-solving gain.

## Metrics

Generated, resolved, failed, no-logs, no-claim; inclusive and strict false-completion rate; baseline and ledger completion precision; 95% Wilson intervals; number of submissions above 20%; deterministic output hashes; runtime and maximum resident set size recorded during validation.

## Stopping rule

Stop after the fixed seven submissions. Require at least 3,000 generated claims. If source count reconciliation cannot be completed, or the minimum is not met, return `INCONCLUSIVE`. H1 is supported only if all three preregistered conditions hold. Do not add or remove submissions based on results.
