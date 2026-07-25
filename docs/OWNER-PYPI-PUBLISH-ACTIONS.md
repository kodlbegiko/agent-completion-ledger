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
- PR #8 identified a case-sensitive remote-URL validation bypass in v0.3.0. The source fix and regression tests are merged to `main` in `e529cbe3249bdee9a50b5791aeb86260dbcc56d3`; the next public package must include that fix.

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

For `testpypi`, `pypi`, and `release-artifacts`:

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

## Prepare security/packaging patch v0.3.1

The first registry release should be `v0.3.1`, not a silent rebuild of an already published Git tag. v0.3.1 is restricted to the reviewed case-insensitive URL rejection fix, packaging/distribution, release assets, reproduction fixes, and documentation/metadata corrections.

Before tagging:

1. Verify `main` contains commit `e529cbe3249bdee9a50b5791aeb86260dbcc56d3` or a descendant and that mixed-case `HTTP://` and `HTTPS://` arguments become `UNVERIFIABLE` before interpreter execution.
2. Set `[project].version` in `pyproject.toml` to `0.3.1`.
3. Add a dated `0.3.1` CHANGELOG entry describing the security fix and packaging/external-validation operations only.
4. Update `CITATION.cff` to `0.3.1` and the actual release date.
5. Add package metadata if approved: project URLs, keywords, intended audience, supported Python classifiers, and operating-system classifier.
6. Keep README installation text on the Git-tag command until PyPI verification is complete.
7. Run the full CI matrix and confirm no unrelated verifier feature change is included.

## Create the immutable tag

After the patch commit passes clean-main CI:

```bash
git switch main
git pull --ff-only
git tag -a v0.3.1 -m "Agent Completion Ledger v0.3.1"
git push origin v0.3.1
```

Pushing the tag does **not** automatically publish to PyPI. This prevents an unconfigured or unapproved registry deployment.

## Publish the exact tag manually

In GitHub Actions, open `publish-package`, choose **Run workflow**, and enter:

```text
tag = v0.3.1
```

The workflow will:

1. validate semver syntax;
2. check out the exact tag;
3. verify the tag resolves to the checked-out commit and matches `pyproject.toml`;
4. build wheel and sdist from that tag;
5. run `twine check` to validate README/package rendering metadata;
6. install and smoke-test the wheel;
7. generate a separate `SHA256SUMS` artifact that is not uploaded as a PyPI distribution;
8. publish wheel and sdist to TestPyPI using OIDC;
9. wait for the protected `pypi` environment;
10. publish the identical wheel and sdist to PyPI using OIDC.

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

For historical v0.3.0 backfill, the same workflow may be run with `v0.3.0` after owner review. This rebuild is reproducible from the immutable tag, but it occurs after the original release date and must be described as a backfilled artifact set. It does not fix the mixed-case URL issue in v0.3.0.

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
