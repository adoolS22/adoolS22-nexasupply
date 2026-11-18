"""Build scenario proposals without ever asserting real NexaSupply exposure."""

from __future__ import annotations

from .models import ExposureAssessment, IntelligenceEvent, IntelligenceMode, ScenarioProposal


DEFAULT_REVIEW_RISK_THRESHOLD = 0.60
DEFAULT_REVIEW_CONFIDENCE_THRESHOLD = 0.45


def propose_scenario(
    event: IntelligenceEvent,
    exposure: ExposureAssessment,
    *,
    mode: IntelligenceMode = IntelligenceMode.CONTROLLED,
    scenario_id: str,
    high_impact_threshold: float = DEFAULT_REVIEW_RISK_THRESHOLD,
    low_confidence_threshold: float = DEFAULT_REVIEW_CONFIDENCE_THRESHOLD,
) -> ScenarioProposal:
    """Convert evidence and explicit hypothetical exposure into a proposal."""
    if not scenario_id.strip():
        raise ValueError("scenario_id is required")
    if not 0 <= high_impact_threshold <= 1 or not 0 <= low_confidence_threshold <= 1:
        raise ValueError("review thresholds must be between 0 and 1")
    if not exposure.rationale.strip():
        raise ValueError("exposure rationale is required")

    needs_review = exposure.risk_score >= high_impact_threshold or exposure.confidence < low_confidence_threshold
    if mode == IntelligenceMode.RESEARCH_ONLY:
        needs_review = True  # Research-only proposals are never eligible for application.
    parameters = {
        "event_category": event.category.value,
        "severity": exposure.severity,
        "likelihood": exposure.likelihood,
        "confidence": exposure.confidence,
        "synthetic_only": True,
    }
    return ScenarioProposal(
        scenario_id=scenario_id,
        event_id=event.event_id,
        mode=mode,
        category=event.category,
        hypothetical_exposure=exposure.rationale,
        synthetic_parameters=parameters,
        confidence=exposure.confidence,
        risk_score=exposure.risk_score,
        requires_review=needs_review,
    )
