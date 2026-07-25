# Owner actions: Wave 1 external validation launch

Status:

```text
READY FOR OWNER OUTREACH
```

No external message has been sent. Current qualifying counts remain:

```text
Real participants: 0
Non-author repositories: 0
Independent reproductions: 0
Independent security reviewers: 0
Targeted outreach sent: 0
```

The owner is the only person authorized to send Wave 1 messages. No workflow, bot, scheduled task, bulk tool, or agent may dispatch them.

## 1. Files to review

Before any outreach, read:

- `docs/outreach/WAVE-1-TARGETS.md`;
- `docs/outreach/WAVE-1-READY-TO-SEND.md`;
- `research/external-validation/outreach-log.csv`;
- `docs/EXTERNAL-VALIDATION-PROTOCOL.md`;
- `research/external-validation/preregistration.md`;
- `docs/THIRD-PARTY-REPRODUCTION.md`;
- `docs/INDEPENDENT-SECURITY-REVIEW.md`.

Do not edit the preregistered research question, H1/H0/H2, effect thresholds, exclusions, fixed task pack, or participant-balanced primary analysis after inspecting human outcomes.

## 2. Per-target approval procedure

Perform these steps independently for every target:

1. Open the target repository and confirm it still exists, is public, and is not archived.
2. Check its latest activity and confirm the proposed request remains proportionate.
3. Read the current contribution guide, issue templates, code of conduct, support policy, security policy, and any AI-use policy.
4. Confirm the documented public channel permits a research, reproduction, or security-review request.
5. Search existing issues/discussions for the same ACL request or a substantially similar discussion.
6. Search `research/external-validation/outreach-log.csv` for any prior contact to the repository or maintainer.
7. Review the exact personalized invitation in `WAVE-1-READY-TO-SEND.md`.
8. Confirm the message still states uncertainty, time estimate, no-secrets boundary, voluntary participation, withdrawal, non-endorsement, no automatic PR, and non-standard status.
9. Record owner approval locally before sending.
10. Send manually through the one approved public channel.
11. Immediately record attempt number, target, role, date, channel, public link, and response state.
12. Do not send a second message before the follow-up rule permits it.
13. Stop immediately if the maintainer declines, asks for removal, closes the request as inappropriate, or indicates that the channel is not permitted.

If any check is ambiguous, mark the target `HOLD` and do not send.

## 3. Wave 1 order

Use this order unless a same-day policy check disqualifies a target. Do not replace a disqualified target without recording the reason and reviewing the reserve list.

### Day 1 — three invitations

1. `W1-M1` — `tmux-python/tmuxp` — maintainer pilot.
2. `W1-M2` — `evalstate/fast-agent` — maintainer pilot.
3. `W1-S1` — `zizmorcore/zizmor` — independent security review.

### Day 3 — three invitations

4. `W1-M3` — `campfirein/byterover-cli` — maintainer pilot.
5. `W1-M4` — `darrenhinde/OpenAgentsControl` — maintainer pilot.
6. `W1-R1` — `tox-dev/tox` — independent reproduction.

### Day 5 — remaining three invitations

7. `W1-M5` — `abinthomasonline/repo2txt` — maintainer pilot.
8. `W1-R2` — `kislyuk/yq` — independent reproduction.
9. `W1-S2` — `zgosalvez/github-actions-ensure-sha-pinned-actions` — independent security review.

### Day 10 or later — at most one follow-up

A follow-up is permitted only when all conditions are true:

- at least five full days have elapsed since the applicable Day 5 send and the follow-up date is Day 10 or later;
- the repository's public policy permits a follow-up;
- the initial message was not declined, removed, locked, or marked inappropriate;
- no response requested no further contact;
- no other channel was used;
- `follow_up_allowed` is recorded as `yes` in the log.

One follow-up is the maximum. It must be shorter than the initial message and contain an easy decline option. No reply after that means `NO RESPONSE — CLOSED`.

## 4. Outreach log requirements

Before the first send, extend or maintain `research/external-validation/outreach-log.csv` so each attempt can record:

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

Only `NON-AUTHOR HUMAN` may count toward external validation. A bot acknowledgment, model review, CI output, repository-owner self-comment, or automated issue response does not count.

Suggested response states:

