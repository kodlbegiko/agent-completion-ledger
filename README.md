# Agent Completion Ledger

Agent Completion Ledger separates **“an output was produced”** from **“the available evidence supports completion.”** It provides deterministic repository contracts, a four-state evidence ledger, a composite GitHub Action, and two reproducible research studies.

## Current evidence

### v0.1.0 pilot

Seven fixed SWE-agent/SWE-bench Verified submissions contained 3,364 generated patches. Under a deliberately weak “generated patch means completed” baseline, 2,041 labels lacked support from the available executable result: **60.67%** (95% Wilson **59.01%–62.31%**).

### v0.2.0 second source

A preregistered Multi-SWE-bench Verified Go/MagentLess source contained 341 completed patches, 25 resolved and 316 unresolved: **92.67%** unsupported (95% Wilson **89.40%–94.99%**). This is a single-source replication, not a real-world prevalence estimate.

Both studies treat benchmark resolution as scoped executable evidence, not proof of semantic correctness, user satisfaction, or agent honesty.

## Reproduce the pilot

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
python -m pip install -e ".[dev]"
agent-completion-ledger reproduce
```

Exit codes: `0` hashes match; `1` analysis ran but hashes differ; `2` environment/input failure.

## Verify a repository completion claim

```bash
agent-completion-ledger init
# edit completion-ledger.yml
agent-completion-ledger validate-contract
agent-completion-ledger verify --format markdown --output completion-report.md
```

Example:

```yaml
schemaVersion: "1"
policy:
  allowedExecutables: [python]
tasks:
  - id: fix-upload-validation
    claim:
      status: completed
      agent: codex
    evidence:
      - id: implementation
        type: file-exists
        path: src/upload_validator.py
      - id: tests
        type: test-command
        command: [python, -m, pytest]
        expectedExitCode: 0
        timeoutSeconds: 300
```

## Evidence states

| State | Meaning |
|---|---|
| `SUPPORTED` | A completion claim exists and all blocking evidence passed. |
| `FAILED` | A completion claim exists and at least one blocking assertion failed. |
| `UNVERIFIABLE` | A completion claim exists but required evidence is absent, unsafe, timed out, or cannot run. |
| `NO_CLAIM` | No completion claim was made. |

Only `SUPPORTED` maps to completed. This improves reporting fidelity; it does not improve the patch or prove true correctness.

## Assertions

`file-exists`, `file-not-exists`, `file-not-empty`, `file-sha256`, `text-contains`, `json-path`, `command`, `test-command`, `build-command`, `exit-code`, `git-diff-contains`, `git-working-tree-clean`, `required-files`, and `forbidden-files`.

Commands are argument arrays, never shell strings. Executables require an allowlist, working directories cannot leave repository root, symlink/path traversal is rejected, and timeouts are mandatory/defaulted. **This is not a sandbox.** Review contracts and run untrusted code in external isolation.

## CLI

```text
agent-completion-ledger init
agent-completion-ledger validate-contract [contract]
agent-completion-ledger verify [--task ID] [--format terminal|json|markdown]
agent-completion-ledger report REPORT.json [--format ...]
agent-completion-ledger reproduce
agent-completion-ledger benchmark --output-dir DIR
agent-completion-ledger generalization
agent-completion-ledger validate-ledger LEDGER.jsonl
```

## GitHub Action

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"
  - uses: kodlbegiko/agent-completion-ledger@v0.2.0
    with:
      contract: completion-ledger.yml
      format: markdown
      output: completion-report.md
```

The v0.2.0 tag/Release must not be assumed available until the owner completes `docs/OWNER-RELEASE-ACTIONS-v0.2.0.md`.

## Validation

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov=agent_completion_ledger --cov-branch
python -m build
```

CI covers Python 3.11/3.12/3.13 on Ubuntu and Python 3.12 on Windows/macOS, wheel installation, deterministic fixture output, full reproduction, the composite action, and real-repository dogfood against Shipcheck and CSV Snapshot.

## Research and external validation status

- v0.1.0 pilot: `SUPPORTED` within documented scope.
- v0.2.0 fixed Multi-SWE-bench source: `SUPPORTED` within documented scope.
- Generic contract engineering: implemented and under CI validation.
- Independent third-party reproduction: **EXTERNAL VALIDATION PENDING**.
- Adoption, saved reviewer time, and product-quality improvement: **UNKNOWN**.

See `RESEARCH.md`, `docs/completion-evidence-contract.md`, `docs/THIRD-PARTY-REPRODUCTION.md`, `docs/v0.2.0-red-team.md`, and `research-manifest-v0.2.0.yml`.
