# Third-party reproduction

Status: **READY FOR EXTERNAL REPRODUCTION — EXTERNAL VALIDATION PENDING**

No independent third party has been fabricated or counted. This document is an invitation and protocol, not evidence that external reproduction has already occurred.

## One-command reproduction

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
python -m pip install -e ".[dev]"
agent-completion-ledger reproduce
```

The command checks Python compatibility, validates the frozen input hash, reruns the v0.1.0 benchmark, validates the aggregate ledger, compares the four primary output hashes, and writes:

- `reproduced-results/reproduction-report.json`
- `reproduced-results/reproduction-summary.md`

## Exit codes

| Code | Meaning |
|---:|---|
| 0 | Complete reproduction; all primary hashes match. |
| 1 | Analysis completed but one or more expected hashes differ. |
| 2 | Environment, manifest, source, or execution error prevented a credible reproduction. |

## Supported automated environments

CI tests Python 3.11, 3.12, and 3.13 on Ubuntu; Python 3.12 on Windows and macOS. The full frozen-data reproduction runs on Ubuntu. Other matrix nodes run deterministic fixture verification, package build, and wheel installation smoke tests.

## What to report

Use the GitHub issue forms or `docs/REPRODUCTION-REPORT-TEMPLATE.md`. Report operating system, Python version, install method, elapsed time, exit code, hash status, whether author help was required, and sanitized obstacles.

Do not submit API keys, credentials, private repository content, personal sensitive data, or private filesystem details.

## Success criterion

A third-party reproduction is counted only when a real external person supplies enough environment and hash evidence to distinguish a successful independent run from an author-run CI job. Until then, the status remains `EXTERNAL VALIDATION PENDING`.
