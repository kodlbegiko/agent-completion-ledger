# Wave 1 external validation targets

Status: **EXTERNAL VALIDATION IN PROGRESS — 1 SENT / 8 NOT SENT**

Status date: **2026-07-25 UTC**

This is a manual research-outreach plan, not a marketing list. Inclusion does not imply consent, endorsement, adoption, or willingness to participate. No private email address is collected or used.

## Selection rules

Wave 1 contains exactly:

- five maintainer-pilot candidates;
- two independent-reproduction candidates;
- two independent-security-review candidates.

Every unsent message requires a same-day owner check of the repository's current contribution policy, issue/discussion templates, code of conduct, prior-contact history, and whether the selected public channel permits a research invitation. If the channel is unclear, do not send.

## Dispatch matrix

| ID | Public repository | Role | Approved public channel | Effort | Current state |
|---|---|---|---|---:|---|
| W1-M1 | `tmux-python/tmuxp` | Maintainer pilot | GitHub Discussions / General | 30–60 min | `SENT — AWAITING RESPONSE` |
| W1-M2 | `evalstate/fast-agent` | Maintainer pilot | GitHub Issue or Discussion after same-day recheck | 30–60 min | `NOT SENT` |
| W1-S1 | `zizmorcore/zizmor` | Independent security review | GitHub Issue only after current AI/contribution-policy review | 30–60 min | `NOT SENT` |
| W1-M3 | `campfirein/byterover-cli` | Maintainer pilot | GitHub Issue or Discussion after template check | 30–60 min | `NOT SENT` |
| W1-M4 | `darrenhinde/OpenAgentsControl` | Maintainer pilot | GitHub Question Issue after policy check | 30–60 min | `NOT SENT` |
| W1-R1 | `tox-dev/tox` | Independent reproduction | GitHub Discussion or Issue, whichever current policy permits | 15–30 min | `NOT SENT` |
| W1-M5 | `abinthomasonline/repo2txt` | Maintainer pilot | GitHub Issue only if a general request remains permitted | 30–60 min | `NOT SENT` |
| W1-R2 | `kislyuk/yq` | Independent reproduction | GitHub Issue Tracker after policy check | 15–30 min | `NOT SENT` |
| W1-S2 | `zgosalvez/github-actions-ensure-sha-pinned-actions` | Independent security review | GitHub Issue after policy check | 30–60 min | `NOT SENT` |

## W1-M1 public send record

- **Repository:** `tmux-python/tmuxp`.
- **Role:** maintainer pilot.
- **Same-day result:** repository public, not archived, active, contribution guidance permits prior discussion, and GitHub Discussions / General was selected over an Issue for the research request.
- **Fit:** Python CLI with explicit `ruff`, `mypy`, and `pytest` contributor evidence plus public coding-agent guidance.
- **Pilot path:** fixed task-pack review with no installation, or one bounded parser/configuration-validation case using public fixtures.
- **Safety boundary:** no shell history, personal tmux configuration, credentials, secrets, private code, or automatic PR.
- **Owner decision:** approved for manual send.
- **Public record:** `https://github.com/tmux-python/tmuxp/discussions/1078`.
- **Current state:** `SENT — AWAITING RESPONSE`.
- **Evidence credit:** none; sending an invitation is not participation or consent.

## Remaining maintainer-pilot candidates

### W1-M2 — `evalstate/fast-agent`

Direct agent/MCP context with unit, integration, simulated-endpoint, and E2E evidence surfaces. Use only an offline bounded task or fixed-material review. Do not request model keys, OAuth credentials, private prompts, conversations, private repositories, or production services.

### W1-M3 — `campfirein/byterover-cli`

TypeScript CLI with build, lint, type-check, unit, and integration evidence. Use one bounded CLI option/output-format case or fixed-material review. Do not request workspace contents, tokens, proprietary repositories, daemon data, submodule credentials, or live LLM access.

### W1-M4 — `darrenhinde/OpenAgentsControl`

Agent-control and evaluation context where generated claims versus repository evidence is directly relevant. Begin with fixed-material or static-only policy/configuration review. Do not execute untrusted plugins, connect agent services, or request API keys, private prompts, or private code.

### W1-M5 — `abinthomasonline/repo2txt`

Deterministic repository-processing behavior with build, unit/E2E, type-check, lint, and CI evidence. Use generated public fixtures only. Do not request a private repository, provider token, local archive, private source, or user content.

## Independent-reproduction candidates

### W1-R1 — `tox-dev/tox`

Reproduction only; no tox integration or endorsement request. Use ACL v0.3.1 in a disposable environment and report version, environment, exact commands, elapsed time, exit code, expected/observed hashes, assistance required, sanitized blockers, and evidence link.

### W1-R2 — `kislyuk/yq`

Reproduction only using ACL's public fixed data. Do not submit local YAML/XML/TOML files, credentials, private code, or sensitive paths.

## Independent-security-review candidates

### W1-S1 — `zizmorcore/zizmor`

Review ACL's GitHub Actions and verifier trust boundaries using only benign ACL fixtures. Read the target's current AI/contribution policy before deciding whether the public channel permits the request. High-risk findings must use ACL private security reporting.

### W1-S2 — `zgosalvez/github-actions-ensure-sha-pinned-actions`

Review immutable action references and GitHub Actions supply-chain controls for ACL only. No third-party workflow attacks, credentials, real secrets, or weaponized payloads.

## Thirty-target audit source

The complete original 30-candidate audit, current fit, audit head, policy summary, contact gate, reserve status, and exclusions remain machine-readable in:

```text
research/external-validation/recruitment-targets.csv
```

A resolved public repository does not authorize contact. Reserve targets may be substituted only after a Wave 1 target is formally held or disqualified, the reason is recorded, and the owner approves the replacement.

## Contact and evidence rules

- One target, one approved public channel.
- No automated dispatch, private email, cross-platform duplicate contact, generated external PR, or unsolicited tag.
- The remaining eight exact messages are in `WAVE-1-READY-TO-SEND.md` and remain owner-review gated.
- W1-M1 may receive at most one policy-permitted follow-up under the existing Day 10-or-later rule.
- A decline, removal, lock, or request to stop ends contact permanently.
- Only a consenting verified `NON-AUTHOR HUMAN` with qualifying evidence may increment external participant or outcome counts.
