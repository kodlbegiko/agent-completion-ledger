# Completion Evidence Contract v1

A contract separates a completion claim from evidence that can be checked in a repository. It is a deterministic reporting mechanism, not a confidence score, model evaluator, or complete sandbox.

## Minimal contract

```yaml
schemaVersion: "1"
policy:
  allowedExecutables: [python]
tasks:
  - id: fix-upload-validation
    description: Reject files above the configured upload limit.
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

## Assertions

v0.2.0 supports:

- `file-exists`, `file-not-exists`, `file-not-empty`, `file-sha256`
- `text-contains`, `json-path`
- `command`, `test-command`, `build-command`, `exit-code`
- `git-diff-contains`, `git-working-tree-clean`
- `required-files`, `forbidden-files`

All command evidence uses an argument array and `shell=False`. The first executable must appear in `policy.allowedExecutables`; remote URL arguments are rejected; commands have a maximum timeout; `workingDirectory` must remain within the repository root.

## Ledger states

- `SUPPORTED`: a completion claim exists and every blocking assertion passed.
- `FAILED`: a completion claim exists and at least one blocking assertion failed.
- `UNVERIFIABLE`: a completion claim exists but required evidence is missing, disallowed, timed out, unsafe, or cannot run.
- `NO_CLAIM`: the contract records no completion claim.

Non-blocking assertions are reported but cannot change an otherwise supported task into `FAILED`.

## Trust boundary

Contracts can request local commands. Treat a contract as reviewed repository policy, not untrusted input. The tool confines declared paths and working directories and avoids shell interpretation, but it does not provide kernel isolation, network isolation, syscall filtering, containerization, or malware protection. Run untrusted repositories in an external sandbox or disposable CI runner.
