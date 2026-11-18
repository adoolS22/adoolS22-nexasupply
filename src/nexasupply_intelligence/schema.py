"""Typed SQL schema for production database migrations.

SQLite development storage is implemented in nexasupply_intelligence.store.
Production deployments should apply this schema with the project's migration tool.
"""

from dataclasses import dataclass

POSTGRES_SCHEMA = """
CREATE TABLE IF NOT EXISTS intelligence_scans (
    scan_id TEXT PRIMARY KEY,
    scan_date DATE NOT NULL UNIQUE,
    state TEXT NOT NULL,
    mode TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS intelligence_events (
    event_id TEXT PRIMARY KEY,
    scan_id TEXT NOT NULL REFERENCES intelligence_scans(scan_id),
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    occurred_at TIMESTAMPTZ,
    discovered_at TIMESTAMPTZ NOT NULL,
    source_metadata JSONB NOT NULL DEFAULT '[]'::jsonb,
    verified_facts JSONB NOT NULL DEFAULT '[]'::jsonb,
    short_summary TEXT NOT NULL DEFAULT '',
    offline BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS scenario_proposals (
    scenario_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES intelligence_events(event_id),
    status TEXT NOT NULL,
    requires_review BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMPTZ,
    synthetic_parameters JSONB NOT NULL,
    rationale TEXT NOT NULL,
    simulated_impact JSONB
);
CREATE TABLE IF NOT EXISTS intelligence_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    scan_id TEXT REFERENCES intelligence_scans(scan_id),
    scenario_id TEXT REFERENCES scenario_proposals(scenario_id),
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS intelligence_daily_reports (
    report_date DATE PRIMARY KEY,
    markdown TEXT NOT NULL,
    json_payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
"""


@dataclass(frozen=True)
class MigrationNotice:
    backend: str = "PostgreSQL"
    note: str = "Use Alembic or the host application's migration framework before production use."
