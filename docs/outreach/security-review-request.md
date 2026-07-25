# Independent security review request — draft only

Status: **NOT SENT — OWNER APPROVAL REQUIRED**

Subject: Request for a bounded independent review of ACL trusted-contract verification

Hello `[REVIEWER OR TEAM]`,

I am seeking an independent review of Agent Completion Ledger, an open-source tool that checks coding-agent completion claims against repository evidence.

The request is deliberately narrow and is expected to take approximately **30–60 minutes** for an initial pass. The highest-priority surfaces are:

- contract replacement and attacker-controlled digest sources;
- SHA-256 pinning before parsing;
- static-only `--no-exec` behavior;
- allow-listed interpreter and subprocess risk;
- path traversal, Windows absolute-path, and symlink handling;
- timeout behavior;
- report information leakage;
- fork-pull-request permissions and secret exposure;
- unsigned in-toto statements being mistaken for attestations;
- signed artifacts being mistaken for software correctness.

The package includes a threat model, trust boundaries, benign reproduction cases, exact commands, and the private reporting route. It does not ask you to test third-party systems, access secrets, or publish an exploit.

ACL is explicitly **not a sandbox**, and the review may conclude that its risk boundary is unsuitable or insufficient. A negative result is useful evidence and will not be reframed as endorsement.

You may provide:

1. a reproduction-only result;
2. a public low-risk finding or documentation concern; or
3. a private vulnerability report through GitHub's security reporting mechanism.

Participation is voluntary, can be stopped at any time, and does not imply endorsement. No repeated contact will be made after a decline.

Review package: `[INDEPENDENT SECURITY REVIEW LINK]`

Repository: `[ACL REPOSITORY LINK]`

Thank you,

`[OWNER NAME / GITHUB HANDLE]`
