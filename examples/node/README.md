# Node.js example

This template assumes a TypeScript repository with `npm test`, `npm run typecheck`, and `npm run build` scripts.

```bash
npm ci
HASH="$(python -c 'import hashlib; print(hashlib.sha256(open("completion-ledger.yml", "rb").read()).hexdigest())')"
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 "$HASH" \
  --format json \
  --output completion-report.json
```

Full mode executes the allow-listed `npm` commands. Review the contract as code and run it only on a disposable runner without secrets when evaluating untrusted contributions. Use `--no-exec` for a static preview; command-dependent tasks will correctly become `UNVERIFIABLE`.
