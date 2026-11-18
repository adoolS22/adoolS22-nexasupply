"""Explicit approval gate and simulation-engine-only scenario application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from .models import IntelligenceMode, ScenarioProposal


class ReviewError(RuntimeError):
    pass


class SimulationEventEngine(Protocol):
    """Adapter to the host application's deterministic simulation event engine."""

    def apply_synthetic_event(self, *, scenario_id: str, category: str, parameters: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class ReviewDecision:
    scenario_id: str
    approved: bool
    reviewer: str
    rationale: str
    decided_at: datetime

    def __post_init__(self) -> None:
        if not self.reviewer.strip() or not self.rationale.strip():
            raise ValueError("reviewer and rationale are required")
        if self.decided_at.tzinfo is None:
            raise ValueError("decided_at must be timezone-aware")


def review_proposal(proposal: ScenarioProposal, *, approved: bool, reviewer: str, rationale: str) -> ReviewDecision:
    """Record a human review decision; caller persists it in the audit store."""
    return ReviewDecision(proposal.scenario_id, approved, reviewer, rationale, datetime.now(timezone.utc))


def apply_approved_proposal(
    proposal: ScenarioProposal,
    decision: ReviewDecision | None,
    engine: SimulationEventEngine,
) -> dict[str, Any]:
    """Apply a synthetic event only through the injected simulation engine.

    No supplier contact, real order, inventory write, or financial action is
    performed here. The host engine is responsible for deterministic simulated
    consequences and its own transaction/audit guarantees.
    """
    if proposal.mode == IntelligenceMode.RESEARCH_ONLY:
        raise ReviewError("research-only proposals cannot be applied")
    if proposal.requires_review and decision is None:
        raise ReviewError("proposal requires an explicit human review decision")
    if decision is not None:
        if decision.scenario_id != proposal.scenario_id:
            raise ReviewError("review decision does not match proposal")
        if not decision.approved:
            raise ReviewError("proposal was rejected")
    result = engine.apply_synthetic_event(
        scenario_id=proposal.scenario_id,
        category=proposal.category.value,
        parameters={**proposal.synthetic_parameters, "synthetic_only": True},
    )
    return {"label": "SIMULATED IMPACT", "scenario_id": proposal.scenario_id, "result": result}
