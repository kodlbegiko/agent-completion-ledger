# OpenTelemetry GenAI mapping

Status: **experimental documentation mapping; no official compatibility claim**.

## Different evidence planes

OpenTelemetry GenAI semantic conventions describe runtime telemetry: spans, events, metrics, operation names, agent/tool activity, model attributes, and workflow context. Agent Completion Ledger describes repository-level acceptance evidence for a coding-agent task. A trace can explain what happened during execution; an ACL report answers whether the configured repository evidence supports the completion claim.

## Possible field mapping

| ACL field | Possible OpenTelemetry carrier | Notes |
|---|---|---|
| Tool name/version | resource or instrumentation scope metadata | Describes the verifier, not the coding agent model |
| Repository identity | span attribute or resource attribute defined by the integrating system | No ACL-specific OTel attribute is standardized |
| Repository commit | VCS-related attribute where available, otherwise custom integration attribute | Preserve the exact Git SHA |
| Task ID | span name suffix or custom task attribute | Do not overload `gen_ai.operation.name` with an ACL ledger state |
| Assertion ID/type/outcome | span events or structured log attributes | Potentially high cardinality; avoid emitting full sensitive paths |
| Ledger status | custom integration attribute or event | `SUPPORTED` is an ACL acceptance result, not a model response status |
| Result digest | custom integrity attribute | A digest is not a trace ID or signature |
| Trace/span IDs | optional external references attached around ACL invocation | Current ACL report schema does not claim native trace export |

## Semantics that do not map

- ACL has no prompts, token usage, model-response messages, sampling parameters, or tool-call event stream.
- OpenTelemetry telemetry does not inherently define the trusted acceptance contract or its four-state decision policy.
- A successful span does not imply `SUPPORTED`; a failed span does not necessarily imply the coding task is unacceptable.
- ACL's result digest is not a replacement for trace context or telemetry backend integrity.

## Recommended integration

Instrument the ACL CLI invocation as a normal process/workflow span and attach only low-cardinality references: task ID, report path, report digest, overall ledger status, contract digest, and execution mode. Keep the full assertion report as an artifact rather than copying potentially sensitive details into telemetry.

No exporter is included because the semantic destination for ACL-specific acceptance fields is not standardized. Adding a runtime exporter now would risk presenting custom attributes as official OpenTelemetry GenAI conventions.

## Information loss

Mapping an ACL report into telemetry usually loses the full contract, assertion messages, deterministic report structure, and reviewer-facing limitations. Mapping a trace into ACL loses the chronological runtime behavior. Store references in both directions rather than converting either artifact into the other.
