from .models import EventCategory, IntelligenceEvent
from .providers import IntelligenceProvider, SourceRecord

OFFLINE_MODE_LABEL = "OFFLINE INTELLIGENCE MODE"

# Small, immutable starter fixtures. Expand with reviewed public case references
# and synthetic examples; do not store full copyrighted article text here.
HISTORICAL_CASE_LIBRARY: tuple[IntelligenceEvent, ...] = (
    IntelligenceEvent(
        event_id="offline-port-congestion-template",
        title="Historical port congestion case template",
        category=EventCategory.PORT_DISRUPTION,
        occurred_at=None,
        discovered_at=__import__("datetime").datetime(2024, 1, 1, tzinfo=__import__("datetime").timezone.utc),
        source_urls=("offline:historical-port-congestion-template",),
        summary="Offline template: assess hypothetical lead-time and routing sensitivity. This is not a live event report.",
        offline=True,
    ),
    IntelligenceEvent(
        event_id="offline-weather-disruption-template",
        title="Historical severe-weather disruption case template",
        category=EventCategory.NATURAL_HAZARD,
        occurred_at=None,
        discovered_at=__import__("datetime").datetime(2024, 1, 1, tzinfo=__import__("datetime").timezone.utc),
        source_urls=("offline:historical-weather-disruption-template",),
        summary="Offline template: evaluate hypothetical transport continuity under severe weather. Not a current incident.",
        offline=True,
    ),
)


def offline_cases() -> tuple[IntelligenceEvent, ...]:
    """Return local cases explicitly marked as offline, not current reports."""
    return HISTORICAL_CASE_LIBRARY


class OfflineIntelligenceProvider:
    """Fallback adapter; never claims live search or current verification."""

    def search_recent_events(self, *, query, since):
        return [
            SourceRecord(
                url=case.source_urls[0],
                title=case.title,
                publisher=OFFLINE_MODE_LABEL,
                published_at=case.occurred_at,
                summary=case.summary,
                is_primary=False,
            )
            for case in offline_cases()
            if query.lower() in case.title.lower() or query.lower() in case.category.value.lower()
        ]

    def fetch_source_details(self, *, url):
        for case in offline_cases():
            if case.source_urls[0] == url:
                return SourceRecord(url, case.title, OFFLINE_MODE_LABEL, case.occurred_at, case.summary)
        raise KeyError(f"offline case not found: {url}")

    def normalize_source(self, source):
        return source

    def verify_event_claims(self, sources):
        return False

    def classify_supply_chain_event(self, sources):
        return "OFFLINE_TEMPLATE"
