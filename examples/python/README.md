# Python example

This template assumes a `src`-layout package with pytest, mypy, and build installed in the environment.

```bash
python -m pip install -e ".[dev]"
HASH="$(python -c 'import hashlib; print(hashlib.sha256(open("completion-ledger.yml", "rb").read()).hexdigest())')"
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$HASH" \
  --format json \
  --output completion-report.json
```

The allow-listed Python interpreter can execute arbitrary local Python modules and scripts. Contract review, least privilege, no secrets, disposable runners, and timeouts remain necessary. `--no-exec` prevents these commands from running and marks their required evidence `UNVERIFIABLE`.
