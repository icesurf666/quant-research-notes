from datetime import UTC, datetime, timedelta

import polars as pl
import pytest

from quant_research_notes import CostModel, apply_costs_and_funding


def test_weight_decision_is_delayed_one_bar() -> None:
    start = datetime(2025, 1, 1, tzinfo=UTC)
    timestamps = [start + timedelta(minutes=15 * index) for index in range(3)]
    weights = pl.DataFrame({"ts": timestamps, "asset": [1.0, 1.0, 1.0]})
    returns = pl.DataFrame({"ts": timestamps, "asset": [0.10, 0.20, 0.30]})

    result = apply_costs_and_funding(weights, returns, CostModel(0.0, 0.0))

    assert result.get_column("gross").to_list() == [0.0, 0.20, 0.30]


def test_net_identity_includes_turnover_cost_and_funding() -> None:
    start = datetime(2025, 1, 1, tzinfo=UTC)
    timestamps = [start + timedelta(minutes=15 * index) for index in range(3)]
    weights = pl.DataFrame({"ts": timestamps, "asset": [1.0, -1.0, -1.0]})
    returns = pl.DataFrame({"ts": timestamps, "asset": [0.0, 0.01, -0.02]})
    funding = pl.DataFrame({"ts": timestamps, "funding": [0.0, -0.001, 0.002]})

    result = apply_costs_and_funding(
        weights,
        returns,
        CostModel(fee_bps=5.0, slippage_bps=3.0),
        funding,
    )
    error = result.select(
        (
            pl.col("net")
            - (pl.col("gross") - pl.col("fees") - pl.col("slippage") + pl.col("funding"))
        )
        .abs()
        .max()
    ).item()
    assert error < 1e-12
    assert result.get_column("turnover").to_list() == [0.0, 1.0, 2.0]


def test_negative_costs_are_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        CostModel(fee_bps=-1.0, slippage_bps=0.0)
