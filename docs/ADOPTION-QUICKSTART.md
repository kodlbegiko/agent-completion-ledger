# 15-minute adoption quickstart

Status: **READY FOR EXTERNAL VALIDATION**. This quickstart has not yet been confirmed by a non-author maintainer.

## 1. Install from the GitHub release source

Agent Completion Ledger is not published on PyPI. Install the released source tag into a virtual environment:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install \
  "agent-completion-ledger @ git+https://github.com/kodlbegiko/agent-completion-ledger.git@v0.3.0"
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## 2. Create a starter contract

```bash
agent-completion-ledger init
```

Edit `completion-ledger.yml` so every task claim has concrete repository evidence. The smallest useful contract is:

```yaml
schemaVersion: "1"
policy:
  allowedExecutables: []
tasks:
  - id: readme-update
    description: The requested documentation file exists and contains the required heading.
    claim:
      status: completed
    evidence:
      - id: readme-exists
        type: file-exists
        path: README.md
      - id: heading-present
        type: text-contains
        path: README.md
        text: "## Installation"
```

## 3. Verify locally

```bash
CONTRACT_SHA256="$(python -c 'import hashlib; print(hashlib.sha256(open("completion-ledger.yml", "rb").read()).hexdigest())')"

agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$CONTRACT_SHA256" \
  --format markdown \
  --output completion-report.md
```

Expected outcomes:

- `SUPPORTED`: all blocking evidence passed;
- `FAILED`: at least one blocking assertion failed;
- `UNVERIFIABLE`: required evidence could not be evaluated or the contract digest mismatched;
- `NO_CLAIM`: the task does not claim completion.

## 4. Add a read-only pull-request workflow

Copy `docs/workflows/static-untrusted-pr.yml` to `.github/workflows/completion-evidence.yml`. It:

- uses `pull_request`, not `pull_request_target`;
- grants only `contents: read`;
- retrieves the contract from the trusted base commit;
- pins its SHA-256;
- disables command assertions for untrusted PR code.

Use `docs/workflows/trusted-main-contract.yml` only after deciding that executing trusted command assertions against untrusted PR code on a disposable runner is acceptable.

## 5. Review the report

Check:

1. repository commit and root identity;
2. contract path, actual digest, and expected digest match;
3. task IDs and ledger states;
4. blocking `FAILED` or `UNVERIFIABLE` assertions;
5. execution mode and stated limitations;
6. result digest if the report is retained or attested.

## Removal

Delete:

```text
completion-ledger.yml
.github/workflows/completion-evidence.yml
```

Then remove the virtual environment or package:

```bash
python -m pip uninstall agent-completion-ledger
```

ACL does not modify repository files during verification except the explicit report output path requested by the caller.

## Security warning

Full mode can execute allow-listed local interpreters and tools. Allow-listing `python`, `node`, or another interpreter does not make scripts safe. Trusted Contract Mode verifies contract bytes; it is not a sandbox. Use `--no-exec`, read-only permissions, no secrets, disposable runners, and immutable action pins for untrusted contributions.

## Pilot feedback

Use the maintainer pilot instructions in `docs/MAINTAINER-PILOT.md` and the repository's pilot recruitment issue. Report setup time, contract line count, CI overhead, unclear steps, and whether any report changed a review decision.
