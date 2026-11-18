"""Generate clearly labeled daily intelligence reports."""

from __future__ import annotations

from datetime import date
from typing import Any

from .offline import OFFLINE_MODE_LABEL


def build_daily_report(*, report_date: date, mode_label: str, events: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    """Build Markdown and JSON-safe payload; summaries must be short factual text."""
    payload: dict[str, Any] = {
        "report_date": report_date.isoformat(),
        "mode_label": mode_label,
        "disclaimer": "NexaSupply is fictional. Potential exposure and consequences below are hypothetical and simulation-only.",
        "events": events,
        "proposals": proposals,
    }
    lines = [
        f"# Real-World Intelligence Report — {report_date.isoformat()}",
        "",
        f"**Mode:** {mode_label}",
        "",
        "> NexaSupply is fictional. This report does not claim NexaSupply or fictional suppliers were affected by real-world events.",
        "",
        "## Events and evidence",
        "",
    ]
    if not events:
        lines.append("No events were collected for this scan.")
    for event in events:
        lines.extend([
            f"### {event.get('title', 'Untitled event')}",
            "",
            "- Label: REAL-WORLD SOURCE",
            f"- Category: {event.get('category', 'UNCLASSIFIED')}",
            f"- Sources: {', '.join(event.get('source_urls', [])) or 'none recorded'}",
            f"- Verified facts: {event.get('verified_facts', 'not established')}",
            "",
            f"{event.get('summary', '')}",
            "",
        ])
    lines.extend(["## Hypothetical proposals", ""])
    if not proposals:
        lines.append("No simulation proposals were generated.")
    for proposal in proposals:
        lines.extend([
            f"### Scenario {proposal.get('scenario_id', 'unassigned')}",
            "",
            "- Label: HYPOTHETICAL EXPOSURE / SYNTHETIC EVENT",
            f"- Hypothetical exposure: {proposal.get('hypothetical_exposure', 'not assessed')}",
            f"- Review required: {proposal.get('requires_review', True)}",
            f"- Simulated impact: {proposal.get('simulated_impact', 'not applied')}",
            "",
        ])
    if mode_label == OFFLINE_MODE_LABEL:
        lines.extend(["## Offline notice", "", f"{OFFLINE_MODE_LABEL}: local templates only; no live search or current-event verification was performed.", ""])
    return "\n".join(lines), payload
