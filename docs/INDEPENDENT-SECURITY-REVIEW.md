# Independent security review package

Status: **READY FOR INDEPENDENT REVIEW — REVIEWER COUNT 0**

Target release: `v0.3.0`

Recommended review time for an initial pass: **30–60 minutes**

Benign reproduction cases: `security/reproduction-cases/`

## Review objective

Assess whether Agent Completion Ledger accurately enforces its documented trust boundary when verifying coding-agent completion evidence. The review is not a request to certify the software, approve its product value, or treat it as a sandbox.

ACL is **not a sandbox**. It performs local filesystem/Git checks and, outside `--no-exec`, may run explicitly allow-listed executables with the verifier process's permissions.

## Security properties claimed

1. An expected contract SHA-256 is checked before parsing the contract.
2. Digest mismatch yields integrity-only `UNVERIFIABLE` and no execution of mismatched policy.
3. `--no-exec` disables command/test/build/exit-code assertions.
4. Blocking command evidence disabled by `--no-exec` cannot become `SUPPORTED`.
5. Evidence paths and working directories remain under the selected repository root.
6. Absolute, Windows-drive, traversal, and symlink evidence paths are rejected.
7. Executed commands use argument arrays with `shell=False`.
8. Executables require an explicit contract allowlist.
9. Remote URL command arguments are rejected case-insensitively.
10. Command execution has a bounded timeout.
11. Command stdout/stderr is not copied into generated reports.
12. Safe untrusted-PR examples use read-only permissions, no secrets, a base-commit contract, and static-only verification.
13. The deterministic result digest detects report-content changes when compared with a retained trusted digest; it is not a signature.
14. The in-toto output is an experimental unsigned statement unless an external attestation system signs an artifact/predicate.

## Trust boundaries

### Reviewed or protected inputs

- the ACL release/action commit;
- the expected contract digest source;
- the contract bytes selected by that digest;
- the CI workflow and runner image;
- dependency resolution and installed packages;
- any external signing/attestation service.

### Potentially untrusted inputs

- pull-request repository contents;
- paths and values referenced by the contract;
- test/build configuration and plugins;
- local interpreters and package-manager lifecycle hooks;
- Git metadata and filenames;
- task IDs, assertion IDs, descriptions, and messages;
- report consumers that may overinterpret a status or attestation.

### Outputs

- terminal, JSON, Markdown, and in-toto reports;
- exit code;
- optional externally signed artifact attestation.

A `SUPPORTED` output means the configured blocking evidence passed. It does not prove semantic correctness, safety, complete requirements, author identity, legal compliance, or user value.

## Attack surface

- YAML and JSON parsing;
- contract digest calculation and comparison;
- filesystem resolution and file reads;
- symlink and platform-path handling;
- Git command invocation and repository metadata;
- command allowlist validation;
- subprocess creation, environment inheritance, working directory, timeout, and termination;
- report construction and serialization;
- composite GitHub Action inputs;
- fork-PR workflow permissions;
- in-toto predicate semantics;
- release/package dependency and action supply chain.

## Priority review scenarios

### 1. Contract replacement

An attacker modifies both code and `completion-ledger.yml` in a pull request. A vulnerable workflow hashes the PR-controlled contract and calls the result “trusted.”

Expected mitigation: the workflow fetches the contract from the reviewed base commit or another protected source, then pins those exact bytes.

Review question: can any documented example still self-pin an untrusted contract while claiming Trusted Contract Mode?

### 2. Digest pinning bypass attempts

Try:

- uppercase/lowercase digest forms;
- malformed length or non-hex input;
- file replacement between hash and parse;
- alternate path spellings;
- newline changes;
- symlink replacement;
- parsing errors in a mismatched contract.

Expected result: invalid or mismatched integrity state must not execute contract commands. Report the precise time-of-check/time-of-use behavior observed.

### 3. Allow-listed interpreter risk

Allow-listing `python`, `node`, `bash`, package managers, test runners, or build tools can execute arbitrary repository code through imports, scripts, plugins, configuration, or lifecycle hooks.

