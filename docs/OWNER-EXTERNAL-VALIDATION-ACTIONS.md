# Owner actions: Wave 1 external validation

Status:

```text
EXTERNAL VALIDATION IN PROGRESS
```

Current verified operational counts:

```text
Real participants: 0
Non-author repositories: 0
Independent reproductions: 0
Independent security reviewers: 0
Targeted outreach sent: 1
Responses: 0
```

First sent record:

```text
W1-M1 — tmux-python/tmuxp
GitHub Discussions / General
https://github.com/tmux-python/tmuxp/discussions/1078
SENT — AWAITING RESPONSE
```

The owner remains the only person authorized to send Wave 1 messages. No workflow, bot, scheduled task, bulk tool, or agent may dispatch them. Sending an invitation does not create a participant or external-evidence result.

## Files to review

Before each remaining outreach action, read:

- `docs/outreach/WAVE-1-TARGETS.md`;
- `docs/outreach/WAVE-1-READY-TO-SEND.md`;
- `research/external-validation/outreach-log.csv`;
- `docs/EXTERNAL-VALIDATION-PROTOCOL.md`;
- `research/external-validation/preregistration.md`;
- `docs/THIRD-PARTY-REPRODUCTION.md`;
- `docs/INDEPENDENT-SECURITY-REVIEW.md`.

Do not edit the preregistered research question, H1/H0/H2, effect thresholds, exclusions, fixed task pack, or participant-balanced primary analysis after inspecting human outcomes.

## Per-target approval procedure

Perform these steps independently for every unsent target:

1. Confirm the repository still exists, is public, and is not archived.
2. Check its latest activity and confirm the proposed request remains proportionate.
3. Read the current contribution guide, issue/discussion templates, code of conduct, support policy, security policy, and AI-use policy.
4. Confirm that the selected public channel permits a research, reproduction, or security-review request.
5. Search existing issues and discussions for the same ACL request or a substantially similar request.
6. Search `outreach-log.csv` for prior contact to the repository or maintainer.
7. Review the exact personalized invitation.
8. Confirm the message still states uncertainty, time estimate, no-secrets boundary, voluntary participation, withdrawal, non-endorsement, no automatic PR, and non-standard status.
9. Record owner approval before sending.
10. Send manually through exactly one approved public channel.
11. Immediately record attempt number, target, role, date, channel, public link, and response state.
12. Do not send a second message before the follow-up rule permits it.
13. Stop immediately if the maintainer declines, asks for removal, closes the request as inappropriate, or states that the channel is not permitted.

If any check is ambiguous, mark the target `HOLD` and do not send.

## Wave 1 order and current progress

### Day 1

1. `W1-M1` — `tmux-python/tmuxp` — maintainer pilot — **SENT; AWAITING RESPONSE**.
2. `W1-M2` — `evalstate/fast-agent` — maintainer pilot — **NOT SENT**.
3. `W1-S1` — `zizmorcore/zizmor` — independent security review — **NOT SENT**.

### Day 3

4. `W1-M3` — `campfirein/byterover-cli` — maintainer pilot — **NOT SENT**.
5. `W1-M4` — `darrenhinde/OpenAgentsControl` — maintainer pilot — **NOT SENT**.
6. `W1-R1` — `tox-dev/tox` — independent reproduction — **NOT SENT**.

### Day 5

7. `W1-M5` — `abinthomasonline/repo2txt` — maintainer pilot — **NOT SENT**.
8. `W1-R2` — `kislyuk/yq` — independent reproduction — **NOT SENT**.
9. `W1-S2` — `zgosalvez/github-actions-ensure-sha-pinned-actions` — independent security review — **NOT SENT**.

Do not replace a disqualified target without recording the reason and obtaining owner approval for a reserve target.

## Follow-up rule

A follow-up is permitted only when all conditions are true:

- the existing Day 10-or-later timing rule has been reached;
- the repository's current public policy permits a follow-up;
- the initial message was not declined, removed, locked, or marked inappropriate;
- no response requested no further contact;
- no other channel was used;
- `follow_up_allowed` is recorded as `yes`.

One follow-up is the maximum. It must be shorter than the initial message and contain an easy decline option. No reply after that becomes `NO RESPONSE — CLOSED`.

## Outreach log requirements

Each attempt must record:

```text
attempt_number
wave_id
target_repository
role
fit
channel
policy_checked_at_utc
owner_approved
sent_at_utc
public_link
response_state
responder_class
participant_id
follow_up_allowed
follow_up_sent_at_utc
withdrawn_at_utc
notes
```

Allowed `responder_class` values:

```text
AUTHOR
AUTOMATION
MODEL
NON-AUTHOR HUMAN
UNKNOWN
```

Only `NON-AUTHOR HUMAN` may count toward external validation. A sent invitation, bot acknowledgment, model review, CI output, repository-owner self-comment, star, reaction, or automated response does not count.

Allowed response states include:

```text
SENT — AWAITING RESPONSE
INTERESTED — CONSENT PENDING
CONSENTED — SCHEDULING
DECLINED — CLOSED
NO RESPONSE — FOLLOW-UP ELIGIBLE
NO RESPONSE — CLOSED
CHANNEL INAPPROPRIATE — CLOSED
WITHDRAWN — CLOSED
COMPLETED
```

Never backfill a sent date, public link, identity class, consent state, or outcome from memory. Use a verifiable record or leave the field blank and state the limitation.

## Handling a maintainer-pilot response

When a real non-author maintainer expresses interest:

1. Confirm that the responder controls or meaningfully reviews the relevant repository; do not infer that solely from a username.
2. Send the consent/privacy material before collecting task outcomes.
3. Explain that the fixed task pack can be reviewed without installing ACL.
4. Offer `--no-exec` static-only mode.
5. Confirm that no private code, secrets, employer-confidential material, sensitive personal data, or hidden reasoning will be submitted.
6. Assign a pseudonymous participant ID only after consent.
7. Store the identity/contact mapping separately from study responses.
8. Freeze and record protocol, task-pack, assignment schedule, and data-template hashes.
9. Assign the counterbalanced condition order and record the random seed.
10. Preserve the original agent summary and the decision recorded before the ledger is shown.
11. Do not interpret `SUPPORTED` as an instruction to merge.
12. Honor withdrawal according to the consent terms.

## Handling reproduction and security responses

An independent reproduction counts only when a verified `NON-AUTHOR HUMAN` reports ACL version, environment, exact commands, elapsed time, exit code, expected and observed status/hashes, assistance required, sanitized blockers, and reviewable evidence.

For security review, use only benign ACL fixtures. No third-party targets, credentials, real secrets, employer-confidential code, public weaponized exploit, sandbox claim, or claim that signed evidence proves correctness is permitted. Suspected high-risk findings go through ACL's GitHub private security reporting route and pause the affected outreach surface pending triage.

## Product boundary

Do not:

- develop v0.4.0;
- publish a new version;
- add assertions, adapters, dashboard, SaaS, or automated outreach;
- reinterpret a lack of replies as a product defect;
- alter hypotheses, thresholds, exclusions, or analysis to obtain a positive result;
- count author, automation, model, bot, CI, synthetic, or unverified activity as human evidence.

Only a validated blocking usability, packaging, cross-platform, or security defect may use the existing v0.3.x feature-freeze exception, and any fix must be minimal.
