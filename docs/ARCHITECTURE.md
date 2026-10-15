# Architecture
Planner/model output is advisory. Deterministic code owns permissions, validation, persistence, retries, idempotency, approvals and external-effect verification.

A timeout after a write is UNKNOWN, not automatically FAILED. Verify the external effect before retrying. If a consequential outcome cannot be established, escalate to a human.

Parallel workers receive projected context and are justified only when evaluation shows an advantage over a single-agent baseline. Track stale results and aggregate worker errors explicitly.
