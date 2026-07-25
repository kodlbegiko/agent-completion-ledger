# Independent security review package

Status: **READY FOR INDEPENDENT REVIEW — REVIEWER COUNT 0**

Target release: **v0.3.1**

Recommended initial review time: **30–60 minutes**

Benign reproduction cases: `security/reproduction-cases/`

## Objective

Assess whether Agent Completion Ledger accurately enforces its documented trust boundary while verifying coding-agent completion evidence. This is not a certification request, product-value review, or request to treat ACL as a sandbox.

ACL is **not a sandbox**. Outside `--no-exec`, explicitly allow-listed executables may run with the verifier process's permissions.

## Claimed security properties

1. `--expected-contract-sha256` is checked before contract parsing.
2. A digest mismatch yields integrity-only `UNVERIFIABLE`, exit code 2, and no mismatched-policy execution.
3. `--no-exec` disables command, test-command, build-command, and exit-code assertions.
4. Disabled blocking command evidence cannot become `SUPPORTED`.
5. Evidence paths and working directories remain under the selected repository root.
6. Absolute, Windows-drive, traversal, and symlink evidence paths are rejected.
7. Commands use argument arrays with `shell=False`.
8. Executables require an explicit contract allowlist.
9. HTTP/HTTPS command arguments are rejected case-insensitively before execution.
10. Command execution has a bounded timeout.
11. Command stdout/stderr is not copied into reports.
12. Safe untrusted-PR examples use read-only permissions, no secrets, a protected/base contract, and static-only verification.
13. `resultDigest` detects report-content changes when compared with a retained trusted digest; it is not a signature.
14. ACL's in-toto output is unsigned structured evidence unless an external attestation system signs the intended artifact.

v0.3.0 remains immutable and affected by the documented mixed-case URL-scheme defect. Review executable-mode URL rejection against v0.3.1.

## Trust boundaries

### Reviewed or protected inputs

- ACL release or pinned action commit;
- expected contract digest source;
- contract bytes selected by that digest;
- workflow and runner image;
- dependency resolution and installed packages;
- any external signing or attestation service.

### Potentially untrusted inputs

- pull-request repository contents;
- contract-referenced paths and values;
- tests, build configuration, plugins, imports, and lifecycle hooks;
- local interpreters and package managers;
- Git metadata and filenames;
- task/assertion IDs, descriptions, and messages;
- report consumers that may overinterpret a status or signature.

### Outputs

- terminal, JSON, Markdown, and in-toto reports;
- process exit code;
- optional externally signed artifact attestation.

`SUPPORTED` means only that configured blocking evidence passed. It does not prove semantic correctness, safe code, complete requirements, author identity, legal compliance, or user value.

## Attack surface

- YAML/JSON parsing and schema validation;
- contract digest calculation and comparison;
- filesystem resolution, file reads, symlink and platform-path behavior;
- Git invocation and metadata;
- command allowlist checks and URL-argument validation;
- subprocess creation, environment inheritance, PATH resolution, timeout, and termination;
- report construction and serialization;
- composite GitHub Action inputs;
- fork-PR permissions and secrets;
- in-toto/attestation semantics;
- package, release, dependency, and action supply chain.

## Priority review scenarios

### 1. Contract replacement and digest source

Test whether an untrusted PR can replace both code and contract while the workflow hashes the PR-controlled contract and calls it trusted. Expected mitigation: contract bytes and expected digest originate from a reviewed base commit or another protected channel.

### 2. Digest pinning bypass and TOCTOU

Review malformed/non-hex digests, upper/lowercase forms, length errors, newline changes, alternate paths, symlink replacement, parsing errors in mismatched policy, and replacement between digest check and parse. Mismatched policy must not execute.

### 3. Allow-listed interpreter risk

Python, Node, shells, package managers, tests, and build tools can execute arbitrary repository code through imports, scripts, plugins, or lifecycle hooks. Confirm documentation and workflows do not imply that allowlisting creates a capability boundary.

### 4. Path, platform, and symlink escapes

Test traversal, POSIX absolute paths, Windows drive/UNC paths, separator variants, nested/broken symlinks, and symlinked working directories. Evidence access must remain under the selected repository root.

