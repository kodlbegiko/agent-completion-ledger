# Completion Evidence Contract v1

A contract separates a coding-task completion claim from repository evidence that can be checked deterministically. It is an acceptance-reporting mechanism, not a confidence score, model evaluator, product-value test, or complete sandbox.

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

## Assertions

Contract schema v1 supports:

- `file-exists`, `file-not-exists`, `file-not-empty`, `file-sha256`;
- `text-contains`, `json-path`;
- `command`, `test-command`, `build-command`, `exit-code`;
- `git-diff-contains`, `git-working-tree-clean`;
- `required-files`, `forbidden-files`.

All command evidence uses an argument array and `shell=False`. The first executable must appear in `policy.allowedExecutables`; remote URL arguments are rejected; commands have a maximum timeout; and `workingDirectory` must remain within the repository root.

## Ledger states

- `SUPPORTED`: a completion claim exists and every blocking assertion passed.
- `FAILED`: a completion claim exists and at least one blocking assertion failed.
- `UNVERIFIABLE`: a completion claim exists but required evidence is missing, disabled, disallowed, timed out, unsafe, mismatched, or unavailable.
- `NO_CLAIM`: the contract records no completion claim.

Non-blocking assertions are reported but cannot change an otherwise supported task into `FAILED`.

## Trusted Contract Mode

```bash
agent-completion-ledger verify \
  --contract completion-ledger.yml \
  --expected-contract-sha256 <64-hex-digest>
```

The verifier hashes exact contract bytes before parsing. If the digest differs, it emits an integrity-only report containing a synthetic `contract-integrity` task with `UNVERIFIABLE`, then exits 2. It does not parse or execute the mismatched contract.

The expected digest must come from a trusted source such as a reviewed base commit, protected configuration, or independent release manifest. Calculating the expected digest from the same untrusted PR contract only confirms self-consistency and does not stop contract replacement.

## Static-only mode

```bash
agent-completion-ledger verify --no-exec
```

Static-only mode evaluates file, content, hash, JSON, multi-path, and Git assertions. It does not run command, test, build, or exit-code assertions. A blocking command assertion is `UNVERIFIABLE`, so a command-dependent task cannot become `SUPPORTED` in this mode.

## Report provenance

Report schema v2 records:

- ACL tool version;
- repository identity and checked-out commit SHA;
- contract path, exact SHA-256, optional expected digest, and match result;
- repository task IDs and evidence assertion IDs;
- trusted mode and full/static/integrity-only execution mode;
- report schema version;
- deterministic result digest.

The result digest covers the canonical report payload before insertion of the digest field. It detects content changes when compared with a separately trusted digest; it is not a cryptographic signature or issuer identity.

## Trust boundary

Contracts can request local commands. Treat a contract as reviewed repository policy, not untrusted input. Path confinement, symlink rejection, argv-only subprocesses, executable allowlists, URL-argument rejection, and timeouts reduce common hazards but do not provide kernel isolation, network isolation, syscall filtering, privilege separation, containerization, dependency safety, or malware protection.

Allow-listed interpreters can execute arbitrary repository code through scripts, imports, plugins, lifecycle hooks, and build backends. Use static-only mode or an external disposable sandbox for untrusted repositories. See `SECURITY.md` and `docs/workflows/`.
