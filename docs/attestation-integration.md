# GitHub Artifact Attestation integration

This integration uses Agent Completion Ledger to create a deterministic report and experimental predicate, then delegates signing and publication to GitHub's maintained attestation action.

## Example workflow

```yaml
name: completion-evidence-attestation
on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write
  attestations: write

jobs:
  attest-completion-evidence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Calculate trusted contract digest
        id: contract
        shell: bash
        run: echo "sha256=$(sha256sum completion-ledger.yml | cut -d' ' -f1)" >> "$GITHUB_OUTPUT"

      - name: Generate deterministic report
        uses: kodlbegiko/agent-completion-ledger@v0.3.0
        with:
          contract: completion-ledger.yml
          expected-contract-sha256: ${{ steps.contract.outputs.sha256 }}
          format: json
          output: completion-report.json

      - name: Generate in-toto statement
        shell: bash
        run: |
          agent-completion-ledger verify \
            --contract completion-ledger.yml \
            --expected-contract-sha256 "${{ steps.contract.outputs.sha256 }}" \
            --format in-toto \
            --output completion-evidence.intoto.json
          jq '.predicate' completion-evidence.intoto.json > completion-evidence.predicate.json

      - name: Attest report with ACL predicate
        uses: actions/attest@v4
        with:
          subject-path: completion-report.json
          predicate-type: https://github.com/kodlbegiko/agent-completion-ledger/predicate/completion-evidence/v1
          predicate-path: completion-evidence.predicate.json

      - uses: actions/upload-artifact@v4
        with:
          name: completion-evidence
          path: |
            completion-report.json
            completion-evidence.intoto.json
```

For a higher-assurance workflow, pin every third-party action, including ACL, to a reviewed full commit SHA rather than relying only on a movable tag.

## Verification

Download the exact `completion-report.json` bytes and verify the GitHub attestation:

```bash
gh attestation verify completion-report.json \
  -R OWNER/REPOSITORY \
  --predicate-type https://github.com/kodlbegiko/agent-completion-ledger/predicate/completion-evidence/v1
```

To inspect the predicate returned by GitHub CLI:

```bash
gh attestation verify completion-report.json \
  -R OWNER/REPOSITORY \
  --predicate-type https://github.com/kodlbegiko/agent-completion-ledger/predicate/completion-evidence/v1 \
  --format json \
  --jq '.[].verificationResult.statement.predicate'
```

## What is and is not established

The attestation can bind the report artifact digest to a GitHub Actions workflow identity and the supplied predicate. It does not prove that:

- the code is safe or semantically correct;
- the contract captures every relevant acceptance condition;
- an allow-listed command was harmless;
- the repository delivered user value;
- a regulator or auditor approved the result.

ACL does not reimplement Sigstore, OIDC, key management, transparency logs, or attestation verification. Those responsibilities remain with GitHub's attestation service and CLI.

## Pull-request safety

Do not grant `id-token: write` or `attestations: write` to an untrusted fork pull request merely to produce a review preview. Use the read-only static workflow in `docs/workflows/static-untrusted-pr.yml`; attest only trusted-branch outputs after review and merge.
