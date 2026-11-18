# Real-World Intelligence Agent — unified V1 specification

## Product objective

A dedicated NexaSupply agent monitors real-world supply-chain developments, validates external information, and converts relevant evidence into strictly hypothetical synthetic proposals for the fictional NexaSupply simulation. The agent never asserts real-world exposure of NexaSupply or fictional suppliers.

## Required labels and semantic boundaries

- `REAL-WORLD SOURCE`: external reference metadata.
- `VERIFIED FACT`: an individually supported claim, with source and confidence attached.
- `POTENTIAL BUSINESS IMPLICATION`: analytical inference, not a fact.
- `HYPOTHETICAL EXPOSURE`: explicit simulation assumption about a fictional entity.
- `SYNTHETIC EVENT`: parameters authored for the simulator.
- `SIMULATED IMPACT`: outcome emitted by the deterministic simulation event engine.

A real event does not automatically imply fictional exposure; exposure analysis must disclose its assumptions and uncertainty.

## Research sources and provider rules

Configurable provider adapters may cover news search, RSS, official company newsrooms, government and regulator publications, port/transport organizations, World Bank, OECD, UNCTAD, industry publications, and reputable international news. Prefer primary and authoritative sources. Do not infer verification from a search snippet or headline. Retain URLs, publisher/title, timestamps, compact factual summaries, and extracted claims; do not retain full copyrighted articles. Follow source terms, rate limits, and robots/access rules; do not bypass access controls.

Provider methods are replaceable behind a stable protocol: `search_recent_events`, `fetch_source_details`, `normalize_source`, `verify_event_claims`, `classify_supply_chain_event`.

When no live provider is configured, use the local case library and visibly mark every output `OFFLINE INTELLIGENCE MODE`. Offline templates are not current-event reports.

## Modes and controls

- Mode A `RESEARCH_ONLY`: gather, normalize, validate, classify, and report; never apply scenarios.
- Mode B `CONTROLLED_INTELLIGENCE` (default): scenario proposals require review for high impact or low confidence; approved scenarios may be dispatched only through the simulation event engine.
- Mode C `FULL_SIMULATION_AUTONOMY`: only expressly policy-authorized low-risk synthetic scenarios may proceed without review. It does not authorize real-world actions.

Any high-impact or low-confidence proposal requires explicit COO review. Research code must never directly update inventory, create real orders, contact suppliers, send customer communications, or execute financial transactions.

## End-to-end workflow

`Real-World Intelligence Scan → Evidence Validation → Event Classification → Company Exposure Analysis → Scenario Proposal → COO Review → Event Engine → Specialist Agents → Simulated Business Operations → Audit Agent → Daily Report`

The repository foundation currently implements the provider adapter contract, metadata validation, evidence score, typed event/proposal models, safe proposal and review gates, SQLite scan/report persistence, offline fallback, and report rendering. Exposure analysis, host event-engine integration, specialist-agent dispatch, dashboard, authenticated COO workflow, durable production audit integration, and external live provider adapters remain host integration work.

## Schedule, reports, and persistence

Default schedule: once per real-world calendar day at 06:00 `Europe/Berlin`. The SQLite development store enforces unique scan dates and persists scan states/reports. Production schema is documented separately; production must use reviewed migrations, retention policy, concurrency controls, authentication, and authorization.

Daily outputs: `reports/intelligence/YYYY-MM-DD.md` plus machine-readable JSON. Reports must state mode, source/evidence, uncertainties, implications, hypothetical assumptions, synthetic parameters, review state, and simulation-only impacts. Never describe a proposal as an applied impact before the event engine confirms it.

## V1 completion criteria

1. Provider failures fall back cleanly and are explicitly labeled offline.
2. Every external factual claim is traceable to a source record; unsupported claims remain unverified.
3. Every proposal is explicitly hypothetical and synthetic.
4. High-risk/low-confidence proposals cannot bypass review.
5. Only the injected event engine can apply a simulation event.
6. Scan state, daily uniqueness, and report payloads persist.
7. Reports cannot conflate real-world events with simulated consequences.
8. Automated tests and CI pass before merge or deployment.
