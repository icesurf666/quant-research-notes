# Day-block diagnostic for a concentrated breakout result

Companion evidence package for
[`14,399 Events Looked Significant. 365 Trading Days Did Not.`](https://www.pkazantsev.com/writing/backtest-day-block-t/)

## Claim

A crypto-perpetual breakout simulation produced a naive event-level t-statistic
of +8.20 across 14,399 events. When the same returns were equal-weighted by
calendar day, the diagnostic produced a t-statistic of -1.66 across 365 daily
means. One market-wide dislocation, 2025-10-10, contained 434 events with an
average net return of +835 bps; excluding that day changed the event-level mean
from +25.98 bps to -3.69 bps.

This is not a trading recommendation and not evidence of a deployable edge.
The point of the package is narrower: a large event count did not make the
event-level estimate robust to common intraday exposure.

## What is public

- the frozen metrics used in the article;
- the return-concentration figure;
- a dependency-free implementation of the day-block diagnostic;
- deterministic tests for grouping and t-stat calculation;
- a manifest that detects drift in the public artifacts.

## Reproducibility boundary

The underlying market-data cache and event-level return series are not
distributed. The public package therefore cannot regenerate the historical
14,399-event result. It can reproduce the calculation on supplied inputs,
test its mechanics, and verify that the published snapshot and figure have not
changed.

The frozen snapshot is derived from a private audit report with SHA-256
`6a888c317c99da707f863e64d0ca94d305f938db03ac9523907eb6f224d56589`.

## Verify

```bash
python -m pytest studies/day-block-t-diagnostic/reproduction/test_day_block_t.py
python studies/day-block-t-diagnostic/verify.py
```

## Interpretation

The daily t-test is a concentration diagnostic, not a universally correct
replacement for cluster-robust standard errors, a block bootstrap, or a
portfolio return series. It also assumes daily means are independent. The
article reports it alongside the naive result to make the weighting choice and
its consequences visible.
