# References and source map

All claims below are paraphrased. Access date: 2026-07-24.

1. **SWE-bench Experiments repository.** Public submission records separate model predictions from execution logs and result artifacts; each evaluated instance can include `patch.diff`, `report.json`, and `test_output.txt`.  
   https://github.com/SWE-bench/experiments

2. **Jimenez et al., “SWE-bench: Can Language Models Resolve Real-World GitHub Issues?”** Defines the benchmark family and execution-based issue-resolution task.  
   https://arxiv.org/abs/2310.06770

3. **Tang et al., “How Coding Agents Fail Their Users.”** Observational analysis of 20,574 real-world coding-agent sessions; inaccurate self-reporting grew as a share of visible misalignment, and most visible resolutions required explicit user correction.  
   https://arxiv.org/abs/2605.29442

4. **Yu et al., “UTBoost.”** Reports insufficient benchmark tests and 345 erroneous patches originally labeled passed, demonstrating that executable benchmark labels are useful but imperfect evidence.  
   https://arxiv.org/abs/2506.09289

5. **Aleithan et al., “SWE-Bench+.”** Reports suspicious benchmark passes associated with weak tests and leakage.  
   https://arxiv.org/abs/2410.06992

6. **Li et al., “STING.”** Uses mutation-guided test augmentation and reports lower reassessed resolved rates, further motivating explicit oracle limitations.  
   https://arxiv.org/abs/2604.01518

7. **AAS-1 Agent Auditability Standard.** An emerging open evidentiary record format for autonomous-agent activity.  
   https://aas-1.org/

8. **Evidence Envelope Specification.** An emerging specification for independently custodied agent execution records.  
   https://theveridic.github.io/VERIDIC/standards/ees/v0.1/

9. **agent-evidence package.** A public package for auditable evidence objects, showing that generic agent-evidence tooling already exists.  
   https://pypi.org/project/agent-evidence/

10. **Cursor Agent Trace.** An open format for tracing AI-generated code, relevant adjacent provenance work.  
    https://github.com/cursor/agent-trace

These references support the problem framing and limitations. The numerical pilot result is derived only from the seven pinned source blobs listed in `data/frozen/submission-summaries.json`.
