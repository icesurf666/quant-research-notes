# Round 2 — Funding carry, and the lockbox that killed it

*Delta-neutral funding carry on Bybit spot + perpetuals. 2026-09-11.*

## Question

Round 1 killed six price-based baselines: they had real gross edge that
transaction costs ate whole. This round asks whether a low-turnover *carry* trade,
where you get paid to hold rather than paying to trade, survives where the price
signals died.

## Strategy

For each coin, hold a long-spot / short-perp unit of equal size. The price legs
cancel, so the book is roughly market-neutral. Being short the perpetual, you
collect funding whenever it is positive. The harvester reads each coin's funding
level, keeps only the positive-funding names (a regime gate that steps aside when
funding turns negative), weights by how much they pay, and rebalances every couple
of weeks so turnover stays tiny.

Scored by the same judge as Round 1: 45 liquid coins, 15m bars, 2021-2025, 76
non-overlapping out-of-sample walk-forward windows, maker two-leg costs, point-in-
time universe, lockbox sealed.

## Two bugs found along the way

1. **Funding was 97% missing.** `download_funding` paged forward, but Bybit
   returns only the most recent ~200 records inside a requested window, so only
   the last page was ever saved (BTC: 200 events instead of 6236). Fixed by paging
   backward from the end timestamp. Before the fix, carry looked dead because the
   income was absent.
2. **Infinite loop on delisted symbols.** `download_klines` had no
   no-forward-progress guard; delisted coins (FTM→Sonic, MATIC→POL) return stale
   tail data outside the window, oscillating forever. Fixed with a
   `next_cursor <= cursor` break.

## Development result (seen data)

- Net +48.6% over ~4.5 years, Sharpe 1.17, positive in 87% of windows
- Positive every year including the 2022 bear (+5.3%), thanks to the regime gate
- Survives a pessimistic 30 bps/side cost (+33.9%); turnover is tiny
- Concentration 0.06; stable when the universe grew from 30 to 45 coins

Every robustness check we had, it passed.

## Null decomposition (does the signal matter?)

Scramble which coin's funding the strategy reads, keep everything else, run 40
seeds. If the signal drives returns, this should collapse.

It made +28.4% (mean of 40 seeds). So more than half the return is **beta**: crypto
funding is structurally positive, and a broad long-spot/short-perp book harvests
that premium regardless of selection. The real +48.6% still sits well above the
null distribution (best null +41.1%, z = 4.1, p = 0.024), so the selection adds a
genuine, statistically real ~+20% on top. Two real things, not one.

## Lockbox confirmation (unseen data) — the verdict

We iterated a lot on the development set (two bug fixes, several signal versions, a
rebalance sweep). That leaks, and walk-forward hides it. So a full year,
2025-09-01 to 2026-09-01, was sealed from the start and never touched. The frozen
strategy traded it once.

| | net return | Sharpe | positive windows |
|---|---:|---:|---:|
| Development (2021-2025, seen) | +48.6% | 1.17 | 87% |
| Lockbox (2025-2026, unseen) | -0.5% | -0.02 | 65% |

**The edge did not confirm.** On data the research never saw, carry was flat.
Turnover was tiny, so it is not costs: the funding premium that paid from 2021 to
2024 was simply not present in 2025-2026, and the selection edge did not survive
either. Part real premium that has since compressed, part overfitting a year of
decisions to one dataset. Probably both.

## Verdict: REJECT (out-of-sample)

No confirmed tradeable edge. Funding carry is a regime-dependent risk premium that
was strong through 2024 and absent in the held-out year.

This is the methodology working, not failing. A result that clears every
robustness check and still dies on held-out data is the normal case in systematic
research. The lockbox found it out for the price of an experiment instead of a
funded account.

## What it costs to know this

The whole arc: six price baselines rejected at the cost wall, one carry candidate
that looked promising on development data and then failed the one test it could not
be tuned against. No strategy to trade, and a research process that can be trusted
to say so.

## Next

- Back to the hypothesis pipeline (factor-residual reversion, cross-sectional
  reversal with entry thresholds) on the same machinery, each with its own lockbox.
- Revisit carry only once enough new data has accumulated to seal a fresh lockbox,
  and test it as an explicitly regime-conditional trade.

## Reproduce

```
PYTHONPATH=src python scripts/run_carry_bybit.py      # development sweep
PYTHONPATH=src python scripts/confirm_lockbox.py       # one-shot lockbox (burns it)
```
