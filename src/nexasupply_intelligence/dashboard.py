"""Render a small real-world intelligence center panel for host dashboards.

Returns framework-neutral view data so the host UI can present event, proposal,
review, and simulation status with explicit semantic labels.
"""

from __future__ import annotations

from typing import Any


LABELS = {
    "source": "REAL-WORLD SOURCE",
    "fact": "VERIFIED FACT",
    "exposure": "HYPOTHETICAL EXPOSURE",
    "synthetic": "SYNTHETIC EVENT",
    "impact": "SIMULATED IMPACT",
}


def intelligence_center_view(*, mode: str, offline: bool, events: list[dict[str, Any]], proposals: list[dict[str, Any]], scan_status: str) -> dict[str, Any]:
    """Return UI-ready data and filter options; presentation stays in host app."""
    return {
        "title": "REAL-WORLD INTELLIGENCE CENTER",
        "mode": mode,
        "offline_banner": "OFFLINE INTELLIGENCE MODE" if offline else None,
        "scan_status": scan_status,
        "filters": ["date", "category", "risk", "confidence", "review_status", "mode"],
        "labels": list(LABELS.values()),
        "events": events,
        "proposals": proposals,
        "notice": "NexaSupply is fictional; real-world evidence is not evidence of actual NexaSupply exposure.",
    }
