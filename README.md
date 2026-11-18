# NexaSupply Real-World Intelligence

Provider-independent foundation for researching external supply-chain information and proposing strictly hypothetical NexaSupply simulation scenarios.

## Safety boundary

NexaSupply is fictional. The package never claims that NexaSupply or a fictional supplier was affected by a real incident. Real events and verified facts are kept distinct from implications, hypothetical exposure, synthetic parameters, and simulated impacts. Real-world research is not itself permission to change business state. Scenario execution can only call an injected simulation event-engine adapter.

## Modes

- `RESEARCH_ONLY`: evidence gathering and classification; never applicable.
- `CONTROLLED_INTELLIGENCE`: default; high-risk or low-confidence scenarios require explicit review.
- `FULL_SIMULATION_AUTONOMY`: for policy-authorized low-risk proposals; human review is still required when proposal policy flags it.

## Included components

- Typed event, claim, exposure, and scenario proposal models.
- Explainable deterministic evidence assessment.
- Replaceable provider protocol and explicitly labeled offline provider/library.
- SQLite persistence for daily scans and reports; PostgreSQL reference schema.
- Scan orchestration with daily uniqueness and 06:00 Europe/Berlin schedule metadata.
- Scenario review gate and simulation-engine-only dispatch.
- Clearly labeled Markdown/JSON daily report builder.

## Development

```bash
python -m pip install -e '.[test]'
python -m pytest -q
```

GitHub Actions workflow is intended to run these tests on pushes and pull requests. A green CI result should be verified in the Actions tab; repository file access cannot execute Python directly.

## Provider integration

Implement `IntelligenceProvider` methods for recent search, source details, normalization, claim verification, and classification. Prefer primary sources, obey access restrictions, and retain concise summaries and source metadata rather than complete articles. Do not describe provider output as verified unless a validation implementation has actually established it.

## Persistence and deployment

SQLite is for development/local use. For production, apply the documented PostgreSQL schema through the host application's migration framework and implement authentication, authorization, audit retention, secrets management, provider-specific rate limits, and operational scheduling. The scanner returns after classification; a host NexaSupply event engine and review UI must be wired in before production operation.
