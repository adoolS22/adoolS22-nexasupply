# NexaSupply implementation plan — Real-World Intelligence Agent

## Phase 1 — Core contracts and safety foundation

- [x] Define real-world/verified/hypothetical/synthetic/simulated distinctions.
- [x] Add source-provider protocol and source metadata bounds.
- [x] Add deterministic evidence assessment, typed models, and review policy.
- [x] Add offline fallback, scan state machine, SQLite store, and report builder.
- [x] Add baseline unit and integration tests.

## Phase 2 — Host application integration

- [ ] Wire the package to the NexaSupply application, supplier/route/product model, event engine, and agent orchestration.
- [ ] Implement real COO identity, authorization, review UI, and durable audit history.
- [ ] Add production migrations and deployment-managed scheduling at 06:00 Europe/Berlin.
- [ ] Implement at least one authorized primary-source/news provider and RSS adapter with rate limits and source terms compliance.
- [ ] Add company exposure analysis using only fictional simulation data and explicit assumptions.
- [ ] Persist scenario proposals, decisions, engine outcomes, and provenance transactionally.

## Phase 3 — Operations and release

- [ ] Deliver the REAL-WORLD INTELLIGENCE CENTER in the actual dashboard, including date/category/risk/confidence/review/mode filters and required visual labels.
- [ ] Add reports at `reports/intelligence/YYYY-MM-DD.md` and matching JSON to the application data pipeline.
- [ ] Execute test/lint/type checks in CI and fix failures.
- [ ] Validate provider outages, duplicate daily runs, unsafe URL handling, approval bypass attempts, and event-engine failures.
- [ ] Merge only after code review, passing CI, and environment-specific configuration.

## Current limitations

This repository currently contains the standalone intelligence foundation, not the NexaSupply application itself. The feature branch is not merged. GitHub file operations cannot execute Python locally; automated test execution is pending an Actions workflow or local runner. An external live provider, actual domain data, dashboard, identity/review service, and event engine are not present here, so no live scans or simulated operations have been performed.
