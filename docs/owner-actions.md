# Owner actions not executable in the current environment

The connected GitHub tooling cannot create tags or Releases and the container has no network-capable `gh` CLI. After CI is green and the PR is merged:

```bash
git clone https://github.com/kodlbegiko/agent-completion-ledger.git
cd agent-completion-ledger
git tag -a v0.1.0 -m "Exploratory pilot v0.1.0"
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0 exploratory pilot" --notes-file CHANGELOG.md
```

Before doing so, verify that the merged commit matches the final commit SHA reported in the delivery note.
