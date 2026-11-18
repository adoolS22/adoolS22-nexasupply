"""Typed domain models separating evidence from simulation assumptions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class IntelligenceMode(StrEnum):
    RESEARCH_ONLY = "RESEARCH_ONLY"
    CONTROLLED = "CONTROLLED_INTELLIGENCE"
    FULL_SIMULATION_AUTONOMY = "FULL_SIMULATION_AUTONOMY"


class EventCategory(StrEnum):
    TRANSPORT = "TRANSPORT"
    PORT_DISRUPTION = "PORT_DISRUPTION"
    NATURAL_HAZARD = "NATURAL_HAZARD"
    GEOPOLITICAL = "GEOPOLITICAL"
    REGULATORY = "REGULATORY"
    SUPPLIER = "SUPPLIER"
    COMMODITY = "COMMODITY"
    LABOR = "LABOR"
    CYBER = "CYBER"
    OTHER = "OTHER"


@dataclass(frozen=True)
class Claim:
    text: str
    supported: bool = False
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("claim text is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("claim confidence must be between 0 and 1")


@dataclass(frozen=True)
class IntelligenceEvent:
    event_id: str
    title: str
    category: EventCategory
    occurred_at: datetime | None
    discovered_at: datetime
    source_urls: tuple[str, ...]
    verified_facts: tuple[Claim, ...] = ()
    summary: str = ""
    offline: bool = False

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.title.strip():
            raise ValueError("event_id and title are required")
        if not self.source_urls:
            raise ValueError("at least one source URL or library reference is required")
        if self.discovered_at.tzinfo is None:
            raise ValueError("discovered_at must be timezone-aware")


@dataclass(frozen=True)
class ExposureAssessment:
    rationale: str
    likelihood: float
    severity: float
    confidence: float
    affected_simulation_entities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (("likelihood", self.likelihood), ("severity", self.severity), ("confidence", self.confidence)):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")

    @property
    def risk_score(self) -> float:
        return round(self.likelihood * self.severity, 3)


@dataclass(frozen=True)
class ScenarioProposal:
    scenario_id: str
    event_id: str
    mode: IntelligenceMode
    category: EventCategory
    hypothetical_exposure: str
    synthetic_parameters: dict[str, Any]
    confidence: float
    risk_score: float
    requires_review: bool
    labels: tuple[str, ...] = field(default=("REAL-WORLD SOURCE", "VERIFIED FACT", "HYPOTHETICAL EXPOSURE", "SYNTHETIC EVENT", "SIMULATED IMPACT"))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0 or not 0.0 <= self.risk_score <= 1.0:
            raise ValueError("confidence and risk_score must be between 0 and 1")
        if not self.hypothetical_exposure.strip():
            raise ValueError("hypothetical exposure must be explicit")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
