from datetime import date

import pytest

from nexasupply_intelligence.state_machine import ScanState
from nexasupply_intelligence.store import IntelligenceStore, ScanAlreadyExists


def test_store_persists_scan_and_prevents_duplicate_day(tmp_path):
    store = IntelligenceStore(tmp_path / "intel.sqlite3")
    store.create_scan("scan-1", date(2026, 11, 18), {"mode": "offline"})
    assert store.get_scan("scan-1")["payload"] == {"mode": "offline"}
    with pytest.raises(ScanAlreadyExists):
        store.create_scan("scan-2", date(2026, 11, 18))
    store.transition_scan("scan-1", ScanState.COLLECTING)
    assert store.get_scan("scan-1")["state"] == "COLLECTING"


def test_store_saves_daily_report(tmp_path):
    store = IntelligenceStore(tmp_path / "intel.sqlite3")
    day = date(2026, 11, 18)
    store.save_daily_report(day, "# Report", {"events": []})
    assert store.get_daily_report(day)["payload"] == {"events": []}
