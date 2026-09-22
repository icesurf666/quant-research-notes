"""Cross-sectional short-horizon reversal used in the first public study."""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class ReversalConfig:
    """Configuration for a causal, unit-gross reversal signal."""

    lookback_bars: int = 8

    def __post_init__(self) -> None:
        if self.lookback_bars < 1:
            raise ValueError("lookback_bars must be positive")


def _symbols(frame: pl.DataFrame) -> list[str]:
    return [column for column in frame.columns if column != "ts"]


def cross_sectional_reversal(
    prices: pl.DataFrame,
    config: ReversalConfig | None = None,
) -> pl.DataFrame:
    """Return causal target weights for a wide price frame.

    A row at time ``t`` uses prices no later than ``t``. Recent relative losers
    receive positive weights and winners receive negative weights. Each non-flat
    row is normalized so that the sum of absolute weights is one.
    """

    config = config or ReversalConfig()
    ordered = prices.sort("ts")
    symbols = _symbols(ordered)
    if not symbols:
        return ordered.select("ts")

    recent = ordered.select(
        "ts",
        (pl.col(symbols) / pl.col(symbols).shift(config.lookback_bars) - 1.0),
    )
    long = recent.unpivot(
        index="ts",
        on=symbols,
        variable_name="symbol",
        value_name="return",
    ).drop_nulls("return")
    if long.is_empty():
        return ordered.select("ts")

    stats = long.group_by("ts").agg(
        mean=pl.col("return").mean(),
        standard_deviation=pl.col("return").std(),
    )
    signal = long.join(stats, on="ts").with_columns(
        signal=pl.when(pl.col("standard_deviation") > 0)
        .then(-(pl.col("return") - pl.col("mean")) / pl.col("standard_deviation"))
        .otherwise(0.0)
    )
    gross = signal.group_by("ts").agg(gross_signal=pl.col("signal").abs().sum())
    normalized = signal.join(gross, on="ts").with_columns(
        weight=pl.when(pl.col("gross_signal") > 0)
        .then(pl.col("signal") / pl.col("gross_signal"))
        .otherwise(0.0)
    )
    return normalized.pivot(on="symbol", index="ts", values="weight").sort("ts")
