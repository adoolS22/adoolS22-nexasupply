from datetime import datetime, timezone

import pytest

from nexasupply_intelligence import (
    EventCategory,
    ExposureAssessment,
    IntelligenceEvent,
    IntelligenceMode,
    propose_scenario,
)


def sample_event():
    return IntelligenceEvent(
        event_id="evt-1",
        title="Port disruption reported",
        category=EventCategory.PORT_DISRUPTION,
        occurred_at=None,
        discovered_at=datetime.now(timezone.utc),
        source_urls=("https://example.test/report",),
        summary="Short factual summary only.",
    )


def test_high_risk_scenario_requires_review():
    proposal = propose_scenario(
        sample_event(),
        ExposureAssessment("Hypothetical route overlap for simulation only", 0.9, 0.9, 0.8),
        scenario_id="scn-1",
    )
    assert proposal.requires_review
    assert proposal.synthetic_parameters["synthetic_only"] is True
    assert "HYPOTHETICAL EXPOSURE" in proposal.labels


def test_low_confidence_scenario_requires_review():
    proposal = propose_scenario(
        sample_event(),
        ExposureAssessment("Hypothetical exposure", 0.2, 0.2, 0.1),
        scenario_id="scn-2",
    )
    assert proposal.requires_review


def test_research_only_always_requires_review():
    proposal = propose_scenario(
        sample_event(),
        ExposureAssessment("Hypothetical exposure", 0.1, 0.1, 0.9),
        mode=IntelligenceMode.RESEARCH_ONLY,
        scenario_id="scn-3",
    )
    assert proposal.requires_review


def test_reject_naive_datetime():
    with pytest.raises(ValueError):
        IntelligenceEvent(
            event_id="x",
            title="x",
            category=EventCategory.OTHER,
            occurred_at=None,
            discovered_at=datetime(2026, 1, 1),
            source_urls=("offline:case-1",),
        )
