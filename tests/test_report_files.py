from datetime import date

from nexasupply_intelligence.offline import OFFLINE_MODE_LABEL
from nexasupply_intelligence.report_files import write_daily_report


def test_writes_markdown_and_machine_readable_daily_report(tmp_path):
    md, js = write_daily_report(output_dir=tmp_path, report_date=date(2026, 11, 18), mode_label=OFFLINE_MODE_LABEL, events=[], proposals=[])
    assert md.name == "2026-11-18.md"
    assert js.name == "2026-11-18.json"
    assert "OFFLINE INTELLIGENCE MODE" in md.read_text()
    assert '"report_date": "2026-11-18"' in js.read_text()
