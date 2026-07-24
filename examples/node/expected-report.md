# Expected Node.js report

A complete fixture produces one `node-feature` task with five passing assertions and overall `SUPPORTED`.

A missing `src/index.ts` or nonzero test/typecheck/build exit code produces `FAILED`. In `--no-exec` mode, the static file assertions still run but the three command assertions are `UNVERIFIABLE`, so the task cannot be reported as `SUPPORTED`.
