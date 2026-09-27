I spent a few weeks building a crypto backtest that looked promising. Then I added trading costs and watched it fall apart.

The strategy: cross-sectional reversal on crypto perpetuals. Buy recent underperformers, short recent outperformers, rebalance every 15 minutes. Before costs: Sharpe 13.44, positive returns in 88% of out-of-sample windows.

After 10 bps per side in fees and slippage: Sharpe -40.13. Zero positive windows. The trading bill was four times the gross alpha.

I tested slowing it down. Daily rebalancing under optimistic maker assumptions got me to Sharpe -0.01. The signal was decaying while it waited.

The failure was clean and the lesson was specific: turnover belongs inside the hypothesis from the start. A pre-cost Sharpe is not a strategy — it's a claim before execution. I already knew this in theory. Running the numbers made it concrete.

I published the full methodology with reproducible results, walk-forward windows, and a SHA-256 fingerprint of the data. A clean documented failure is more useful than a buried one — both for me and for anyone running similar experiments.

If you've seen a backtest collapse once execution entered the model — what caused it? Turnover, spread, fill probability, market impact?

→ https://dev.to/pavel_kkkkazantsev/my-crypto-backtest-had-a-sharpe-of-134-then-i-added-trading-costs-5718
