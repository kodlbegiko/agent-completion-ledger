# Recruitment target rationale

Status: **WAVE 1 SELECTED — NOTHING SENT**

Launch audit date: **2026-07-25 UTC**

## Purpose

This document explains how public repositories were screened for Agent Completion Ledger external validation. It is a target-selection record, not consent, endorsement, adoption evidence, or permission to contact anyone.

The current operational decision is:

```text
READY FOR OWNER OUTREACH
```

Current qualifying counts remain zero for real participants, non-author repositories, independent reproductions, independent security reviewers, outreach sends, and responses.

## Public-data and privacy rule

The audit used only public GitHub repository metadata, public repository files, public contribution/issue policies, public issues, and public commit heads. It did not collect private email addresses, personal sensitive data, private source, credentials, or employer-confidential information.

Repository names identify public projects, not verified individual maintainers. The owner must not infer identity, authority, or consent from a username or organization name.

## Current classification rubric

### `CURRENT HIGH FIT`

- public and not archived;
- current repository head resolves and recent-maintenance evidence remains credible;
- explicit tests/build or deterministic review evidence;
- manageable 30–60 minute task or review-only path;
- relevant coding-agent, developer-tool, repository-processing, or evidence-review context;
- low enough security/privacy burden for public fixtures;
- a plausible public channel exists, subject to same-day policy verification.

### `CURRENT MEDIUM FIT`

The repository is technically plausible but has one or more material frictions: unclear invitation channel, network/provider behavior, database or Kubernetes setup, mixed toolchains, broader scope, maintainer-load risk, or less direct coding-agent context.

### `CURRENT LOW FIT`

Technically credible, but domain consequence, native dependencies, compatibility burden, or setup make a short first-wave pilot disproportionate.

### `NO LONGER SUITABLE`

The repository disappeared, became private/archived, lost required test/build evidence, stopped accepting contributions, or developed a policy/risk conflict. No original target met this condition in the 2026-07-25 launch re-audit.

### `DO NOT CONTACT`

The representative use creates third-party network/legal/security risk, or the project is a large enterprise target excluded from the first wave.

## Launch re-audit result

All original 30 repositories still existed, were public, were not archived, and had a resolvable current head during the audit. That technical status does not authorize contact.

Current classification:

| Classification | Count |
|---|---:|
| `CURRENT HIGH FIT` | 5 |
| `CURRENT MEDIUM FIT` | 21 |
| `CURRENT LOW FIT` | 2 |
| `NO LONGER SUITABLE` | 0 |
| `DO NOT CONTACT` | 2 |
| **Total** | **30** |

Machine-readable per-target status, audit head, contact gate, and Wave 1 role are in `research/external-validation/recruitment-targets.csv`.

## Wave 1 selection

### Five maintainer pilots

1. `tmux-python/tmuxp`
2. `evalstate/fast-agent`
3. `campfirein/byterover-cli`
4. `darrenhinde/OpenAgentsControl`
5. `abinthomasonline/repo2txt`

These provide Python, TypeScript, agent-framework, agent-control, and repository-processing contexts with explicit test/build surfaces and bounded review-only or static-only paths.

### Two independent reproductions

1. `tox-dev/tox`
2. `kislyuk/yq`

These are selected for Python packaging/testing familiarity. The request is to reproduce ACL v0.3.1 from its public repository, not to integrate ACL into their projects.

### Two independent security reviews

1. `zizmorcore/zizmor`
2. `zgosalvez/github-actions-ensure-sha-pinned-actions`

These specialized targets are additions for the security-review role; they are not substitutes used to inflate the original 30-candidate maintainer frame. Their public work is directly relevant to GitHub Actions trust boundaries, permissions, action pinning, and supply-chain review.

Complete target records and exact message references are in `docs/outreach/WAVE-1-TARGETS.md`. Normative messages are in `docs/outreach/WAVE-1-READY-TO-SEND.md`.

## Why several original HIGH FIT candidates were reduced

- `SeemSeam/claude_codex_bridge`: direct fit, but a clearly permitted research-invitation channel was not verified and integration setup raises risk.
- `jhlee0409/claude-code-history-viewer`: relevant, but privacy and desktop/Tauri setup make the first-wave task less bounded.
- `aandrew-me/tgpt`: direct AI CLI context, but network/provider behavior must be isolated.
- `mergestat/mergestat-lite`: deterministic outputs, but organization/SQL setup increases friction.
- `JohannesKaufmann/html-to-markdown`: excellent tests, but verified issue forms are bug/feature-specific and do not clearly permit a research invitation.

Reduction is not a quality judgment. It is a first-wave risk and proportionality decision.

## Reserves

Medium-fit repositories remain reserves only. Replacing a disqualified Wave 1 target requires:

1. recording the disqualification reason;
2. verifying the reserve repository's current policy and public channel;
3. preparing a new individualized message;
4. owner approval;
5. preserving the 30-contact stop rule and avoiding duplicate contact.

Do not substitute `projectdiscovery/uncover` or `NVIDIA/skills`.

## Contact gate

A target marked `APPROVED_FOR_OWNER_REVIEW` is not approved for automatic sending. Before each send, the owner must:

1. reopen the current contribution, issue, support, conduct, security, and AI policies;
2. confirm the exact public channel is appropriate;
3. search for duplicate discussion and prior ACL contact;
4. review the exact invitation;
5. approve it manually;
6. record the send and public link in the outreach log.

Ambiguity means `HOLD`, not permission.

## Safety exclusions

Do not request:

- secrets or credentials;
- private repositories or private code;
- private prompts, conversations, shell history, or local history databases;
- employer-confidential information;
- production database, Kubernetes, cloud, or API access;
- network load/scanning against third parties;
- real sensitive data;
- hidden reasoning or personal sensitive data.

Use public/generated fixtures, fixed task-pack material, reproduction-only work, or `--no-exec` static review whenever possible.

## No-contact and follow-up policy

- one initial message per repository;
- one public channel only;
- no automatic issue/PR creation;
- no cross-platform repeat contact;
- no follow-up before Day 10;
- one follow-up maximum and only where policy permits;
- a decline/removal request ends contact immediately;
- no response is not consent;
- after 30 compliant targeted attempts with no non-author participation, stop expansion and evaluate maintenance mode.

## Evidence boundary

Target selection, invitation quality, release verification, tests, downloads, stars, CI, model review, and author-owned dogfood are not human external-validation results. Only consented `NON-AUTHOR HUMAN` evidence may support H1/H0/H2, adoption, reviewer benefit, or external maintenance willingness.