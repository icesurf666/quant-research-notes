**Title:**
Crypto cross-sectional reversal: Sharpe 13.4 → -40.1 after adding 10 bps/side

---

I ran a cross-sectional reversal baseline on 451 Bybit USDT perp symbols, 15-min bars, Jan 2021–Sep 2025. 76 non-overlapping OOS windows.

**Zero-cost:**

| Metric | Value |
|---|---:|
| Annualized Sharpe | 13.44 |
| Positive OOS windows | 67 / 76 (88%) |
| Max drawdown | -11.62% |
| Summed absolute turnover | 29,451 |

That last row is the warning I ignored for about twenty minutes.

**After 10 bps/side (6 fees + 4 slippage):**

| Metric | Value |
|---|---:|
| Annualized Sharpe | -40.13 |
| Positive OOS windows | 0 / 76 |
| Cost / gross alpha | 4.00× |

The signal rebalances every 15 minutes. A stable negative cost stream annualized from 15-min observations produces a theatrically bad Sharpe — the -40 is mostly math, not 4000% losses. The real number is that trading costs consumed 4× the gross PnL.

**Slowing it down** (15 bps/side pessimistic scenario):

| Rebalance | Net Sharpe | Positive windows |
|---|---:|---:|
| 15 min | -66.00 | 0/76 |
| 4 hours | -16.24 | 0/76 |
| 1 day | -4.45 | 10/76 |

Best tested corner: daily rebalance + 3 bps/side → Sharpe -0.01, 39/76 positive. Still not there.

The pattern is real in-sample. The naive implementation can't capture it after friction. My takeaway: turnover belongs inside the hypothesis from day one, not in the cleanup after the backtest looks good.

Full methodology, code, and reproducibility notes: https://dev.to/pavel_kkkkazantsev/my-crypto-backtest-had-a-sharpe-of-134-then-i-added-trading-costs-5718

Has anyone found a way to trade short-horizon reversal at 15-min bars profitably? Curious what execution approaches actually work here.
