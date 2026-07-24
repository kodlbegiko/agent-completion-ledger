# Owner release actions for v0.1.0 and v0.2.0

The connected GitHub interface can verify tags but cannot read or create GitHub Releases. Perform these commands from an authenticated GitHub CLI environment after the v0.2.0 PR is merged and main CI is green.

## Verify v0.1.0 release

```bash
gh release view v0.1.0 --repo kodlbegiko/agent-completion-ledger
```

If this returns “release not found”, create it without moving the existing tag:

```bash
gh release create v0.1.0 \
  --repo kodlbegiko/agent-completion-ledger \
  --verify-tag \
  --title "Agent Completion Ledger v0.1.0" \
  --notes-file docs/release-notes-v0.1.0.md
```

## Publish v0.2.0

Confirm main points at the intended merge commit, then:

```bash
git fetch origin main --tags
git checkout main
git pull --ff-only
git tag -s v0.2.0 -m "Agent Completion Ledger v0.2.0"
git push origin v0.2.0
gh release create v0.2.0 \
  --repo kodlbegiko/agent-completion-ledger \
  --verify-tag \
  --title "Agent Completion Ledger v0.2.0" \
  --notes-file docs/release-notes-v0.2.0.md
```

Then verify:

```bash
gh release view v0.2.0 --repo kodlbegiko/agent-completion-ledger --json url,tagName,targetCommitish,isDraft,isPrerelease
```

Do not mark the release complete if the tag target differs from the merged, green main commit.
