from datetime import datetime, timezone

import pytest

from nexasupply_intelligence import EventCategory, ExposureAssessment, IntelligenceEvent, IntelligenceMode, propose_scenario
from nexasupply_intelligence.review import ReviewError, apply_approved_proposal, review_proposal


class FakeEngine:
    def __init__(self):
        self.calls = []

    def apply_synthetic_event(self, *, scenario_id, category, parameters):
        self.calls.append((scenario_id, category, parameters))
        return {"status": "applied"}


def proposal(mode=IntelligenceMode.CONTROLLED, exposure=None):
    event = IntelligenceEvent("event", "Disruption", EventCategory.TRANSPORT, None, datetime.now(timezone.utc), ("offline:case",), offline=True)
    return propose_scenario(event, exposure or ExposureAssessment("Hypothetical only", .9, .9, .9), mode=mode, scenario_id="scenario")


def test_high_impact_requires_approval_and_uses_only_simulation_engine():
    scenario = proposal()
    engine = FakeEngine()
    with pytest.raises(ReviewError):
        apply_approved_proposal(scenario, None, engine)
    decision = review_proposal(scenario, approved=True, reviewer="COO", rationale="Approved for simulation")
    result = apply_approved_proposal(scenario, decision, engine)
    assert result["label"] == "SIMULATED IMPACT"
    assert len(engine.calls) == 1
    assert engine.calls[0][2]["synthetic_only"] is True


def test_research_only_cannot_be_applied():
    scenario = proposal(IntelligenceMode.RESEARCH_ONLY)
    with pytest.raises(ReviewError):
        apply_approved_proposal(scenario, None, FakeEngine())
