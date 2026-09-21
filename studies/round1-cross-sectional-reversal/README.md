# Round 1: cross-sectional reversal

Companion artifact for **My Crypto Strategy Had a Sharpe of 7. And Still Lost
Money**.

The study documents a rejected baseline, not a trading recommendation. The
public package contains the article, frozen result summaries, figures, and the
minimal signal/cost implementation used to explain the mechanics.

## Reproducibility boundary

Level: **logic and deterministic tests**.

The repository verifies signal direction, unit-gross normalization, one-bar
execution delay, turnover, and the net PnL identity. It does not ship the Bybit
market-data cache and therefore cannot independently regenerate the historical
Sharpe values. The metrics are frozen evidence exported from the internal run.

Run every public gate with:

```bash
make quality
```
