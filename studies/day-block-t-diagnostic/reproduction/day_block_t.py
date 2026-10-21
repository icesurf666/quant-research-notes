"""A small, dependency-free day-block t-statistic diagnostic."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from math import sqrt
from statistics import fmean, stdev

Timestamp = str | date | datetime


@dataclass(frozen=True)
class DayBlockResult:
    """Summary of equal-weighted calendar-day return means."""

    n_events: int
    n_days: int
    daily_mean_bps: float
    t_stat: float
    daily_returns_bps: tuple[float, ...]


def _calendar_day(timestamp: Timestamp) -> date:
    if isinstance(timestamp, datetime):
        return timestamp.date()
    if isinstance(timestamp, date):
        return timestamp
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()


def daily_means_bps(
    returns_bps: Iterable[float], timestamps: Iterable[Timestamp]
) -> tuple[float, ...]:
    """Group event returns by calendar day and return one mean per day."""

    grouped: dict[date, list[float]] = defaultdict(list)
    count = 0
    for return_bps, timestamp in zip(returns_bps, timestamps, strict=True):
        grouped[_calendar_day(timestamp)].append(float(return_bps))
        count += 1
    if count < 2:
        raise ValueError("at least two events are required")
    if len(grouped) < 2:
        raise ValueError("at least two calendar days are required")
    return tuple(fmean(grouped[day]) for day in sorted(grouped))


def one_sample_t(values: Iterable[float]) -> float:
    """Return the usual sample-SD one-sample t-statistic against zero."""

    observations = tuple(float(value) for value in values)
    if len(observations) < 2:
        raise ValueError("at least two observations are required")
    sample_sd = stdev(observations)
    if sample_sd == 0:
        raise ValueError("t-statistic is undefined for zero-variance observations")
    return fmean(observations) / (sample_sd / sqrt(len(observations)))


def day_block_t(returns_bps: Iterable[float], timestamps: Iterable[Timestamp]) -> DayBlockResult:
    """Compute the calendar-day diagnostic for a sequence of event returns."""

    returns = tuple(float(value) for value in returns_bps)
    days = daily_means_bps(returns, timestamps)
    return DayBlockResult(
        n_events=len(returns),
        n_days=len(days),
        daily_mean_bps=fmean(days),
        t_stat=one_sample_t(days),
        daily_returns_bps=days,
    )
