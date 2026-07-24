# Agent Completion Ledger v0.2.0

- Adds Completion Evidence Contract schema v1.
- Adds 14 deterministic evidence assertion types.
- Adds `init`, `validate-contract`, `verify`, `report`, and single-command `reproduce` workflows.
- Adds a composite GitHub Action and cross-platform CI.
- Adds real-repository dogfood adapters for Shipcheck and CSV Snapshot.
- Adds a preregistered Multi-SWE-bench Go generalization study.
- Adds third-party reproduction forms and reporting protocol.

Limitations: contracts are trusted policy; command execution is not sandboxed; passing evidence does not prove semantic correctness or product value; external reproduction remains pending until real third-party reports exist.
