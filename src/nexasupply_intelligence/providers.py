"""Provider-independent external source contracts and safety validation."""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from urllib.parse import urlparse


@dataclass(frozen=True)
class SourceRecord:
    url: str
    title: str
    publisher: str
    published_at: datetime | None
    summary: str
    is_primary: bool = False

    def __post_init__(self) -> None:
        if not self.url.strip() or not self.title.strip() or not self.publisher.strip():
            raise ValueError("source URL, title, and publisher are required")
        if self.published_at is not None and self.published_at.tzinfo is None:
            raise ValueError("published_at must be timezone-aware")
        if not self.url.startswith("offline:"):
            parsed = urlparse(self.url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("external source URLs must use HTTPS")
        if len(self.summary) > 2000:
            raise ValueError("summary exceeds 2000 characters; store concise notes, not full articles")


class IntelligenceProvider(Protocol):
    """Replaceable provider adapter; must obey source access rules."""

    def search_recent_events(self, *, query: str, since: datetime) -> list[SourceRecord]: ...

    def fetch_source_details(self, *, url: str) -> SourceRecord: ...

    def normalize_source(self, source: SourceRecord) -> SourceRecord: ...

    def verify_event_claims(self, sources: list[SourceRecord]) -> bool: ...

    def classify_supply_chain_event(self, sources: list[SourceRecord]) -> str: ...
