from __future__ import annotations

import json
from pathlib import Path

import pytest
from day_block_t import daily_means_bps, day_block_t, one_sample_t


def test_groups_events_before_weighting_calendar_days() -> None:
    result = day_block_t(
        [10.0, 20.0, -5.0, 5.0],
        [
            "2025-01-01T10:00:00Z",
            "2025-01-01T20:00:00Z",
            "2025-01-02T01:00:00Z",
            "2025-01-02T23:00:00Z",
        ],
    )

    assert result.n_events == 4
    assert result.n_days == 2
    assert result.daily_returns_bps == pytest.approx((15.0, 0.0))
    assert result.daily_mean_bps == pytest.approx(7.5)
    assert result.t_stat == pytest.approx(1.0)


def test_requires_multiple_calendar_days() -> None:
    with pytest.raises(ValueError, match="calendar days"):
        daily_means_bps([1.0, 2.0], ["2025-01-01T00:00:00Z", "2025-01-01T01:00:00Z"])


def test_rejects_zero_variance_t_statistic() -> None:
    with pytest.raises(ValueError, match="zero-variance"):
        one_sample_t([3.0, 3.0])


def test_public_snapshot_matches_article_headline_values() -> None:
    evidence = Path(__file__).parents[1] / "evidence" / "results.json"
    snapshot = json.loads(evidence.read_text(encoding="utf-8"))

    assert snapshot["simulation"]["event_count"] == 14399
    assert snapshot["simulation"]["trading_days"] == 365
    assert snapshot["event_level"]["naive_t_stat"] == 8.2
    assert snapshot["day_block_diagnostic"]["t_stat"] == -1.66
    assert snapshot["october_10_2025_sensitivity"]["mean_net_bps"] == 835.0
