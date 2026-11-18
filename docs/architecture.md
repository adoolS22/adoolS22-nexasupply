# NexaSupply Intelligence Architecture

## Bounded component responsibilities

- **Source providers** retrieve metadata and concise source summaries within provider terms; they do not mutate business state.
- **Evidence validator** records per-claim provenance and score; a score is prioritization metadata, not proof.
- **Classifier** assigns a controlled event category and must preserve uncertainty.
- **Exposure analyst** uses only explicit fictional simulation data and labels its assumptions.
- **Proposal builder** emits synthetic-only scenario parameters.
- **Human review service** stores reviewer, decision, rationale, and timestamp.
- **Event-engine adapter** is the sole mutation boundary for simulated operations.
- **Audit/report services** retain decisions and render the real/hypothetical/simulated distinctions.

## Data flow

```text
Providers → SourceRecord → Claims/Evidence → Event Classification
         → Hypothetical Exposure → Synthetic Proposal → Review Policy
         → Injected Simulation Event Engine → Simulated Impact → Audit/Report
```

Provider errors must be visible and fall back to the local library. Fallback never fabricates a current event or verified claim. Persist scan status so retries are observable and daily uniqueness is enforced.

## Trust boundaries

External source text is untrusted data, never executable instructions. Validate URLs and bounded metadata; do not fetch arbitrary private-network URLs in a future HTTP adapter. Store no credentials in the repository. Keep provider secrets in a deployment secret manager. Apply request timeouts, rate limits, and allowlisted provider endpoints in any network implementation.

## Integration status

The package is intentionally host-agnostic and has no existing NexaSupply application to attach to in this repository. The simulation engine, supplier/inventory domain model, dashboard, review identity, scheduler process, and production database must be supplied by the host application. The reference SQLite adapter is not a multi-worker production database.
