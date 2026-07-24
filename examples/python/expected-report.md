# Expected Python report

A complete fixture produces one `python-feature` task with five passing assertions and overall `SUPPORTED`.

Missing package files or nonzero pytest/mypy/build exit codes produce `FAILED`. Static-only mode evaluates the two file assertions but reports command-dependent acceptance evidence as `UNVERIFIABLE`.
