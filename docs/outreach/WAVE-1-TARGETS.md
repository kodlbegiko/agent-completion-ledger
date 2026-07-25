# Wave 1 external validation targets

Status: **NOT SENT — OWNER REVIEW REQUIRED**

Audit date: **2026-07-25 UTC**

Operational decision: **READY FOR OWNER OUTREACH**

This is a manual research-outreach plan, not a marketing list. Inclusion does not imply consent, endorsement, adoption, or willingness to participate. No email address was collected. No message, issue, pull request, tag, or social post was sent by this preparation work.

## Selection rules

Wave 1 contains exactly:

- five maintainer-pilot candidates;
- two independent-reproduction candidates;
- two independent-security-review candidates.

Every initial message requires a same-day owner check of the repository's current contribution policy, issue templates, code of conduct, prior-contact history, and whether the proposed public channel permits a research invitation. If the channel is unclear, **do not send**.

## Wave 1 dispatch matrix

| ID | Public repository/profile | Role | Public contact channel | Estimated effort | Status |
|---|---|---|---|---:|---|
| W1-M1 | `tmux-python/tmuxp` | Maintainer pilot | GitHub Issue after same-day policy check | 30–60 min | `NOT SENT` |
| W1-M2 | `evalstate/fast-agent` | Maintainer pilot | GitHub Issue after duplicate/policy check | 30–60 min | `NOT SENT` |
| W1-M3 | `campfirein/byterover-cli` | Maintainer pilot | GitHub Issue after issue-template check | 30–60 min | `NOT SENT` |
| W1-M4 | `darrenhinde/OpenAgentsControl` | Maintainer pilot | GitHub Question Issue | 30–60 min | `NOT SENT` |
| W1-M5 | `abinthomasonline/repo2txt` | Maintainer pilot | GitHub Issue only if a general request is permitted | 30–60 min | `NOT SENT` |
| W1-R1 | `tox-dev/tox` | Independent reproduction | GitHub Discussion or Issue, whichever policy permits | 15–30 min | `NOT SENT` |
| W1-R2 | `kislyuk/yq` | Independent reproduction | GitHub Issue Tracker after policy check | 15–30 min | `NOT SENT` |
| W1-S1 | `zizmorcore/zizmor` | Independent security review | GitHub Issue only after reading its AI/contribution policy | 30–60 min | `NOT SENT` |
| W1-S2 | `zgosalvez/github-actions-ensure-sha-pinned-actions` | Independent security review | GitHub Issue after policy check | 30–60 min | `NOT SENT` |

The exact normative messages are sections `W1-M1` through `W1-S2` in `WAVE-1-READY-TO-SEND.md`. They must be sent without silently removing the uncertainty, privacy, withdrawal, non-endorsement, or non-standard language.

## Maintainer-pilot candidates

### W1-M1 — `tmux-python/tmuxp`

- **Role:** maintainer pilot.
- **Current evidence:** public, not archived, current head `1d906960779c0b5fe4d582629497f878ed99849e` resolved during the launch audit.
- **Fit rationale:** Python CLI with explicit `ruff`, `mypy`, and `pytest` contributor commands and public coding-agent guidance. A parser or configuration-validation case can use public fixtures without personal tmux data.
- **Relevant policy:** `.github/contributing.md` asks contributors to discuss changes before making them and explicitly lists formatting, type-checking, and test commands.
- **Pilot path:** fixed task-pack review with no install, or a bounded static/test contract using public fixtures.
- **Safety notes:** never request shell history, personal tmux configuration, credentials, or private repositories.
- **Exact invitation:** `W1-M1` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

### W1-M2 — `evalstate/fast-agent`

- **Role:** maintainer pilot.
- **Current evidence:** public, not archived, current head `f848d91a53b6df05f12bb288532c871cc0cc7b84` resolved during the launch audit.
- **Fit rationale:** direct agent/MCP context. `pyproject.toml` defines unit, integration, simulated-endpoint, and e2e markers, allowing an offline bounded task or review-only session.
- **Relevant policy:** the public issue tracker currently contains technical questions and feature proposals. The owner must check for duplicates and any updated research-request policy immediately before sending.
- **Pilot path:** fixed task-pack review, static-only mode, or a small configuration/tool-registration case using unit or simulated-endpoint tests.
- **Safety notes:** no model API keys, private prompts, conversations, live provider calls, OAuth credentials, or production services.
- **Exact invitation:** `W1-M2` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

### W1-M3 — `campfirein/byterover-cli`

