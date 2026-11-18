from datetime import datetime, timezone

from nexasupply_intelligence.models import EventCategory, ExposureAssessment, IntelligenceEvent
from nexasupply_intelligence.offline import OFFLINE_MODE_LABEL, OfflineIntelligenceProvider
from nexasupply_intelligence.reports import build_daily_report
from nexasupply_intelligence.scanner import IntelligenceScanner
from nexasupply_intelligence.state_machine import ScanState
from nexasupply_intelligence.store import IntelligenceStore


def test_offline_provider_labels_and_returns_templates():
    provider = OfflineIntelligenceProvider()
    records = provider.search_recent_events(query="supply chain", since=datetime.now(timezone.utc))
    assert records
    assert all(record.publisher == OFFLINE_MODE_LABEL for record in records)
    assert provider.verify_event_claims(records) is False


def test_scanner_persists_offline_scan(tmp_path):
    store = IntelligenceStore(tmp_path / "scan.sqlite3")
    scanner = IntelligenceScanner(store)
    result = scanner.run_scan(
        scan_id="daily-2026-11-18",
        scan_date=__import__("datetime").date(2026, 11, 18),
        queries=("supply chain",),
        since=datetime(2026, 11, 17, tzinfo=timezone.utc),
    )
    assert result.state == ScanState.CLASSIFIED
    assert result.mode_label == OFFLINE_MODE_LABEL
    assert store.get_scan(result.scan_id)["state"] == "CLASSIFIED"


def test_report_disclaims_hypothetical_impact():
    markdown, payload = build_daily_report(
        report_date=__import__("datetime").date(2026, 11, 18),
        mode_label=OFFLINE_MODE_LABEL,
        events=[],
        proposals=[],
    )
    assert "NexaSupply is fictional" in markdown
    assert OFFLINE_MODE_LABEL in markdown
    assert payload["disclaimer"]
