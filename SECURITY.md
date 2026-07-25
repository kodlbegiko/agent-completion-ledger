# Security policy

Report vulnerabilities privately through GitHub's security reporting mechanism rather than a public issue. Do not publish proof-of-concept secrets, private repository contents, or exploit payloads in a public issue.

## Supported versions

| Version | Security status |
|---|---|
| `0.3.1` | Current security and packaging patch. |
| `0.3.0` | Affected by case-sensitive remote-URL argument rejection; use `--no-exec` for untrusted external repositories and upgrade to `0.3.1`. |
| `<0.3.0` | Not supported for the current trusted-contract security boundary. |

The v0.3.1 correction rejects `http://` and `https://` command arguments case-insensitively before an allow-listed executable receives them. This is input validation, not execution isolation. ACL remains **not a sandbox**.

## Trust model

Completion contracts are reviewed repository policy, not safe untrusted input. The verifier performs local filesystem checks and may execute explicitly allow-listed commands with the current process permissions.

The implementation:

- uses command argument arrays with `shell=False`;
- rejects absolute, Windows-drive, traversal, and symlink evidence paths;
- confines working directories to the selected repository root;
- requires an executable allowlist;
- rejects remote URL command arguments case-insensitively;
- enforces timeouts;
- does not automatically fetch contracts, dependencies, or remote scripts;
- does not transmit telemetry or repository contents;
- does not include command stdout/stderr in reports.

## Trusted Contract Mode

`--expected-contract-sha256` pins the exact contract bytes. The digest is checked before parsing the contract. A mismatch produces an integrity-only `UNVERIFIABLE` report and exit code 2; the mismatched contract is not parsed or executed.

Hash pinning protects only the selected contract bytes. It does not prove that:

- the trusted contract is complete or safe;
- an allow-listed executable is benign;
- the checked-out repository code is safe;
- the expected digest came from an independent trusted channel;
- the runner, action code, dependencies, or operating system are uncompromised.

For pull requests, obtain the contract and expected digest from the reviewed base commit or another protected source. Do not calculate the expected digest from an untrusted PR contract and then describe that as pinning.

## Static-only mode

`--no-exec` disables `command`, `test-command`, `build-command`, and `exit-code` assertions. Static file, hash, JSON, multi-path, and Git assertions still run. A blocking command assertion becomes `UNVERIFIABLE`; it never becomes `SUPPORTED` merely because execution was disabled.

Static-only mode reduces code-execution exposure but is not a complete sandbox. Filesystem metadata, Git operations, parsers, and the verifier process still operate on untrusted repository content.

## Interpreter risk

Allow-listing `python`, `node`, `bash`, a package manager, or another interpreter can permit arbitrary local code execution through modules, scripts, lifecycle hooks, test plugins, or build configuration. The allowlist limits the first executable name; it is not a capability system or script validator.

Use:

- disposable GitHub-hosted or externally sandboxed runners;
- `permissions: contents: read` for review workflows;
- no secrets in untrusted PR jobs;
- `pull_request`, not `pull_request_target`, when PR code is checked out and evaluated;
- immutable full-SHA pins for high-trust third-party actions;
- network and filesystem isolation external to ACL when required.

## Report confidentiality and integrity

Reports record task IDs, contract paths, assertion IDs, repository identity, commit SHA, status, and assertion messages. These values may reveal internal names even though command stdout/stderr is omitted. Do not place secrets in contract values, paths, task IDs, report output locations, reproduction issues, or dogfood artifacts.

The deterministic `resultDigest` detects report-content changes when a trusted digest is retained. It is not a signature. The experimental in-toto statement is unsigned structured data unless an external attestation system signs it. A valid signature or GitHub Artifact Attestation establishes issuer/artifact binding under that system; it does not prove program correctness, safety, contract completeness, product value, or regulatory compliance.

## Non-goals

ACL does **not** provide a container, VM, network namespace, syscall filter, privilege separation, malware scanner, key-management service, transparency log, identity system, compliance certification, or complete sandbox.
