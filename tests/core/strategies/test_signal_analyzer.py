import os
import sys
from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

# Ensure core can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from core.strategies.signal_analyzer import SignalAnalyzer


class TestSignalAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return SignalAnalyzer()

    def test_filter_by_time_preserves_recent_signals(self, analyzer):
        now_utc = datetime.now(timezone.utc)
        recent_signals = [
            {"id": 1, "timestamp": now_utc - timedelta(hours=1)},
            {"id": 2, "timestamp": now_utc - timedelta(hours=12)},
        ]

        filtered = analyzer._filter_by_time(recent_signals)
        assert len(filtered) == 2

    def test_filter_by_time_removes_stale_signals(self, analyzer):
        now_utc = datetime.now(timezone.utc)
        mixed_signals = [
            {"id": 1, "timestamp": now_utc - timedelta(hours=1)},
            {"id": 2, "timestamp": now_utc - timedelta(hours=25)},  # Stale
            {"id": 3, "timestamp": now_utc - timedelta(days=2)},  # Stale
        ]

        filtered = analyzer._filter_by_time(mixed_signals)
        assert len(filtered) == 1
        assert filtered[0]["id"] == 1

    def test_filter_by_time_handles_different_types(self, analyzer):
        now_utc = datetime.now(timezone.utc)
        recent_str = (now_utc - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

        # Make naive datetime by removing tzinfo from a recent UTC time
        recent_naive = (now_utc - timedelta(hours=3)).replace(tzinfo=None)

        # Make a pandas timestamp
        recent_pd = pd.Timestamp(now_utc - timedelta(hours=4))

        # Make a stale string signal
        stale_str = (now_utc - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

        signals = [
            {"id": "str_signal", "timestamp": recent_str},
            {"id": "naive_signal", "timestamp": recent_naive},
            {"id": "pd_signal", "timestamp": recent_pd},
            {"id": "stale_signal", "timestamp": stale_str},
            {"id": "invalid_signal", "timestamp": "not-a-timestamp"},
            {"id": "missing_timestamp", "other_field": "val"},
        ]

        filtered = analyzer._filter_by_time(signals)

        # We should keep 3 valid, recent signals
        assert len(filtered) == 3

        # Ensure the ones we kept are the recent ones
        kept_ids = {s["id"] for s in filtered}
        assert "str_signal" in kept_ids
        assert "naive_signal" in kept_ids
        assert "pd_signal" in kept_ids

        # Ensure stale and invalid ones are filtered out
        assert "stale_signal" not in kept_ids
        assert "invalid_signal" not in kept_ids
        assert "missing_timestamp" not in kept_ids
