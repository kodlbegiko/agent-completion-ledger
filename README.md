# Agent Completion Ledger

**Repository-level acceptance evidence contracts for coding-agent tasks.**

Agent Completion Ledger (ACL) separates **“an output was produced”** from **“the configured repository evidence supports this completion claim.”** It evaluates file, hash, JSON, Git, test, and build evidence and returns one deterministic state: `SUPPORTED`, `FAILED`, `UNVERIFIABLE`, or `NO_CLAIM`.

中文定位：**針對 AI 程式代理任務，以 Repository 與 CI 證據驗證完成宣稱的接受契約。**

## Scope

ACL is responsible for task completion claims, repository/CI evidence, deterministic acceptance status, CI integration, and reviewer-facing reports.

ACL is **not** complete agent tracing, chain-of-thought storage, general operation audit, agent identity, regulatory certification, artifact build provenance, a complete sandbox, a product-value test, or proof of semantic correctness. See `docs/ecosystem-positioning.md`.

## Installation status

The current released source is `v0.3.0`. ACL is **not published on PyPI**. Install from the GitHub release tag or clone the repository:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install \
  "agent-completion-ledger @ git+https://github.com/kodlbegiko/agent-completion-ledger.git@v0.3.0"
```

For development:

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
python -m pip install -e ".[dev]"
```

GitHub Releases provide source archives. Wheel and sdist builds are validated in CI, but no PyPI publication is claimed.

## Quick verification

```bash
agent-completion-ledger init
# edit completion-ledger.yml
agent-completion-ledger validate-contract

CONTRACT_SHA256="$(python -c 'import hashlib; print(hashlib.sha256(open("completion-ledger.yml", "rb").read()).hexdigest())')"
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$CONTRACT_SHA256" \
  --format markdown \
  --output completion-report.md
```

Example contract:

```yaml
schemaVersion: "1"
policy:
  allowedExecutables: [python]
tasks:
  - id: fix-upload-validation
    claim:
      status: completed
      agent: coding-agent
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
| `UNVERIFIABLE` | Required evidence is absent, unsafe, timed out, disabled, mismatched, or unavailable. |
| `NO_CLAIM` | No completion claim was made. |

Only `SUPPORTED` maps to completed. It does not prove that the patch is secure, semantically correct, or valuable.

## Trusted Contract Mode

`--expected-contract-sha256` pins the exact contract bytes before parsing. A mismatch produces an integrity-only `UNVERIFIABLE` report and nonzero exit code. Obtain the expected digest from a protected base branch or another trusted channel; hashing an untrusted PR contract and accepting its own digest is not meaningful pinning.

Every JSON and Markdown report records:

- tool version and report schema version;
- repository identity and commit SHA;
- contract path, actual digest, and optional expected digest;
- task and assertion identifiers;
- trusted/static execution mode;
- deterministic result digest.

Trusted Contract Mode is byte-integrity checking, **not a sandbox**.

## Static-only mode

```bash
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$CONTRACT_SHA256" \
  --no-exec
```

`--no-exec` evaluates file, hash, JSON, multi-path, and Git assertions without running command assertions. A blocking command assertion becomes `UNVERIFIABLE`; it is never incorrectly upgraded to `SUPPORTED`.

## in-toto statement

```bash
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$CONTRACT_SHA256" \
  --format in-toto \
  --output completion-evidence.intoto.json
```

The output uses an in-toto Statement v1 envelope with ACL's experimental, versioned custom predicate. Unsigned output is structured evidence only. See `docs/in-toto-predicate.md` and `docs/attestation-integration.md`.

## Assertions

`file-exists`, `file-not-exists`, `file-not-empty`, `file-sha256`, `text-contains`, `json-path`, `command`, `test-command`, `build-command`, `exit-code`, `git-diff-contains`, `git-working-tree-clean`, `required-files`, and `forbidden-files`.

Commands are argv arrays with `shell=False`; executables require an allowlist; evidence paths and working directories are confined to the repository root; symlinks/traversal are rejected; and timeouts apply. Allow-listed interpreters can still execute malicious local code. Use disposable, least-privilege external isolation for untrusted repositories.

## GitHub Action

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"
  - id: contract
    shell: bash
    run: echo "sha256=$(sha256sum completion-ledger.yml | cut -d' ' -f1)" >> "$GITHUB_OUTPUT"
  - uses: kodlbegiko/agent-completion-ledger@v0.3.0
    with:
      contract: completion-ledger.yml
      expected-contract-sha256: ${{ steps.contract.outputs.sha256 }}
      format: markdown
      output: completion-report.md
```

For untrusted pull requests, use `docs/workflows/static-untrusted-pr.yml`, which reads the contract from the base commit, uses `pull_request`, grants only `contents: read`, exposes no secrets, and enables `no-exec`. For high assurance, pin actions to reviewed full commit SHAs.

## CLI

```text
agent-completion-ledger init
agent-completion-ledger validate-contract [contract]
agent-completion-ledger verify [--task ID] [--expected-contract-sha256 HASH]
                               [--no-exec]
                               [--format terminal|json|markdown|in-toto]
agent-completion-ledger report REPORT.json [--format ...]
agent-completion-ledger reproduce
agent-completion-ledger benchmark --output-dir DIR
agent-completion-ledger generalization
agent-completion-ledger validate-ledger LEDGER.jsonl
```

## Validation

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov=agent_completion_ledger --cov-branch
python -m build
```

CI covers Python 3.11/3.12/3.13 on Ubuntu and Python 3.12 on Windows/macOS, branch coverage, wheel installation, deterministic report output, predicate schema validation, safe workflow fixtures, composite-action integration, full reproduction, and dogfood against Shipcheck and CSV Snapshot.

## Research evidence

- v0.1.0 fixed SWE-agent/SWE-bench Verified pilot: `SUPPORTED` within its documented executable-oracle scope.
- v0.2.0 preregistered Multi-SWE-bench Go/MagentLess source: `SUPPORTED` within its documented scope.
- These studies do not estimate real-world prevalence or prove semantic correctness.

## External validation and impact

- Engineering hardening: implemented and under release CI.
- External study materials: `READY FOR EXTERNAL VALIDATION`.
- Real external participants: **0**.
- Non-author repository integrations: **0**.
- Independent adoption, reviewer-time savings, changed real decisions, product-quality improvement, and realized public impact: **EXTERNAL VALIDATION PENDING / UNKNOWN**.

See `docs/ADOPTION-QUICKSTART.md`, `docs/EXTERNAL-VALIDATION-PROTOCOL.md`, `research/external-validation/preregistration.md`, `SECURITY.md`, and `docs/v0.3.0-red-team.md`.
