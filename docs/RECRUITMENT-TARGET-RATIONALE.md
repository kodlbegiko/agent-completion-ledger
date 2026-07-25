# Recruitment target rationale

Status: **OWNER REVIEW REQUIRED — NO OUTREACH SENT**

Candidate count: **30 public candidates**

Selection date: **2026-07-25 UTC**

Source file: `research/external-validation/recruitment-targets.csv`

## Purpose

The matrix identifies public repositories or maintainer types that could provide a bounded 30–60 minute pilot of Agent Completion Ledger. It is a research sampling frame, not a marketing list. Inclusion does not authorize contact, imply endorsement, or prove willingness to participate.

## Public-data method

Candidates were selected from public GitHub repository search results using filters equivalent to:

```text
pushed after 2026-04-01 or 2026-05-01
archived:false
public repository
moderate repository size
CLI or developer-tools topic
Python, TypeScript, Go, or repository-tooling context
```

The audit did not collect private email addresses, scrape personal websites, or infer private employment details. The only proposed contact surfaces are public GitHub Issues or Discussions, and those may be used only after explicit repository-owner approval for this mission.

A repository matching a search filter is only evidence of recent public activity at search time. Before any contact, the owner must re-check its latest commit, contribution policy, issue templates, code of conduct, and whether research requests are permitted.

## Fit rubric

### HIGH FIT

- recent public maintenance;
- clear tests or build outputs;
- bounded task suitable for 30–60 minutes;
- strong coding-agent, repository automation, or deterministic CLI context;
- no need for secrets or private source code;
- expected contract can be authored with ordinary file/test/build evidence.

### MEDIUM FIT

The repository appears usable, but setup complexity, reviewer availability, domain knowledge, native dependencies, network behavior, or larger project scope may increase friction.

### LOW FIT

A safe task may exist, but the pilot is likely to exceed the time budget, require unusual domain knowledge, or create higher security/privacy burden.

### EXCLUDE

Do not contact under the current protocol. The repository is a large-enterprise target, normally performs potentially harmful external scanning, requires unsafe credentials, or otherwise conflicts with the low-risk pilot.

## Distribution

| Fit | Count |
|---|---:|
| HIGH FIT | 10 |
| MEDIUM FIT | 16 |
| LOW FIT | 2 |
| EXCLUDE | 2 |
| Total | 30 |

## Top 10 HIGH FIT candidates

1. `tmux-python/tmuxp` — Python CLI, pytest evidence, and public coding-agent guidance.
2. `evalstate/fast-agent` — AI-agent framework with direct completion-review relevance.
3. `SeemSeam/claude_codex_bridge` — coding-agent bridge with bounded configuration/routing tasks.
4. `campfirein/byterover-cli` — TypeScript developer CLI with build/test acceptance surfaces.
5. `darrenhinde/OpenAgentsControl` — agent-control repository where claim/evidence separation is central.
6. `jhlee0409/claude-code-history-viewer` — coding-agent tooling that can use sanitized fixtures.
7. `abinthomasonline/repo2txt` — deterministic repository-processing CLI with low setup friction.
8. `aandrew-me/tgpt` — Go AI CLI that can be piloted with offline/mocked tasks.
9. `mergestat/mergestat-lite` — Git analytics CLI with repository/query evidence.
10. `JohannesKaufmann/html-to-markdown` — deterministic Go conversion library with fixture-based ground truth.

Personalized drafts for these ten candidates are in `docs/outreach/personalized-target-drafts.md`. They are drafts only and are marked `NOT SENT`.

## Required pre-contact review

For each proposed contact, the owner must record:

- repository still active and not archived;
- public contribution/research requests are permitted;
- no recent maintainer notice asking users not to open support/research issues;
- proposed task is genuinely bounded and does not require secrets;
- no prior contact to the same maintainer for this mission;
- message is individualized and uses the correct public channel;
- contact count is incremented in the outreach log;
- withdrawal or no-response is respected.

## Contact limits

- Maximum one initial message per repository.
- Maximum one follow-up only when the maintainer explicitly invites it or the owner has adopted a documented follow-up policy.
- No automated issue creation, email sending, tagging, or cross-posting.
- Stop recruitment expansion after 30 targeted contacts if no non-author agrees; evaluate `RESEARCH COMPLETE — MAINTENANCE MODE` rather than increasing volume.

## Excluded candidates

### `projectdiscovery/uncover`

Excluded because ordinary use involves external security/attack-surface data. A representative pilot could create network, authorization, or third-party risk; a nonrepresentative offline task would not answer the research question well.

### `NVIDIA/skills`

Excluded because it is large-enterprise-owned and unsuitable for a small independent pilot under the stated selection rules. No unsolicited contact is proposed.

## Interpretation limits

The matrix does not establish a random sample, market demand, adoption intent, or maintainer consent. It is designed to make recruitment targeted, auditable, non-automated, and stoppable.