```text
NOT SENT
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

Never backfill a sent date, link, identity class, or consent state from memory. Use the public record or leave the field blank.

## 5. Handling a maintainer-pilot response

When a real non-author maintainer expresses interest:

1. Confirm the responder controls or meaningfully reviews the relevant repository; do not infer identity from a username alone.
2. Send the consent/privacy material before collecting task outcomes.
3. Explain that they may review the fixed task pack without installing ACL.
4. Offer `--no-exec` static-only mode.
5. Confirm no private code, secrets, employer-confidential material, sensitive personal data, or hidden reasoning will be submitted.
6. Assign a pseudonymous participant ID only after consent.
7. Store the identity/contact mapping separately from study responses.
8. Freeze and record protocol, task-pack, assignment schedule, and data-template hashes.
9. Assign the counterbalanced condition order and record the random seed.
10. Preserve the original agent summary and the decision recorded before the ledger is shown.
11. Do not interpret `SUPPORTED` as an instruction to merge.
12. Honor withdrawal according to the consent terms.

## 6. Handling an independent reproduction response

A reproduction counts only when a `NON-AUTHOR HUMAN` reports enough evidence to identify:

- ACL version/tag and commit;
- operating system and Python version;
- exact install/reproduction command;
- elapsed time and process exit code;
- expected and observed hash/status;
- whether author help was required;
- sanitized warnings or blockers;
- a public evidence link or reviewable report.

Use v0.3.1. Do not count author CI, the release smoke test, synthetic rows, or a model-run reproduction.

## 7. Handling an independent security-review response

Direct reviewers to `docs/INDEPENDENT-SECURITY-REVIEW.md` and `security/reproduction-cases/README.md`.

The review must remain benign:

- no third-party targets;
- no credentials or real secrets;
- no employer-confidential code;
- no public weaponized exploit;
- no claim that ACL is a sandbox;
- no claim that signed evidence equals software correctness.

For a suspected high-risk issue:

1. stop at the minimum benign evidence;
2. use GitHub private security reporting for `kodlbegiko/agent-completion-ledger`;
3. pause outreach for the affected execution surface;
4. do not publish exploit details;
5. use the feature-freeze security exception only after triage;
6. add a regression test and patch only when the finding is validated;
7. resume affected recruitment only after a safe fix/review decision.

## 8. Real repository integration measurements

For each consenting non-author integration, use `research/external-validation/adoption-integration-template.csv` and measure rather than estimate:

- pseudonymous participant ID;
- repository type and language;
- task family and ACL version;
- installation time;
- contract authoring time;
- contract line count and assertion count;
- baseline CI time and CI-with-ACL time;
- decision before and after ledger;
- whether the decision changed;
- false acceptance and false rejection against agreed ground truth;
- ambiguity before/after;
- time to first blocking evidence;
- maintainer willingness to retain the contract;
- number of author-assistance interventions;
- subjective conditions that could not be automated;
- security/privacy concerns.

Do not collect secrets, private source, employer-confidential information, hidden reasoning, sensitive personal data, or non-consensual identity information.

## 9. Analysis gate

Do not run or publish confirmatory human-effect analysis until at least five eligible participants complete the fixed study.

Before analysis:

1. validate consent and data schema;
2. exclude templates, synthetic dry runs, author-owned rows, model-only rows, duplicates, and documented exclusions;
3. record missing data and protocol deviations;
4. leave preregistration and thresholds unchanged;
5. use participant-balanced condition summaries as the primary analysis;
6. keep pooled row-level results as sensitivity analysis only;
7. show all favorable and unfavorable H1 thresholds;
8. distinguish confirmatory findings from exploratory integration observations.

With zero eligible human rows, the only valid operational conclusion is:

```text
READY FOR OWNER OUTREACH
```

## 10. PyPI status

PyPI is **OPTIONAL ADOPTION FRICTION REDUCTION**, not a prerequisite for Wave 1.

The verified v0.3.1 GitHub tag and Release assets are sufficient for task-pack review, Git-tag installation, reproduction, and security review. PyPI remains unpublished and must not be represented otherwise.

Remaining PyPI owner work is documented in `docs/OWNER-PYPI-PUBLISH-ACTIONS.md`:

- configure protected `testpypi` and `pypi` environments;
- register Trusted Publishers;
- run `publish-package` with `tag = v0.3.1`;
- verify TestPyPI before approving production;
- verify a clean production `pip install agent-completion-ledger==0.3.1` before changing README installation guidance.

Do not delay Wave 1 solely because PyPI is pending.

## 11. Decision and stop rules

Do not select `EXTERNAL VALUE SUPPORTED` until every preregistered GO requirement is met.

Do not change thresholds to avoid a negative result. After 30 compliant targeted contacts with no non-author participation, or when the other STOP conditions are met, stop feature expansion and evaluate:

```text
RESEARCH COMPLETE — MAINTENANCE MODE
```

Until a real non-author response is consented and enrolled, the status remains:

```text
READY FOR OWNER OUTREACH
```