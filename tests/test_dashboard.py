from nexasupply_intelligence.dashboard import intelligence_center_view
from nexasupply_intelligence.offline import OFFLINE_MODE_LABEL


def test_dashboard_view_marks_offline_mode_and_labels():
    view = intelligence_center_view(mode="CONTROLLED_INTELLIGENCE", offline=True, events=[], proposals=[], scan_status="IDLE")
    assert view["title"] == "REAL-WORLD INTELLIGENCE CENTER"
    assert view["offline_banner"] == OFFLINE_MODE_LABEL
    assert "HYPOTHETICAL EXPOSURE" in view["labels"]
    assert "review_status" in view["filters"]
