# Independent security review reproduction cases

Status: **BENIGN LOCAL CASES — NOT AN EXPLOIT KIT**

These cases exercise documented boundaries using only files in this repository, a short local sleep, and a non-routable `.invalid` URL string. They must not be pointed at third-party systems or used with secrets.

## Setup

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
git switch research/external-validation-operations
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

All commands below write reports under a disposable temporary directory.

```bash
mkdir -p /tmp/acl-security-review
```

## Case 1: trusted static success

Expected result: `SUPPORTED` with a matching contract digest and no command execution.

```bash
CONTRACT=security/reproduction-cases/contracts/static-safe.yml
DIGEST="$(python -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$CONTRACT")"
agent-completion-ledger verify \
  --contract "$CONTRACT" \
  --repo-root security/reproduction-cases/repository \
  --expected-contract-sha256 "$DIGEST" \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/static-safe.json
```

Inspect:

```bash
python -m json.tool /tmp/acl-security-review/static-safe.json
```

## Case 2: contract replacement / digest mismatch

Expected result: exit code `2`, integrity-only `UNVERIFIABLE`, and no parsing/execution of mismatched policy.

```bash
set +e
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/static-safe.yml \
  --repo-root security/reproduction-cases/repository \
  --expected-contract-sha256 0000000000000000000000000000000000000000000000000000000000000000 \
  --format json \
  --output /tmp/acl-security-review/digest-mismatch.json
STATUS=$?
set -e
test "$STATUS" -eq 2
```

Reviewers should confirm that the report contains the actual and expected digest and does not claim trusted success.

## Case 3: `--no-exec` does not upgrade command evidence

The fixture command would fail if executed. Expected result under `--no-exec`: blocking command evidence is `UNVERIFIABLE`, not `SUPPORTED`.

```bash
CONTRACT=security/reproduction-cases/contracts/interpreter-disabled.yml
DIGEST="$(python -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$CONTRACT")"
set +e
agent-completion-ledger verify \
  --contract "$CONTRACT" \
  --repo-root security/reproduction-cases/repository \
  --expected-contract-sha256 "$DIGEST" \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/interpreter-disabled.json
STATUS=$?
set -e
test "$STATUS" -ne 0
```

## Case 4: repository-root traversal rejection

Expected result: `UNVERIFIABLE`; ACL must not inspect `../outside.txt`.

```bash
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/path-traversal.yml \
  --repo-root security/reproduction-cases/repository \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/path-traversal.json || true
```

## Case 5: Windows absolute-path rejection

Expected result on every operating system: `UNVERIFIABLE`; the Windows drive path must not be opened.

```bash
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/windows-absolute.yml \
  --repo-root security/reproduction-cases/repository \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/windows-absolute.json || true
```

## Case 6: symlink rejection

Create a symlink inside the disposable fixture directory. Expected result: `UNVERIFIABLE`; ACL must not follow it.

```bash
ln -s public.txt security/reproduction-cases/repository/link.txt
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/symlink.yml \
  --repo-root security/reproduction-cases/repository \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/symlink.json || true
rm security/reproduction-cases/repository/link.txt
```

On systems where ordinary users cannot create symlinks, record the case as unavailable rather than changing permissions.

## Case 7: mixed-case remote URL rejection

Expected result: `UNVERIFIABLE` with exit code `2` before Python receives the mixed-case `HTTPS://...` argument. The `.invalid` domain is reserved for examples and must not be contacted.

```bash
set +e
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/remote-url.yml \
  --repo-root security/reproduction-cases/repository \
  --format json \
  --output /tmp/acl-security-review/remote-url.json
STATUS=$?
set -e
test "$STATUS" -eq 2
```

## Case 8: subprocess timeout

Expected result: timeout/`UNVERIFIABLE` in substantially less than the two-second sleep.

```bash
python - <<'PY'
import subprocess
import time

started = time.monotonic()
completed = subprocess.run(
    [
        "agent-completion-ledger",
        "verify",
        "--contract",
        "security/reproduction-cases/contracts/timeout.yml",
        "--repo-root",
        "security/reproduction-cases/repository",
        "--format",
        "json",
        "--output",
        "/tmp/acl-security-review/timeout.json",
    ],
    check=False,
)
elapsed = time.monotonic() - started
print({"exitCode": completed.returncode, "elapsedSeconds": elapsed})
assert elapsed < 1.5
PY
```

Timing can vary on overloaded runners. A failure of the conservative 1.5-second bound should be reported with environment details, not silently discarded.

## Case 9: command output is not copied into reports

The command emits a benign marker. Expected result: verification may be `SUPPORTED`, but the marker must not appear in the JSON report.

```bash
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/report-nondisclosure.yml \
  --repo-root security/reproduction-cases/repository \
  --format json \
  --output /tmp/acl-security-review/report-nondisclosure.json
! grep -q ACL_BENIGN_OUTPUT_MARKER_DO_NOT_REPORT \
  /tmp/acl-security-review/report-nondisclosure.json
```

This checks only stdout/stderr omission. Paths, task IDs, assertion IDs, repository identity, and messages can still reveal internal names.

## Case 10: in-toto statement interpretation

Generate an unsigned statement:

```bash
CONTRACT=security/reproduction-cases/contracts/static-safe.yml
DIGEST="$(python -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$CONTRACT")"
agent-completion-ledger verify \
  --contract "$CONTRACT" \
  --repo-root security/reproduction-cases/repository \
  --expected-contract-sha256 "$DIGEST" \
  --no-exec \
  --format in-toto \
  --output /tmp/acl-security-review/static-safe.intoto.json
```

Expected interpretation: the file is structured evidence only. It does not establish signer identity, runner trust, software correctness, compliance, or absence of tampering after generation.

## Reporting template

```markdown
Reviewer pseudonymous ID:
ACL tag/commit:
Operating system and Python version:
Case ID:
Expected security property:
Observed result:
Reproduction command:
Affected file/line:
Severity rationale:
Suggested mitigation:
Public or private report:
```

High-risk findings must be submitted through GitHub private security reporting. Do not publish exploit details, credentials, private source code, or third-party targets.
