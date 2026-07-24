# Minimal static example

Copy `completion-ledger.yml` to a repository whose root `README.md` contains an `## Installation` heading.

```bash
HASH="$(python -c 'import hashlib; print(hashlib.sha256(open("completion-ledger.yml", "rb").read()).hexdigest())')"
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$HASH" \
  --no-exec \
  --format markdown \
  --output completion-report.md
```

Expected status: `SUPPORTED` when both static assertions pass. Delete the contract, report, and workflow to remove the integration.
