# Agent Completion Ledger v0.3.1

v0.3.1 is a narrowly scoped security and packaging patch under the project's `FEATURE FREEZE`.

## Security correction

v0.3.0 rejected command arguments beginning with lowercase `http://` or `https://`, but the comparison was case-sensitive. A mixed-case argument such as `HTTPS://example.invalid/code.py` could therefore reach an allow-listed executable instead of becoming `UNVERIFIABLE`.

v0.3.1 normalizes each command argument before the remote-URL prefix check. Lowercase and uppercase HTTP/HTTPS forms are covered by unit regression tests and a benign end-to-end reproduction case.

This correction does **not** make Agent Completion Ledger a sandbox. Allow-listed interpreters, test runners, build systems, plugins, lifecycle hooks, dependencies, and repository code still execute with the verifier process's permissions. Use disposable least-privilege runners and `--no-exec` for untrusted review workflows when command execution is unnecessary.

## Packaging and distribution

- Package version and citation metadata updated to `0.3.1`.
- PyPI metadata expanded with project URLs, keywords, audience, license, operating-system, supported-Python, quality-assurance, and testing classifiers.
- Wheel and sdist are built from the immutable release commit.
- `twine check` validates package metadata and README rendering.
- The wheel is installed and smoke-tested in a clean virtual environment.
- `SHA256SUMS` is generated for the wheel and sdist.
- GitHub Release assets include the wheel, sdist, and checksum file.
- PyPI Trusted Publishing remains owner-controlled, OIDC-only, TestPyPI-first, and protected by GitHub environments; no long-lived registry token is stored.

## External-validation status

This release does not add product features and does not change the preregistered external study.

At release preparation:

- real external participants: 0;
- non-author repository integrations: 0;
- independent reproductions: 0;
- independent security reviewers: 0;
- reviewer time savings, decision improvement, adoption, and public impact: not demonstrated.

The correct project state remains `READY FOR RECRUITMENT`, not `EXTERNAL VALUE SUPPORTED`.

## Installation

GitHub tag installation:

```bash
python -m pip install \
  "agent-completion-ledger @ git+https://github.com/kodlbegiko/agent-completion-ledger.git@v0.3.1"
```

After production PyPI publication is separately verified:

```bash
python -m pip install agent-completion-ledger==0.3.1
```

Do not interpret package provenance, checksums, a GitHub Release, an ACL `SUPPORTED` result, or an external signature as proof of software correctness or product value.