- **Role:** maintainer pilot.
- **Current evidence:** public, not archived, current head `1052ac1a5dd0fde4da8693d4712064f7876c269c` resolved during the launch audit.
- **Fit rationale:** TypeScript CLI with documented `npm ci`, build, lint, type-check, unit-test, and integration-test surfaces. Its output and CLI-option tasks are suitable for explicit acceptance evidence.
- **Relevant policy:** `CONTRIBUTING.md` welcomes issue reports and contributions and documents the test workflow. Owner must still check the current issue form before sending.
- **Pilot path:** review-only task pack or one bounded CLI option/output-format case using in-memory/mocked tests.
- **Safety notes:** no workspace content, access tokens, proprietary repositories, daemon data, submodule credentials, or live LLM calls.
- **Exact invitation:** `W1-M3` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

### W1-M4 — `darrenhinde/OpenAgentsControl`

- **Role:** maintainer pilot.
- **Current evidence:** public, not archived, current head `37ca233fa5597a5abb90cba73165deafffe0344f` resolved during the launch audit.
- **Fit rationale:** agent-control and evaluation repository where separating generated claims from repository evidence is directly relevant.
- **Relevant policy:** the repository documents Question, Feature Request, Bug, and Improvement issue types and has a public contribution/evaluation workflow.
- **Pilot path:** fixed task-pack review or a small policy/configuration task beginning with static-only evidence.
- **Safety notes:** do not execute untrusted plugins, connect agent services, or request API keys, private prompts, or private code.
- **Exact invitation:** `W1-M4` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

### W1-M5 — `abinthomasonline/repo2txt`

- **Role:** maintainer pilot.
- **Current evidence:** public, not archived, current head `e22512fc7552b1a1edf09604f27d7f80dc80a656` resolved during the launch audit.
- **Fit rationale:** deterministic repository-processing application with documented build, unit/E2E, type-check, lint, and CI commands. Its contribution guide describes a privacy-first browser-processing boundary.
- **Relevant policy:** `CONTRIBUTING.md` is public and detailed, but the owner must confirm that a general research request is permitted by the current issue forms before sending.
- **Pilot path:** fixed task-pack review or a filtering/output-order task using a generated public fixture.
- **Safety notes:** no private repository, provider token, private source, local archive, or user content.
- **Exact invitation:** `W1-M5` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

## Independent-reproduction candidates

### W1-R1 — `tox-dev/tox`

- **Role:** independent reproduction; no integration request.
- **Current evidence:** public, not archived, current head `ccb12fc2e1bb9df0da860be4af175e9b97949fbc` resolved during the launch audit.
- **Fit rationale:** established Python testing and packaging maintainers can assess whether the public v0.3.1 reproduction is actually portable and understandable.
- **Relevant policy:** use only the public Discussion or Issue channel that the owner confirms is appropriate for a bounded reproduction request.
- **Expected effort:** 15–30 minutes.
- **Safety notes:** run only the public ACL repository; do not use private tox projects, plugins, credentials, or employer infrastructure.
- **Exact invitation:** `W1-R1` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

### W1-R2 — `kislyuk/yq`

- **Role:** independent reproduction; no integration request.
- **Current evidence:** public, not archived, current head `ff9fc4b18d0bcbfb7758ff82bf1f36b60020b48a` resolved during the launch audit.
- **Fit rationale:** compact, stable Python CLI with declared test extras, build metadata, type checking, linting, and a public issue tracker.
- **Relevant policy:** the project publishes an Issue Tracker URL; owner must confirm that a one-time reproduction request is appropriate before sending.
- **Expected effort:** 15–30 minutes.
- **Safety notes:** use only ACL's public fixed data; do not submit local YAML/XML/TOML files, credentials, or private paths.
- **Exact invitation:** `W1-R2` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

## Independent-security-review candidates

### W1-S1 — `zizmorcore/zizmor`

- **Role:** independent security review.
- **Current evidence:** public, not archived, current head `9f0243ffb342989b90bbe8c0f6b1d1ea3da5d627` resolved during the launch audit.
- **Fit rationale:** direct expertise in GitHub Actions security, workflow trust boundaries, permissions, action pinning, and supply-chain review.
- **Relevant policy:** `CONTRIBUTING.md` says to read the project's AI policy and generally favors opening or replying to an issue when unsure. The owner must read that policy and confirm an invitation is permitted before sending.
- **Expected effort:** 30–60 minute initial pass.
- **Safety notes:** only benign ACL fixtures; no third-party targets, real secrets, or public high-risk exploit details. High-risk findings go to ACL's GitHub private security reporting route.
- **Exact invitation:** `W1-S1` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

### W1-S2 — `zgosalvez/github-actions-ensure-sha-pinned-actions`

- **Role:** independent security review.
- **Current evidence:** public, not archived, current head `3db98c0363e2fa5df3e1c4c471777a7c10b24cc9` resolved during the launch audit.
- **Fit rationale:** narrowly relevant experience with immutable action references and GitHub Actions supply-chain controls.
- **Relevant policy:** the public contribution guide covers opening issues/PRs and requires tests for functional changes. Owner must check the current issue form before sending.
- **Expected effort:** 30–60 minute initial pass.
- **Safety notes:** review ACL only; no third-party workflow attacks, credentials, or weaponized payloads. High-risk findings use ACL private security reporting.
- **Exact invitation:** `W1-S2` in `WAVE-1-READY-TO-SEND.md`.
- **Status:** `NOT SENT`.

