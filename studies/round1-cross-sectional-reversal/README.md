# Round 1: cross-sectional reversal

Companion artifact for **My Crypto Backtest Had a Sharpe of 13.4. Then I Added
Trading Costs**.

The study documents a rejected baseline, not a trading recommendation. The
public package contains the article, the complete machine-readable result
snapshot used by the article, figures generated from that snapshot, and the
minimal signal/cost implementation used to explain the mechanics.

## Reproducibility boundary

Level: **frozen evidence plus logic and deterministic tests**.

The repository verifies signal direction, unit-gross normalization, one-bar
execution delay, turnover, the net PnL identity, every published display value,
and all artifact hashes. `evidence/results.json` also records the data-tree hash,
runtime versions, and hashes of the source files used in the internal run.

The Bybit market-data cache is not distributed, so this repository cannot
independently regenerate the historical Sharpe values. It can verify that the
published article, figures, result snapshot, and review record have not drifted.

Run every public gate with:

```bash
make quality
```
