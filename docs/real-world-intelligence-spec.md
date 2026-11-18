# Real-World Intelligence Agent Specification

## Purpose

NexaSupply is fictional. The agent monitors external supply-chain information and produces evidence-backed proposals for a simulation. It must never state that NexaSupply or fictional suppliers were actually affected by real incidents.

## Mandatory separation

Every record and report distinguishes:

1. `REAL_WORLD_EVENT` — an event reported outside NexaSupply.
2. `VERIFIED_FACT` — a claim supported by retained source metadata and validation.
3. `POTENTIAL_BUSINESS_IMPLICATION` — an analytical interpretation.
4. `HYPOTHETICAL_NEXASUPPLY_EXPOSURE` — a simulation assumption, not a real impact.
5. `SYNTHETIC_EVENT` — parameters generated for the simulation.
6. `SIMULATED_IMPACT` — deterministic consequences inside the fictional environment.

## Modes

- **Research Only:** research, normalization, validation, and classification only.
- **Controlled Intelligence (default):** scenario proposals may enter review; high-impact or low-confidence proposals require COO review.
- **Full Simulation Autonomy:** only explicitly authorized low-risk proposals can be applied.

The agent never directly changes inventory, creates real supplier orders, contacts real companies, sends customer messages, or executes financial transactions. Only the event engine and deterministic business services apply simulation changes.

## Provider layer

Providers implement replaceable contracts for recent-event search, source-detail retrieval, normalization, claim verification, and event classification. Primary sources are preferred. The system stores metadata, URLs, short summaries, and extracted claims—not complete copyrighted articles. Access rules and robots restrictions must be respected.

If no provider is configured, a local historical case library is used and all outputs are labeled `OFFLINE INTELLIGENCE MODE`.

## Workflow

`Scan → Evidence Validation → Event Classification → Exposure Analysis → Scenario Proposal → COO Review → Event Engine → Specialist Agents → Simulated Operations → Audit Agent → Daily Report`

The scan is designed for one run per real-world calendar day at 06:00 Europe/Berlin by default. Scan state is explicit and persistable. Daily reports use `reports/intelligence/YYYY-MM-DD.md` plus a machine-readable JSON report.
