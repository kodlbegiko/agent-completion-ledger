# Owner actions: PyPI Trusted Publishing

Status: **GITHUB RELEASE VERIFIED — PYPI NOT PUBLISHED**

Agent Completion Ledger v0.3.1 is released on GitHub with a verified wheel, sdist, and `SHA256SUMS`. The package is **not published on PyPI**. Do not change the primary installation instructions to `pip install agent-completion-ledger` until production PyPI publication and a clean-environment installation have been verified.

## Completed

- Current release: `v0.3.1`.
- Release commit: `703d63d6fb9a4329327634d5ae6e21030e13075e`.
- Tag resolves exactly to the release commit.
- Release is neither draft nor prerelease.
- Wheel, sdist, and `SHA256SUMS` are attached.
- Release checksums passed.
- Released wheel clean-environment smoke test passed.
- Runtime and package metadata both report `0.3.1`.
- Security correction for case-insensitive HTTP/HTTPS command arguments is included.
- Human-readable verification: `docs/v0.3.1-release-verification.md`.
- Machine-readable verification: `docs/v0.3.1-release-verification.json`.

## Remaining owner configuration

### 1. Secure PyPI accounts

1. Sign in to PyPI and TestPyPI using an owner-controlled account.
2. Enable two-factor authentication.
3. Store recovery codes offline.
4. Confirm the GitHub repository remains public and controlled by `kodlbegiko`.

### 2. Create protected GitHub environments

Create or verify:

```text
testpypi
pypi
```

For both environments:

- require an owner or trusted reviewer approval;
- restrict deployment to the intended repository and release workflow where supported;
- do not add long-lived API tokens;
- do not expose unrelated repository or organization secrets.

The existing `release-artifacts` environment may be retained for future GitHub Release asset workflows, but the v0.3.1 GitHub Release is already complete.

### 3. Register the TestPyPI pending publisher

Configure exactly:

```text
Project name: agent-completion-ledger
Owner: kodlbegiko
Repository: agent-completion-ledger
Workflow filename: publish-pypi.yml
Environment: testpypi
```

### 4. Register the PyPI pending publisher

Configure exactly:

```text
Project name: agent-completion-ledger
Owner: kodlbegiko
Repository: agent-completion-ledger
Workflow filename: publish-pypi.yml
Environment: pypi
```

If PyPI reports that the exact project name is unavailable, stop. Do not silently select a confusingly similar name.

## Publish the verified tag

After both pending publishers and protected environments are configured, open GitHub Actions, select `publish-package`, choose **Run workflow**, and enter:

```text
tag = v0.3.1
```

The workflow is designed to:

1. validate semver syntax;
2. check out the exact immutable tag;
3. verify the tag matches the checked-out commit and `pyproject.toml` version;
4. build wheel and sdist from that tag;
5. run `twine check`;
6. smoke-test the wheel;
7. generate a separate checksum artifact;
8. publish to TestPyPI using OIDC;
9. wait for production environment approval;
10. publish the identical distributions to PyPI using OIDC.

No long-lived PyPI token is required or stored.

## Verify TestPyPI before production approval

Use a disposable environment:

```bash
python -m venv /tmp/acl-testpypi
. /tmp/acl-testpypi/bin/activate
python -m pip install --upgrade pip
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  agent-completion-ledger==0.3.1
agent-completion-ledger --help
python -c "import importlib.metadata as m; print(m.version('agent-completion-ledger'))"
```

Confirm:

- description and README render correctly;
- wheel and sdist are listed;
- Trusted Publishing/provenance is shown;
- console script starts;
- installed version is `0.3.1`;
- no unexpected package or dependency is installed.

Only then approve the `pypi` environment.

## Verify production PyPI

```bash
python -m venv /tmp/acl-pypi
. /tmp/acl-pypi/bin/activate
python -m pip install --upgrade pip
python -m pip install agent-completion-ledger==0.3.1
agent-completion-ledger --help
python -c "import importlib.metadata as m; print(m.version('agent-completion-ledger'))"
```

Expected version:

```text
0.3.1
```

Inspect the PyPI file hashes and publication provenance. Record the project URL and successful workflow run in a repository status document.

## README switch gate

Only after production verification, change the primary installation command to:

```bash
pip install agent-completion-ledger
```

Retain the exact-version and Git-tag installation options for reproducibility.

## Failure handling

- If TestPyPI fails, do not approve production.
- If the package name is unavailable, record PyPI distribution as `BLOCKED`.
- If tag/version validation fails, do not alter or delete the existing tag.
- If registry artifacts are incorrect, do not overwrite them. Yank the affected registry release when appropriate, document the reason, and publish a new patch version under the feature-freeze rules.
