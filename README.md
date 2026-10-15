# Reliable Agent Runtime
Production-oriented reference for durable, observable and recoverable agent workflows.

Core rule: **an agent's belief that an action succeeded is not proof the external system changed.**

Implements explicit workflow state, validated tool calls, checkpoints, idempotency boundaries, bounded retries, ambiguous-write effect verification, human approval, execution traces, concurrent supervisor/workers, context projection, stale-result detection, Playwright verification boundary, LangGraph integration boundary, and system-level evaluation.

`pip install -e ".[dev]" && pytest -q`

PostgreSQL/Redis/Playwright/LangGraph are represented by production-facing adapters or optional integration boundaries; unit tests use deterministic local substitutes. The included evaluator can calculate a 48% token reduction when supplied corresponding measurements, but the repository does not itself prove a historical 48% production result.
