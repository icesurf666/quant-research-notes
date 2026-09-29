# Capstone — three obvious crypto edges, and the honest test that killed each

*2026-09-11. Summary of the HFM research so far.*

## The premise

Retail crypto trading content is mostly hype: "I built a bot that prints." I
wanted the opposite. Build one honest research platform (point-in-time universe,
walk-forward, realistic costs, structure-preserving nulls, a sealed lockbox) and
run the obvious edges through it. Keep what survives, and be specific about what
kills the rest.

Three families went through. None produced a robust, confirmed, tradeable edge.
Each failed a different test, and which test caught it is the interesting part.

## 1. Price mean reversion — killed by costs

Cross-sectional reversal, cointegration, and factor-residual reversion all have a
strong *gross* edge: cross-sectional reversal ran a gross Sharpe of 7 to 13,
positive in 80%+ of out-of-sample windows. On 15-minute crypto, prices snap back;
they don't trend.

The edge is real and untradeable. Rebalancing a continuous book at 15m, costs run
5 to 10x the size of the raw edge. I tried everything to save it: entry/exit
thresholds, hysteresis to hold positions, a coarser 1-hour timeframe, slower
rebalancing. Turnover stayed high and net stayed negative or at break-even, with
no parameter plateau (adjacent settings swung from +45% to -60%). At taker fees it
was wiped out entirely.

**Verdict: REJECT.** A real premium the size of its own transaction cost.

## 2. Funding carry — killed by the lockbox

Long spot, short the perpetual, collect funding. Low turnover by design, so costs
can't grind it down. On development data it looked great: +48.6% net over 4.5
years, Sharpe 1.17, positive in 87% of windows, positive every year including the
2022 bear.

Two tests took it apart. A null test (scramble which coin's funding the strategy
reads) still made +28%, so more than half the return was beta, the structural
funding premium, not selection. The selection alpha that remained was real
(z = 4.1, p = 0.024). Then the lockbox: a full year, 2025-09 to 2026-09, sealed
from day one and never touched. The frozen strategy made **-0.5%** on it. The
funding premium that paid from 2021 to 2024 was simply not present in 2025-2026.

**Verdict: REJECT out-of-sample.** A regime-dependent premium that faded, plus
some overfitting to one dataset.

## 3. Daily cross-sectional momentum — killed by robustness

At 15m, momentum loses (short-horizon is reversion). At a daily horizon with a
weekly rebalance, momentum has a real gross premium and, crucially, tiny turnover,
so it survives costs where mean reversion could not. The best single run made
+96.7% net even at taker fees.

But it isn't robust. The lookback sweep was jagged (l=7 +33%, l=10 -23%, l=14
+97%, l=21 +35%), so the +96.7% headline was a lucky parameter, not a plateau; the
honest estimate is closer to +7%/yr. And it is regime-dependent: half the return
came from the 2021 bull alone, and 2022 was negative. Positive in bull, negative
in bear is residual market beta, not neutral alpha.

**Verdict: WEAK.** Survives costs, but not the robustness checks.

## What each test caught

| Edge | Gross | The honest test that killed it | Verdict |
|---|---|---|---|
| Price mean reversion | Sharpe 7-13 | transaction costs (turnover) | REJECT |
| Funding carry | +48.6% dev | the sealed lockbox (unseen year) | REJECT OOS |
| Daily momentum | +97% best | robustness (no plateau, regime-dependent) | WEAK |

Costs, a held-out year, and a parameter sweep. Three different failure modes,
three different guards. A strategy that clears one often dies on another.

## The actual result

No strategy to trade. That is the common outcome in this field, and the point was
never to force a winner. It was to build a process that finds out cheaply, with an
experiment instead of a funded account, and tells the truth about what it finds.

The obvious retail edges are obvious to everyone, so they are arbitraged to the
cost of trading them, they are regime-dependent, or they are not robust. A durable
edge needs a structural advantage (latency, data, capital) or a genuinely novel
signal, neither of which is a weekend project. Knowing that, precisely and from my
own data, is worth more than another suspicious backtest.

## What exists now

A reusable research stack: data layer, point-in-time universe, walk-forward
engine, cost and funding model, metrics with bootstrap and Deflated Sharpe,
structure-preserving nulls, a lockbox, an experiment registry, and a report
generator. Any new hypothesis is a thin plugin scored by the same judge.

Round reports: [round1_alpha_tournament.md](round1_alpha_tournament.md),
[round2_funding_carry.md](round2_funding_carry.md).
