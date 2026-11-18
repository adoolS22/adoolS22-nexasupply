from datetime import datetime, timezone

import pytest

from nexasupply_intelligence.providers import SourceRecord


def test_source_rejects_http_and_long_article_text():
    with pytest.raises(ValueError):
        SourceRecord("http://example.test", "t", "p", None, "summary")
    with pytest.raises(ValueError):
        SourceRecord("https://example.test", "t", "p", None, "x" * 2001)


def test_source_accepts_concise_https_metadata():
    record = SourceRecord("https://example.test/report", "Title", "Publisher", datetime.now(timezone.utc), "Short factual note", True)
    assert record.is_primary
