# Security policy

Report vulnerabilities privately through GitHub's security reporting mechanism rather than a public issue.

## Trust model

Completion contracts are reviewed repository policy, not safe untrusted input. The verifier performs local filesystem checks and may execute explicitly allow-listed commands with the current process permissions.

The implementation:

- uses command argument arrays with `shell=False`;
- rejects absolute, Windows-drive, traversal, and symlink evidence paths;
- confines working directories to the selected repository root;
- requires an executable allowlist;
- rejects remote URL command arguments;
- enforces timeouts;
- does not automatically fetch contracts, dependencies, or remote scripts;
- does not transmit telemetry or repository contents.

It does **not** provide a container, VM, network namespace, syscall filter, privilege separation, malware scanner, or complete sandbox. A malicious allow-listed local executable can still read or change data available to the runner. Use disposable, least-privilege CI or an external sandbox for untrusted repositories.

Do not place secrets in contract files, reports, reproduction issues, or dogfood artifacts. Command stdout/stderr is not included in the default report, reducing accidental data exposure.
