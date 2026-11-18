"""Small SQLite persistence adapter for durable scans and daily reports."""

from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .state_machine import ScanState


class ScanAlreadyExists(RuntimeError):
    pass


class IntelligenceStore:
    """SQLite store; one scan per calendar date, safe to use with local paths."""

    def __init__(self, database: str | Path = "nexasupply-intelligence.sqlite3") -> None:
        self.database = str(database)
        with self._connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id TEXT PRIMARY KEY,
                    scan_date TEXT NOT NULL UNIQUE,
                    state TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL DEFAULT '{}'
                );
                CREATE TABLE IF NOT EXISTS daily_reports (
                    report_date TEXT PRIMARY KEY,
                    markdown TEXT NOT NULL,
                    json_payload TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.database, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def create_scan(self, scan_id: str, scan_date: date, payload: dict[str, Any] | None = None) -> None:
        if not scan_id.strip():
            raise ValueError("scan_id is required")
        try:
            with self._connect() as db:
                db.execute(
                    "INSERT INTO scans(scan_id, scan_date, state, updated_at, payload_json) VALUES (?, ?, ?, ?, ?)",
                    (scan_id, scan_date.isoformat(), ScanState.CREATED.value, datetime.now(timezone.utc).isoformat(), json.dumps(payload or {}, sort_keys=True)),
                )
        except sqlite3.IntegrityError as exc:
            raise ScanAlreadyExists(f"a scan already exists for {scan_date.isoformat()} or id {scan_id}") from exc

    def transition_scan(self, scan_id: str, state: ScanState, payload: dict[str, Any] | None = None) -> None:
        with self._connect() as db:
            cursor = db.execute(
                "UPDATE scans SET state = ?, updated_at = ?, payload_json = COALESCE(?, payload_json) WHERE scan_id = ?",
                (state.value, datetime.now(timezone.utc).isoformat(), json.dumps(payload, sort_keys=True) if payload is not None else None, scan_id),
            )
            if cursor.rowcount != 1:
                raise KeyError(f"scan not found: {scan_id}")

    def get_scan(self, scan_id: str) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute("SELECT * FROM scans WHERE scan_id = ?", (scan_id,)).fetchone()
        if row is None:
            raise KeyError(f"scan not found: {scan_id}")
        result = dict(row)
        result["payload"] = json.loads(result.pop("payload_json"))
        return result

    def save_daily_report(self, report_date: date, markdown: str, payload: dict[str, Any]) -> None:
        if not markdown.strip():
            raise ValueError("markdown report cannot be empty")
        with self._connect() as db:
            db.execute(
                "INSERT INTO daily_reports(report_date, markdown, json_payload, created_at) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(report_date) DO UPDATE SET markdown=excluded.markdown, json_payload=excluded.json_payload, created_at=excluded.created_at",
                (report_date.isoformat(), markdown, json.dumps(payload, sort_keys=True), datetime.now(timezone.utc).isoformat()),
            )

    def get_daily_report(self, report_date: date) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute("SELECT * FROM daily_reports WHERE report_date = ?", (report_date.isoformat(),)).fetchone()
        if row is None:
            raise KeyError(f"report not found: {report_date.isoformat()}")
        result = dict(row)
        result["payload"] = json.loads(result.pop("json_payload"))
        return result
