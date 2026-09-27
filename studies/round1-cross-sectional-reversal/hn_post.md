Title:
Show HN: Crypto reversal backtest – Sharpe 13.4 before costs, -40.1 after

Body:

Built a cross-sectional reversal strategy on 451 Bybit perps, 15-min bars, 2021–2025. 76 out-of-sample windows. Pre-cost Sharpe was 13.44, 88% positive windows. Looked great.

Then I added 10 bps per side. Sharpe dropped to -40.13. Zero positive windows. Trading costs consumed 4× the gross PnL.

The -40 is a bit theatrical (stable negative cost stream annualized from 15-min bars), but the ratio is real: the bill was four times the alpha.

Slowing rebalancing to daily got me to -4.45 under pessimistic costs, -0.01 under maker assumptions. Nothing survived cleanly.

I wrote up the full methodology with reproducible results and a SHA-256 fingerprint of the data snapshot. Mostly publishing because a clean failure seems more useful than leaving it in a drawer.

Curious if anyone's made short-horizon reversal work after real execution costs — threshold entries, passive fills, something else?
