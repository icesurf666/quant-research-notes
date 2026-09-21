from datetime import UTC, datetime, timedelta

import polars as pl
import pytest

from pkazantsev_research import ReversalConfig, cross_sectional_reversal


def _prices() -> pl.DataFrame:
    start = datetime(2025, 1, 1, tzinfo=UTC)
    return pl.DataFrame(
        {
            "ts": [start + timedelta(minutes=15 * index) for index in range(4)],
            "loser": [100.0, 99.0, 98.0, 97.0],
            "middle": [100.0, 100.0, 100.0, 100.0],
            "winner": [100.0, 101.0, 102.0, 103.0],
        }
    )


def test_losers_are_long_and_winners_are_short() -> None:
    weights = cross_sectional_reversal(_prices(), ReversalConfig(lookback_bars=1))
    last = weights.row(-1, named=True)
    assert last["loser"] > 0
    assert last["winner"] < 0


def test_non_flat_rows_have_unit_gross_exposure() -> None:
    weights = cross_sectional_reversal(_prices(), ReversalConfig(lookback_bars=1))
    symbols = [column for column in weights.columns if column != "ts"]
    gross = weights.select(
        pl.sum_horizontal(pl.col(symbol).abs() for symbol in symbols).alias("gross")
    )
    values = gross.filter(pl.col("gross") > 0).get_column("gross").to_list()
    assert values == pytest.approx([1.0, 1.0, 1.0])


def test_lookback_must_be_positive() -> None:
    try:
        ReversalConfig(lookback_bars=0)
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("zero lookback must be rejected")
