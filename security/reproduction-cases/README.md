# Independent security review reproduction cases

Status: **BENIGN LOCAL CASES — NOT AN EXPLOIT KIT**

Target release: **v0.3.1**

These cases exercise documented boundaries using only files in this repository, a short local sleep, and a reserved non-routable `.invalid` URL string. Do not point them at third-party systems or run them with secrets.

## Setup

```bash
git clone --branch v0.3.1 --depth 1 \
  https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS examples below write reports under a disposable directory:

```bash
mkdir -p /tmp/acl-security-review
```

Record any platform adaptation rather than silently changing the expected property.

## Case 1 — trusted static success

Expected: `SUPPORTED`, matching contract digest, no command execution.

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
python -m json.tool /tmp/acl-security-review/static-safe.json
```

## Case 2 — contract replacement/digest mismatch

Expected: exit code `2`, integrity-only `UNVERIFIABLE`, and no parsing or execution of mismatched policy.

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

Confirm that the report contains actual/expected digests and does not claim trusted success.

## Case 3 — `--no-exec` cannot upgrade command evidence

The fixture command would fail if executed. Expected: blocking command evidence is `UNVERIFIABLE`, never `SUPPORTED`.

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

## Case 4 — repository-root traversal rejection

Expected: `UNVERIFIABLE`; ACL must not inspect `../outside.txt`.

```bash
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/path-traversal.yml \
  --repo-root security/reproduction-cases/repository \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/path-traversal.json || true
```

## Case 5 — Windows absolute-path rejection

Expected on every OS: `UNVERIFIABLE`; the Windows drive path must not be opened.

```bash
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/windows-absolute.yml \
  --repo-root security/reproduction-cases/repository \
  --no-exec \
  --format json \
  --output /tmp/acl-security-review/windows-absolute.json || true
```

## Case 6 — symlink rejection

Expected: `UNVERIFIABLE`; ACL must not follow the evidence symlink.

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

If ordinary users cannot create symlinks, record the case as unavailable; do not elevate permissions.

## Case 7 — mixed-case remote URL rejection

Expected in v0.3.1: `UNVERIFIABLE` with exit code `2` before Python receives the mixed-case `HTTPS://...` argument. The `.invalid` value must not be contacted.

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

The immutable v0.3.0 release is expected to exhibit the documented affected behavior and must not be used as the patched comparison target.

## Case 8 — subprocess timeout

Expected: timeout/`UNVERIFIABLE` in substantially less than the fixture's two-second sleep.

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

Timing can vary on overloaded runners. Report the environment and measured time rather than discarding a failure.

## Case 9 — command output not copied into reports

Expected: the benign marker must not appear in the JSON report.

```bash
agent-completion-ledger verify \
  --contract security/reproduction-cases/contracts/report-nondisclosure.yml \
  --repo-root security/reproduction-cases/repository \
  --format json \
  --output /tmp/acl-security-review/report-nondisclosure.json
! grep -q ACL_BENIGN_OUTPUT_MARKER_DO_NOT_REPORT \
  /tmp/acl-security-review/report-nondisclosure.json
```

This tests stdout/stderr omission only. Paths, repository identity, task IDs, assertion IDs, and messages may still reveal internal names.

## Case 10 — in-toto interpretation

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

Expected interpretation: structured evidence only. It does not establish signer identity, runner trust, software correctness, compliance, or absence of later tampering.

## Report template

```markdown
Reviewer pseudonymous ID:
ACL tag/commit:
Operating system and Python version:
Case ID:
Expected security property:
Observed result:
Exact reproduction command:
Affected file/line:
Severity rationale:
Suggested mitigation:
Public evidence link or private report reference:
```

High-risk findings must use GitHub private security reporting for `kodlbegiko/agent-completion-ledger`. Do not publish exploit details, credentials, private source, or third-party targets.