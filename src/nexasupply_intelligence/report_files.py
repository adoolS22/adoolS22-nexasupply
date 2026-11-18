"""Versioned JSON serialization for daily intelligence reports."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .reports import build_daily_report


def write_daily_report(*, output_dir: str | Path, report_date: date, mode_label: str, events: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> tuple[Path, Path]:
    """Write YYYY-MM-DD.md and YYYY-MM-DD.json without overwriting other dates."""
    markdown, payload = build_daily_report(report_date=report_date, mode_label=mode_label, events=events, proposals=proposals)
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stem = report_date.isoformat()
    md_path = folder / f"{stem}.md"
    json_path = folder / f"{stem}.json"
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return md_path, json_path
