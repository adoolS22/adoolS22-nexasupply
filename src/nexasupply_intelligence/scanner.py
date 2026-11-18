"""A minimal, provider-agnostic orchestration layer with no real-world side effects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Callable

from .offline import OFFLINE_MODE_LABEL, OfflineIntelligenceProvider
from .providers import IntelligenceProvider, SourceRecord
from .state_machine import ScanState, ScanStateMachine
from .store import IntelligenceStore, ScanAlreadyExists


@dataclass(frozen=True)
class ScanResult:
    scan_id: str
    scan_date: date
    state: ScanState
    mode_label: str
    sources: tuple[SourceRecord, ...]


class IntelligenceScanner:
    """Coordinates scan lifecycle; downstream simulation engine is injected separately."""

    def __init__(self, store: IntelligenceStore, provider: IntelligenceProvider | None = None) -> None:
        self.store = store
        self.provider = provider or OfflineIntelligenceProvider()
        self.mode_label = "LIVE PROVIDER MODE" if provider is not None else OFFLINE_MODE_LABEL

    def run_scan(
        self,
        *,
        scan_id: str,
        scan_date: date,
        queries: tuple[str, ...],
        since: datetime,
    ) -> ScanResult:
        self.store.create_scan(scan_id, scan_date, {"mode_label": self.mode_label})
        machine = ScanStateMachine()
        sources: list[SourceRecord] = []
        try:
            machine.transition(ScanState.COLLECTING)
            self.store.transition_scan(scan_id, machine.state)
            for query in queries:
                sources.extend(self.provider.search_recent_events(query=query, since=since))
            machine.transition(ScanState.VALIDATING)
            self.store.transition_scan(scan_id, machine.state)
            normalized = [self.provider.normalize_source(source) for source in sources]
            machine.transition(ScanState.CLASSIFIED)
            self.store.transition_scan(scan_id, machine.state, {"source_count": len(normalized), "mode_label": self.mode_label})
            # This foundation stops before scenario creation or simulated effects.
            return ScanResult(scan_id, scan_date, machine.state, self.mode_label, tuple(normalized))
        except Exception as exc:
            if machine.state not in (ScanState.FAILED, ScanState.APPLIED, ScanState.REJECTED):
                machine.transition(ScanState.FAILED)
                self.store.transition_scan(scan_id, machine.state, {"error_type": type(exc).__name__})
            raise


def scheduled_scan_time() -> tuple[int, int, str]:
    """Default intended schedule: once daily at 06:00 Europe/Berlin."""
    return (6, 0, "Europe/Berlin")
