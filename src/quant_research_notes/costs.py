"""Execution delay, turnover, trading costs, funding, and net PnL."""

from __future__ import annotations

from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class CostModel:
    """Fixed per-side trading costs in basis points."""

    fee_bps: float = 6.0
    slippage_bps: float = 4.0

    def __post_init__(self) -> None:
        if self.fee_bps < 0 or self.slippage_bps < 0:
            raise ValueError("costs cannot be negative")


def _symbols(frame: pl.DataFrame) -> list[str]:
    return [column for column in frame.columns if column != "ts"]


def _live(column: str) -> pl.Expr:
    """A decision at t is live from t+1."""

    return pl.col(column).shift(1).fill_null(0.0)


def apply_costs_and_funding(
    weights: pl.DataFrame,
    returns: pl.DataFrame,
    cost_model: CostModel,
    funding_pnl: pl.DataFrame | None = None,
) -> pl.DataFrame:
    """Compute gross PnL, turnover, costs, optional funding, and net PnL.

    ``funding_pnl`` is an already signed frame with columns ``ts`` and
    ``funding``. Keeping funding alignment outside this compact public function
    avoids pretending this repository reproduces exchange-specific ingestion.
    """

    symbols = _symbols(weights)
    if not symbols:
        raise ValueError("weights must contain at least one symbol column")
    if set(_symbols(returns)) != set(symbols):
        raise ValueError("weights and returns must contain the same symbols")

    merged = weights.sort("ts").join(returns.sort("ts"), on="ts", suffix="_return")
    gross = pl.sum_horizontal(_live(symbol) * pl.col(f"{symbol}_return") for symbol in symbols)
    turnover = pl.sum_horizontal(
        (_live(symbol) - pl.col(symbol).shift(2).fill_null(0.0)).abs() for symbol in symbols
    )
    output = merged.select(
        "ts",
        gross.alias("gross"),
        turnover.alias("turnover"),
    )
    if funding_pnl is None:
        output = output.with_columns(pl.lit(0.0).alias("funding"))
    else:
        output = output.join(funding_pnl.select("ts", "funding"), on="ts", how="left")
        output = output.with_columns(pl.col("funding").fill_null(0.0))

    fee_rate = cost_model.fee_bps / 10_000
    slippage_rate = cost_model.slippage_bps / 10_000
    output = output.with_columns(
        (pl.col("turnover") * fee_rate).alias("fees"),
        (pl.col("turnover") * slippage_rate).alias("slippage"),
    )
    return output.with_columns(
        (pl.col("gross") - pl.col("fees") - pl.col("slippage") + pl.col("funding")).alias("net")
    )
