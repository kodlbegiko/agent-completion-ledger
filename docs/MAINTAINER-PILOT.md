# Maintainer pilot

Status: **RECRUITMENT PREPARED — REAL PARTICIPANTS 0**

## Goal

Test whether ACL can be installed, configured, and used by a non-author maintainer without direct author assistance, and whether its report changes or clarifies a real coding-task review.

## Eligibility

- You maintain or regularly review a software repository.
- You are not an author of Agent Completion Ledger.
- You can select a completed or recently reviewed coding task that contains no confidential information.

## Pilot steps

1. Read `ADOPTION-QUICKSTART.md` without author assistance.
2. Record setup start time.
3. Install from the released GitHub tag.
4. Create one contract for one real coding task.
5. Record contract authoring time and non-comment line count.
6. Run locally, then add either the static PR workflow or a trusted-branch workflow.
7. Record CI duration before and after adding ACL.
8. Review the coding task first from its ordinary summary/diff.
9. Record an initial accept/reject/insufficient-evidence decision.
10. Open the ACL report and record whether the decision, confidence, ambiguity, or first blocking issue changes.
11. Remove ACL if you do not want to retain it; removal is a valid pilot outcome.

## Required report

Copy this template into the recruitment/tracking issue:

```markdown
Repository: public URL or "private/not disclosed"
Participant ID: pseudonym
Task family: Python / Node / other
ACL version:
Setup minutes:
Contract authoring minutes:
Contract non-comment lines:
Baseline CI seconds:
ACL CI seconds:
Initial decision: accept / reject / insufficient evidence
Decision after report: accept / reject / insufficient evidence
Did the report change the decision? yes / no
First blocking issue found faster? yes / no / not applicable
Ambiguity before (1–5):
Ambiguity after (1–5):
Would maintain the contract (1–5):
Security or privacy concern:
Most confusing step:
Removal completed? yes / no / retained
```

## Evidence standard

A public integration counts only when a non-author repository contains a working contract and CI run or a reproducible local report tied to a commit. A private integration may contribute anonymized timing/usability data but cannot be independently inspected unless the maintainer shares sufficient redacted evidence.

## Safety

- Do not paste secrets, private code, client names, or credentials.
- Start with `--no-exec` for untrusted pull requests.
- Never use `pull_request_target` to execute fork code.
- Use read-only permissions and disposable runners.
- Contract hash pinning protects the selected contract bytes, not the safety of the commands they invoke.

## Exit criteria

The project may report external-validation progress only from actual non-author evidence. Synthetic dry-run records, project-author dogfood, and model-generated reviews do not count.
