# Migration from v0.1.0 to v0.2.0

v0.1.0 aggregate benchmark commands remain available. v0.2.0 adds runtime dependencies (`PyYAML` and `jsonschema`) and generic repository contracts.

## Reproduction

Replace the multi-command manual sequence with:

```bash
agent-completion-ledger reproduce
```

## New repository verification

```bash
agent-completion-ledger init
# edit completion-ledger.yml
agent-completion-ledger validate-contract
agent-completion-ledger verify --format markdown --output completion-report.md
```

## Behavioral changes

- Package version becomes `0.2.0`.
- `validate-ledger` remains for v0.1 aggregate JSONL records.
- Generic task verification uses `validate-contract`, `verify`, and `report`.
- An unverifiable claimed task returns exit code 2; a failed claimed task returns 1.
- Command assertions require an explicit executable allowlist and never use a shell.