Expected documentation property: ACL does not claim that an allowlist makes code safe. Review whether the Action/examples create a misleading default or expose secrets/network access.

### 4. Path and symlink escapes

Test relative traversal, POSIX absolute paths, Windows drive/UNC forms, separator variants, nested symlinks, broken symlinks, symlinked working directories, and platform-specific normalization.

Expected result: evidence access stays under the selected repository root and does not follow symlink evidence paths.

### 5. Timeout and subprocess behavior

Review:

- timeout precision;
- child/grandchild process termination;
- signal handling;
- resource exhaustion;
- inherited environment and file descriptors;
- executable resolution/PATH manipulation;
- behavior on Windows, macOS, and Linux.

ACL's timeout is not a resource sandbox. A subprocess may affect the runner before termination.

### 6. Report information leakage

Command stdout/stderr should be omitted. However, report fields deliberately include repository identity, commit, contract path/digest, task/assertion IDs, assertion types, status, and messages.

Review whether malformed filenames, YAML values, exception text, JSON values, or Git metadata can place secrets or excessive internal detail in a report. Never test with real secrets.

### 7. Fork pull-request secret exposure

Review every PR example for:

- `pull_request_target` misuse;
- write permissions;
- `id-token: write` or attestation permissions;
- secrets/environment credentials;
- credential persistence in checkout;
- untrusted action/workflow modification;
- base-contract acquisition before PR code evaluation.

Expected boundary: untrusted preview workflows are read-only and static-only, with no secrets.

### 8. in-toto misinterpretation

An unsigned ACL Statement uses the in-toto Statement envelope but is not itself a signed attestation. A valid signature or GitHub Artifact Attestation proves an issuer/artifact binding under that system; it does not establish software correctness, safe execution, complete contract requirements, or regulatory approval.

Review whether schema, names, documentation, or UI examples could cause a consumer to infer more.

### 9. Signed artifact does not equal software correctness

Confirm the attestation example signs the intended report bytes and uses the expected predicate type. Then test the documentation boundary: a correctly signed `FAILED`, `UNVERIFIABLE`, incomplete, or maliciously authored contract report can still be authentic.

### 10. Package and Action supply chain

Review tag mutability, third-party action references, dependency pins, build isolation, provenance, release assets, Trusted Publishing, and the risk of installing from a movable tag rather than a full commit SHA.

## Reproduction commands

Install the tagged release in a disposable environment:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install \
  "agent-completion-ledger @ git+https://github.com/kodlbegiko/agent-completion-ledger.git@v0.3.0"
agent-completion-ledger --help
```

Run the fixed package reproduction:

```bash
agent-completion-ledger reproduce --output-dir reproduced-results
```

Run the benign security cases from a source checkout:

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
python -m pip install -e ".[dev]"
cat security/reproduction-cases/README.md
```

The full step-by-step commands and expected results are in `security/reproduction-cases/README.md`.

## Finding report format

For a public low-risk finding or documentation defect:

```markdown
Reviewer pseudonymous ID:
ACL version/tag and commit:
Affected file/line:
Expected security property:
Observed result:
Minimal benign reproduction:
Impact and preconditions:
Severity rationale:
Suggested mitigation:
Environment:
```

Do not publish proof-of-concept secrets, private repository content, weaponized payloads, or instructions that directly harm third parties.

## High-risk handling

For a suspected high-risk vulnerability:

1. stop public reproduction at the minimum evidence necessary;
2. use GitHub private security reporting for `kodlbegiko/agent-completion-ledger`;
3. include affected versions and a benign reproduction when possible;
4. do not open a public issue with exploit details;
5. pause high-assurance claims and external recruitment for the affected surface;
6. remediate under the feature-freeze security exception;
7. add regression tests and disclose only after an appropriate fix/review decision.

## Review completion criteria

An independent security review counts only when a non-author supplies at least:

- reviewer pseudonymous ID;
- version/commit;
- reviewed scenarios;
- commands or inspection method;
- findings or explicit no-finding result;
- limitations and environment;
- public evidence link or private-report reference.

Model-only comments, author review, CI success, and this prepared package do not count. Current independent reviewer count remains **0**.
