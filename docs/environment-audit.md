# Environment capability audit

| Capability | Status | Evidence / decision |
|---|---|---|
| Public web search and document reading | AVAILABLE | Web search, GitHub pages, arXiv, public technical documents |
| Download public data | PARTIALLY AVAILABLE | Controlled downloader rejects JSON/HTML; GitHub connector can read pinned public files; repo includes a normal-network fetch helper |
| Python execution | AVAILABLE | Python 3.13.5, 5 vCPU, 5.9 GiB RAM |
| Node.js / TypeScript | AVAILABLE | Node 22.16.0, npm 10.9.2; not needed by selected pilot |
| Install open-source dependencies | PARTIALLY AVAILABLE | Current package mirror returned 503/no distribution for ruff, mypy, build; project uses standard library and CI installs pinned dev tools |
| Create files, charts, tests | AVAILABLE | 39 GiB free disk; generated source, data, reports, and tests |
| GitHub read/write | AVAILABLE | Authenticated connector with admin/push on target repository |
| Create new repository | UNAVAILABLE | Connector exposes no repository-creation action; selected existing empty `agent-completion-ledger` repository |
| Commit, branch, PR, merge, Actions logs | AVAILABLE | Connector supports Git objects, PRs, merges, workflow runs/jobs/logs |
| Tag and GitHub Release | UNAVAILABLE | No tag/release action and no `gh` CLI/network path; owner action is documented |
| GPU | UNAVAILABLE / NOT NEEDED | CPU-only analysis selected |
| Direct container internet | UNAVAILABLE | DNS resolution blocked; acquisition performed through public connector |
