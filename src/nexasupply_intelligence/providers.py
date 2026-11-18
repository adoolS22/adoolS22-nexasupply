"""Provider-independent source contracts."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class SourceRecord:
    url: str
    title: str
    publisher: str
    published_at: datetime | None
    summary: str
    is_primary: bool = False


class IntelligenceProvider(Protocol):
    def search_recent_events(self, *, query: str, since: datetime) -> list[SourceRecord]: ...

    def fetch_source_details(self, *, url: str) -> SourceRecord: ...

    def normalize_source(self, source: SourceRecord) -> SourceRecord: ...

    def verify_event_claims(self, sources: list[SourceRecord]) -> bool: ...

    def classify_supply_chain_event(self, sources: list[SourceRecord]) -> str: ...
