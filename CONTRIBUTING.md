# Contributing

Open an issue before changing evidence-state semantics, adding a source to a confirmatory study, or expanding the command security model.

New assertions must include schema updates, deterministic reports, path/security analysis, pass/fail/unverifiable tests, and cross-platform considerations. New adapters must pin an immutable source and reject inconsistent count identities rather than silently repairing them.

Run:

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov=agent_completion_ledger --cov-branch
python -m build
```

Do not submit private trajectories, credentials, personal data, hidden chain-of-thought, unlicensed bulk datasets, virtual environments, or generated dependency directories.