### 5. Remote URL argument rejection

Confirm lower-, upper-, and mixed-case `http://` and `https://` arguments become `UNVERIFIABLE` before an allow-listed interpreter receives them. Use only the included `.invalid` benign fixture.

### 6. Timeout and subprocess behavior

Review child/grandchild termination, signals, PATH manipulation, inherited environment/file descriptors, resource exhaustion, and Windows/macOS/Linux behavior. ACL's timeout is not resource isolation.

### 7. Report information leakage

Confirm stdout/stderr omission while testing whether filenames, YAML/JSON values, exceptions, Git metadata, paths, task IDs, assertion IDs, or messages can reveal excessive information. Never use real secrets.

### 8. Fork pull-request permissions

Review examples for `pull_request_target`, write permissions, `id-token: write`, secrets, credential persistence, untrusted workflow changes, and whether the base contract is acquired before PR code evaluation.

### 9. in-toto and signed-artifact interpretation

An unsigned Statement is not an attestation. A valid signature or GitHub Artifact Attestation establishes an issuer/artifact relationship under that system; it does not establish correctness, safe execution, complete requirements, or regulatory approval. A correctly signed `FAILED`, `UNVERIFIABLE`, incomplete, or maliciously authored report can still be authentic.

### 10. Package and Action supply chain

Review tag mutability, release/tag binding, third-party action references, dependency pins, build isolation, release assets/checksums, OIDC Trusted Publishing preparation, and the risk of using movable tags instead of reviewed full commit SHAs.

## Reproduction setup

Read the latest reviewed instructions from `main`, then execute the immutable `v0.3.1` code from a separate worktree:

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
git switch main
cat docs/INDEPENDENT-SECURITY-REVIEW.md
cat security/reproduction-cases/README.md

git worktree add ../acl-v0.3.1 v0.3.1
cd ../acl-v0.3.1
python -m venv .venv
. .venv/bin/activate
python -m pip install -e "[dev]"
agent-completion-ledger --help
```

The separation is intentional:

- review instructions come from the latest reviewed `main` checkout;
- the executable under test is pinned to immutable `v0.3.1`;
- ACL is not a sandbox, including when an executable is allow-listed;
- use only the supplied benign local fixtures, never third-party targets or real secrets.

Run the fixed package reproduction from the `acl-v0.3.1` worktree:

```bash
agent-completion-ledger reproduce --output-dir reproduced-results
```

Return to the `main` checkout when consulting or copying the current security-case instructions. Execute corresponding cases only against the pinned `v0.3.1` worktree.

The cases use repository fixtures, a short local sleep, and a reserved `.invalid` URL string. They must not be redirected to third-party systems or run with secrets.

## Finding format

For a public low-risk finding or documentation concern:

```markdown
Reviewer pseudonymous ID:
ACL version/tag and commit:
Reviewed scenario/case ID:
Affected file/line:
Expected security property:
Observed result:
Minimal benign reproduction:
Impact and preconditions:
Severity rationale:
Suggested mitigation:
Operating system and Python version:
Public evidence link:
```

Do not publish credentials, private source, employer-confidential data, weaponized payloads, or instructions that directly harm third parties.

## High-risk handling

For a suspected high-risk vulnerability:

1. stop public reproduction at the minimum benign evidence;
2. use GitHub private security reporting for `kodlbegiko/agent-completion-ledger`;
3. include affected versions and a benign reproduction where possible;
4. do not open a public issue containing exploit details;
5. pause outreach for the affected execution surface;
6. remediate only under the feature-freeze security exception after validation;
7. add a regression test and disclose only after an appropriate fix/review decision.

## What counts as an independent review

A review counts only when a `NON-AUTHOR HUMAN` supplies:

- pseudonymous reviewer ID;
- reviewed ACL tag/commit;
- scenarios or inspection method;
- commands or reproducible evidence;
- findings or an explicit no-finding result;
- limitations and environment;
- a public evidence link or private-report reference.

Author review, model comments, CI, release verification, and prepared materials do not count. Current independent reviewer count remains **0**.
