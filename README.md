# Agent Completion Ledger

## Research question

Across seven fixed public SWE-agent submissions to SWE-bench Verified, how often would **“a patch was generated, therefore the task is complete”** produce a completion label unsupported by the benchmark's executable result? Can a deterministic evidence-gated ledger keep status reporting faithful to the evidence actually available?

## Why this matters

Generation and verification are different events. Collapsing them transfers review cost and risk to users. This project measures that reporting gap; it does **not** claim that SWE-bench tests perfectly capture user intent or that benchmark agents literally made natural-language claims.

## Pilot design and main result

The sample was fixed before aggregate analysis: seven named historical SWE-agent submissions, 3,500 benchmark slots. A generated patch is the baseline completion claim. `resolved` is scoped executable support, `no_logs` is unverifiable, and other generated attempts fail under the available oracle.

**Result:** 3,364 generated claims; 1,323 supported; 2,035 failed; 6 unverifiable. The inclusive oracle-unsupported completion-label rate was **60.67%** (95% Wilson interval **59.01%–62.31%**). Excluding unverifiable claims produced **60.60%**. All seven submissions exceeded the preregistered 20% threshold.

**Verdict: `SUPPORTED` within this reporting scope.** The result is not a real-world prevalence estimate. The primary rate is the complement of benchmark support among generated patches; the reusable contribution is the evidence-state adapter, frozen source record, protocol, tests, and falsification outputs.

```bash
python -m pip install -e .
PYTHONHASHSEED=0 agent-completion-ledger benchmark --output-dir reproduced-results
```

## Evidence states

| State | Meaning |
|---|---|
| `SUPPORTED` | Executable benchmark result supports completion |
| `FAILED` | Generated attempt is not supported and has evaluation evidence |
| `UNVERIFIABLE` | Generated attempt lacks evaluation logs |
| `NO_CLAIM` | No generated patch exists |

Only `SUPPORTED` maps to `COMPLETED`. This yields 100% completion-label precision **relative to the supplied oracle by construction**; it does not improve task-solving accuracy.

## Reproduce and validate

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov
python -m build
PYTHONHASHSEED=0 agent-completion-ledger benchmark --output-dir /tmp/a
PYTHONHASHSEED=321 agent-completion-ledger benchmark --output-dir /tmp/b
diff -u /tmp/a/output-hashes.json /tmp/b/output-hashes.json
```

Independent source re-extraction on a normal network:

```bash
python scripts/fetch_public_results.py
PYTHONPATH=src python scripts/extract_source_counts.py
```

## Exit codes

| Command | 0 | 1 | 2 |
|---|---|---|---|
| `benchmark` / `analyze` | H1 supported | H1 not supported | input/configuration failure |
| `validate-ledger` | valid | invalid | read failure |

## Repository map

- `RESEARCH.md` — complete report
- `docs/methodology-preregistered.md` — hypotheses, definitions, stopping rule
- `docs/candidate-selection.md` — 21 candidates, 15 fields each, and scores
- `docs/red-team.md` — twelve adversarial critiques and executed tests
- `docs/references.md` — source map
- `data/frozen/` — immutable derived counts with upstream blob SHAs
- `results/published/` — JSON, CSV, JSONL, sensitivity, hashes, runtime
- `schemas/ledger.schema.json` — aggregate evidence-record schema
- `src/`, `scripts/`, `tests/` — adapters, CLI, reproduction, and tests
- `research-manifest.yml` — commands, hashes, environment, limitations

## Limitations

One benchmark family, one agent lineage, purposive sampling, repeated tasks, and an imperfect oracle. Compact result files support aggregate failed counts but not exact failed IDs without an external task universe. The upstream experiments repository had no root `LICENSE` file when checked, so this repository commits derived facts rather than full source files.
