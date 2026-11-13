"""Dependency-free fixture for the large_share unit-mismatch mechanism."""

from __future__ import annotations

from collections.abc import Sequence


def percentile_linear(values: Sequence[float], quantile: float) -> float:
    """Return a linearly interpolated percentile for a non-empty finite sample."""
    if not values:
        raise ValueError("values must not be empty")
    if not 0.0 <= quantile <= 1.0:
        raise ValueError("quantile must be in [0, 1]")
    ordered = sorted(values)
    index = (len(ordered) - 1) * quantile
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = index - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def large_share(trade_quantities: Sequence[float], threshold: float) -> float:
    """Share of absolute trade quantity at or above an individual-trade threshold."""
    total = sum(abs(quantity) for quantity in trade_quantities)
    if total == 0:
        return 0.0
    selected = sum(abs(quantity) for quantity in trade_quantities if abs(quantity) >= threshold)
    return selected / total


def example_fixture() -> tuple[list[float], list[float]]:
    """Synthetic quantities chosen to reproduce the public 4.3 vs 1,730 example."""
    individual_trades = [1.0, 2.0, 4.3, 4.3]
    per_second_nav = [500.0, 1500.0, 1730.0, 1730.0]
    return individual_trades, per_second_nav
