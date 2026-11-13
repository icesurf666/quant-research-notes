from __future__ import annotations

import pytest
from feature_contract import example_fixture, large_share, percentile_linear


def test_public_aaveusdt_example_has_the_stated_ratio() -> None:
    trades, nav = example_fixture()
    trade_p75 = percentile_linear(trades, 0.75)
    nav_p75 = percentile_linear(nav, 0.75)

    assert trade_p75 == pytest.approx(4.3)
    assert nav_p75 == pytest.approx(1730.0)
    assert nav_p75 / trade_p75 == pytest.approx(402.3255813953488)


def test_per_second_threshold_collapses_an_individual_trade_feature() -> None:
    trades, nav = example_fixture()
    batch_threshold = percentile_linear(trades, 0.75)
    live_threshold = percentile_linear(nav, 0.75)

    assert large_share(trades, batch_threshold) == pytest.approx(8.6 / 11.6)
    assert large_share(trades, live_threshold) == 0.0


def test_percentile_rejects_invalid_input() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        percentile_linear([], 0.75)
    with pytest.raises(ValueError, match="must be in"):
        percentile_linear([1.0], 1.1)
