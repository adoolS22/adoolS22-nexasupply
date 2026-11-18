"""Deterministic, explainable evidence assessment.

Scores are not claims of truth. They prioritize review using source quality,
claim corroboration, freshness, and directness of evidence.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceAssessment:
    score: float
    confidence: str
    reasons: tuple[str, ...]


def assess_evidence(
    *,
    authoritative_sources: int = 0,
    corroborating_sources: int = 0,
    source_count: int = 0,
    has_primary_document: bool = False,
    claim_is_direct: bool = False,
    stale: bool = False,
) -> EvidenceAssessment:
    """Return a bounded evidence score and transparent reasons.

    Inputs are counts or explicit booleans supplied by a provider-independent
    validation layer. Invalid negative counts are rejected.
    """
    counts = (authoritative_sources, corroborating_sources, source_count)
    if any(value < 0 for value in counts):
        raise ValueError("source counts cannot be negative")
    if authoritative_sources > source_count or corroborating_sources > source_count:
        raise ValueError("specialized source counts cannot exceed source_count")

    score = 0.0
    reasons: list[str] = []
    score += min(authoritative_sources, 3) * 0.20
    score += min(corroborating_sources, 3) * 0.10
    score += min(source_count, 5) * 0.04
    if has_primary_document:
        score += 0.18
        reasons.append("primary document available")
    if claim_is_direct:
        score += 0.10
        reasons.append("claim directly supported by source")
    if stale:
        score -= 0.20
        reasons.append("source freshness penalty applied")

    score = round(max(0.0, min(1.0, score)), 3)
    if score >= 0.75:
        confidence = "HIGH"
    elif score >= 0.45:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"
    if authoritative_sources:
        reasons.append(f"{authoritative_sources} authoritative source(s)")
    if corroborating_sources:
        reasons.append(f"{corroborating_sources} corroborating source(s)")
    if not reasons:
        reasons.append("insufficient supporting evidence")
    return EvidenceAssessment(score, confidence, tuple(reasons))
