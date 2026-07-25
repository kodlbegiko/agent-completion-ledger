# Owner actions: PyPI Trusted Publishing and release artifacts

Status: **PREPARED — NOT PUBLISHED**

Agent Completion Ledger is **not published** on PyPI at the time this document was written. Do not change the README to `pip install agent-completion-ledger` until the production PyPI project and clean-environment installation have been verified.

## Audit findings

- Declared package name: `agent-completion-ledger`.
- Current released version: `0.3.0` / tag `v0.3.0`.
- Existing CI has built wheel and sdist and installed the wheel in a clean smoke-test environment.
- The v0.3.0 GitHub Release currently records GitHub-generated source archives only; no project-built wheel, sdist, or `SHA256SUMS` asset is recorded.
- The exact package name did not appear in an unauthenticated public PyPI search during the audit. This is not an authoritative reservation check; the owner must create a pending publisher or project to confirm availability.
- PyPI requires an owner-side Trusted Publisher configuration. Repository automation cannot complete that account action.

## Required owner configuration

### 1. Secure the accounts

1. Sign in to PyPI and TestPyPI using an owner-controlled account.
2. Enable two-factor authentication and retain recovery codes offline.
3. Confirm the GitHub repository remains public and controlled by `kodlbegiko`.
4. Review the publication workflow before registering it as a trusted publisher.

### 2. Create protected GitHub environments

Create these repository environments:

```text
testpypi
pypi
release-artifacts
```

For `pypi` and `release-artifacts`:

- require an owner or trusted reviewer approval;
- restrict deployment branches/tags to protected release tags where the GitHub plan supports it;
- do not add long-lived API tokens;
- do not expose repository or organization secrets to these jobs.

### 3. Register TestPyPI pending publisher

On TestPyPI, add a pending GitHub Actions publisher with exactly:

```text
Project name: agent-completion-ledger
Owner: kodlbegiko
Repository: agent-completion-ledger
Workflow filename: publish-pypi.yml
Environment: testpypi
```

### 4. Register PyPI pending publisher

On PyPI, add a pending GitHub Actions publisher with exactly:

```text
Project name: agent-completion-ledger
Owner: kodlbegiko
Repository: agent-completion-ledger
Workflow filename: publish-pypi.yml
Environment: pypi
```

If PyPI reports that the name is unavailable, stop. Do not publish under a confusingly similar name without a separate naming review and documentation update.

## Prepare packaging-only v0.3.1

The first registry release should be `v0.3.1`, not a silent rebuild of an already published Git tag. v0.3.1 is restricted to packaging, distribution, release assets, security/reproduction fixes, and documentation/metadata corrections.

Before tagging:

1. Set `[project].version` in `pyproject.toml` to `0.3.1`.
2. Add a dated `0.3.1` CHANGELOG entry describing only packaging/distribution and external-validation operations.
3. Update `CITATION.cff` to `0.3.1` and the actual release date.
4. Add package metadata if approved: project URLs, keywords, intended audience, supported Python classifiers, and operating-system classifier.
5. Keep README installation text on the Git-tag command until PyPI verification is complete.
6. Run the full CI matrix and confirm no core verifier feature change is included.

## Create and publish the tag

After the pending publishers and environments are configured:

```bash
git switch main
git pull --ff-only
git tag -a v0.3.1 -m "Agent Completion Ledger v0.3.1"
git push origin v0.3.1
```

The `publish-package` workflow will:

1. verify the tag matches `pyproject.toml`;
2. build wheel and sdist from the tagged commit;
3. run `twine check` to validate README/package rendering metadata;
4. install and smoke-test the built wheel;
5. generate `SHA256SUMS`;
6. publish to TestPyPI using OIDC;
7. wait for the protected `pypi` environment;
8. publish the identical artifacts to PyPI using OIDC.

No long-lived PyPI token is stored.

## Verify TestPyPI before approving production

From a disposable environment, use the exact TestPyPI version and allow dependencies from production PyPI:

```bash
python -m venv /tmp/acl-testpypi
. /tmp/acl-testpypi/bin/activate
python -m pip install --upgrade pip
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  agent-completion-ledger==0.3.1
agent-completion-ledger --help
```

Confirm:

- project description renders correctly;
- wheel and sdist are listed;
- provenance/Trusted Publishing is shown;
- console script starts;
- no dependency confusion or unexpected package is installed.

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

Inspect PyPI file hashes and publication provenance. Record the verified project URL and workflow run in a release-status document.

## Attach GitHub Release artifacts

After creating the `v0.3.1` GitHub Release, run the `build-release-artifacts` workflow manually with:

```text
tag = v0.3.1
```

Approve the `release-artifacts` environment. The workflow checks out the exact tag, confirms version/tag equality, builds and smoke-tests wheel/sdist, generates `SHA256SUMS`, and uploads all three asset types to the existing GitHub Release.

For historical v0.3.0 backfill, the same workflow may be run with `v0.3.0` after owner review. This rebuild is reproducible from the immutable tag, but it occurs after the original release date and must be described as a backfilled artifact set.

## README switch gate

Only after production verification, change the primary installation block to:

```bash
pip install agent-completion-ledger
```

Retain the exact-version and Git-tag installation options for reproducibility.

## Failure handling

- If TestPyPI fails, do not approve production.
- If the package name is unavailable, stop and record `BLOCKED` for PyPI distribution.
- If tag/version mismatch occurs, delete no existing tag; create a corrected patch release.
- If published artifacts are incorrect, do not overwrite them on PyPI. Yank the affected release if appropriate, document the reason, fix under the feature-freeze rules, and publish a new patch version.