## Thirty-target launch re-audit

All original 30 repositories were re-resolved through the public GitHub repository interface on 2026-07-25. Every repository still existed, was public, and was not archived. A resolved head does not itself authorize contact. Current fit incorporates setup, policy, privacy, security, scope, and first-wave workload.

| Rank | Repository | Current status | Contact decision |
|---:|---|---|---|
| 1 | `tmux-python/tmuxp` | `CURRENT HIGH FIT` | Wave 1 maintainer |
| 2 | `evalstate/fast-agent` | `CURRENT HIGH FIT` | Wave 1 maintainer |
| 3 | `SeemSeam/claude_codex_bridge` | `CURRENT MEDIUM FIT` | Hold for explicit channel/policy check |
| 4 | `campfirein/byterover-cli` | `CURRENT HIGH FIT` | Wave 1 maintainer |
| 5 | `darrenhinde/OpenAgentsControl` | `CURRENT HIGH FIT` | Wave 1 maintainer |
| 6 | `jhlee0409/claude-code-history-viewer` | `CURRENT MEDIUM FIT` | Reserve; privacy/setup friction |
| 7 | `abinthomasonline/repo2txt` | `CURRENT HIGH FIT` | Wave 1 maintainer |
| 8 | `aandrew-me/tgpt` | `CURRENT MEDIUM FIT` | Reserve; network/provider isolation needed |
| 9 | `mergestat/mergestat-lite` | `CURRENT MEDIUM FIT` | Reserve; organization/SQL setup friction |
| 10 | `JohannesKaufmann/html-to-markdown` | `CURRENT MEDIUM FIT` | Do not send in Wave 1; verified issue forms are bug/feature-specific |
| 11 | `tox-dev/tox` | `CURRENT MEDIUM FIT` | Wave 1 reproduction |
| 12 | `dalibo/pg_activity` | `CURRENT MEDIUM FIT` | Reserve; database setup |
| 13 | `kislyuk/yq` | `CURRENT MEDIUM FIT` | Wave 1 reproduction |
| 14 | `dooit-org/dooit` | `CURRENT MEDIUM FIT` | Reserve |
| 15 | `six-ddc/plow` | `CURRENT MEDIUM FIT` | Reserve; no external load traffic |
| 16 | `alexellis/arkade` | `CURRENT MEDIUM FIT` | Reserve; downloads/infrastructure risk |
| 17 | `charmbracelet/glamour` | `CURRENT MEDIUM FIT` | Reserve; maintainer-load risk |
| 18 | `hairyhenderson/gomplate` | `CURRENT MEDIUM FIT` | Reserve; data-source execution risk |
| 19 | `guptarohit/asciigraph` | `CURRENT MEDIUM FIT` | Reserve; less direct agent context |
| 20 | `danvergara/dblab` | `CURRENT MEDIUM FIT` | Reserve; database setup |
| 21 | `dnote/dnote` | `CURRENT MEDIUM FIT` | Reserve; broader application scope |
| 22 | `kubewall/kubewall` | `CURRENT MEDIUM FIT` | Reserve; Kubernetes setup |
| 23 | `fosslife/devtools-x` | `CURRENT MEDIUM FIT` | Reserve; indirect research fit |
| 24 | `flawiddsouza/Restfox` | `CURRENT MEDIUM FIT` | Reserve; credentials/live-endpoint risk |
| 25 | `tach-org/tach` | `CURRENT MEDIUM FIT` | Reserve; mixed toolchain |
| 26 | `cortesi/modd` | `CURRENT MEDIUM FIT` | Reserve; subprocess risk |
| 27 | `sunscrapers/djoser` | `CURRENT LOW FIT` | Do not send in Wave 1; authentication consequence/complexity |
| 28 | `rasterio/rasterio` | `CURRENT LOW FIT` | Do not send in Wave 1; native/domain setup |
| 29 | `projectdiscovery/uncover` | `DO NOT CONTACT` | External-scanning/network/legal risk |
| 30 | `NVIDIA/skills` | `DO NOT CONTACT` | Large-enterprise first-wave exclusion |

The two security-review targets are specialized role additions, not replacements used to inflate the original 30-candidate maintainer sampling frame.

## Stop and follow-up rules

- One initial message per repository.
- No second channel for the same person or project.
- A decline, removal request, or indication that the channel is inappropriate ends contact immediately.
- One follow-up no earlier than Day 10, and only where repository policy permits it and no decline was received.
- No response is not consent.
- Every send and response must be recorded in `research/external-validation/outreach-log.csv`.
- After 30 compliant targeted attempts with no non-author participation, stop recruitment expansion and evaluate `RESEARCH COMPLETE — MAINTENANCE MODE`.